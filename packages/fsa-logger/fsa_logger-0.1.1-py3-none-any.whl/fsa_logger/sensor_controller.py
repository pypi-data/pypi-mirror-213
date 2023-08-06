import asyncio
import os
import time
import uuid
from asyncio import Queue
from threading import Lock
from typing import List, Optional

import pandas as pd
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

from dateutil.relativedelta import relativedelta

from pydantic import BaseModel
from datetime import datetime

from pydantic.fields import FieldInfo, Field

from .config.config import AppConfig
from .config.log_config import logger

from .imu_sensor_service import ImuSensorDevice, ImuDataPacket, get_supported_adapters


class SensorCaptureReport(BaseModel):
    sample_rate: float = 0
    axis: list[str] = []
    address: str = None
    alias: str = None
    location: str = None
    packets_received: int = 0
    first_packet: int = 0
    first_packet_at: datetime = 0
    last_packet: int = 0
    last_packet_at: datetime = 0
    duration: float = 0
    packets_missed: int = 0
    samples_received: int = 0

    streams_count: int = 0
    streams_min: int = 0
    streams_mean: float = 0
    streams_max: int = 0

    def format_sensor_streams_summary_report(self):
        return f'Sensor {self.address} has {self.streams_count} continuous streams with ' \
               f'{self.streams_mean:.1f} samples in avg (min: {self.streams_min}, max: {self.streams_max})'

    def format_sensor_data_capture_report(self):
        return f'Sensor {self.address} received {self.samples_received} samples on axis {self.axis} in ' \
               f'{self.duration:.1f} sec. ({self.samples_received / self.duration:.1f}' \
               f' samples/sec.)'

    def format_sensor_packet_capture_report(self):
        packet_miss_ratio = 100*self.packets_missed / (self.packets_received + self.packets_missed) if self.packets_missed else 0
        return f'Sensor {self.address} received {self.packets_received} packets [{self.first_packet}:{self.last_packet}] in ' \
               f'{self.duration:.1f} sec. ({self.packets_received / self.duration:.1f}' \
               f' packets/sec.). Missed packets: {self.packets_missed} ({self.packets_missed / self.duration:.1f} per sec.) - {packet_miss_ratio:.1f}%'


class SensorController:
    _adapters = {}
    _known_sensors = []
    _connected_sensors = []
    _enabled_sensors = []

    __packets_received = {}
    __packets_lock = Lock()

    _config: AppConfig = AppConfig()

    @property
    def connected_sensors(self):
        return self._connected_sensors[:]  # [:] returns a copy

    @property
    def known_sensors(self):
        return self._known_sensors[:]  # [:] returns a copy

    @property
    def sensors_enabled(self):
        return self._enabled_sensors[:]  # [:] returns a copy

    @property
    def available_adapters(self):
        return list(self._adapters.keys())

    @property
    def _aux_adapter(self):
        if not self._adapters:
            return None
        else:
            return list(self._adapters.values())[0]

    def get_known_sensor(self, address):
        for sensor in self.known_sensors:
            if sensor.address == address:
                return sensor

        return None

    async def start(self):
        """
        Initializes sensor controller ang gets available adapters
        """
        await self.stop()

        adapters = get_supported_adapters()
        used_adapters = {}
        if not adapters:
            logger.warning('No adapters available!!')
        else:
            for port, adapter in adapters.items():
                logger.info(f'Enabling adapter {adapter.__class__.__name__} at port {port}...')
                try:
                    adapter.enable()
                    logger.info(f'Enabling adapter {adapter.__class__.__name__} at port {port}... Done')
                    used_adapters[port] = adapter
                except Exception as ex:
                    logger.warning(
                        f'Failed to enable adapter {adapter.__class__.__name__} at port {port}! Exception: {ex}')

                # limit adapters collected
                if self._config.max_adapters and len(used_adapters) == self._config.max_adapters:
                    break

        self._adapters.update(used_adapters)
        known_sensors = self._aux_adapter.load_imu_sensors_known()
        if known_sensors:
            self._known_sensors.extend(known_sensors.values())

    async def stop(self):
        """
        Stop sensor controller and frees resources
        """
        for port, adapter in self._adapters.items():
            logger.info(f'Disabling adapter {adapter.__class__.__name__} at port {port}...')
            adapter.disable()
            logger.info(f'Disabling adapter {adapter.__class__.__name__} at port {port}... Done.')

        self._adapters.clear()
        self._known_sensors.clear()

    async def search_sensors(self, auto_connect=False):
        """
        Launch a sensor search
        :return:
        """
        if not self._aux_adapter:
            logger.warning('No adapters available!!')
            return None

        sensors = self._aux_adapter.search_imu_sensors()
        for sensor in sensors:
            if sensor not in self._known_sensors:
                self._known_sensors.append(sensor)

        if auto_connect:
            await self.connect_sensors(sensors)

        return sensors

    async def connect_sensors(self, sensors: list[ImuSensorDevice] = None):
        """
        Establishes connection with the sensors provided. If sensors is None, uses all available sensors
        :param sensors:
        """
        sensors = sensors or [s for s in self.known_sensors if not s.connected]

        for sensor in sensors:
            await self.connect_sensor(sensor)

    async def connect_sensor(self, sensor: ImuSensorDevice,
                             write_default_config=_config.sensor_use_default_configuration):
        """
        Establishes connection with the required sensor
        :param sensor: Sensor to connect with
        :param write_default_config: writes stored config
        :return: True if connected (or already connected) or False if error or max sensor connected reached
        """
        if not self._aux_adapter:
            logger.warning('No adapters available!!')
            return False

        if self._config.max_sensors_connected and len(self.connected_sensors) >= self._config.max_sensors_connected:
            logger.warning(f'Max sensor connected reached, skip connect')
            return False

        if sensor.connected:
            logger.warning(f'Sensor {sensor.address} already connected!?')
            return True

        connect_adapter = None
        connect_adapter_name = None

        for name, adapter in self._adapters.items():
            adapter_sensors = len(adapter.sensors_connected)
            if adapter_sensors == self._config.max_sensors_per_adapter:
                logger.debug(
                    f'Adapter {name} has {adapter_sensors} sensor(s) connected (limit={self._config.max_sensors_per_adapter}), skipping')
                continue

            if connect_adapter is None or adapter_sensors < len(connect_adapter.sensors_connected):
                connect_adapter = adapter
                connect_adapter_name = name

        if not connect_adapter:
            logger.info(f'Cannot connect with sensor {sensor.address}, no available adapters')
            return False

        logger.info(f'Connecting sensor {sensor.address} with adapter at {connect_adapter_name}')
        connected = connect_adapter.connect_imu_sensor(sensor)
        if connected:
            self._connected_sensors.append(sensor)
            if sensor not in self._known_sensors:
                self._known_sensors.append(sensor)
            # if write_default_config:
            #     sensor.write_configuration()
            # else:
            #     sensor.read_current_configuration()
            if write_default_config:
                sensor.write_configuration(sample_rate=self._config.default_sensor_sample_rate,
                                           axis=self._config.default_sensor_axis,
                                           scale=self._config.default_sensor_scale)
            else:
                sensor.write_configuration()

        return connected

    async def disconnect_sensors(self, sensors: list[ImuSensorDevice]):
        """
        Disconnect indicated sensors
        :param sensors:
        """
        for sensor in sensors:
            await self.disconnect_sensor(sensor)
            if sensor not in self._known_sensors:
                self._known_sensors.append(sensor)

    async def disconnect_sensor(self, sensor: ImuSensorDevice):
        """
        Disconnect indicated sensor
        :param sensor:
        """
        sensor.disconnect()
        if sensor in self._connected_sensors:
            self._connected_sensors.remove(sensor)

    async def start_capture(self, sensors: list[ImuSensorDevice] = None, collect_data=True, verbose=False):
        """
        Starts a capture process in the sensors indicated
        :param sensors: Sensors to enable capture
        :param collect_data: whether to collect received data or not (False for testing comms. purposes)
        :param verbose: display received data on real time
        :return:
        """
        if not self._aux_adapter:
            logger.warning('No adapters available!!')
            return False

        if self._enabled_sensors:
            logger.warning('Ongoing capture in process, will stop and loose data')
            await self.stop_capture(discard_data=True)

        if collect_data:
            self.__packets_received = {sensor: [] for sensor in sensors}
        else:
            self.__packets_received = None

        sensors = sensors or self.connected_sensors

        def receive_packet(sensor, imu_packet: ImuDataPacket, missed_packets):
            if not collect_data:  # ignore packets
                return
            with self.__packets_lock:
                # return [] will discard packets from sensor if not registered (just in case)
                sensor_packets = self.__packets_received.get(sensor, [])
                sensor_packets.append((imu_packet, missed_packets))

        for sensor in sensors:
            logger.info(f'Enabling capture on sensor {sensor.address}...')
            sensor.verbose = verbose
            enabled = sensor.enable_capture(callback=receive_packet)
            if enabled:
                logger.info(f'Enabling capture on sensor {sensor.address}... Done')
                self._enabled_sensors.append(sensor)
                capture_started = True
            else:
                logger.warning(f'Failed to enable capture on sensor {sensor.address}! (will continue)')

        if collect_data:
            self.__background_task = asyncio.create_task(self.__save_packets_background())

        return capture_started

    async def stop_capture(self, discard_data=False):
        """
        Stops ongoing capture process
        :param discard_data: ignore received data
        :return:
        """
        if not self._aux_adapter:
            logger.warning('No adapters available!!')
            return

        for sensor in self._enabled_sensors:
            logger.info(f'Disabling capture on sensor {sensor.address}...')
            sensor.disable_capture()
            logger.info(f'Disabling capture on sensor {sensor.address}... Done')

        self._enabled_sensors.clear()

        if discard_data:
            return None

        logger.info('Awaiting data collection...')
        sensors_files, sensors_packet_files = await asyncio.wait_for(self.__background_task, timeout=None)
        logger.info(f'Awaiting data collection... Done.')
        return sensors_files, sensors_packet_files

    def inflate_sensors_data(self, sensors_files, sensors_packet_files, sensors,
                             keep_cache=_config.keep_sensor_cache_files):
        sensors_data = []
        sensors_packets = []
        sensors_reports = []

        for sensor_file, packet_file in zip(sensors_files, sensors_packet_files):
            sensor_data = pd.read_parquet(sensor_file)
            packet_data = pd.read_parquet(packet_file)
            if not keep_cache:
                os.remove(sensor_file)
                os.remove(packet_file)
            sensor_address = packet_data['sensor'].iloc[0]
            sensor: ImuSensorDevice = next((sensor for sensor in sensors if sensor_address == sensor.address))
            if sensor:
                sensor_data['location'] = sensor.location
                sensor_data['sensor_alias'] = sensor.alias

            start_timestamp = packet_data['timestamp'].iloc[0].timestamp()
            sensor_data['delta_t'] = sensor_data['sensor_time'].diff()
            delta_t = sensor_data['delta_t'].min()
            delta_t_2 = delta_t / 2
            sensor_data['packet_stream'] = sensor_data['delta_t'].apply(lambda dt: 1 if dt - delta_t > delta_t_2 else 0).cumsum()
            sensor_data['timestamp'] = pd.to_datetime(sensor_data['sensor_time'] + start_timestamp, unit='s')

            # generate sensor capture report
            sensor_capture_report = self.generate_sensor_capture_report(packet_data=packet_data, sensor_data=sensor_data, sensor=sensor)
            sensors_reports.append(sensor_capture_report)
            sensors_data.append(sensor_data)
            sensors_packets.append(packet_data)

        sensors_data = pd.concat(sensors_data)
        sensors_packets = pd.concat(sensors_packets)
        absolute_start_timestamp = sensors_data['timestamp'].min().timestamp()
        sensors_data['absolute_time'] = sensors_data['timestamp'].apply(
            lambda t: t.timestamp() - absolute_start_timestamp)
        return sensors_data, sensors_packets, sensors_reports

    def generate_sensor_capture_report(self, sensor=None, packet_data=None, sensor_data=None, generate_streams_report=True):
        sensor_capture_report = SensorCaptureReport()

        if sensor:
            sensor_capture_report.address = sensor.address
            sensor_capture_report.location = sensor.location
            sensor_capture_report.alias = sensor.alias

        if isinstance(packet_data, pa.Table):
            sensor_capture_report.packets_received = len(packet_data)
            sensor_capture_report.packets_missed = np.sum(packet_data['missed_packets'])
            sensor_capture_report.first_packet = packet_data['packet_num'][0].as_py()
            sensor_capture_report.first_packet_at = packet_data['timestamp'][0].as_py()
            sensor_capture_report.last_packet = packet_data['packet_num'][-1].as_py()
            sensor_capture_report.last_packet_at = packet_data['timestamp'][-1].as_py()
            sensor_capture_report.duration = sensor_capture_report.last_packet_at.timestamp() - sensor_capture_report.first_packet_at.timestamp()
        elif isinstance(packet_data, pd.DataFrame):
            sensor_capture_report.packets_received = len(packet_data)
            sensor_capture_report.packets_missed = int(packet_data['missed_packets'].sum())
            sensor_capture_report.first_packet = int(packet_data['packet_num'].iloc[0])
            sensor_capture_report.first_packet_at = packet_data['timestamp'].iloc[0]
            sensor_capture_report.last_packet = int(packet_data['packet_num'].iloc[-1])
            sensor_capture_report.last_packet_at = packet_data['timestamp'].iloc[-1]
            sensor_capture_report.duration = sensor_capture_report.last_packet_at.timestamp() - sensor_capture_report.first_packet_at.timestamp()

        if isinstance(sensor_data, pa.Table):
            delta_t = sensor_data['delta_t'][1].as_py()
            sensor_capture_report.sample_rate = 1 / delta_t
            sensor_capture_report.axis = [c for c in sensor_data.columns if 'acc' in c]
            sensor_capture_report.samples_received = len(sensor_data)

        elif isinstance(sensor_data, pd.DataFrame):
            delta_t = sensor_data['delta_t'].iloc[1]
            sensor_capture_report.sample_rate = 1 / delta_t
            sensor_capture_report.axis = [c for c in sensor_data.columns if 'acc' in c]
            sensor_capture_report.samples_received = len(sensor_data)
            sensor_capture_report.duration = sensor_capture_report.last_packet_at.timestamp() - sensor_capture_report.first_packet_at.timestamp()
            if generate_streams_report:
                streams_summary = sensor_data.groupby('packet_stream').count()['timestamp'].describe()
                sensor_capture_report.streams_count = int(streams_summary["count"])
                sensor_capture_report.streams_mean = streams_summary["mean"]
                sensor_capture_report.streams_min = int(streams_summary["min"])
                sensor_capture_report.streams_max = int(streams_summary["max"])

        return sensor_capture_report

    def print_packet_capture_report(self, sensor_capture_reports):
        logger.info("*" * 140)
        logger.info('*' + 'Packet summary report'.center(138) + '*')
        logger.info("*" * 140)
        logger.info(f'Received packets from {len(sensor_capture_reports)} sensors')
        logger.info("-" * 140)
        for sensor_capture_report in sensor_capture_reports:
            sensor_capture_report:SensorCaptureReport
            logger.info(sensor_capture_report.format_sensor_packet_capture_report())

        logger.info("-" * 140)

    def print_data_capture_report(self, sensor_capture_reports):
        logger.info("*" * 140)
        logger.info('*' + 'Data summary report'.center(138) + '*')
        logger.info("*" * 140)
        logger.info(f'Received data from {len(sensor_capture_reports)} sensors')
        logger.info("-" * 140)
        for sensor_capture_report in sensor_capture_reports:
            sensor_capture_report:SensorCaptureReport
            logger.info(sensor_capture_report.format_sensor_data_capture_report())

        logger.info("-" * 140)

    def print_streams_capture_report(self, sensor_capture_reports):
        logger.info("*" * 140)
        logger.info('*' + 'Streams summary report'.center(138) + '*')
        logger.info("*" * 140)
        logger.info(f'Received data from {len(sensor_capture_reports)} sensors')
        logger.info("-" * 140)
        for sensor_capture_report in sensor_capture_reports:
            sensor_capture_report:SensorCaptureReport
            logger.info(sensor_capture_report.format_sensor_streams_summary_report())

        logger.info("-" * 140)

    async def __save_packets_background(self):

        async def wait_for(wait_period):
            wake_up_time = time.time() + wait_period
            while time.time() < wake_up_time and self._enabled_sensors:
                await asyncio.sleep(0.1)
            # while wait_period > 0 and self._enabled_sensors:
            #     await asyncio.sleep(0.1)
            #     wait_period -= .1

        async def save_batch(batch):
            with self.__packets_lock:
                packets = self.__packets_received
                self.__packets_received = {sensor: [] for sensor in enabled_sensors}

            await self.__save_packets(packets, base_path=base_path, batch=batch)

        time_str = datetime.utcnow().isoformat(timespec='seconds').replace(':', '.')
        cache_path = os.path.join(self._config.data_path, 'sensor_cache')
        os.makedirs(cache_path, exist_ok=True)
        base_path = os.path.join(cache_path, time_str)
        batch_num = 0

        self.__collecting_data = True
        enabled_sensors = self._enabled_sensors[:]  # make copy

        # initial delay
        await wait_for(self._config.background_save_period)

        while self._enabled_sensors:
            logger.info('Background saving packets...')
            await save_batch(batch_num)
            logger.info('Background saving packets... Done.')
            batch_num += 1
            await wait_for(self._config.background_save_period)

        # save remaining packets
        logger.info('Background saving last packets...')
        await save_batch(batch_num)
        num_batches = batch_num + 1
        logger.info('Background saving last packets... Done.')

        # merge data
        logger.info('Merging background saved data...')
        sensors_tables, sensors_packet_tables = self.__merge_sensors_cache(sensors=enabled_sensors,
                                                                           num_batches=num_batches,
                                                                           base_path=base_path)
        logger.info('Merging background saved data... Done.')
        return sensors_tables, sensors_packet_tables

    def __merge_sensors_cache(self, sensors, num_batches, base_path):
        sensors_tables = []
        sensors_packet_tables = []
        for sensor in sensors:
            sensor_id = sensor.address.replace(':', '-')
            sensor_tables = []
            packet_tables = []

            for i in range(num_batches):
                sensor_file = f'{base_path}-{sensor_id}-{i:03}.parquet'
                if os.path.exists(sensor_file):
                    sensor_table = pq.read_table(sensor_file)
                    os.remove(sensor_file)
                    sensor_tables.append(sensor_table)
                packet_file = f'{base_path}-{sensor_id}-{i:03}-packets.parquet'
                if os.path.exists(packet_file):
                    packet_table = pq.read_table(packet_file)
                    packet_tables.append(packet_table)
                    os.remove(packet_file)

            sensor_data: pa.Table = pa.concat_tables(sensor_tables)
            packet_data: pa.Table = pa.concat_tables(packet_tables)
            sensor_data = sensor_data.append_column('sensor',
                                                    pa.array([sensor.address] * len(sensor_data), pa.string()))
            packet_data = packet_data.append_column('sensor',
                                                    pa.array([sensor.address] * len(packet_data), pa.string()))
            sensor_file = f'{base_path}-{sensor_id}.parquet'
            packet_file = f'{base_path}-{sensor_id}-packets.parquet'
            pq.write_table(sensor_data, where=sensor_file)
            pq.write_table(packet_data, where=packet_file)
            sensors_tables.append(sensor_file)
            sensors_packet_tables.append(packet_file)

        return sensors_tables, sensors_packet_tables

    async def __save_packets(self, packets, base_path, batch=0):

        for sensor, sensor_packets in packets.items():
            sensor: ImuSensorDevice
            if not sensor_packets:
                continue
            axis_names = sensor.axis.get_axis_names()
            num_axis = len(axis_names)
            time_data = [np.array(p.absolute_time).reshape(-1, 1) for p, missed in sensor_packets]
            np_time_data = np.concatenate(time_data).reshape(-1, 1)
            acc_data = [np.array(p.acc).reshape(-1, num_axis) for p, missed in sensor_packets]
            np_acc_data = np.concatenate(acc_data)
            if self._config.save_raw_acc:
                raw_data = [np.array(p.raw).reshape(-1, num_axis) for p, missed in sensor_packets]
                np_raw_data = np.concatenate(raw_data)
            if self._config.save_raw_acc:
                names = ['sensor_time'] + [f'acc_{name}' for name in axis_names] + [f'raw_{name}' for name in
                                                                                    axis_names]
                np_data = np.concatenate((np_time_data, np_acc_data, np_raw_data), axis=1)
            else:
                names = ['sensor_time'] + [f'acc_{name}' for name in axis_names]
                np_data = np.concatenate((np_time_data, np_acc_data), axis=1)

            sensor_table = pa.Table.from_arrays(arrays=np_data.transpose(), names=names)
            packet_data = np.array([[p.rx_timestamp, p.packet_num, missed] for p, missed in sensor_packets])
            packet_table = pa.Table.from_arrays(arrays=packet_data.transpose(),
                                                names=['timestamp', 'packet_num', 'missed_packets'])

            # save sensor table
            sensor_id = sensor.address.replace(':', '-')
            sensor_file = f'{base_path}-{sensor_id}-{batch:03}.parquet'
            pq.write_table(sensor_table, where=sensor_file)

            # save packet table
            packet_file = f'{base_path}-{sensor_id}-{batch:03}-packets.parquet'
            pq.write_table(packet_table, where=packet_file)

            # packet capture report
            sensor_capture_report = self.generate_sensor_capture_report(sensor=sensor, packet_data=packet_table)
            logger.info(sensor_capture_report.format_sensor_packet_capture_report())

    def print_sensor_packet_capture_report(self, sensor: str, packet_table: pa.Table):
        packets_received = len(packet_table)
        if isinstance(packet_table, pa.Table):
            packets_missed = np.sum(packet_table['missed_packets'])
            first_packet = packet_table['packet_num'][0].as_py()
            first_packet_at = packet_table['timestamp'][0].as_py()
            last_packet = packet_table['packet_num'][-1].as_py()
            last_packet_at = packet_table['timestamp'][-1].as_py()
        else:
            packets_missed = packet_table['missed_packets'].sum()
            first_packet = packet_table['packet_num'].iloc[0]
            first_packet_at = packet_table['timestamp'].iloc[0]
            last_packet = packet_table['packet_num'].iloc[-1]
            last_packet_at = packet_table['timestamp'].iloc[-1]
        duration = last_packet_at.timestamp() - first_packet_at.timestamp()

        logger.info(f'Sensor {sensor} received {packets_received} packets [{first_packet}:{last_packet}] in '
                    f'{duration:.1f} seconds ({packets_received / duration:.1f}'
                    f' packets/second). Missed packets: {packets_missed} ({packets_missed / duration:.1f} per second)')
