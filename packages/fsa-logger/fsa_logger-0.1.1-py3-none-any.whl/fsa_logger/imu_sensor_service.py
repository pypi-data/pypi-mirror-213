from __future__ import annotations
import errno
import json
import logging
import os
import time
from datetime import datetime

from ble_driver import BLEDevice, GenericBLEService, DeviceScanRecord
from ble_driver import BlatannBLEService, EzSerialBLEService

from fsa_logger.config.config import AppConfig
from fsa_logger.sensor_api import ControlPointApi, SensorSampleRate, SensorScale, SensorAxis, SensorPresetConfig, \
    SERVICE_UUID, SENSOR_STREAMING_CHARACTERISTIC_UUID, CONTROL_POINT_CHARACTERISTIC_UUID, IMU_SENSOR_NAME, \
    ACC_DATA_LENGTH, MAX_PACKET_NUMBER

config = AppConfig()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ImuDataPacket:
    raw: [] = None
    acc: [] = None
    acc_x: [] = None
    acc_y: [] = None
    acc_xy: [] = None
    acc_z: [] = None
    absolute_time: [] = None
    num_samples: int = 0
    duration: float = 0
    rx_timestamp: datetime = None
    packet_num: int = 0
    delta_t: float = 0

    def __init__(self):
        self.raw = []
        self.acc = []
        self.acc_x = []
        self.acc_y = []
        self.acc_xy = []
        self.acc_z = []
        self.absolute_time = []

    @staticmethod
    def parse_packet(data: list, scale: SensorScale, sample_rate: SensorSampleRate, axis: SensorAxis,
                     unpack=False) -> ImuDataPacket:
        """
        Decode received packet into IMU data
        :param data: data_array
        :param conf: sensor configuration
        :param unpack: whether to unpack acc values in to axis
        :return:
        """

        # Verify length:
        expected_len = ACC_DATA_LENGTH + 2
        if len(data) != expected_len:
            logger.warning(
                f'Error decoding packet: actual length ({len(data)}) differs from expected length ({expected_len}) ==> return None')
            return None

        freq = sample_rate.get_frequency()

        # axis = get_sensor_config_axis_names(conf)

        scale_factor = scale.get_scale_factor()

        axis_names = axis.get_axis_names()
        num_axis = len(axis_names)
        imu_packet = ImuDataPacket()
        imu_packet.rx_timestamp = datetime.utcnow()
        imu_packet.num_samples = int(ACC_DATA_LENGTH / 2 / num_axis)
        imu_packet.delta_t = 1 / freq
        imu_packet.duration = imu_packet.num_samples * imu_packet.delta_t

        # decode num_packet
        imu_packet.packet_num = ImuDataPacket.__get_unsigned_short(data[ACC_DATA_LENGTH:])

        # parse acc_data
        for i in range(0, ACC_DATA_LENGTH, 2):
            if config.save_raw_acc:
                imu_packet.raw.append(ImuDataPacket.__get_unsigned_short(data[i:]))
            imu_packet.acc.append(ImuDataPacket.__get_signed_short(data[i:]) * scale_factor)

        # samples absolute_time
        imu_packet.absolute_time = [i * imu_packet.delta_t for i in range(imu_packet.num_samples)]

        if unpack:
            acc_i = iter(imu_packet.acc)
            axis_names = axis.get_axis_names()
            if num_axis == 3:
                for (acc_x, acc_y, acc_z) in zip(acc_i, acc_i, acc_i):
                    imu_packet.acc_x.append(acc_x)
                    imu_packet.acc_y.append(acc_y)
                    imu_packet.acc_z.append(acc_z)

            elif num_axis == 2:
                for (acc_y, acc_z) in zip(acc_i, acc_i):
                    imu_packet.acc_y.append(acc_y)
                    imu_packet.acc_z.append(acc_z)
            else:
                if 'X' in axis_names:
                    imu_packet.acc_x = imu_packet.acc[:]
                if 'Y' in axis_names:
                    imu_packet.acc_y = imu_packet.acc[:]
                if 'Z' in axis_names:
                    imu_packet.acc_z = imu_packet.acc[:]

        return imu_packet

    @staticmethod
    def __get_signed_short(data):
        return int.from_bytes([data[0], data[1]], byteorder='little', signed=True)
        # return int.from_bytes([data[0], data[1]], byteorder='big', signed=True)

    @staticmethod
    def __get_unsigned_short(data):
        return int.from_bytes([data[0], data[1]], byteorder='little', signed=False)


class ImuSensorDevice(BLEDevice):
    __capture_enabled = False
    __ext_callback = False
    __next_packet_number = -1
    __next_packet_absolute_time = 0

    _alias: str = ''
    _config: SensorPresetConfig = SensorPresetConfig.YZ_3_2_KHZ
    _sample_rate: SensorSampleRate = SensorSampleRate.SAMPLE_RATE_6400HZ_HF
    _axis: SensorAxis = SensorAxis.AXIS_ONLY_YZ
    _scale: SensorScale = SensorScale.SCALE_16G
    _location: str = 'Unknown'

    _verbose: bool = False

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, value):
        self._verbose = value

    @property
    def label(self):
        return f'{self.address} - {self.alias}'

    @property
    def alias(self):
        return self._alias

    @alias.setter
    def alias(self, value):
        self._alias = value

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value
        if self._config != SensorPresetConfig.CUSTOM:
            self._axis, self._sample_rate, self_scale = self._config.get_sensor_configs()

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def sample_rate(self):
        return self._sample_rate

    @sample_rate.setter
    def sample_rate(self, value):
        self._sample_rate = value

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value

    @property
    def axis(self):
        return self._axis

    @axis.setter
    def axis(self, value):
        self._axis = value

    def reconnected(self):
        """
        To be called when connection restored, activate capture if was enabled
        """

        if self.__capture_enabled:
            self.enable_capture()

    def enable_capture(self, callback=False):
        """
        Enables capture service

        :param callback: external callback to be notified about new data
        :return: True if success
        """
        if not self.connected:
            logger.warning(f'Sensor {self.address} is not connected')
            return

        self.__next_packet_number = -1
        self.__next_packet_absolute_time = 0

        def callback_wrapper(sensor, value):
            sensor.__handle_value(value)

        if self._service.subscribe_to_characteristic(self, service_uuid=SERVICE_UUID,
                                                     char_uuid=SENSOR_STREAMING_CHARACTERISTIC_UUID,
                                                     callback=callback_wrapper):
            self.__capture_enabled = True
            if callback:
                self.__ext_callback = callback
            return True
        else:
            return False

    def disable_capture(self):
        """
        Disables capture service
        """
        self.__ext_callback = False
        self._service.unsubscribe_from_characteristic(self, service_uuid=SERVICE_UUID,
                                                      char_uuid=SENSOR_STREAMING_CHARACTERISTIC_UUID)
        self.__capture_enabled = False

    def read_current_configuration(self):
        self.read_sample_rate()
        self.read_axis()
        self.read_scale()

    def read_sample_rate(self):
        """
        Retrieves sensor current sample_rate
        """
        command = [
            ControlPointApi.COMMAND_GET.value,
            ControlPointApi.PARAM_SAMPLE_RATE.value,
        ]
        response = self._send_command(command)
        if response:
            self._sample_rate = SensorSampleRate(response[0])
            logger.info(f'Sample rate for {self.address}: {self._sample_rate}')

    def read_scale(self):
        """
        Retrieves sensor current scale
        """
        command = [
            ControlPointApi.COMMAND_GET.value,
            ControlPointApi.CP_PARAM_SCALE.value,
        ]
        response = self._send_command(command)
        if response:
            self._scale = SensorScale(response[0])
            logger.info(f'Sensor scale for {self.address}: {self._scale}')

    def read_axis(self):
        """
        Retrieves sensor current axis
        """
        command = [
            ControlPointApi.COMMAND_GET.value,
            ControlPointApi.CP_PARAM_AXIS.value,
        ]
        response = self._send_command(command)
        if response:
            self._axis = SensorAxis(response[0])
            logger.info(f'Sensor axis for {self.address}: {self._axis}')

    def write_configuration(self, sample_rate: SensorSampleRate = None, scale: SensorScale = None,
                            axis: SensorAxis = None):
        """
        Writes sensor configuration
        """
        sample_rate = sample_rate or self._sample_rate
        scale = scale or self._scale
        axis = axis or self._axis

        command = [
            ControlPointApi.COMMAND_SET.value,
            sample_rate.value,
            scale.value,
            axis.value,
        ]
        response = self._send_command(command)
        if response:
            result = ControlPointApi(response[0])
            if result == ControlPointApi.COMMAND_SET_RESPONSE_OK:
                logger.info(f'Sensor {self.address} configuration set: {sample_rate}, {scale}, {axis}')
                self._sample_rate = sample_rate
                self._scale = scale
                self._axis = axis
            else:
                logger.warning(
                    f'Failed to write configuration {sample_rate}, {scale}, {axis} for {self.address}, response={response}')

    def _send_command(self, command):
        """
        Send a command to the control_point char and gets response
        :param command:
        """
        if not self.connected:
            logger.warning(f'Sensor {self.address} is not connected')
            return

        success = self.write_characteristic(service_uuid=SERVICE_UUID, char_uuid=CONTROL_POINT_CHARACTERISTIC_UUID,
                                            data=command, acknowledged=True)
        if success:
            # wait for response
            time.sleep(0.1)
            response = self.read_characteristic(service_uuid=SERVICE_UUID,
                                                char_uuid=CONTROL_POINT_CHARACTERISTIC_UUID)
            return response
        else:
            logger.warning(f'Failed to send command {command} to {self.address}')
            return None

    def __handle_value(self, value):
        # Only process data if external callback is set
        if not self.__ext_callback:
            return

        imu_packet = ImuDataPacket.parse_packet(data=value, scale=self.scale,
                                                sample_rate=self.sample_rate, axis=self.axis)
        # Discard wrong packets
        if imu_packet is None:
            return

        # init packet_number to the current packet
        if self.__next_packet_number == -1:
            self.__next_packet_number = imu_packet.packet_num
            logger.info(f'Received a first packet from {self.address} with num_packet={imu_packet.packet_num}')
        elif self._verbose:
            # logger.info(f'{self.address} received packet nº {imu_packet.packet_num}.\t acc={imu_packet.acc[0:6]}...')
            print(f'{self.address} received packet nº {imu_packet.packet_num}.\t acc={imu_packet.acc[0:6]}...')

        # check packet missed
        missed_packets = imu_packet.packet_num - self.__next_packet_number

        if missed_packets > 0:
            logger.warning(
                f'Missed {missed_packets} packet from {self.address} (received={imu_packet.packet_num}, expected={self.__next_packet_number})!!!')
            self.__next_packet_number = imu_packet.packet_num

            # fix next_packet_absolute_time
            self.__next_packet_absolute_time += missed_packets * imu_packet.duration
            # packet.duration must be that of the previous packet, but we can assume are always the same...

        # set packet samples absolute_time
        imu_packet.absolute_time = [t + self.__next_packet_absolute_time for t in imu_packet.absolute_time]

        # prepare next packet absolute time
        self.__next_packet_absolute_time += imu_packet.duration
        # prepare next packet number
        self.__next_packet_number += 1
        # check overflow
        if self.__next_packet_number > MAX_PACKET_NUMBER:
            self.__next_packet_number = 0

        # notify external callback
        if callable(self.__ext_callback):
            self.__ext_callback(self, imu_packet, missed_packets)

    def json_dumps(self):
        return json.dumps(self.json())

    def json(self):
        sensor_json = {
            'name': self.name,
            'address': self.address,
            'mac_address': self.mac_address,
            'alias': self.alias,
            'location': self.location,
            'scale': self.scale.name,
            'axis': self.axis.name,
            'sample_rate': self.sample_rate.name,
            'config': self.config.name,
        }
        return sensor_json

    @staticmethod
    def json_load(json):
        imu_sensor = ImuSensorDevice()
        imu_sensor.name = json.get('name') or imu_sensor.name
        imu_sensor.address = json.get('address') or imu_sensor.address
        imu_sensor.mac_address = json.get('mac_address') or imu_sensor.mac_address
        imu_sensor.alias = json.get('alias') or imu_sensor.alias
        imu_sensor.location = json.get('location') or imu_sensor.location
        imu_sensor.scale = SensorScale[json.get('scale', imu_sensor.scale.name)]
        imu_sensor.axis = SensorAxis[json.get('axis', imu_sensor.axis.name)]
        imu_sensor.sample_rate = SensorSampleRate[json.get('sample_rate', imu_sensor.sample_rate.name)]
        imu_sensor.config = SensorPresetConfig[json.get('config', imu_sensor.config.name)]
        return imu_sensor

    @staticmethod
    def json_loads(json_str):
        return ImuSensorDevice.json_load(json.loads(json_str))


class GenericImuSensorService:
    __BLEService: GenericBLEService = None

    last_imu_sensors_found = []
    sensors_connected = []
    __known_imu_sensors = {}  # Singleton

    def __init__(self, service: GenericBLEService):
        self.__BLEService = service
        self.sensors_connected = []

    def enable(self):
        self.__BLEService.enable()
        self.load_imu_sensors_known()

    def disable(self):
        self.__BLEService.disable()
        self.save_imu_sensors_known()

    def get_imu_sensor(self, address):
        if address in self.__known_imu_sensors:
            return self.__known_imu_sensors.get(address)
        else:
            return None

    def clear_imu_sensors_known(self):
        self.__known_imu_sensors.clear()

    def save_imu_sensors_known(self):
        cache_dir = os.path.join(config.data_path, 'cache')
        try:
            os.makedirs(cache_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        filename = os.path.join(cache_dir, 'known_devices.json')
        known_devices = []
        for address, imu_sensor in self.__known_imu_sensors.items():
            imu_sensor: ImuSensorDevice
            known_devices.append(imu_sensor.json())
        with open(filename, 'w') as known_devices_file:
            json.dump(known_devices, known_devices_file, indent=4)

    def load_imu_sensors_known(self):
        filename = os.path.join(config.data_path, 'cache', 'known_devices.json')
        try:
            with open(filename, 'r') as known_devices_file:
                known_devices = json.load(known_devices_file)
                for device in known_devices:
                    imu_sensor = ImuSensorDevice.json_load(device)
                    self.__known_imu_sensors[imu_sensor.address] = imu_sensor
                return self.__known_imu_sensors
        except IOError:
            return False

    def parse_device_scan_record(self, device_record: DeviceScanRecord):
        # Check device Name
        device_name = device_record.scan_record.device_name
        if device_name is None or not device_name.startswith(IMU_SENSOR_NAME):
            return None

        imu_sensor = self.get_imu_sensor(device_record.address)
        if imu_sensor is None:
            imu_sensor = ImuSensorDevice()
            imu_sensor.name = device_name
            imu_sensor.address = device_record.address
            imu_sensor.mac_address = device_record.mac_address

        # save known device
        self.__known_imu_sensors[imu_sensor.address] = imu_sensor

        return imu_sensor

    def search_imu_sensors(self):
        """
        Performs imu sensors search
        :return:
        """
        if self.__BLEService.adapter is None:
            self.__BLEService.enable()

        logger.info("searching imu sensors, please wait...")
        devices_found = self.__BLEService.find_devices()

        self.last_imu_sensors_found = []
        device_record: DeviceScanRecord
        if devices_found:
            for address, device_record in devices_found.items():
                imu_sensor = self.parse_device_scan_record(device_record)
                if imu_sensor is not None:
                    self.last_imu_sensors_found.append(imu_sensor)

        self.save_imu_sensors_known()
        return self.last_imu_sensors_found

    def connect_imu_sensor(self, imu_sensor: ImuSensorDevice, on_connection_lost=False):
        def connection_lost(imu_sensor, reason):
            if imu_sensor in self.sensors_connected:
                self.sensors_connected.remove(imu_sensor)
            if callable(on_connection_lost):
                on_connection_lost(imu_sensor, reason)

        def reconnected(imu_sensor: ImuSensorDevice):
            time.sleep(0.01)
            imu_sensor.reconnected()

        result = self.__BLEService.connect_device(imu_sensor, on_disconnect=connection_lost,
                                                  on_reconnect=reconnected)
        if not result:
            imu_sensor.connected = False
            return False

        # descubrimos servicios
        logger.debug(f'Connected to {imu_sensor.address}. Discovering services...')
        services = self.__BLEService.load_services(imu_sensor)
        if not services:
            logger.warning("Failed to discover services")
            imu_sensor.disconnect()
            imu_sensor.connected = False
            return False

        imu_sensor.connected = True
        logger.debug('Done')

        self.sensors_connected.append(imu_sensor)

        return True

    def disconnect_imu_sensor(self, imu_sensor: ImuSensorDevice):
        if not imu_sensor.connected:
            logger.warning(f'ImuSensor {imu_sensor.address} was not connected')
            return False

        imu_sensor.disconnect()
        if imu_sensor in self.sensors_connected:
            self.sensors_connected.remove(imu_sensor)
        return True


class BlatannImuSensorService(GenericImuSensorService):

    def __init__(self, port):
        service = BlatannBLEService(port=port)
        super().__init__(service)


class EzSerialImuSensorService(GenericImuSensorService):

    def __init__(self, port):
        service = EzSerialBLEService(port=port)
        super().__init__(service)


def get_adapter(port):
    supported_ports_hwids = {
        'USB VID:PID=1915:C00A': BlatannImuSensorService,
        'USB VID:PID=0403:6001': EzSerialImuSensorService,
    }
    for hwid, adapter in supported_ports_hwids.items():
        if hwid in port.hwid:
            return adapter
    return None


def get_supported_adapters():
    from serial.tools.list_ports import comports
    ports = comports(False)
    adapters = {}
    for p in ports:

        adapter = get_adapter(p)
        if adapter is not None:
            adapters[p.name] = adapter(p.device)

    return adapters
