"""
This file is intended to give an example on how to use most of the functions provided by the library
"""

import time

from src.kelctl import *

with KELSerial('/dev/ttyACM0', 115200, True) as load:
    print("Model: ", load.model)
    m1 = load.memories[0]
    m1.recall()
    m2 = load.memories[99]
    m2.save()

    load.settings.beep.off()
    load.settings.lock.off()
    load.settings.dhcp.off()
    load.settings.trigger.off()
    load.settings.compensation.off()
    print("SYST beep: ", load.settings.beep.get())
    print("SYST lock: ", load.settings.lock.get())
    print("SYST dhcp: ", load.settings.dhcp.get())
    print("SYST trigger: ", load.settings.trigger.get())
    print("SYST comp: ", load.settings.compensation.get())
    load.settings.beep.on()
    load.settings.lock.on()
    load.settings.dhcp.on()
    load.settings.trigger.on()
    load.settings.compensation.on()
    print("SYST beep: ", load.settings.beep.get())
    print("SYST lock: ", load.settings.lock.get())
    print("SYST dhcp: ", load.settings.dhcp.get())
    print("SYST trigger: ", load.settings.trigger.get())
    print("SYST comp: ", load.settings.compensation.get())

    load.settings.ipaddress = "10.0.0.123"
    print("SYST IPAD: ", load.settings.ipaddress)
    load.settings.ipaddress = "10.0.0.234"
    print("SYST IPAD: ", load.settings.ipaddress)

    load.settings.subnetmask = "255.255.255.0"
    print("SYST SMASK", load.settings.subnetmask)
    load.settings.subnetmask = "255.255.0.0"
    print("SYST SMASK", load.settings.subnetmask)

    load.settings.gateway = "10.0.0.1"
    print("SYST GATE: ", load.settings.gateway)
    load.settings.gateway = "10.0.0.2"
    print("SYST GATE: ", load.settings.gateway)

    load.settings.baudrate = BaudRate(3)
    print("SYST Baud: ", load.settings.baudrate)
    load.settings.baudrate = BaudRate(4)
    print("SYST Baud: ", load.settings.baudrate)

    load.settings.macaddress = "00-80-41-ae-fd-7e"
    print("SYST Mac: ", load.settings.macaddress)
    load.settings.macaddress = "01:80:41:ae:fd:7e"
    print("SYST Mac: ", load.settings.macaddress)

    load.settings.port = 12345
    print("SYST Port: ", load.settings.port)
    load.settings.port = 23456
    print("SYST Port: ", load.settings.port)

    load.settings.voltage_limit = 100
    print("Volt Limit: ", load.settings.voltage_limit)
    load.settings.voltage_limit = 80
    print("Volt Limit: ", load.settings.voltage_limit)

    load.settings.current_limit = 20
    print("Curr Limit: ", load.settings.current_limit)
    load.settings.current_limit = 15
    print("Curr Limit: ", load.settings.current_limit)

    load.settings.power_limit = 200
    print("Pow Limit: ", load.settings.power_limit)
    load.settings.power_limit = 100
    print("Pow Limit: ", load.settings.power_limit)

    load.settings.resistance_limit = 200
    print("Res Limit: ", load.settings.resistance_limit)
    load.settings.resistance_limit = 300
    print("Res Limit: ", load.settings.resistance_limit)

    print("DevInfo: ", load.device_info)

    print("Status: ", load.status)

    load.voltage = 20
    print("Voltage: ", load.voltage)
    load.voltage = 30
    print("Voltage: ", load.voltage)

    load.current = 10
    print("Current: ", load.current)
    load.current = 15
    print("Current: ", load.current)

    load.power = 30
    print("Power: ", load.power)
    load.power = 35
    print("Power: ", load.power)

    load.resistance = 40
    print("Resistance: ", load.resistance)
    load.resistance = 50
    print("Resistance: ", load.resistance)

    load.input.on()
    print("Input: ", load.input.get())
    load.input.off()
    print("Input: ", load.input.get())

    print("Out-Volt:", load.measured_voltage)
    print("Out-Power:", load.measured_power)
    print("Out-Current:", load.measured_current)

    print("Set-Function:", load.function)
    load.function = Mode.constant_voltage
    print("Set-Function:", load.function)
    load.function = Mode.short
    print("Set-Function:", load.function)

    steps = [ListStep(3, 0.002, 5), ListStep(2, 0.003, 3), ListStep(2, 0.005, 2)]
    testlist = LoadList(3, 10, steps, 6)
    print("TestList:", testlist.__str__())
    load.set_list(testlist)
    print("GetList:", load.get_list(3))

    ocpList = OCPList(1, 10, 4, 20, 15, 1, 1, 5, 30, 10.52, 8.34)
    print("OCPLIST:", ocpList.__str__())
    load.set_ocp(ocpList)
    print("OCPList-get:", load.get_ocp(1))

    oppList = OPPList(1, 11, 4, 20, 15, 1, 1, 5, 30, 10.52, 8.34)
    print("OPPList:", oppList.__str__())
    load.set_opp(oppList)
    print("OPPList-get:", load.get_opp(1))

    battList = BattList(1, 20.23, 10, 10, 30, 5)
    print("BattList:", battList.__str__())
    load.set_batt(battList)
    print("BattList-get:", load.get_batt(1))
    print("BattCap:", load.get_batt_cap())
    print("BattTime:", load.get_batt_time())

    dyn1List = CVList(30.02, 20.05, 1.5, 30)
    print("Dyn1List: ", dyn1List.__str__())
    load.set_dynamic_mode(dyn1List)
    print("Dyn1List-get: ", load.get_dynamic_mode())

    dyn2List = CCList(0.4, 0.5, 5, 6, 3, 40)
    print("Dyn2List: ", dyn2List.__str__())
    load.set_dynamic_mode(dyn2List)
    print("Dyn2List-get: ", load.get_dynamic_mode())

    dyn3List = CRList(5, 10, 3, 40)
    print("Dyn3List: ", dyn3List.__str__())
    load.set_dynamic_mode(dyn3List)
    print("Dyn3List-get: ", load.get_dynamic_mode())

    dyn4List = CWList(6, 9, 3, 40)
    print("Dyn4List: ", dyn4List.__str__())
    load.set_dynamic_mode(dyn4List)
    print("Dyn4List-get: ", load.get_dynamic_mode())

    dyn5List = PulseList(0.3, 0.2, 4, 6, 5)
    print("Dyn5List: ", dyn5List.__str__())
    load.set_dynamic_mode(dyn5List)
    print("Dyn5List-get: ", load.get_dynamic_mode())

    dyn6List = ToggleList(0.2, 0.3, 5, 7)
    print("Dyn6List: ", dyn6List.__str__())
    load.set_dynamic_mode(dyn6List)
    print("Dyn6List.get: ", load.get_dynamic_mode())

    load.input.on()
    time.sleep(4)
    print("curr-trig: ", load.measured_current)
    load.trigger()
    print("curr-trig: ", load.measured_current)
    time.sleep(4)
    load.trigger()
    print("curr-trig2: ", load.measured_current)
    load.input.off()

    exList = OPPList(2, 10, 5, 10, 6, 3, 3, 7, 20, 5, 3)
    try:
        load.set_opp(exList)
    except ValueError as e:
        print(e)

    try:
        load.current = 25
    except ValueOutOfLimitError as e:
        print(e)
