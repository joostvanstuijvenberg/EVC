from EVCInterface import EVCInterface

NODE_ID_PRE = 0x30

if __name__ == '__main__':
    evc = EVCInterface(NODE_ID_PRE)
    # evc.enable_module(True)
    print(f'Module enabled . . . . . . . : ', evc.is_module_enabled())
    print(f'Ambient temperature. . . . . : ', evc.get_ambient_temperature())
    print(f'Input L1 AC voltage. . . . . : ', evc.get_ac_input_l1_voltage())
    # print(f'Input L2 AC voltage. . . . . : ', evc.get_ac_input_l2_voltage())
    # print(f'Input L3 AC voltage. . . . . : ', evc.get_ac_input_l3_voltage())
    # evc.enable_module(False)
