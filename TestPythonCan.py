import can


def read(request: can.Message) -> can.Message:
    response = None
    try:
        print(request)
        bus.send(request, timeout=0.5)
        response = bus.recv(timeout=1.0)
        print(response)
    except can.CanError as e:
        print(f'CANbus communication failure', e)
    return response


if __name__ == '__main__':
    bus = can.interface.Bus(channel=0, bustype='vector', interface='vector', bitrate=500000)

    read_keep_alive = can.Message(
        arbitration_id=0x0630,
        dlc=0x08,
        data=[0x40, 0x00, 0x21, 0x00, 0x00, 0x00, 0x00, 0x00],
        is_extended_id=False
    )
    # bus.send_periodic(read_keep_alive, 0.5, None, True)

    read_temp_ac_heatsink = can.Message(
        arbitration_id=0x0630,
        dlc=0x08,
        data=[0x40, 0x40, 0x21, 0x00, 0x00, 0x00, 0x00, 0x00],
        is_extended_id=False
    )

    read_temp_ambient = can.Message(
        arbitration_id=0x0630,
        dlc=0x08,
        data=[0x40, 0x36, 0x21, 0x00, 0x00, 0x00, 0x00, 0x00],
        is_extended_id=False
    )

    read_ac_input_voltage_L1 = can.Message(
        arbitration_id=0x0630,
        dlc=0x08,
        data=[0x40, 0x21, 0x21, 0x00, 0x00, 0x00, 0x00, 0x00],
        is_extended_id=False
    )

    # print("Vector bus status: ", bus.state)
    data = read(read_temp_ac_heatsink)
    temp_ac_heatsink = int.from_bytes(data.data[4:6], byteorder='little', signed=True)
    print(f'AC heat sink temperature:', temp_ac_heatsink / 10)

    data = read(read_temp_ambient)
    temp_ambient = int.from_bytes(data.data[4:6], byteorder='little', signed=True)
    print(f'Ambient temperature:', temp_ambient / 10)

    data = read(read_ac_input_voltage_L1)
    ac_input_voltage_L1 = int.from_bytes(data.data[4:6], byteorder='little', signed=True)
    print(f'AC input voltage:', ac_input_voltage_L1 / 10)

    # bus.stop_all_periodic_tasks()
