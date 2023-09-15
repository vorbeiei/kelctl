"""
Serial communication with Korad KEL103 and potentially KEL102 electronic loads.

The intent is to give easy access to the electronic load,
eliminating the need to know special codes.

The object supports the python `with` statement to release the serial
port automatically:

from KELSerial import KELSerial

with KELSerial('/dev/tty.usbmodemfd121') as device:
    print("Model: ", device.model)
    print("Status: ", device.status)

LICENSE: MIT

RESOURCES:

This library has been initially copied from the py-korad-serial project(https://github.com/starforgelabs/py-korad-serial) and been modified to work with the electronic loads.


"""

# from time import sleep
from .kellists import *
from .kelenums import *
from .kelerrors import *
import re
import serial
import ipaddress

# define Modes that support setting directly
settableModes = [Mode.constant_voltage, Mode.constant_current, Mode.constant_resistance, Mode.constant_power, Mode.short]


class Status(object):

    def __init__(self, status):
        """ Initialize object with a KELSerial status character.

        :param status: Status value
        :type status: int[]
        """
        super(Status, self).__init__()
        self.raw = status
        status_values = status.split(",")
        self.beep = OnOffState(int(status_values[0]))
        self.baudrate = BaudRate(int(status_values[1]))
        self.lock = OnOffState(int(status_values[2]))
        self.trigger = OnOffState(int(status_values[3]))
        self.comm = OnOffState(int(status_values[4]))
        # 1 more values is put out, unused according to documentation(though lock status and trigger status also is not mentioned and still available)

    def __repr__(self):
        return "{0}".format(self.raw)

    def __str__(self):
        message = "Beep: {0}, Lock: {1}, Baudrate: {2}, Trigger: {3}, Comm: {4}"
        return message.format(
            self.beep.name,
            self.lock.name,
            self.baudrate.b,
            self.trigger.name,
            self.comm.name
        )

    def __unicode__(self):
        return self.__str__()


def float_or_none(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def on_off_setting_or_none(value):
    try:
        return OnOffState(value)
    except (TypeError, ValueError):
        return None


class KELSerial(object):
    """
    Wrapper for communicating with a KEL103(and possibly KEL102)
    electronic load as a serial interface.
    """

    class Memory(object):
        """ Wrap a memory setting. """

        def __init__(self, serial_, memory_number):
            super(KELSerial
                  .Memory, self).__init__()
            self.__serial = serial_
            self.number = memory_number

        def recall(self):
            """ Recall this memory's settings.  """
            self.__serial.send("*RCL {0}".format(self.number))

        def save(self):
            """ Save the current value to this memory. """
            self.__serial.send("*SAV {0}".format(self.number))

    class OnOffButton(object):
        """ Wrap an on/off button. """

        def __init__(self, serial_, on_command, off_command, get_command):
            super(KELSerial
                  .OnOffButton, self).__init__()
            self.__serial = serial_
            self._on = on_command
            self._off = off_command
            self._get = get_command

        def on(self):
            self.__serial.send(self._on)

        def off(self):
            self.__serial.send(self._off)

        def get(self):
            return on_off_setting_or_none(self.__serial.send_receive(self._get))

    class Serial(object):
        """ Serial operations.

        There are some quirky things in communication. They go here.
        """

        def __init__(self, port, rate=115200, debug=False):
            super(KELSerial
                  .Serial, self).__init__()

            self.debug = debug
            self.port = serial.Serial(port, rate, timeout=1)

        def read_string(self, line_number=1):
            """ Read a string.

            It appears that the KEL103 returns
            newline terminated strings.

            :return: str
            """
            output = ""

            for line in range(1, line_number + 1):
                output += self.port.readline().decode()

            if self.debug:
                print("read: {0}".format(output))

            return output.strip('\n')

        def send(self, text):
            if self.debug:
                print("_send: ", text)
            # sleep(0.1) # may be needed, needs testing

            text = "%s\n" % text
            self.port.write(text.encode('ascii'))

        def send_receive(self, text, line_number=1):
            self.send(text)

            return self.read_string(line_number)

    def __init__(self, port, rate=115200, debug=False):
        super(KELSerial, self).__init__()

        self.__serial = KELSerial.Serial(port, rate, debug)

        # Memory recall/save buttons 1 through 100 -> mapped to memories 0 to 99
        self.memories = [
            KELSerial
            .Memory(self.__serial, i) for i in range(1, 101)
        ]

        self.input = KELSerial.OnOffButton(self.__serial, ":INP ON", ":INP OFF", ":INP?")
        self.settings = KELSerial.Settings(self.__serial)

    class Settings(object):
        def __init__(self, serial_):
            super(KELSerial
                  .Settings, self).__init__()
            self.__serial = serial_

            self.beep = KELSerial.OnOffButton(self.__serial, ":SYST:BEEP ON", ":SYST:BEEP OFF", ":SYST:BEEP?")
            self.lock = KELSerial.OnOffButton(self.__serial, ":SYST:LOCK ON", ":SYST:LOCK OFF", ":SYST:LOCK?")
            self.dhcp = KELSerial.OnOffButton(self.__serial, ":SYST:DHCP 1", ":SYST:DHCP 0", ":SYST:DHCP?")
            self.trigger = KELSerial.OnOffButton(self.__serial, ":SYST:EXIT ON", ":SYST:EXIT OFF", ":SYST:EXIT?")
            self.compensation = KELSerial.OnOffButton(self.__serial, ":SYST:COMP ON", ":SYST:COMP OFF", ":SYST:COMP?")

            """
            Since changing limits seems to only work on upper limit there seems to be not much point of getting lower limit.
            This applies to all limits.
            """
        @property
        def current_limit(self):
            result = self.__serial.send_receive(":CURR:UPP?")
            return float_or_none(result.rstrip("A"))

        @current_limit.setter
        def current_limit(self, value):
            self.__serial.send(":CURR:UPP {0:5.4f}A".format(value))

        @property
        def voltage_limit(self):
            result = self.__serial.send_receive(":VOLT:UPP?")
            return float_or_none(result.rstrip("V"))

        @voltage_limit.setter
        def voltage_limit(self, value):
            self.__serial.send(":VOLT:UPP {0:5.4f}V".format(value))

        @property
        def resistance_limit(self):
            result = self.__serial.send_receive(":RES:UPP?")
            return float_or_none(result.rstrip("OHM"))

        @resistance_limit.setter
        def resistance_limit(self, value):
            self.__serial.send(":RES:UPP {0:5.4f}OHM".format(value))

        @property
        def power_limit(self):
            result = self.__serial.send_receive(":POW:UPP?")
            return float_or_none(result.rstrip("W"))

        @power_limit.setter
        def power_limit(self, value):
            self.__serial.send(":POW:UPP {0:5.4f}W".format(value))

        def factoryreset(self):
            self.__serial.send(":SYST:FACTRESET")

        @property
        def baudrate(self):
            result = self.__serial.send_receive(
                ":SYST:BAUD?"
            )
            return BaudRate(int(result))

        @baudrate.setter
        def baudrate(self, rate: BaudRate):
            self.__serial.send(":SYST:BAUD {0}".format(rate.b))

        @property
        def subnetmask(self):
            result = self.__serial.send_receive(
                ":SYST:SMASK?"
            )
            return str(result)

        @subnetmask.setter
        def subnetmask(self, value: str):
            ip = ipaddress.ip_address(value)
            self.__serial.send(":SYST:SMASK {0}".format(ip))

        @property
        def ipaddress(self):
            result = self.__serial.send_receive(
                ":SYST:IPAD?"
            )
            return str(result)

        @ipaddress.setter
        def ipaddress(self, value: str):
            ip = ipaddress.ip_address(value)
            self.__serial.send(":SYST:IPAD {0}".format(ip))

        @property
        def gateway(self):
            result = self.__serial.send_receive(
                ":SYST:GATE?"
            )
            return str(result)

        @gateway.setter
        def gateway(self, value: str):
            ip = ipaddress.ip_address(value)
            self.__serial.send(":SYST:GATE {0}".format(ip))

        @property
        def macaddress(self):
            result = self.__serial.send_receive(
                ":SYST:MAC?"
            )
            return str(result)

        @macaddress.setter
        def macaddress(self, value: str):
            """ verifying proper mac address """
            if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", value.lower()):
                self.__serial.send(":SYST:MAC {0}".format(value.replace(":", "-")))
            else:
                raise ValueError

        @property
        def port(self):
            result = self.__serial.send_receive(
                ":SYST:PORT?"
            )
            return int(result)

        @port.setter
        def port(self, value: int):
            self.__serial.send(":SYST:PORT {0}".format(value))

    def __enter__(self):
        """ See documentation for Python's ``with`` command.
        """
        return self

    def __exit__(self, _type, value, traceback):
        """ See documentation for Python's ``with`` command.
        """
        self.close()
        return False

    # ##################################################################
    # Serial operations
    # ##################################################################

    @property
    def is_open(self):
        """ Report whether the serial port is open.
        :rtype: bool
        """
        return self.__serial.port.isOpen()

    def close(self):
        """ Close the serial port """
        self.__serial.port.close()

    def open(self):
        """ Open the serial port """
        self.__serial.port.open()

    # ##################################################################
    # Load operations
    # ##################################################################

    def trigger(self):
        """Simulate an external trigger, used for Pulse and trigger dynamic mode"""
        self.__serial.send("*TRG")

    def set_list(self, load_list: LoadList, recall=True):
        load_list.validate()
        self.__serial.send(load_list.__str__())

        if recall:
            self.recall_list(load_list.save_slot)

    def recall_list(self, list_number: int):
        if 1 > list_number > 7:
            raise ValueError("save-slot can only be from 1-7")

        self.__serial.send(":RCL:LIST " + str(list_number))

    def get_list(self, list_number: int):

        if 1 > list_number > 7:
            raise ValueError("save-slot can only be from 1-7")

        self.recall_list(list_number)
        list_string = self.__serial.send_receive(":RCL:LIST?")

        list_string = list_string.replace(" ", "")

        split_string = list_string.split(",")
        current_range = float(split_string[0][0:6])
        loop_number = int(split_string[-1])
        split_string = split_string[2:-1]
        steps = []
        count = int(len(split_string) / 3)
        for s in range(count):
            steps.append(ListStep(float(split_string.pop(0)[0:5]), float(split_string.pop(0)[0:5]), float(split_string.pop(0)[0:5])))

        return LoadList(list_number, current_range, steps, loop_number)

    def set_ocp(self, ocp_list: OCPList, recall=True):
        ocp_list.validate()

        self.__serial.send(ocp_list.__str__())

        if recall:
            self.recall_ocp(ocp_list.save_slot)

    def recall_ocp(self, list_number: int):
        if 1 > list_number > 10:
            raise ValueError("save-slot can only be from 1-10")

        self.__serial.send(":RCL:OCP " + str(list_number))

    def get_ocp(self, list_number: int):

        if 1 > list_number > 10:
            raise ValueError("save-slot can only be from 1-10")

        self.recall_ocp(list_number)
        list_string = self.__serial.send_receive(":RCL:OCP?")

        list_string = list_string.replace(" ", "").replace("A", "").replace("S", "").replace("V", "")

        split_string = list_string.split(",")
        on_voltage = float(split_string[0])
        on_delay = float(split_string[1])
        current_range = float(split_string[2])
        on_current = float(split_string[3])
        step_current = float(split_string[4])
        step_delay = float(split_string[5])
        off_current = float(split_string[6])
        ocp_voltage = float(split_string[7])
        max_overcurrent = float(split_string[8])
        min_overcurrent = float(split_string[9])

        return OCPList(list_number, on_voltage, on_delay, current_range, on_current, step_current, step_delay, off_current, ocp_voltage, max_overcurrent, min_overcurrent)

    def set_opp(self, opp_list: OPPList, recall=True):
        opp_list.validate()

        self.__serial.send(opp_list.__str__())

        if recall:
            self.recall_opp(opp_list.save_slot)

    def recall_opp(self, list_number: int):
        if 1 > list_number > 10:
            raise ValueError("save-slot can only be from 1-10")

        self.__serial.send(":RCL:OPP " + str(list_number))

    def get_opp(self, list_number: int):

        if 1 > list_number > 10:
            raise ValueError("save-slot can only be from 1-10")

        self.recall_opp(list_number)
        list_string = self.__serial.send_receive(":RCL:OPP?")

        list_string = list_string.replace(" ", "").replace("A", "").replace("S", "").replace("V", "").replace("W", "")

        split_string = list_string.split(",")
        on_voltage = float(split_string[0])
        on_delay = float(split_string[1])
        current_range = float(split_string[2])
        on_power = float(split_string[3])
        step_power = float(split_string[4])
        step_delay = float(split_string[5])
        off_power = float(split_string[6])
        opp_voltage = float(split_string[7])
        max_overpower = float(split_string[8])
        min_overpower = float(split_string[9])

        return OPPList(list_number, on_voltage, on_delay, current_range, on_power, step_power, step_delay, off_power,
                       opp_voltage, max_overpower, min_overpower)

    def set_batt(self, batt_list: BattList, recall=True):
        batt_list.validate()

        self.__serial.send(batt_list.__str__())

        if recall:
            self.recall_batt(batt_list.save_slot)

    def recall_batt(self, list_number: int):
        if 1 > list_number > 10:
            raise ValueError("save-slot can only be from 1-10")

        self.__serial.send(":RCL:BATT " + str(list_number))

    def get_batt(self, list_number: int):

        if 1 > list_number > 10:
            raise ValueError("save-slot can only be from 1-10")

        self.recall_batt(list_number)
        list_string = self.__serial.send_receive(":RCL:BATT?")

        list_string = list_string.replace(" ", "").replace("AH", "").replace("M", "").replace("V", "").replace("A", "")

        split_string = list_string.split(",")
        current_range = float(split_string[0])
        discharge_current = float(split_string[1])
        cutoff_voltage = float(split_string[2])
        cutoff_capacity = float(split_string[3])
        cutoff_time = float(split_string[4])

        return BattList(list_number, current_range, discharge_current, cutoff_voltage, cutoff_capacity, cutoff_time)

    def get_batt_time(self):
        batt_time = self.__serial.send_receive(":BATT:TIM?").replace("M", "")
        return float_or_none(batt_time)

    def get_batt_cap(self):
        batt_cap = self.__serial.send_receive(":BATT:CAP?").replace("AH", "")
        return float_or_none(batt_cap)

    def get_dynamic_mode(self):
        if self.function not in [Mode.dynamic_cv, Mode.dynamic_cc, Mode.dynamic_cr, Mode.dynamic_cw, Mode.dynamic_pulse,
                                 Mode.dynamic_toggle]:
            raise InvalidModeError(self.function)

        list_string = self.__serial.send_receive(":DYN?")
        list_string = list_string.replace(" ", "").replace("AH", "").replace("V", "").replace("A/uS", "").replace("HZ", "").replace("%", "").replace("A", "").replace("OHM", "").replace("W", "").replace("S", "")
        split_string = list_string.split(",")
        mode_string = int(split_string[0])

        match mode_string:
            case 1:
                voltage1 = float(split_string[1])
                voltage2 = float(split_string[2])
                frequency = float(split_string[3])
                duty_cycle = float(split_string[4])

                return CVList(voltage1, voltage2, frequency, duty_cycle)
            case 2:
                slope1 = float(split_string[1])
                slope2 = float(split_string[2])
                current1 = float(split_string[3])
                current2 = float(split_string[4])
                frequency = float(split_string[5])
                duty_cycle = float(split_string[6])

                return CCList(slope1, slope2, current1, current2, frequency, duty_cycle)
            case 3:
                resistance1 = float(split_string[1])
                resistance2 = float(split_string[2])
                frequency = float(split_string[3])
                duty_cycle = float(split_string[4])

                return CRList(resistance1, resistance2, frequency, duty_cycle)
            case 4:
                power1 = float(split_string[1])
                power2 = float(split_string[2])
                frequency = float(split_string[3])
                duty_cycle = float(split_string[4])

                return CWList(power1, power2, frequency, duty_cycle)
            case 5:
                slope1 = float(split_string[1])
                slope2 = float(split_string[2])
                current1 = float(split_string[3])
                current2 = float(split_string[4])
                duration = float(split_string[5])

                return PulseList(slope1, slope2, current1, current2, duration)
            case 6:
                slope1 = float(split_string[1])
                slope2 = float(split_string[2])
                current1 = float(split_string[3])
                current2 = float(split_string[4])

                return ToggleList(slope1, slope2, current1, current2)
            case _:
                raise InvalidModeError(list_string)

    def recall_dynamic_mode(self):
        return self.__serial.send_receive(":DYN?")

    def set_dynamic_mode(self, dynamic_list, recall=True):

        match dynamic_list.function:
            case Mode.dynamic_cv:
                limit = self.settings.voltage_limit
            case Mode.dynamic_cc:
                limit = self.settings.current_limit
            case Mode.dynamic_cr:
                limit = self.settings.resistance_limit
            case Mode.dynamic_cw:
                limit = self.settings.power_limit
            case Mode.dynamic_pulse:
                limit = self.settings.current_limit
            case Mode.dynamic_toggle:
                limit = self.settings.current_limit
            case _:
                raise ValueError()

        dynamic_list.validate(limit)

        self.__serial.send(dynamic_list.__str__())

        if recall:
            self.recall_dynamic_mode()

    @property
    def device_info(self):
        # Will just return full string, every item can already be gotten separately.
        """
        output is

        DHCP:0
        IP:192.168.1.198
        NETMASK:255.255.255.0
        GateWay:192.168.1.1
        MAC:70-2f-eb-48-4d-56
        PORT:18190
        BAUDRATE:115200
        """
        return self.__serial.send_receive(":SYST:DEVINFO?", 7)

    @property
    def model(self):
        """ Report the load model information.

        :rtype: str
        """
        return self.__serial.send_receive("*IDN?")

    @property
    def status(self):
        """ Report the load status.

        :rtype: KELSerial
    .Status or None
        """
        self.__serial.send(":STAT?")

        status = self.__serial.read_string()
        if len(status) == 0:
            return None
        else:
            return Status(status)

    @property
    def function(self):
        result = self.__serial.send_receive(
            ":FUNC?"
        )
        if len(result) == 0:
            return None
        else:
            return Mode(result)

    @function.setter
    def function(self, mode: Mode):
        if mode in settableModes:
            self.__serial.send(":FUNC {0}".format(mode.value))
        else:
            raise NoModeSetError(mode)

    @property
    def current(self):
        result = self.__serial.send_receive(
            ":CURR?"
        )
        return float_or_none(result.rstrip("A"))

    @current.setter
    def current(self, value):
        limit = self.settings.current_limit
        if value <= limit:
            self.__serial.send(":CURR {0:5.4f}A".format(value))
        else:
            raise ValueOutOfLimitError(value, limit)

    @property
    def voltage(self):
        return float_or_none(self.__serial.send_receive(":VOLT?").rstrip("V"))

    @voltage.setter
    def voltage(self, value):
        limit = self.settings.voltage_limit
        if value <= limit:
            self.__serial.send(":VOLT {0:5.4f}V".format(value))
        else:
            raise ValueOutOfLimitError(value, limit)

    @property
    def resistance(self):
        return float_or_none(self.__serial.send_receive(":RES?").rstrip("OHM"))

    @resistance.setter
    def resistance(self, value):
        limit = self.settings.resistance_limit
        if value <= limit:
            self.__serial.send(":RES {0:5.4f}OHM".format(value))
        else:
            raise ValueOutOfLimitError(value, limit)

    @property
    def power(self):
        return float_or_none(self.__serial.send_receive(":POW?").rstrip("W"))

    @power.setter
    def power(self, value):
        limit = self.settings.power_limit
        if value <= limit:
            self.__serial.send(":POW {0:5.4f}W".format(value))
        else:
            raise ValueOutOfLimitError(value, limit)

    @property
    def measured_current(self):
        """ Retrieve this device's currently sensed current.

        :return: Amperes
        :rtype: float or None
        """
        result = self.__serial.send_receive(
            ":MEAS:CURR?"
        )
        return float_or_none(result.rstrip("A"))

    @property
    def measured_voltage(self):
        """ Retrieve this device's currently sensed voltage.

        :return: Volts
        :rtype: float or None
        """
        result = self.__serial.send_receive(
            ":MEAS:VOLT?"
        )
        return float_or_none(result.rstrip("V"))

    @property
    def measured_power(self):
        """ Retrieve this device's used power.

        :return: Watts
        :rtype: float or None
        """
        result = self.__serial.send_receive(
            ":MEAS:POW?"
        )
        return float_or_none(result.rstrip("W"))
