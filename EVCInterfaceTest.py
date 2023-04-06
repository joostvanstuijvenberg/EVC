from EVCInterface import EVCInterface

NODE_ID_PRE = 0x30

if __name__ == '__main__':
    evc = EVCInterface(NODE_ID_PRE)
    evc.set_verbose(False)

    # 0x2100 Module enable
    evc.enable_module(True)
    # print(f'Module enabled. . . . . . . . . . : ', evc.is_module_enabled())  # 2100 IS WRITE-ONLY OBJECT??

    # 0x2101 Module status
    status = evc.get_module_status()
    print(f'Module status . . . . . . . . . . : ', status)
    print(f'Module status CHARGER ON . .  . . : ', status & evc.MODULE_STATUS_CHARGER_ON is True)
    print(f'Module status POWER ERROR . . . . : ', status & evc.MODULE_STATUS_POWER_ERROR is True)
    print(f'Module status INPUT OVERVOLTAGE . : ', status & evc.MODULE_STATUS_INPUT_OVERVOLTAGE is True)
    print(f'Module status INPUT UNDERVOLTAGE. : ', status & evc.MODULE_STATUS_INPUT_UNDERVOLTAGE is True)
    print(f'Module status OUTPUT OVERVOLTAGE. : ', status & evc.MODULE_STATUS_OUTPUT_OVERVOLTAGE is True)
    print(f'Module status OUTPUT UNDERVOLTAGE : ', status & evc.MODULE_STATUS_OUTPUT_UNDERVOLTAGE is True)
    print(f'Module status OVERTEMPERATURE . . : ', status & evc.MODULE_STATUS_OVERTEMPERATURE is True)
    print(f'Module status UAX ERROR . . . . . : ', status & evc.MODULE_STATUS_UAUX_ERROR is True)
    print(f'Module status Charging / V2G. . . : ', 'Charging' if status & evc.MODULE_STATUS_CHARGE_OR_V2G else 'V2G')
    print(f'Module status GRID ERROR. . . . . : ', status & evc.MODULE_STATUS_GRID_ERROR is True)
    print(f'Module status HW INTERLOCK ERROR. : ', status & evc.MODULE_STATUS_HW_INTERLOCK_ERROR is True)
    print(f'Module status SERVICE MODE. . . . : ', status & evc.MODULE_STATUS_SERVICE_MODE is True)

    # 0x2109 UDC output setpoint
    evc.set_dc_output_voltage_setpoint(24.5)
    print(f'DC output voltage setpoint. . . . . : ', evc.get_dc_output_voltage_setpoint())

    # 0x210A IDC output setpoint
    # evc.set_dc_output_current_setpoint(4.5)
    # print(f'DC output current setpoint. . . . . : ', evc.get_dc_output_current_setpoint())

    # 0x210F UDC undervoltage setpoint- <--
    # evc.set_output_undervoltage_setpoint(44.5)
    # print(f'DC output undervoltage setpoint . . . : ', evc.get_udc_output_setpoint())

    # 0x2121 - 0x2123 UAC input L1/L2/L3
    print(f'Input L1 AC voltage . . . . . . . : ', evc.get_ac_input_l1_voltage())
    print(f'Input L2 AC voltage . . . . . . . : ', evc.get_ac_input_l2_voltage())
    print(f'Input L3 AC voltage. . .. . . . . : ', evc.get_ac_input_l3_voltage())

    # 0x2136 Temperature ambient
    print(f'Ambient temperature . . . . . . . : ', evc.get_ambient_temperature())

    # - enable
    # - max en min spanning (setpoints)
    # - v2g of g2v
    # - laadstroom of ontlaadstroom kunnen instellen

    evc.enable_module(False)
