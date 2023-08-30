from .kelerrors import *
from .kelenums import *


class ListStep(object):
    def __init__(self, current: float, current_slope: float, duration: float):
        self.current = float(current)
        self.current_slope = float(current_slope)
        self.duration = float(duration)


class LoadList(object):
    def __init__(self, save_slot: int, current_range: float, steps: [ListStep], loop_number: int):

        self.save_slot = int(save_slot)
        self.current_range = float(current_range)
        self.steps = steps
        self.loop_number = int(loop_number)

    def __str__(self):
        list_string = ":LIST {slot:d},{range:5.4f}A,{step_number:d},".format(slot=self.save_slot,
                                                                             range=self.current_range,
                                                                             step_number=len(self.steps))
        step_string = ""

        for s in self.steps:
            step_string = step_string + "{current:5.4f}A,{slope:5.4f}A/uS,{duration:5.4f}S,".format(current=s.current,
                                                                                                    slope=s.current_slope,
                                                                                                    duration=s.duration)

        list_string = list_string + "{steps}{loops}".format(steps=step_string, loops=self.loop_number)
        return list_string

    def validate(self):
        if 1 > self.save_slot > 7:
            raise ValueError("save-slot can only be from 1-7")
        if len(self.steps) > 84:
            raise ValueError("a maximum of 84 steps is allowed")
        for s in self.steps:
            if s.current > self.current_range:
                raise ValueOutOfLimitError(s.current, self.current_range, "current set is out of current range")


class OCPList(object):
    def __init__(self, save_slot: int, on_voltage: float, on_delay: float, current_range: float, initial_current: float,
                 step_current: float, step_delay: float, off_current: float, ocp_voltage: float, max_overcurrent: float,
                 min_overcurrent: float):

        self.save_slot = int(save_slot)
        self.on_voltage = float(on_voltage)
        self.on_delay = float(on_delay)
        self.current_range = float(current_range)
        self.initial_current = float(initial_current)
        self.step_current = float(step_current)
        self.step_delay = float(step_delay)
        self.off_current = float(off_current)
        self.ocp_voltage = float(ocp_voltage)
        self.max_overcurrent = float(max_overcurrent)
        self.min_overcurrent = float(min_overcurrent)

    def __str__(self):
        ocp_string = ":OCP {0:d},{1:5.4f}V,{2:5.4f}S,{3:5.4f}A,{4:5.4f}A,{5:5.4f}A,{6:5.4f}S,{7:5.4f}A,{8:5.4f}V,{9:5.4f}A,{10:5.4f}A".format(
            self.save_slot, self.on_voltage, self.on_delay, self.current_range, self.initial_current, self.step_current,
            self.step_delay, self.off_current, self.ocp_voltage, self.max_overcurrent, self.min_overcurrent)

        return ocp_string

    def validate(self):
        if 1 > self.save_slot > 10:
            raise ValueError("save-slot can only be from 1-10")
        if self.initial_current >= self.current_range:
            raise ValueOutOfLimitError(self.initial_current, self.current_range,
                                       "Current values must be below current range")
        if self.initial_current <= self.max_overcurrent:
            raise ValueError("initial current must be above max overcurrent")
        if self.off_current > self.min_overcurrent:
            raise ValueError("off current must be below other current values")
        if self.max_overcurrent <= self.min_overcurrent:
            raise ValueError("max overcurrent must be above min overcurrent")
        if self.step_current > self.initial_current:
            raise ValueError("current step must be same or lower than initial current")


class OPPList(object):
    def __init__(self, save_slot: int, on_voltage: float, on_delay: float, current_range: float, initial_power: float,
                 step_power: float, step_delay: float, off_power: float, opp_voltage: float, max_overpower: float,
                 min_overpower: float):

        self.save_slot = int(save_slot)
        self.on_voltage = float(on_voltage)
        self.on_delay = float(on_delay)
        self.current_range = float(current_range)
        self.initial_power = float(initial_power)
        self.step_power = float(step_power)
        self.step_delay = float(step_delay)
        self.off_power = float(off_power)
        self.opp_voltage = float(opp_voltage)
        self.max_overpower = float(max_overpower)
        self.min_overpower = float(min_overpower)

    def __str__(self):
        opp_string = ":OPP {0:d},{1:5.4f}V,{2:5.4f}S,{3:5.4f}A,{4:5.4f}W,{5:5.4f}W,{6:5.4f}S,{7:5.4f}W,{8:5.4f}V,{9:5.4f}W,{10:5.4f}W".format(
            self.save_slot, self.on_voltage, self.on_delay, self.current_range, self.initial_power, self.step_power,
            self.step_delay, self.off_power, self.opp_voltage, self.max_overpower, self.min_overpower)

        return opp_string

    def validate(self):
        if 1 > self.save_slot > 10:
            raise ValueError("save-slot can only be from 1-10")
        if self.initial_power <= self.max_overpower:
            raise ValueError("initial power must be above max overpower")
        if self.off_power > self.min_overpower:
            raise ValueError("off power must be below other power values")
        if self.max_overpower <= self.min_overpower:
            raise ValueError("max overpower must be above min overpower")
        if self.step_power > self.initial_power:
            raise ValueError("power step must be same or lower than initial power")


class BattList(object):
    def __init__(self, save_slot: int, current_range: float, discharge_current: float, cutoff_voltage: float, cutoff_capacity: float, cutoff_time: float):

        self.save_slot = save_slot
        self.current_range = float(current_range)
        self.discharge_current = float(discharge_current)
        self.cutoff_voltage = float(cutoff_voltage)
        self.cutoff_capacity = float(cutoff_capacity)
        self.cutoff_time = float(cutoff_time)

    def __str__(self):
        batt_string = ":BATT {0:d},{1:5.4f}A,{2:5.4f}A,{3:5.4f}V,{4:5.4f}AH,{5:5.4f}M".format(self.save_slot, self.current_range, self.discharge_current, self.cutoff_voltage, self.cutoff_capacity, self.cutoff_time)

        return batt_string

    def validate(self):
        if 1 > self.save_slot > 10:
            raise ValueError("save-slot can only be from 1-10")
        if self.discharge_current >= self.current_range:
            raise ValueError("discharge current has to be lower or same as current range")


class CVList(object):
    def __init__(self, voltage1: float, voltage2: float, frequency: float, duty_cycle: float):
        self.function = Mode.dynamic_cv
        self.voltage1 = float(voltage1)
        self.voltage2 = float(voltage2)
        self.frequency = float(frequency)
        self.duty_cycle = float(duty_cycle)

    def __str__(self):
        cv_string = ":DYN 1,{0:5.4f}V,{1:5.4f}V,{2:5.4f}HZ,{3:5.4f}%".format(self.voltage1, self.voltage2, self.frequency, self.duty_cycle)

        return cv_string

    def validate(self, limit: float):
        if self.voltage2 > limit < self.voltage1:
            raise ValueOutOfLimitError(max(self.voltage2, self.voltage1), limit, "voltage value out of set limits")
        if self.duty_cycle >= 100:
            raise ValueOutOfLimitError(self.duty_cycle, 100, "duty cycle must be below 100%")


class CCList(object):
    def __init__(self, slope1: float, slope2: float, current1: float, current2: float, frequency: float, duty_cycle: float):
        self.function = Mode.dynamic_cc
        self.slope1 = float(slope1)
        self.slope2 = float(slope2)
        self.current1 = float(current1)
        self.current2 = float(current2)
        self.frequency = float(frequency)
        self.duty_cycle = float(duty_cycle)

    def __str__(self):
        cc_string = ":DYN 2,{0:5.4f}A/uS,{1:5.4f}A/uS,{2:5.4f}A,{3:5.4f}A,{4:5.4f}HZ,{5:5.4f}%".format(self.slope1, self.slope2, self.current1, self.current2, self.frequency, self.duty_cycle)

        return cc_string

    def validate(self, limit: float):
        if self.current2 > limit < self.current1:
            raise ValueOutOfLimitError(max(self.current2, self.current1), limit, "current value out of set limits")
        if self.duty_cycle >= 100:
            raise ValueOutOfLimitError(self.duty_cycle, 100, "duty cycle must be below 100%")


class CRList(object):
    def __init__(self, resistance1: float, resistance2: float, frequency: float, duty_cycle: float):
        self.function = Mode.dynamic_cr
        self.resistance1 = float(resistance1)
        self.resistance2 = float(resistance2)
        self.frequency = float(frequency)
        self.duty_cycle = float(duty_cycle)

    def __str__(self):
        cr_string = ":DYN 3,{0:5.4f}OHM,{1:5.4f}OHM,{2:5.4f}HZ,{3:5.4f}%".format(self.resistance1, self.resistance2, self.frequency, self.duty_cycle)

        return cr_string

    def validate(self, limit: float):
        if self.resistance2 > limit < self.resistance1:
            raise ValueOutOfLimitError(max(self.resistance2, self.resistance1), limit,
                                       "resistance value out of set limits")
        if self.duty_cycle >= 100:
            raise ValueOutOfLimitError(self.duty_cycle, 100, "duty cycle must be below 100%")


class CWList(object):
    def __init__(self, power1: float, power2: float, frequency: float, duty_cycle: float):
        self.function = Mode.dynamic_cw
        self.power1 = float(power1)
        self.power2 = float(power2)
        self.frequency = float(frequency)
        self.duty_cycle = float(duty_cycle)

    def __str__(self):
        cw_string = ":DYN 4,{0:5.4f}W,{1:5.4f}W,{2:5.4f}HZ,{3:5.4f}%".format(self.power1, self.power2, self.frequency, self.duty_cycle)

        return cw_string

    def validate(self, limit: float):
        if self.power2 > limit < self.power1:
            raise ValueOutOfLimitError(max(self.power2, self.power1), limit, "power value out of set limits")
        if self.duty_cycle >= 100:
            raise ValueOutOfLimitError(self.duty_cycle, 100, "duty cycle must be below 100%")


class PulseList(object):

    def __init__(self, slope1: float, slope2: float, current1: float, current2: float, duration: float):
        self.function = Mode.dynamic_pulse
        self.slope1 = float(slope1)
        self.slope2 = float(slope2)
        self.current1 = float(current1)
        self.current2 = float(current2)
        self.duration = float(duration)

    def __str__(self):
        pulse_string = ":DYN 5,{0:5.4f}A/uS,{1:5.4f}A/uS,{2:5.4f}A,{3:5.4f}A,{3:5.4f}S".format(self.slope1, self.slope2, self.current1, self.current2, self.duration)

        return pulse_string

    def validate(self, limit: float):
        if self.current2 > limit < self.current1:
            raise ValueOutOfLimitError(max(self.current2, self.current1), limit, "current value out of set limits")


class ToggleList(object):
    def __init__(self, slope1: float, slope2: float, current1: float, current2: float):
        self.function = Mode.dynamic_toggle
        self.slope1 = float(slope1)
        self.slope2 = float(slope2)
        self.current1 = float(current1)
        self.current2 = float(current2)

    def __str__(self):
        toggle_string = ":DYN 6,{0:5.4f}A/uS,{1:5.4f}A/uS,{2:5.4f}A,{3:5.4f}A".format(self.slope1, self.slope2, self.current1, self.current2)

        return toggle_string

    def validate(self, limit: float):
        if self.current2 > limit < self.current1:
            raise ValueOutOfLimitError(max(self.current2, self.current1), limit, "current value out of set limits")
