from aenum import Enum, MultiValueEnum


class Mode(Enum):
    """ Represents modes.

    These values should correspond to the values returned
    by the ``FUNCtion?`` command.
    """
    constant_voltage = "CV"
    constant_current = "CC"
    constant_resistance = "CR"
    constant_power = "CW"
    battery = "BATTERY"  # read only
    short = "SHORt"  # NOT a typo, actual output
    OCP = "OCP"  # read only
    LIST = "LIST"  # read only
    OPP = "OPP"  # read only
    dynamic_cv = "CONTINUOUS CV"  # read only - all dynamic modes
    dynamic_cc = "CONTINUOUS CC"
    dynamic_cr = "CONTINUOUS CR"
    dynamic_cw = "CONTINUOUS CW"
    dynamic_pulse = "PULSE"
    dynamic_toggle = "TOGGLE"


class BaudRate(MultiValueEnum):
    """
    These first values correspond to the baud rate returned
    by the ``STATUS?`` command. The scond values correspond to the baud rate returned by the ``:SYST:BAUD?`` command.
    """
    _init_ = 'a b'
    R9600 = (0, 9600)
    R19200 = (1, 19200)
    R38400 = (2, 38400)
    R57600 = (3, 57600)
    R115200 = (4, 115200)


class OnOffState(MultiValueEnum):
    """ Represents on/off states.

    This could just as easily be done as a Boolean, but is explicit.
    """
    off = (0, "OFF")
    on = (1, "ON")
