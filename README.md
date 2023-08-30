# KELctl
This is a Python 3 library to provide easier means of controlling a Korad KEL103 electronic load over a serial connection. It will probably also work with a KEL102 load but this is untested.
I would recommend, in addition to this documentation, to also check the test.py file for examples on hwo to use the library. Additionally more details about certain aspects on how the load works are provided in the KEL-103 protocol documentation.

It uses the [aenum library](https://github.com/ethanfurman/aenum).
The minimum required python version required is 3.10.

This library has been initially copied from the [py-korad-serial project](https://github.com/starforgelabs/py-korad-serial) and been modified to work with the electronic loads instead of power supplies.


## Hardware
The [ Korad KEL103/KEL102 ](https://www.koradtechnology.com/product/81.html) is sold under different names and brands i.e. RND 320-KEL103.


# Usage
Examples for basic usage of all functions are included in the test.py file.

The object supports the python `with` statement to release the serial
port automatically:

```
from KELSerial import KELSerial

with KELSerial('/dev/ttyACM0') as load:
    print("Model: ", load.model)
    print("Status: ", load.status)
```


# Class  Documentation

## `KELSerial` Class

### Constructor `__init__(port, debug=False)`

The constructor takes a string containing the serial device to attach to.
If `debug` is set to `True`, then data sent and received is printed to output.
___

### `input` Attribute

Turns on and off the input of the load.

`load.input.on()` and `load.input.off()`

Gets state of input and returns an [OnOffState](#onoffstate-class)

`load.input.get()` returns OnOffState.off or OnOffState.on
___

### `memories` Attribute

This is an array of memory settings for all memories from 1-100 on unit mapped to the array from 0 to 99. Can be used to save and recall memories on unit.
The saved values can not be retrieved directly from the unit. When recalling a memory the corresponding mode on unit will be set together with the saved value.
Memories will not return anything.

```
m1 = load.memories[0]
m1.recall()
m2 = load.memories[99]
m2.save()
```
___

### `model` property (read-only)

Returns the load model information.

`RND 320-KEL103 V2.60 SN:01234567`
___

### `device_info` property (read-only)

Returns some device information as a multiline string.
`load.device_info` returns:
```
DHCP:0
IP:192.168.1.198
NETMASK:255.255.255.0
GateWay:192.168.1.1
MAC:70-2f-eb-48-4d-56
PORT:18190
BAUDRATE:115200
```
___

### `status` property

Returns a [Status object](#status-class) representing current status of certain settings.

`load.status` returns [Status](#status-class)
___

### `voltage` property

Sets the voltage value for the constant voltage mode and switches to it. Takes float as value in Volts.

Raises [ValueOutOfLimitError](#valueoutoflimiterror-class) when trying to set value above set limits.

`load.voltage = 30.05`

Gets the voltage value for constant voltage mode. Returns float value in Volts.

`load.voltage` returns `30.05` as float or returns none
___

### `current` property

Sets the current value for the constant current mode and switches to it. Takes float as value in Amps.

Raises [ValueOutOfLimitError](#valueoutoflimiterror-class) when trying to set value above set limits.

`load.current = 10.05`

Gets the current value for constant current mode. Returns float value in Amps.

`load.current` returns `10.05` as float or returns none
___

### `power` property

Sets the power value for the constant power mode and switches to it. Takes float as value in Watts.

Raises [ValueOutOfLimitError](#valueoutoflimiterror-class) when trying to set value above set limits.

`load.power = 20.05`

Gets the power value for constant power mode. Returns float value in Watts.

`load.power` returns `20.05` as float or returns none
___

### `resistance` property

Sets the resistance value for the constant resistance mode and switches to it. Takes float as value in Ohms.

Raises [ValueOutOfLimitError](#valueoutoflimiterror-class) when trying to set value above set limits.

`load.resistance = 2000.05`

Gets the resistance value for constant resistance mode. Returns float value in Ohms.

`load.resistance` returns `2000.05` as float or returns none
___

### `measured_voltage` property (read-only)

Reads the voltage currently present at device. Returns float value in Volts.

`load.measured_voltage` returns `30.05` as float or returns none
___

### `measured_power` property (read-only)

Reads the power currently present at device. Returns float value in Watts.

`load.measured_power` returns `20.05` as float or returns none
___

### `measured_current` property (read-only)

Reads the current currently present at device. Returns float value in Amps.

`load.measured_current` returns `10.05` as float or returns none
___

### `function` property

Sets the mode/function of the load. Setting the function in this way is limited to certain modes(constant-voltage, constant-current, constant-resistance, constant-power, short). Trying to set other mode will raise a [NoModeSetError](#nomodeseterror-class).
Takes a [Mode](#mode-class)(Enum) as input.

`load.function = Mode.constant_voltage`

Gets currently active function and returns it as [Mode](#mode-class)(Enum).

`load.function` returns `Mode.constant_voltage`
___

### `set_list` function

Sets and saves a list and optionally recalls the list on device. Recall option defaults to true if not used. Takes a [LoadList object](#loadlist-class) as input and will validate the list before setting it to prevent errors on device. Will raise a ValueError or [ValueOutOfLimitError](#valueoutoflimiterror-class) on failed validation.
```
steps = [ListStep(3, 0.002, 5), ListStep(2, 0.003, 3), ListStep(2, 0.005, 2)]
testList = LoadList(3, 10, steps, 6)
load.set_list(testList, True)
```
___

### `get_list` function

Recalls and then retrieves selected list by save-slot and returns [LoadList object](#loadlist-class). Will raise ValueError if trying to get invalid list(valid is 1-7).

`load.get_list(3)` returns [LoadList](#loadlist-class)
___

### `recall_list` function

Recalls existing list on device. Recalling non-existing list will result in error on device. Will raise ValueError if trying to get invalid list(valid is 1-7).

`load.recall_list(3)`
___

### `set_ocp` function

Sets and saves an OCP-list and if set recalls the list on device. Recall option defaults to true if not used. Takes a [OCPList object](#opplist-class) as input and will validate the list before setting it to prevent errors on device. Will raise a ValueError or [ValueOutOfLimitError](#valueoutoflimiterror-class) on failed validation.
```
ocpList = OCPList(1, 10, 4, 20, 15, 1, 1, 5, 30, 10.52, 8.34)
load.set_ocp(ocpList)
```
___

### `get_ocp` function

Recalls and then retrieves selected OCP-list by save-slot and returns [OCPList object](#opplist-class). Will raise ValueError if trying to get invalid list(valid is 1-10).

`load.get_ocp(1)` returns [OCPList](#opplist-class)
___

### `recall_ocp` function

Recalls existing OCP-list on device. Recalling non-existing list will result in error on device. Will raise ValueError if trying to get invalid list(valid is 1-10).

`load.recall_ocp(1)`
___

### `set_opp` function

Sets and saves an OPP-list and if set recalls the list on device. Recall option defaults to true if not used. Takes an [OPPList object](#opplist-class) as input and will validate the list before setting it to prevent errors on device. Will raise a ValueError or [ValueOutOfLimitError](#valueoutoflimiterror-class) on failed validation.
```
oppList = OPPList(1, 11, 4, 20, 15, 1, 1, 5, 30, 10.52, 8.34)
load.set_opp(oppList)
```
___

### `get_opp` function

Recalls and then retrieves selected OPP-list by save-slot and returns [OPPList object](#opplist-class). Will raise ValueError if trying to get invalid list(valid is 1-10).

`load.get_opp(1)` returns [OPPList](#opplist-class)
___

### `recall_opp` function

Recalls existing OPP-list on device. Recalling non-existing list will result in error on device. Will raise ValueError if trying to get invalid list(valid is 1-10).

`load.recall_opp(1)`
___

### `set_batt` function

Sets and saves a Battery-test-list and if set recalls the list on device. Recall option defaults to true if not used. Takes an [BattList object](#battlist-class) as input and will validate the list before setting it to prevent errors on device. Will raise a ValueError or [ValueOutOfLimitError](#valueoutoflimiterror-class) on failed validation.
```
battList = BattList(1, 20.23, 10, 10, 30, 5)
load.set_batt(battList)
```
___

### `get_batt` function

Recalls and then retrieves selected Battery-test-list by save-slot and returns [BattList object](#battlist-class). Will raise ValueError if trying to get invalid list(valid is 1-10).

`load.get_batt(1)` returns [BattList](#battlist-class)
___

### `recall_batt` function

Recalls existing Battery-test-list on device. Recalling non-existing list will result in error on device. Will raise ValueError if trying to get invalid list(valid is 1-10).

`load.recall_batt(1)`
___

### `get_batt_cap` function

Returns current capacity measured from battery-test. Returns AH as float.

`load.get_batt_cap()` returns `5.1234` as float or returns none
___

### `get_batt_time` function

Returns current time battery-test has been running. Returns minutes as float.

`load.get_batt_time()` returns `5.1234` as float or returns none
___

### `set_dynamic_mode` function

Sets and saves a dynamic-mode-list and if set recalls the list on device. Recall option defaults to true if not used. Takes one of the six [dynamic-list objects](#dynamic-lists) as input and will validate the list before setting it to prevent errors on device. Will raise a [ValueOutOfLimitError](#valueoutoflimiterror-class) on failed validation.
```
dyn1List = CVList(30.02, 20.05, 1.5, 30)
load.set_dynamic_mode(dyn1List)
```
___

### `get_dynamic_mode` function

Recalls and gets currently set dynamic-mode and returns appropriate [dynamic-list object](#dynamic-lists) depending on which of the dynamic modes is set. Will raise [InvalidModeError](#invalidmodeerror-class) when function is called with device not in a dynamic mode.

`load.get_dynamic_mode()` returns [dynamic-list object](#dynamic-lists)
___

### `recall_dynamic_mode` function

Recalls dynamic mode and returns string returned from unit. This function is required to be called after setting a dynamic mode before being able to use it(Per default is done in set method already).

`load.recall_dynamic_mode()`
___
___

### `settings` attribute

The settings attribute is an instance of the Settings class giving access to the various settings of the device.


#### `beep` attribute

Turns on or off the "beep" setting or returns state as [OnOffState](#onoffstate-class).

`load.settings.beep.on()` or `load.settings.beep.off()`

Gets state of setting and returns [OnOffState](#onoffstate-class).

`load.settings.beep.get()` returns OnOffState.on or OnOffState.off
___

#### `lock` attribute

Turns on or off the "lock" setting causing the keys on front of unit to be locked or unlocked.

`load.settings.lock.on()` or `load.settings.lock.off()`

Gets state of setting and returns [OnOffState](#onoffstate-class).

`load.settings.lock.get()` returns OnOffState.on or OnOffState.off
___

#### `dhcp` attribute

Turns on or off "DHCP" setting.

`load.settings.dhcp.on()` or `load.settings.dhcp.off()`

Gets state of setting and returns [OnOffState](#onoffstate-class).

`load.settings.dhcp.get()` returns OnOffState.on or OnOffState.off
___

#### `trigger` attribute

Turns on or off the "Trigger" setting which will enable or disable the external trigger input on device. Does not affect the trigger command over serial or on device.

`load.settings.trigger.on()` or `load.settings.trigger.off()`

Gets state of setting and returns [OnOffState](#onoffstate-class).

`load.settings.trigger.get()` returns OnOffState.on or OnOffState.off
___

#### `compensation` attribute

Turns on or off the "Compensation" setting which will enable or disable the external compensation function. With compensation on according to official documentation Memories are unavailable.

`load.settings.compensation.on()` or `load.settings.compensation.off()`

Gets state of setting and returns [OnOffState](#onoffstate-class).

`load.settings.compensation.get()` returns OnOffState.on or OnOffState.off
___

#### `ipaddress` property

Sets the IP-Address of device. IP-Address will be verified to ensure proper formatting. Will raise ValueError if improperly formatted

`load.settings.ipaddress = "10.0.0.123"`

Gets the IP-Adress of device.

`load.settings.ipaddress` returns `10.0.0.123`
___

#### `subnetmask` property

Sets the Subnetmask of device. Subnetmask will be verified to ensure proper formatting. Will raise ValueError if improperly formatted

`load.settings.subnetmask = "255.255.255.0"`

Gets the Subnetmask of device.

`load.settings.subnetmask` returns `255.255.255.0`
___

#### `gateway` property

Sets the Gateway of device. Gateway will be verified to ensure proper formatting. Will raise ValueError if improperly formatted

`load.settings.gateway = "10.0.0.1"`

Gets the Gateway of device.

`load.settings.gateway` returns `10.0.0.1`
___

#### `macaddress` property

Sets the Mac-Address of device. Mac-Address will be verified to ensure proper formatting. Will raise ValueError if improperly formatted. Will take addresses using either `:` or `-` as separator.

`load.settings.macaddress = "00-80-41-ae-fd-7e"`

Gets the Mac-Address of device.

`load.settings.macaddress` returns `01:80:41:ae:fd:7e`
___

#### `baudrate` property

Sets the Baudrate of device. Takes [BaudRate](#baudrate-class) Enum.

`load.settings.baudrate = BaudRate(3)"` or `load.settings.baudrate = BaudRate(57600)"` or `load.settings.baudrate = BaudRate.R57600"`

Gets the Baudrate of device.

`load.settings.baudrate` returns [BaudRate](#baudrate-class) Enum.
___

#### `port` property

Sets the network Port of device.

`load.settings.port = 12345"`

Gets the network Port of device.

`load.settings.port` returns `12345` as Integer
___

#### `voltage_limit` property

Sets the voltage limit of device. Takes float as value in Volts.

`load.settings.voltage_limit = 100.05`

Gets the voltage limit of device. Returns float value in Volts.

`load.settings.voltage_limit` returns `100.05` as float or returns none
___

#### `current_limit` property

Sets the current limit of device. Takes float as value in Amps.

`load.settings.current_limit = 20.05`

Gets the current limit of device. Returns float value in Amps.

`load.settings.current_limit` returns `20.05` as float or returns none
___

#### `power_limit` property

Sets the power limit of device. Takes float as value in Watts.

`load.settings.power_limit = 200.05`

Gets the power limit of device. Returns float value in Watts.

`load.settings.power_limit` returns `200.05` as float or returns none
___

#### `resistance_limit` property

Sets the resistance limit of device. Takes float as value in Ohms.

`load.settings.resistance_limit = 2000.05`

Gets the resistance limit of device. Returns float value in Ohms.

`load.settings.resistancer_limit` returns `2000.05` as float or returns none
___

#### `factoryreset` function

Resets the device to it's factory-settings. This may disrupt the serial connection for it to be reenabled/baud rate set again on device directly.

`load.settings.factoryreset()`
___
___

## `Status` class

Object representing the values returned by the `:STAT ?` command.
Consists of `beep`, `lock`, `trigger`, `comm` as [OnOffState](#onoffstate-class) and `baudrate` as [BaudRate](#baudrate-class).


### `__str__` function

Will return the mentioned variables as readable String.
`Beep: on, Lock: on, Baudrate: 115200, Trigger: on, Comm: on`
___

## `ListStep` class

The ListStep class represents a single step from a LoadList class.
It consists of the following values: current(in Amps, float), current_slope(rate at which current will change to defined value in A/uS, float), duration(duration of this step in seconds, float)

`step = ListStep(3, 0.002, 5)`
___

## `LoadList` class

The LoadList class represents all values required for using the list function of the device.

It consists of the following values: 

save-slot(in which save-slot 1-7 the list will be saved in, int), current_range(the limit up to which value the current can be set in Amps, Lists are not restricted by limits set in settings, float), steps(an array of ListStep objects), loop_number(how often the steps will be repeated, int)
```
steps = [ListStep(3, 0.002, 5), ListStep(2, 0.003, 3), ListStep(2, 0.005, 2)]
testlist = LoadList(3, 10, steps, 6)
```


### `validate` function

This function will validate a LoadList to make sure that the save-slot is between 1 and 7, that there are a maximum of 84 steps and that current values are within set range.
Will raise ValueError or [ValueOutOfLimitError](#valueoutoflimiterror-class) if validation failed.
`testlist.validate()`


### `__str__` function

Function will return the string required to be sent to device to set the list.
___

## `OCPList` class

The OCPList class represents all values required for using the OCP function of the device.

It consists of the following values: 

save-slot(in which save-slot 1-10 the list will be saved in, int), on_voltage(voltage above which test will start in Volts, float), on_delay(delay in seconds after reaching on_voltage after which test starts, float), current_range(the limit up to which value the current can be set in Amps, Lists are not restricted by limits set in settings, float), initial_current(current at which test starts out in Amps, float), step_current(current value in Amps which each step will go down by, float), step_delay(delay in seconds after each step before next step down, float), off_current(current in Amps below which test will stop, float), ocp_voltage(value in Volts above voltage has to rise for successful test, float), max_overcurrent(max current value in Amps at which OCP has to disengage at for successful test, float), min_overcurrent(min current value in Amps at which OCP has to disengage at for successful test, float)
```
ocpList = OCPList(1, 10, 4, 20, 15, 1, 1, 5, 30, 10.52, 8.34)
```


### `validate` function

This function will validate an OCPList to make sure that the save-slot is between 1 and 10, that current values are within set range and several checks for values(refer to protocol documentation for detailed requirements on values).
Will raise ValueError or [ValueOutOfLimitError](#valueoutoflimiterror-class) if validation failed.
`ocplist.validate()`


### `__str__` function

Function will return the string required to be sent to device to set the list.
___

## `OPPList` class

The OPPList class represents all values required for using the OPP function of the device.

It consists of the following values: 

save-slot(in which save-slot 1-10 the list will be saved in, int), on_voltage(voltage above which test will start in Volts, float), on_delay(delay in seconds after reaching on_voltage after which test starts, float), current_range(the limit up to which value the current can be set in Amps, Lists are not restricted by limits set in settings, float), initial_power(power at which test starts out in Watts, float), step_power(power value in Watts which each step will go down by, float), step_delay(delay in seconds after each step before next step down, float), off_power(power in Watts below which test will stop, float), opp_voltage(value in Volts above voltage has to rise for successful test, float), max_overpower(max power value in Watts at which OPP has to disengage at for successful test, float), min_overpower(min power value in Watts at which OPP has to disengage at for successful test, float)
```
oppList = OPPList(1, 10, 4, 20, 15, 1, 1, 5, 30, 10.52, 8.34)
```


### `validate` function

This function will validate an OPPList to make sure that the save-slot is between 1 and 10 and several checks for values(refer to protocol documentation for detailed requirements on values).
Will raise ValueError or [ValueOutOfLimitError](#valueoutoflimiterror-class) if validation failed.
`opplist.validate()`


### `__str__` function

Function will return the string required to be sent to device to set the list.
___

## `BattList` class

The BattList class represents all values required for using the Battery test function of the device.

It consists of the following values: 

save-slot(in which save-slot 1-10 the list will be saved in, int), current_range(the limit up to which value the current can be set in Amps, Lists are not restricted by limits set in settings, float), discharge_current(current in Amps at which the battery will be discharged at, float), cutoff_voltage(voltage in Volts at which test will stop, float), cutoff_capacity(capacity in AH at which test will stop, float), cutoff_time(time in minutes after which the test will stop, float)
```
battList = BattList(1, 20.23, 10, 10, 30, 5)
```


### `validate` function

This function will validate an BattList to make sure that the save-slot is between 1 and 10 and that the discharge current is within set current range.
Will raise ValueError if validation failed.
`battList.validate()`


### `__str__` function

Function will return the string required to be sent to device to set the list.
___
___

## Dynamic Lists

These are the 6 different dynamic list classes.


### `CVList` class

The CVList class represents all values required for using the constant voltage dynamic mode function of the device.

It consists of the following values: 

voltage1(first voltage value in Volts, float), voltage2(second voltage in Volts, float), frequency(frequency in Hz at which voltage switching will perform full cycle, float), duty_cycle(portion in % the second voltage will be in use, float)
```
dyn1List = CVList(30.02, 20.05, 1.5, 30)
```


#### `validate` function

This function will validate a CVList to make sure that voltage values are below limit in settings and that the duty cycle is below 100%.
Will raise [ValueOutOfLimitError](#valueoutoflimiterror-class) if validation failed.
`dyn1List.validate()`


#### `__str__` function

Function will return the string required to be sent to device to set the list.
___

### `CCList` class

The CCList class represents all values required for using the constant current dynamic mode function of the device.

It consists of the following values: 

slope1(rate at which current will rise to first value in A/uS, float), slope2(rate at which current will rise to second value in A/uS, float), current1(first current value in Amps, float), current2(second current in Amps, float), frequency(frequency in Hz at which current switching will perform full cycle, float), duty_cycle(portion in % the second current will be in use, float)
```
dyn2List = CCList(0.4, 0.5, 5, 6, 3, 40)
```


#### `validate` function

This function will validate a CCList to make sure that current values are below limit in settings and that the duty cycle is below 100%.
Will raise [ValueOutOfLimitError](#valueoutoflimiterror-class) if validation failed.
`dyn2List.validate()`


#### `__str__` function

Function will return the string required to be sent to device to set the list.
___

### `CRList` class

The CRList class represents all values required for using the constant resistance dynamic mode function of the device.

It consists of the following values: 

resistance1(first resistance value in Ohms, float), resistance2(second resistance in Ohms, float), frequency(frequency in Hz at which resistance switching will perform full cycle, float), duty_cycle(portion in % the second resistance will be in use, float)
```
dyn3List = CRList(30.02, 20.05, 1.5, 30)
```


#### `validate` function

This function will validate a CRList to make sure that resistance values are below limit in settings and that the duty cycle is below 100%.
Will raise [ValueOutOfLimitError](#valueoutoflimiterror-class) if validation failed.
`dyn3List.validate()`


#### `__str__` function

Function will return the string required to be sent to device to set the list.
___

### `CWList` class

The CWList class represents all values required for using the constant power dynamic mode function of the device.

It consists of the following values: 

power1(first power value in Watts, float), power2(second power in Watts, float), frequency(frequency in Hz at which power switching will perform full cycle, float), duty_cycle(portion in % the second power will be in use, float)
```
dyn4List = CWList(6, 9, 3, 40)
```


#### `validate` function

This function will validate a CWList to make sure that power values are below limit in settings and that the duty cycle is below 100%.
Will raise [ValueOutOfLimitError](#valueoutoflimiterror-class) if validation failed.
`dyn4List.validate()`


#### `__str__` function

Function will return the string required to be sent to device to set the list.
___

### `PulseList` class

The PulseList class represents all values required for using the pulse dynamic mode function of the device.

It consists of the following values: 

slope1(rate at which current will rise to first value in A/uS, float), slope2(rate at which current will rise to second value in A/uS, float), current1(first current in Amps, float), current2(second current in Amps, float),duration(duration in seconds the second current value will stay on after receiving trigger, float)
```
dyn5List = PulseList(0.3, 0.2, 4, 6, 5)
```


#### `validate` function

This function will validate a PulseList to make sure that current values are below limit in settings.
Will raise [ValueOutOfLimitError](#valueoutoflimiterror-class) if validation failed.
`dyn5List.validate()`


#### `__str__` function

Function will return the string required to be sent to device to set the list.
___

### `ToggleList` class

The ToggleList class represents all values required for using the toggle dynamic mode function of the device.

It consists of the following values: 

slope1(rate at which current will rise to first value in A/uS, float), slope2(rate at which current will rise to second value in A/uS, float), current1(first current in Amps, float), current2(second current in Amps, float)
```
dyn6List = ToggleList(0.3, 0.2, 4, 6)
```


#### `validate` function

This function will validate a ToggleList to make sure that current values are below limit in settings.
Will raise [ValueOutOfLimitError](#valueoutoflimiterror-class) if validation failed.
`dyn6List.validate()`


#### `__str__` function

Function will return the string required to be sent to device to set the list.
___
___

## Enums

Describes the Enums used, making use of aenums MultiValueEnum.


### `Mode` class

Represents the various modes/functions the device operates in to provide more useful names bound to the values used by the load.
The following modes are included:
```
constant_voltage = "CV"
constant_current = "CC"
constant_resistance = "CR"
constant_power = "CW"
battery = "BATTERY"  # read only
short = "SHORt"
OCP = "OCP"  # read only
LIST = "LIST"  # read only
OPP = "OPP"  # read only
dynamic_cv = "CONTINUOUS CV"  # read only like all dynamic modes
dynamic_cc = "CONTINUOUS CC"
dynamic_cr = "CONTINUOUS CR"
dynamic_cw = "CONTINUOUS CW"
dynamic_pulse = "PULSE"
dynamic_toggle = "TOGGLE"
```
___

### `BaudRate` class

Represents the available baud rates the device operates in to provide a single type of value for the different ways the load outputs it in.
Due to using a MultiValueEnum you can get both values from the Enum like this:

```
rate = BaudRate.R57600
print("First Value: ", rate.a)
print("Second Value: ", rate.b)
```

The following rates are included:
```
R9600 = (0, 9600)
R19200 = (1, 19200)
R38400 = (2, 38400)
R57600 = (3, 57600)
R115200 = (4, 115200)
```
___

### `OnOffState` class

Represents the on/off state to provide a single type of value for the different ways the load outputs it in.
Due to using a MultiValueEnum you can get both values from the Enum like this:

```
state = OnOffState.on
print("First Value: ", state.a)
print("Second Value: ", state.b)
```

The following rates are included:
```
off = (0, "OFF")
on = (1, "ON")
```
___
___

## Custom Errors

### `InvalidModeError` class

This exception is raised when trying to get a mode that is not currently set. For example if the current mode is not a dynamic mode, trying to get the information from a dynamic mode will result in this error since the unit can only return a dynamic mode that is set and recalled.

The error will return both the `mode` the load currently operates in and a `message`.
___

### `ValueOutOfLimitError` class

This exception is raised for errors in the input value. Since there apparently exists a firmware bug allowing setting values above limits for resistance and power(see protocol docs) the library will check and limit values itself and raise this error if trying to set values outside of limits.

The error will return the `value` that was tried to be set, the `limit` that is currently set and a `message`
___

### `NoModeSetError` class

This exception is raised when trying to set a mode that does not support being set directly(read-only in [Mode](#mode-class)-Enum).

The error will return the `mode` that was tried to be set and a `message`.