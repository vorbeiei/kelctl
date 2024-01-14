# Korad KEL103 commands over serial connection

This documentation is intended as an improved, more complete and corrected version of the official one. Adding information missing from the original and obtained from their own sample programs or by trial and error as well as correcting various errors throughout the official documentation.

Obviously this information may still be missing things or have errors in which case Pull requests or Issues are welcome.


## `*IDN?` command

**Parameters:** none

**Command Interpretation:** Returns product information

**Setup:** none

**Query:** `*IDN?`

**Return:** `RND 320-KEL103 V2.60 SN:01234567`

___

## `*SAV` command

**Parameters:** `save-slot`

**Parameter Description:** Any number between 1 and 100 for save slot

**Command Interpretation:** Stores current value for basic modes(CC,CV,CR,CW) to save slot in unit

**Setup:** `*SAV 20`

**Query:** none

___

## `*RCL` command

**Parameters:** `save-slot`

**Parameter Description:** Any number between 1 and 100 for save slot

**Command Interpretation:** Recalls value from save slot in unit and switches to corresponding mode

**Setup:** none

**Query:** `*RCL 20`

**Return:** none

___

## `*TRG` command

**Parameters:** none

**Command Interpretation:** Simulates an external trigger command, only valid in the pulse and flip(toggle) dynamic modes.

**Setup:** `*TRG`

**Query:** none

___

## `:SYST:` or `:SYSTem:` commands

### Boolean commands

**Parameters:** `BEEP` or `DHCP` or `LOCK` or `EXIT` or `COMP` **and** `?` or `ON` or `OFF`

**Parameter Interpretation:** Buzzer or DHCP-status or Lockstate or external Trigger(Exit) or remote-compensation **and** get or set on or off

**Command Interpretation:** Set or get system parameters. DHCP uses `1` and `0` instead of `ON` and `OFF`

**Setup:** `:SYST:BEEP ON`

**Query:** `:SYST:BEEP?`

**Return:** `ON`

### Value commands

**Parameters:** `SMASK` or `IPAD` or `GATE` or `BAUD` or `MAC` or `PORT` or `DEVINFO` or `FACTRESET` **and** `?` or `value`

**Parameter Interpretation:** Subnetmask or IP-Address or Gateway or Baudrate or MAC-Address or Port or Device-info or Factory-reset **and** get or set value

**Command Interpretation:** Set or get system parameters.

**Setup:** `:SYST:SMASK 255.255.255.0` 

**Query:** `:SYST:SMASK?`

**Return:** `255.255.255.0` 

___

## `:STAT?` or `:STATus` command

**Parameters:** none

**Command Interpretation:** Get device status. First number is buzzer status, second is baudrate(0-9600, 1-19200, 2-38400, 3-57600, 4-115200), third is lock status, fourth is trigger status(EXIT, enable/disable external trigger, does not affect internal and trigger over remote control), fifth is remote-compensation-status and the last one is either unused or unknown as of now.

**Setup:** none

**Query:** `:STAT?`

**Return:** `0,4,0,0,0,0` 

___

## `:INP` or `:INPut` command

**Parameters:** `state` or `?`

**Parameter Interpretation:** either OFF or ON or get status

**Command Interpretation:** Set input of device to on or off and get status of input.

**Setup:** `:INP ON`

**Query:** `:INP?`

**Return:** `ON`

___

## `:VOLT` or `:VOLTage` command

**Parameters:** `value` or `?`

**Parameter Interpretation:** Voltage value or get currently set voltage

**Command Interpretation:** Set or get voltage for constant voltage mode, will also switch to CV mode when setting. When trying to set value higher than set limit, value will be set to limit.

**Setup:** `:VOLT 10V`

**Query:** `:VOLT?`

**Return:** `10.000V`

### `:VOLT:UPP` or `:VOLTage:LOW` command

**Parameters:** `value` or `?`

**Parameter Interpretation:** Voltage value or get currently set voltage

**Command Interpretation:** Set or get upper voltage limit and get lower limit. When trying to set value higher than device limits, actual device limit is set. Limits are only enforced in direct modes.

**Setup:** `:VOLT:UPP 100V`

**Query:** `:VOLT:UPP?`

**Return:** `100.00V`

___

## `:CURR` or `:CURRent` command

**Parameters:** `value` or `?`

**Parameter Interpretation:** Current value or get currently set current

**Command Interpretation:** Set or get current for constant current mode, will also switch to CC mode when setting. When trying to set value higher than set limit, value will be set to limit.

**Setup:** `:CURR 10A`

**Query:** `:CURR?`

**Return:** `10.000A`

### `:CURR:UPP` or `:CURRent:LOW` command

**Parameters:** `value` or `?`

**Parameter Interpretation:** Current value or get currently set current

**Command Interpretation:** Set or get upper current limit and get lower limit. When trying to set value higher than device limits, actual device limit is set. Limits are only enforced in direct modes.

**Setup:** `:CURR:UPP 10A`

**Query:** `:CURR:UPP?`

**Return:** `10.000A`

___

## `:RES` or `:RESistance` command

**Parameters:** `value` or `?`

**Parameter Interpretation:** Resistance value or get currently set resistance

**Command Interpretation:** Set or get resistance for constant resistance mode, will also switch to CR mode when setting. When setting values outside of set limits, limit is set to limit value of power in OHMs. For example upper limit is set to 6000OHM and CR value then set to 7000OHM will actually set whatever power limit is set(i.e.250W -> 250OHM). This seems to be a mixup with the power limit since the reverse happens with that one. Basically this means that power and resistance limits are unreliable and should not be trusted. Set limits still work for input at device, since there increasing values above limit simply is not possible. (May be fixed in later revisions of device?)

**Setup:** `:RES 10OHM`

**Query:** `:RES?`

**Return:** `10.000OHM`

### `:RES:UPP` or `:RESistance:LOW` command

**Parameters:** `value` or `?`

**Parameter Interpretation:** Resistance value or get currently set resistance

**Command Interpretation:** Set or get upper resistance limit and get lower limit. When setting values outside of device limits, limit is supposed to be set to the highest actual possible value, which does not seem to work, see above description for details. Limits are only enforced in direct modes.

**Setup:** `:RES:UPP 10OHM`

**Query:** `:RES:UPP?`

**Return:** `10.000OHM`

___

## `:POW` or `:POWer` command

**Parameters:** `value` or `?`

**Parameter Interpretation:** Power value or get currently set power

**Command Interpretation:** Set or get power for constant power mode, will also switch to CW mode when setting. When setting values outside of set limits, limit is set to resistance limit value in Watts. For example upper limit is set to 50W and CW value then set to 70W will actually show whatever value the resistance limit is set to in Watts be set and will actually go over the 70W value. Basically this means that power and resistance limits are unreliable and should not be trusted for use over serial. Set limits still work for input at device, since there increasing values above limit simply is not possible.(May be fixed in later revisions of device?)

**Setup:** `:POW 100W`

**Query:** `:POW?`

**Return:** `100.00W`

### `:POW:UPP` or `:POWer:LOW` command

**Parameters:** `value` or `?`

**Parameter Interpretation:** Power value or get currently set power

**Command Interpretation:** Set or get upper power limit and get lower limit. When setting values outside of device limits, limit is supposed to be set to the highest actual possible value, which does not seem to work, see above description for details. Limits are only enforced in direct modes.

**Setup:** `:POW:UPP 100W`

**Query:** `:POW:UPP?`

**Return:** `100.00W`

___

## `:FUNC` or `:FUNCtion` command

**Parameters:** `CV` or `CC` or `CR` or `CW` or `SHORt`

**Parameter Interpretation:** For setting constant voltage/current/resistance/power or short mode

**Command Interpretation:** Get current mode in use or set certain modes(setting only works with CV,CC,CR,CW,short)

**Setup:** `:FUNC SHOR`

**Query:** `FUNC?`

**Return:** `CV` or `CC` or `CR` or `CW` or `SHORt` or `BATTERY` or `OCP` or `LIST` or `OPP` or `TOGGLE`(dynamic mode 6) or `PULSE`(dynamic mode 5) or `CONTINUOUS CW`(dynamic mode 4) or `CONTINUOUS CR`(dynamic mode 3) or `CONTINUOUS CC`(dynamic mode 2) or `CONTINUOUS CV`(dynamic mode 1)

___

## `:MEAS` or `:MEASure` command

**Parameters:** `CURR`/`CURRent` or `VOLT`/`VOLTage` or `POW`/`POWer`

**Parameter Interpretation:** what to measure - current,voltage or power

**Command Interpretation:** Get currently measured value for chosen parameter

**Setup:** none

**Query:** `:MEAS:VOLT?` or `:MEAS:CURR?` or `:MEAS:POW?`

**Return:** `7.4486V` or `3.2415A` or `24.145W`

___

## `:LIST` command

**Parameters:** `list-number,current-range,number of steps,` and steps[`current,current-slope,duration,`] and `number of loops`

**Parameter Interpretation:** the number of save-slot the list is saved to and the range of current used and the number of steps the list includes(up to a maximum of 84(unconfirmed) steps). The next values are the steps in the format of: current, slope(change rate) and duration. Those values repeat for the amount of steps previously defined. After the steps the last number is the number of loops the group will run for

**Command Interpretation:** This function will run several loops of a group of defined steps of constant current settings

**Setup:** `:LIST 5,20A,3,3A,0.01A/uS,5S,7A,0.02A/uS,9S,9A,0.05A/uS,6S,4`

**Query:** none

___

## `:OCP` command

**Parameters:** `save-slot,Von,Von delay,current range,initial current,current step,step delay,cutoff current,OCP voltage,max overcurrent,min overcurrent`

**Parameter Interpretation:** the number of the save slot,Voltage that has to be reached for test to start,delay after voltage has been reached before test starts,current range the test will operate in, initial current that will be drawn at start of test(has to be higher than cutoff current/max overcurrent/min overcurrent), by how much the current will be decreased with each step(has to be lower or same than initial current), how long between steps, at which current the test will stop(has to be lower than the other currents), under which value the voltage has to drop to be considered an OCP kicking in, top end of range for pass(has to be larger than min overcurrent and cutoff current but below initial current), bottom end of range for pass(has to be below initial current and max overcurrent but higher than cutoff current)

**Command Interpretation:** This mode will test an overcurrent protection of a device. It functions by starting in an overload condition after a defined voltage has been reached at which point it expects the voltage to drop below the defined value. The load will then gradually decrease the current draw until it reaches the point the overcurrent protection of the device under test drops out and the voltage will return to normal. If the point where the voltage returns to normal(OCP drops out) is within the range defined the unit will display "pass" otherwise "fail"

**Setup:** `:OCP 2,15V,5S,3A,2A,0.1A,1S,1A,10V,1.5A,1.06A`

**Query:** none

___

## `:OPP` command

**Parameters:** `save-slot,Von,Von delay,current range,initial power,power step,step delay,cutoff power,OPP voltage,max overpower,min overpower`

**Parameter Interpretation:** same as OCP mode but with controlling/testing power instead of current

**Command Interpretation:** same as OCP mode but with controlling/testing power instead of current, current-range value seems to be doing nothing here

**Setup:** `:OPP 7,12V,5S,3A,50W,1W,1S,10W,20V,30W,10.024W`

**Query:** none

___

## `:BATT` or `:BATTery` command

**Parameters:** `save slot,current-range,discharge current,cutoff voltage,cutoff capacity,cutoff time`

**Parameter Interpretation:** save slot settings are saved to, current-range of test, constant current battery is discharged at, voltage at which point test will stop, capacity at which point test will stop, passed time at which test is stopped

**Command Interpretation:** This mode will basically perform a capacity check on a battery which can be cut off by either reaching an end voltage, a specified capacity or time. Will display capacity at end of test on device.

**Setup:** `:BATT 1,30A,7A,35V,11AH,30M`

**Query:** none

___

### `:BATT:TIM` or `:BATTery:TIM` command

**Parameters:** `?`

**Command Interpretation:** Gets current running time of battery test mode

**Setup:** none

**Query:** `:BATT:TIM?`

**Return:** `0.9547M`

### `:BATT:CAP` or `:BATTery:CAP` command

**Parameters:** `?`

**Command Interpretation:** Gets current capacity of battery test mode

**Setup:** none

**Query:** `:BATT:CAP?`

**Return:** `0.1093AH`

___

## `:RCL` commands

### `LIST` command

**Parameters:** `1`-`7` or `?`

**Parameter Interpretation:** recall saved list 1-7 or recall values saved in that list

**Command Interpretation:** First recall list with value which should be an existing store, then recall values saved in list. When values are recalled from non-existing list there is no return and recalling empty list will get error on device potentially causing issues with serial connection. Same thing seems to happen on list with loop value set to less than 3.

**Setup:** `:RCL:LIST 5`

**Query:** `:RCL:LIST?`

**Return:** `20.000A,03, 3.000A, 0.010A/uS, 5.000S, 7.000A, 0.020A/uS, 9.000S, 9.000A, 0.050A/uS, 6.000S,4`

### `OCP` command

**Parameters:** `1`-`10` or `?`

**Parameter Interpretation:** recall saved OCP profiles 1-10 or recall values saved in that OCP profile

**Command Interpretation:** First recall OCP profile with value which should be an existing store, then recall values saved in profile. When values are recalled from non-existing profile there is no return and recalling empty list will get error on device.

**Setup:** `:RCL:OCP 5`

**Query:** `:RCL:OCP?`

**Return:** `15.000V, 5.000S, 3.000A, 2.000A, 0.100A, 5.000S, 0.200A,10.000V, 1.500A, 1.100A`

### `OPP` command

**Parameters:** `1`-`10` or `?`

**Parameter Interpretation:** recall saved OPP profiles 1-10 or recall values saved in that OPP profile

**Command Interpretation:** First recall OPP profile with value which should be an existing store, then recall values saved in profile. When values are recalled from non-existing profile there is no return and recalling empty list will get error on device.

**Setup:** `:RCL:OPP 5`

**Query:** `:RCL:OPP?`

**Return:** `12.000V, 5.000S, 3.000A,50.000W, 1.000W, 1.000S,10.000W,20.000V,30.000W,10.024W`

### `BATT` command

**Parameters:** `1`-`10` or `?`

**Parameter Interpretation:** recall saved battery profiles 1-10 or recall values saved in that profile

**Command Interpretation:** First recall OPP profile with value which should be an existing store, then recall values saved in profile. When values are recalled from non-existing profile there is no return and recalling empty list will get error on device.

**Setup:** `:RCL:BATT 1`

**Query:** `RCL:BATT?`

**Return:** `30.000A, 7.000A,35.000V,11.000AH,30.000M`

___

## `:DYN` commands

Dynamic modes need to be recalled by `:DYN?` before using

### Dynamic mode 1 - dynamic CV

**Parameters:** `1,Voltage1,Voltage2,Switching-Frequency,duration-percentage` or `?`

**Parameter Interpretation:** Chooses mode 1 which is dynamic constant voltage, voltage #1, voltage #2, basically how long a full cycle will take in Hz, how much of the cycle voltage #2 will be on

**Command Interpretation:** This will use dynamic mode 1: dynamic constant voltage, which will switch between two CV settings at defined interval and duration. Switching frequency will choose at which frequency a full cycle is run(i.e. 1Hz means full cycle will last 1 second) of which voltage #1 will be run for defined percentage of time(i.e. 70% will run voltage #2 for 0.7 seconds and voltage #1 for 0.3 seconds). Frequency seems to be able to be set between 0.001Hz and 15000Hz.(Untested if or how it actually works at high frequencies)

**Setup:** `:DYN 1,5V,5.5V,0.2HZ,70%`

**Query:** `:DYN?`

**Return:** `1, 5.000V, 5.500V, 0.200HZ,70.000%`

### Dynamic mode 2 - dynamic CC

**Parameters:** `2,slope1,slope2,current1,current2,switching-frequency,duration-percentage` or `?`

**Parameter Interpretation:** Chooses mode 2 which is dynamic constant current, current change slope for current #1, current change slope for current #2, current #1, current #2, basically how long a full cycle will take in Hz, how much of the cycle current #2 will be on

**Command Interpretation:** This will use dynamic mode 2: dynamic constant current, which will switch between two CC settings at defined interval and duration. Switching frequency will choose at which frequency a full cycle is run(i.e. 1Hz means full cycle will last 1 second) of which current #1 will be run for defined percentage of time(i.e. 70% will run current #2 for 0.7 seconds and current #1 for 0.3 seconds). Frequency seems to be able to be set between 0.001Hz and 15000Hz.(Untested if or how it actually works at high frequencies). The slopes define how fast the current will change to the next current value. Slope #1 should be the value for change to current #1 according to documentation but untested.

**Setup:** `:DYN 2,0.001A/uS,0.1A/uS,1A,2A,0.1HZ,70%`

**Query:** `:DYN?`

**Return:** `2, 0.001A/uS, 0.100A/uS, 1.000A, 2.000A, 0.100HZ,70.000%`

### Dynamic mode 3 - dynamic CR

**Parameters:** `3,resistance1,resistance2,switching-frequency,duration-percentage` or `?`

**Parameter Interpretation:** Chooses mode 3 which is dynamic constant resistant, resistance #1, resistance #2, basically how long a full cycle will take in Hz, how much of the cycle resistance #2 will be on

**Command Interpretation:** This will use dynamic mode 3: dynamic constant resistance, which will switch between two CR settings at defined interval and duration. Switching frequency will choose at which frequency a full cycle is run(i.e. 1Hz means full cycle will last 1 second) of which resistance #1 will be run for defined percentage of time(i.e. 70% will run resistance #2 for 0.7 seconds and resistance #1 for 0.3 seconds). Frequency seems to be able to be set between 0.001Hz and 15000Hz.(Untested if or how it actually works at high frequencies).

**Setup:** `:DYN 3,10OHM,20OHM,0.1HZ,70%`

**Query:** `:DYN?`

**Return:** `3,10.000OHM,20.000OHM, 0.100HZ,70.000%`

### Dynamic mode 4 - dynamic CW

**Parameters:** `4,power1,power2,switching-frequency,duration-percentage` or `?`

**Parameter Interpretation:** Chooses mode 4 which is dynamic constant power, power #1, power #2, basically how long a full cycle will take in Hz, how much of the cycle power #2 will be on

**Command Interpretation:** This will use dynamic mode 4: dynamic constant power, which will switch between two CW settings at defined interval and duration. Switching frequency will choose at which frequency a full cycle is run(i.e. 1Hz means full cycle will last 1 second) of which power #1 will be run for defined percentage of time(i.e. 70% will run power #2 for 0.7 seconds and power #1 for 0.3 seconds). Frequency seems to be able to be set between 0.001Hz and 15000Hz.(Untested if or how it actually works at high frequencies).

**Setup:** `:DYN 4,10W,20W,0.1HZ,70%`

**Query:** `:DYN?`

**Return:** `4,10.000W,20.000W, 0.100HZ,70.000%`

### Dynamic mode 5 - dynamic current pulse

**Parameters:** `5,slope1,slope2,current1,current2,duty-time` or `?`

**Parameter Interpretation:** Chooses mode 5 which is dynamic current pulse, slope #1, slope #2, current #1, current #2, time in seconds pulse will last

**Command Interpretation:** This will use dynamic mode 5: dynamic current pulse, which will apply a constant current and upon receiving a trigger signal(at the unit or over remote) a current pulse will be applied for as long as defined. Sending additional triggers while a pulse is active will reset timer of pulse.

**Setup:** `:DYN 5,0.1A/uS,0.001A/uS,1A,3A,10S`

**Query:** `:DYN?`

**Return:** `5, 0.100A/uS, 0.001A/uS, 1.000A, 3.000A,10.000S`

### Dynamic mode 6 - dynamic current toggle

**Parameters:** `6,slope1,slope2,current1,current2` or `?`

**Parameter Interpretation:** Chooses mode 6 which is dynamic current trigger, slope #1, slope #2, current #1, current #2

**Command Interpretation:** This will use dynamic mode 6: dynamic current trigger, which will apply a constant current and upon receiving a trigger signal(at the unit or over remote) the other set current will be applied.

**Setup:** `:DYN 6,0.1A/uS,0.001A/uS,3A,1A`

**Query:** `:DYN?`

**Return:** `6, 0.100A/uS, 0.001A/uS, 3.000A, 1.000A`


**NOTE**: setting values always require the symbol after the value: `A` for current, `V` for voltage, `W` for power, `OHM` for resistance, `A/uS` for current slope, `S` for time in seconds, `M` for time in minutes(only used for battery mode), `%` for percentages, `HZ` for frequencies