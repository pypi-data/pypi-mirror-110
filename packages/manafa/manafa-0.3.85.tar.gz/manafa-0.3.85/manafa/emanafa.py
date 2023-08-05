import os
import time
import pprint
from manafa.services.batteryStatsService import BatteryStatsService
from manafa.services.service import *
from manafa.services.perfettoService import PerfettoService
from manafa.perfetto.perfettoParser import PerfettoCPUfreqParser
from manafa.batteryStats.BatteryStatsParser import BatteryStatsParser
import argparse
from manafa.utils.Logger import log, LogSeverity
from manafa.utils.Utils import execute_shell_command, mega_find, get_resources_dir, is_float
from datetime import datetime, timezone

MANAFA_RESOURCES_DIR = get_resources_dir()

DEFAULT_PROFILE = os.path.join(MANAFA_RESOURCES_DIR, "profiles", "power_profile.xml")
DEFAULT_TIMEZONE = "GMT"


def get_last_boot_time(bts_file=None):
    """Retrieves timestamp of device last boot, either from the batterystats output filename that contains that info or the device itself
        Args:
          bts_file:

        Returns:
          timestamp as float: secs.ms
    """
    res, out, err = execute_shell_command(
        "adb shell cat /proc/stat | grep btime | awk '{print $2}'")  # executeShCommand("adb shell cat /proc/stat | grep btime | awk '{print $2}'")
    if res != 0 or len(out) == 0:
        log("no device connected. Assuming Boot time of battery stats file", LogSeverity.ERROR)
        flds = bts_file.split("-") if bts_file is not None else []
        if len(flds) > 1:
            boot_time = flds[2].replace(".log", "")
            log("Boot time: " + boot_time, LogSeverity.WARNING)
            return int(float(boot_time))
        else:
            log("no device connected. Assuming Boot time 0", LogSeverity.WARNING)
            return 0
        # raise Exception("Invalid boot time ")
    # print("[Warning]: no device connected. Assuming Boot time %d" % boot_time)
    return float(out.strip())



class EManafa(Service):
    """Main class that abstracts all the steps of the profiling procedure

    Attributes:
        resources_dir: directory where aux resources are contained
        power_profile: the power profile to be used in the profiling sessions
        boot_time: device's last boot timestamp
        batterystats: batterystats service
        perfetto: perfetto service
        timezone: device timezone
        unplugged: if the device is not charging
        bat_events: Batterystats parser
        pft_out_file: perfetto service output file
        bts_out_file: batterystats output file
    """

    def __init__(self, power_profile=None, timezone=None, resources_dir=MANAFA_RESOURCES_DIR):
        """Inits EManafa"""
        Service.__init__(self)
        self.resources_dir = resources_dir
        self.power_profile = power_profile if power_profile is not None else self.inferPowerProfile()
        self.boot_time = 0
        log("Power profile file: " + self.power_profile, LogSeverity.INFO)
        self.batterystats = BatteryStatsService()
        self.perf_events = None
        self.perfetto = PerfettoService()
        self.timezone = timezone if timezone is not None else self.__inferTimezone()
        self.unplugged = False
        self.bat_events = None
        self.pft_out_file = None
        self.bts_out_file = None

    def config(self, **kwargs):
        pass

    def init(self):
        """inits inner services and virtually unplugs device if it is fully charged"""
        self.boot_time = get_last_boot_time()
        self.batterystats.init(boot_time=self.boot_time)
        self.perfetto.init(boot_time=self.boot_time)
        self.__unplug_if_fully_charged()


    def start(self):
        """starts inner services"""
        self.batterystats.start()
        self.perfetto.start()

    def stop(self):
        """starts inner services"""
        self.bts_out_file = self.batterystats.stop()
        self.pft_out_file = self.perfetto.stop()
        log("Perfetto file:  %s" % self.pft_out_file)
        self.parseResults(self.bts_out_file, self.pft_out_file)
        if self.unplugged:
            self.__plug_back()
        return self.bts_out_file, self.pft_out_file


    def clean(self):
        """calls clean methods from inner services to clean previous result files"""
        self.batterystats.clean()
        self.perfetto.clean()

    def parseResults(self, bts_file=None, pf_file=None):
        """parses results from output results files of perfetto and batterystats
            Args:
                bts_file: batterystats output file. if none, uses self.bts_out_file
                pf_file: perfetto output file. if none, uses self.pft_out_file
        """
        if bts_file is None:
            bts_file = self.bts_out_file
        if pf_file is None:
            pf_file = self.pft_out_file
        if bts_file is None or pf_file is None:
            log("Empty result files",
                log_sev=LogSeverity.FATAL)
        self.boot_time = get_last_boot_time(bts_file)
        self.bat_events = BatteryStatsParser(self.power_profile, timezone=self.timezone)
        self.bat_events.parseFile(bts_file)
        self.perf_events = PerfettoCPUfreqParser(self.power_profile, self.boot_time, timezone=self.timezone)
        self.perf_events.parseFile(pf_file)


    # energy calc related stuff
    def getConsumptionInBetween(self, start_time=0, end_time=9905715380):
        """retrieves energy consumption and device events between a timestamp interval
            Args:
                start_time: begin timestamp
                end_time: end timestamp
            Returns:
                total: system-level energy consumption
                per_component: per-component energy consumption
                metrics: batterystats info containing events occurred during the interval. for each type of event, it
                presents
        """
        total, per_component = self.calculateNonCpuEnergy(start_time, end_time)
        total_cpu = self.calculateCPUEnergy(start_time, end_time)
        metrics = self.bat_events.getEventsInBetween(start_time,end_time)
        per_component['cpu'] += total_cpu
        return total + total_cpu, per_component, metrics

    def calculateNonCpuEnergy(self, start_time, end_time):
        """Obtains energy consumption of device between a timestamp interval for every component except cpu. for cpu retrieves only the state recorded in battarystats
            Args:
                start_time: begin timestamp
                end_time: end timestamp
            Returns:
                total: system-level energy consumption without cpu energy consumption
                per_component: per-component energy consumption without cpu energy consumption
        """
        c_beg_bef, c_beg_aft = self.bat_events.getClosestPair( start_time)
        total = 0
        per_component_consumption = {}
        last_event = self.bat_events.events[c_beg_bef]
        last_time = start_time
        for i, x in enumerate(self.bat_events.events[c_beg_aft:]):
            if x.time > end_time:
                break
            delta_time = abs(x.time - last_time)
            tot_curr, comps_curr = last_event.getCurrentOfBatStatEvent()
            total += tot_curr * (last_event.getVoltageValue()) * delta_time
            for comp, comp_curr in comps_curr.items():
                if comp not in per_component_consumption:
                    per_component_consumption[comp] = 0
                if is_float(comp_curr):
                    per_component_consumption[comp] += (comp_curr * last_event.getVoltageValue() * delta_time)
            last_event = x
            last_time = x.time

        delta_time = end_time - last_time
        if delta_time < 0.0:
            log(time.time(), "Error calculating delta (<0) ", LogSeverity.FATAL)
        tot_curr, comps_curr = last_event.getCurrentOfBatStatEvent()
        total += tot_curr * (last_event.getVoltageValue()) * (delta_time)
        for comp, comp_curr in comps_curr.items():
            if comp not in per_component_consumption:
                per_component_consumption[comp] = 0
            if is_float(comp_curr):
                per_component_consumption[comp] += (comp_curr * last_event.getVoltageValue() * delta_time)
        return total, per_component_consumption

    def calculateCPUEnergy(self, start_time, end_time):
        """calculates cpu energy consumption of device between a timestamp interval
            Args:
                start_time: begin timestamp
                end_time: end timestamp
            Returns:
                total: cpu energy consumption
        """
        c_beg_bef, c_beg_aft = self.bat_events.getClosestPair(start_time)
        # c_end_bef,c_end_aft =  getClosestPair(self.perf_events.events, end_time)
        total = 0
        last_event = self.perf_events.events[c_beg_bef]
        last_time = start_time
        tot_time = 0
        for i, x in enumerate(self.perf_events.events[c_beg_aft:]):
            if x.time > end_time:
                break
            # print("between %f - %f" %(last_time,x.time) )
            # get different states of cpu btween perf event interval
            # print( x.time - last_time )
            l = self.bat_events.getCPUSamplesInBetween(last_time, x.time)
            # TODO : test to assert if x.time - last_time  = sum( deltas_of_L )
            for sample in l:
                delta, state, voltage = sample[0], sample[1], sample[2]
                cpus_current = last_event.calculateCPUsCurrent(state, self.perf_events.power_profile)
                tot_time += delta
                total += (cpus_current) * delta * voltage
            last_event = x
            last_time = x.time

        # after calcs'''
        # TODO merge with cycle just like with non cpu
        l = self.bat_events.getCPUSamplesInBetween(last_time, end_time)
        for sample in l:
            delta, state, voltage = sample[0], sample[1], sample[2]
            cpus_current = last_event.calculateCPUsCurrent(state, self.perf_events.power_profile)
            tot_time += delta
            total += (cpus_current) * delta * voltage
        # TODO just like non cpu
        # print(tot_time)
        return total



    def __extractPowerProfile(self, filename):
        """ Extracts power_profile.xml file from the device, by pulling framework-res.apk and using apktool to unzip the apk
            If the process fails, retrieves DEFAULT_PROFILE filepath
            Args:
                filename: the target name of the file
            Returns:
                filename: the name of the extracted xml file
        """
        # extracting power_profile.xml from device
        res, suc, v = execute_shell_command("adb pull /system/framework/framework-res.apk %s" % self.resources_dir)
        if res == 0:
            cmd = """java -jar {res_dir}/apktool_2.4.0.jar d -s {res_dir}/framework-res.apk -f -o {res_dir}/out_jar_dir/""".format(
                res_dir=self.resources_dir)
            res, suc, v = execute_shell_command(cmd)
            pp_file = self.resources_dir + "/out_jar_dir/res/xml/power_profile.xml"
            if res == 0:
                # cp to profiles, remove out_jar_dir and framework-res.apk
                res, _, _ = execute_shell_command(
                    "cp {extracted_file} \"{res_dir}/profiles/{new_file}\" ; rm -rf {res_dir}/out_jar_dir {res_dir}/framework-res.apk".format(
                        extracted_file=pp_file, new_file=filename, res_dir=self.resources_dir))
                if res == 0:
                    return filename

        return DEFAULT_PROFILE

    def inferPowerProfile(self):
        """picks the most appropriate power profile file. power profile files present in self.resources_dir contains a device model id in the filename, which is determinated by ro.product.model property. if there is an adequate file locally, it retrieves such filename. Otherwise, it extracts the profile from the device using __extractPowerProfile
            Returns:
               filename: the name of the  xml file
       """
        res, device_model, _ = execute_shell_command("adb shell getprop ro.product.model")
        if res == 0 and device_model != "":
            model_profile_file = """power_profile_{device_model}.xml""".format(
                device_model=device_model.replace(" ", "").strip().lower())
            matching_profiles = mega_find(self.resources_dir, pattern=model_profile_file, maxdepth=2)
            if len(matching_profiles) > 0:
                return matching_profiles[0]
            else:
                # if power profile not present in profiles directory, extract from device
                power_profile = self.__extractPowerProfile(model_profile_file)
                print(power_profile)
                return power_profile
        else:
            return DEFAULT_PROFILE

    def __inferTimezone(self):
        """ Obtains device timezone. if there is no device connected, returns DEFAULT_TIMEZONE
            Returns:
                tz: device timezone
        """
        res, out, err = execute_shell_command("adb shell date")
        default_tz = DEFAULT_TIMEZONE
        if res == 0 and len(out) > 0:
            default_tz = out.split(" ")[-2]
        log("Using timezone: %s" % default_tz)
        return "WET" if default_tz == "WEST" else default_tz

    def __unplug_if_fully_charged(self):
        """ virtually unplugs device charger, by calling dumpsys battery unplug
        """
        # battery stats file comes empty when battery level == 100
        # using adb to trick device to think it is not charging th battery
        res, o, e = execute_shell_command("adb shell dumpsys battery | grep level | grep 100")
        has_full_charge = res == 0 and "100" in o
        if has_full_charge:
            # mock unplug
            res, o, e = execute_shell_command("adb shell dumpsys battery unplug")
            if res == 0:
                self.unplugged = True
                log("virtually unplugging battery charger while running (battery == 100)", LogSeverity.WARNING)

    def __plug_back(self):
        """plugs back the device"""
        res, o, e = execute_shell_command("adb shell dumpsys battery reset")
        self.unplugged = False

def has_connected_devices():
    """checks if there are devices connected via adb"""
    res, o, e = execute_shell_command("adb devices -l | grep -v attached")
    return res == 0 and len(o) > 2

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--profile", default=None, type=str)
    parser.add_argument("-t", "--timezone", default=None, type=str)
    parser.add_argument("-pft", "--perfettofile", default=None, type=str)
    parser.add_argument("-bts", "--batstatsfile", default=None, type=str)
    args = parser.parse_args()
    has_device_conn = has_connected_devices()
    invalid_file_args = (args.perfettofile is None or args.batstatsfile is None)
    if not has_device_conn and invalid_file_args:
        log("Fatal error. No connected devices and result files submitted for analysis", LogSeverity.FATAL)
        exit(-1)
    g = EManafa(power_profile=args.profile, timezone=args.timezone, resources_dir=MANAFA_RESOURCES_DIR)
    if has_device_conn and invalid_file_args:
        g.init()
        g.start()
        print("start testing...")
        time.sleep(7)  # do work
        print("stop testing...")
        g.stop()
    else:
        g.parseResults(args.batstatsfile, args.perfettofile)
    begin = g.bat_events.events[0].time  # first collected sample from batterystats
    end = g.bat_events.events[-1].time  # last collected sample from batterystats
    p, c, z = g.getConsumptionInBetween(begin, end)
    print("TOTAL: ")
    print(p)
    print(c)
    print(z)
