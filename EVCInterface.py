import can


class EVCInterface:
    """
    Wrapper class for the PRE Electrical Vehicle Charger
    ----------------------------------------------------
    J. van Stuijvenberg
    Centre of Expertise - Biobased Economy
    Avans Hogeschool Breda

    Note that the requirement for CANbus messages on a regular basis (at least one every 1000ms), as
    documented under 3.3 (page 10), seems to be addressed by the Vector VN1610 interface.

    CC BY-SA 4.0
    """
    # Global parameters
    EVC_INTERFACE_VERBOSE_OUTPUT = False

    # CAN-bus (default) parameters
    EVC_DEFAULT_CHANNEL = 0
    EVC_DEFAULT_NODE_ID = 0x30
    EVC_DEFAULT_BITRATE = 500000
    EVC_VECTOR_BUS_TYPE = 'vector'
    EVC_VECTOR_INTERFACE = 'vector'

    # CAN-bus data frame parameters for PRE EVC in SEnDlab configuration
    DATA_FRAME_DLC = 0x08
    DATA_FRAME_NO_SUB_INDEX = 0x00

    # Command byte (CD) values for specific read and write value sizes
    MASTER_READS_FROM_SLAVE = 0x40
    MASTER_WRITES_TO_SLAVE_4_BYTES = 0x23
    MASTER_WRITES_TO_SLAVE_3_BYTES = 0x27
    MASTER_WRITES_TO_SLAVE_2_BYTES = 0x2B
    MASTER_WRITES_TO_SLAVE_1_BYTES = 0x2F

    # Command byte (CD) values for specific response value sizes
    SUCCESSFUL_READ_RESPONSE_4_BYTES = 0x43
    SUCCESSFUL_READ_RESPONSE_3_BYTES = 0x47
    SUCCESSFUL_READ_RESPONSE_2_BYTES = 0x4B
    SUCCESSFUL_READ_RESPONSE_1_BYTES = 0x4F
    SUCCESSFUL_WRITE_RESPONSE = 0x60

    # CANopen objects for PRE EVC (little endian)
    MODULE_ENABLE = [0x00, 0x21]
    VOLTAGE_DC_OUTPUT_SETPOINT = [0x09, 0x21]
    CURRENT_DC_OUTPUT_SETPOINT = [0x0A, 0x21]
    VOLTAGE_DC_UNDERVOLTAGE_SETPOINT = [0x0F, 0x21]
    VOLTAGE_AC_INPUT_L1 = [0x21, 0x21]
    TEMPERATURE_AMBIENT = [0x36, 0x21]

    def __init__(self, node_id=EVC_DEFAULT_NODE_ID, channel=EVC_DEFAULT_CHANNEL, bitrate=EVC_DEFAULT_BITRATE):
        """
        node_id : int
            1-byte CANbus node id, default 0x30 for PRE EVC
        channel : int | str
            CANbus channel, default 0 for SEnDlab configuration
        bitrate : int
            CANbus data transfer rate, default 500000 for PRE EVC
        """
        self._node_id = node_id
        self._bus = can.interface.Bus(
            channel=channel,
            bustype=self.EVC_VECTOR_BUS_TYPE,
            interface=self.EVC_VECTOR_INTERFACE,
            bitrate=bitrate
        )

    def _arbitration_id(self):
        """
        Adds this EVC's node id to the base 0x0600 to get a full CANID.
        :return: full CANbus node id, default 0x0630
        """
        return 0x0600 + self._node_id

    def _canopen_message(self, data):
        return can.Message(
            arbitration_id=self._arbitration_id(),
            dlc=self.DATA_FRAME_DLC,
            data=data,
            is_extended_id=False
        )

    def _query(self, request: can.Message, verbose: bool = False) -> can.Message | None:
        """
        Attempts a synchronous read and write cycle to the EVC.
        :param request: CANopen message to be sent to the EVC
        :param verbose: dump the written and received messages to the console
        :return: CANopen response read from the EVC
        """
        try:
            self._bus.send(request, timeout=0.5)
            if self.EVC_INTERFACE_VERBOSE_OUTPUT or verbose:
                print(request)
            response = self._bus.recv(timeout=1.0)
            if self.EVC_INTERFACE_VERBOSE_OUTPUT or verbose:
                print(response)
            return response
        except can.CanError as e:
            print(f'CANbus communication failure', e)
        return None

    # ----------------------------------------------------------------------------------------------------
    # 2100 MODULE ENABLE (R/W)
    # ----------------------------------------------------------------------------------------------------
    def is_module_enabled(self) -> bool:
        """
        See if the power module is enabled.
        :return: power module enabled status
        """
        read_module_enabled = self._canopen_message(
            data=[self.MASTER_READS_FROM_SLAVE] + self.MODULE_ENABLE +
                 [self.DATA_FRAME_NO_SUB_INDEX, 0x00, 0x00, 0x00, 0x00]
        )
        # DIT FORMAT GAAN AANHOUDEN
        return int.from_bytes(self._query(read_module_enabled).data[4:6], byteorder='little', signed=True) > 0

    def enable_module(self, enabled=True) -> bool:
        """
        Enable or disable the power module.
        :param enabled: requested enabled/disabled status
        :return: result (see: is_module_enabled())
        """
        write_module_enabled = can.Message(
            arbitration_id=self._arbitration_id(),
            dlc=self.DATA_FRAME_DLC,
            data=[self.MASTER_READS_FROM_SLAVE] + self.MODULE_ENABLE +
                 [self.DATA_FRAME_NO_SUB_INDEX, 0xF0, 0x00, 0x00, 0x00],
            is_extended_id=False
        )
        return int.from_bytes(self._query(write_module_enabled).data[4:6], byteorder='little', signed=True) > 0

    # ----------------------------------------------------------------------------------------------------
    # 2121 VOLTAGE AC INPUT L1 (R)
    # ----------------------------------------------------------------------------------------------------
    def get_ac_input_l1_voltage(self) -> float:
        """
        Returns the measured L1 AC input voltage (line-neutral).
        :return: L1 AC input voltage
        """
        read_ac_input_l1_voltage = can.Message(
            arbitration_id=self._arbitration_id(),
            dlc=self.DATA_FRAME_DLC,
            data=[self.MASTER_READS_FROM_SLAVE] + self.VOLTAGE_AC_INPUT_L1 +
                 [self.DATA_FRAME_NO_SUB_INDEX, 0x00, 0x00, 0x00, 0x00],
            is_extended_id=False
        )
        return int.from_bytes(self._query(read_ac_input_l1_voltage).data[4:6], byteorder='little', signed=True) / 10

    # ----------------------------------------------------------------------------------------------------
    # 2136 TEMPERATURE_AMBIENT (R)
    # ----------------------------------------------------------------------------------------------------
    def get_ambient_temperature(self) -> float:
        """
        Returns the ‘ambient’ temperature, where the sensor is fitted on the PCB (not near local
        heat sources). Measured in steps of 0.1 °C
        :return: ambient temperature
        """
        read_ambient_temperature = can.Message(
            arbitration_id=self._arbitration_id(),
            dlc=self.DATA_FRAME_DLC,
            data=[self.MASTER_READS_FROM_SLAVE] + self.TEMPERATURE_AMBIENT +
                 [self.DATA_FRAME_NO_SUB_INDEX, 0x00, 0x00, 0x00, 0x00],
            is_extended_id=False
        )
        return int.from_bytes(self._query(read_ambient_temperature).data[4:6], byteorder='little', signed=True) / 10
