import asyncio
import time
from datetime import datetime
import os

import numpy as np
from pydantic import BaseModel
from pydantic.fields import FieldInfo, Field, Union
import pandas as pd

import plotly.express as px
from questionary import text

from .config.log_config import logger

from fsa_logger.config.config import AppConfig
from .sensor_controller import SensorController, SensorCaptureReport
from .utils import plot_figure

config = AppConfig()


class LoggerSession(BaseModel):
    created_at: datetime = FieldInfo(default_factory=datetime.now)
    # session_id: uuid.UUID = FieldInfo(default_factory=uuid.uuid4)
    name: str = config.default_session_name
    session_type: str = config.default_session_type
    session_duration: float = 0
    session_notes: str = None
    sensors_reports: list[SensorCaptureReport] = None
    session_analyzed: Union[bool, datetime] = None

    session_raw_data: pd.DataFrame = Field(None, exclude=True)
    session_packets: pd.DataFrame = Field(None, exclude=True)
    session_data: pd.DataFrame = Field(None, exclude=True)

    @property
    def session_id(self):
        session_id = self.created_at.isoformat(sep=' ', timespec='seconds').replace(":", '.')
        return f'{session_id}_{self.name}'

    @property
    def session_raw_data_path(self):
        return f'{self.session_path}_raw_data.parquet'

    @property
    def session_packets_path(self):
        return f'{self.session_path}_packets.parquet'

    @property
    def session_data_path(self):
        return f'{self.session_path}_data.parquet'

    @property
    def session_file(self):
        return f'{self.session_path}.json'

    @property
    def session_path(self):
        return os.path.join(config.data_path, 'session', f'{str(self.session_id)}')

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
        # json_encoders = {
        #     ImuSensorDevice: lambda s:s.json_dumps()
        # }


def create_file_path(filename):
    os.makedirs(os.path.split(filename)[0], exist_ok=True)


class SessionController:
    _current_session: LoggerSession = None
    _config: AppConfig = AppConfig()

    @property
    def current_session(self):
        return self._current_session

    @current_session.setter
    def current_session(self, value):
        self._current_session = value

    def merge_sessions(self, sessions, delete_sessions=False):

        sessions_data = []
        sessions_packets = []
        merge_session = LoggerSession()
        merge_session.sensors_reports = []

        for session in sessions:
            logger.info(f'Loading session {session.session_id} data...')
            self.load_session_data(session)
            if merge_session.created_at > session.created_at:
                merge_session.created_at = session.created_at
                merge_session.name = f'{session.name} (merged)'
                merge_session.session_type = session.session_type
                merge_session.session_notes = session.session_notes

            merge_session.sensors_reports.extend(session.sensors_reports)
            sessions_data.append(session.session_raw_data)
            sessions_packets.append(session.session_packets)
            logger.info(f'Loading session {session.session_id} data... Done.')

        logger.info('Merging data...')
        merge_session.session_raw_data = pd.concat(sessions_data)
        merge_session.session_packets = pd.concat(sessions_packets)
        absolute_start_timestamp = merge_session.session_raw_data['timestamp'].min().timestamp()
        merge_session.session_raw_data['absolute_time'] = merge_session.session_raw_data['timestamp'].apply(
            lambda t: t.timestamp() - absolute_start_timestamp)

        for sensor, sensor_data in merge_session.session_raw_data.groupby('sensor'):
            delta_t = sensor_data['delta_t'].min()
            delta_t_2 = delta_t / 2
            sensor_data['packet_stream'] = sensor_data['delta_t'].apply(lambda dt: 1 if dt - delta_t > delta_t_2 else 0).cumsum()


        merge_session.session_duration = merge_session.session_raw_data['absolute_time'].max()
        logger.info('Merging data... Done.')

        if delete_sessions:
            logger.info('Deleting merged sessions...')
            for session in sessions:
                self.delete_session(session, delete_data=True)
            logger.info('Deleting merged sessions... Done.')

        logger.info('Saving merged session...')
        self.save_session(merge_session)
        logger.info('Saving merged session... Done.')

        return merge_session

    def load_sessions(self):
        session_path = os.path.join(self._config.data_path, 'session')
        os.makedirs(session_path, exist_ok=True)
        session_files = os.listdir(session_path)
        session_files = [f for f in session_files if f.endswith('json')]
        sessions = []
        for session_file in session_files:
            session = LoggerSession.parse_file(os.path.join(session_path, session_file))
            sessions.append(session)

        return sessions

    def load_session_data(self, session: LoggerSession):

        def load_dataframe(data_path):
            file_name = f'{data_path}.parquet'
            if os.path.exists(file_name):
                return pd.read_parquet(file_name)
            elif os.path.exists(data_path):  # use partition
                return pd.read_parquet(data_path)
            else:
                return None

        session.session_raw_data = load_dataframe(session.session_raw_data_path)
        session.session_packets = load_dataframe(session.session_packets_path)
        session.session_data = load_dataframe(session.session_data_path)
        session.session_analyzed = isinstance(session.session_data, pd.DataFrame)

    def save_session(self, session: LoggerSession, out_path=None):
        if out_path:
            session_path = os.path.join(out_path, session.session_id)
        else:
            session_path = session.session_path
        create_file_path(session_path)

        # save json info
        with open(f'{session_path}.json', 'w') as json_file:
            json_file.write(session.json())

        self.save_session_data(session, out_path=out_path)

    def save_session_data(self, session: LoggerSession, parquet=True, excel=False, csv=False, out_path=None):
        if out_path:
            session_path = os.path.join(out_path, session.session_id)
        else:
            session_path = session.session_path
        create_file_path(session_path)

        def save_dataframe(data: pd.DataFrame, data_path):
            if isinstance(data, pd.DataFrame) and not data.empty:
                create_file_path(data_path)
                if parquet:
                    parquet_args = {
                        'coerce_timestamps': 'us',
                        'allow_truncated_timestamps': True,
                    }
                    if config.use_parquet_partition:
                        partition_cols = ['sensor_alias']
                        data.to_parquet(data_path, partition_cols=partition_cols, **parquet_args)
                    else:
                        data.to_parquet(f'{data_path}.parquet', **parquet_args)
                if csv:
                    data.to_csv(f'{data_path}.csv')
                if excel:
                    data.to_excel(f'{data_path}.xlsx')

        save_dataframe(session.session_raw_data, f'{session_path}_raw_data')
        save_dataframe(session.session_packets, f'{session_path}_packets')
        save_dataframe(session.session_data, f'{session_path}_data')

    def delete_session(self, session: LoggerSession, delete_data=True):

        if delete_data:
            self.delete_session_data(session)

        if os.path.exists(session.session_file):
            os.remove(session.session_file)

    def delete_session_data(self, session: LoggerSession):
        if os.path.exists(session.session_data_path):
            os.remove(session.session_data_path)

        if os.path.exists(session.session_raw_data_path):
            os.remove(session.session_raw_data_path)

    def analyze_session_data(self, session: LoggerSession, plot_result=False):
        if not isinstance(session.session_raw_data, pd.DataFrame) or session.session_raw_data.empty:
            self.load_session_data(session)

        if not isinstance(session.session_raw_data, pd.DataFrame) or session.session_raw_data.empty:
            logger.warning(f'Session {session.session_id} has no data, cannot analyze')
            return None
        else:
            logger.warning(f'Analyzing session {session.session_id}...')

        from scipy.fft import rfft, rfftfreq
        session_ffts = []
        for sensor, sensor_data in session.session_raw_data.groupby('sensor'):
            sensor_ffts = []
            logger.info(f'Analyzing sensor {sensor} packet streams...')
            for packet_stream, sensor_stream_data in sensor_data.groupby('packet_stream'):
                num_samples = len(sensor_stream_data)
                if num_samples < config.analyze_min_stream_samples:
                    logger.info(
                        f'Sensor {sensor} packet stream {packet_stream} has {num_samples}, less than min required samples ({config.analyze_min_stream_samples}. Skipping')
                    continue
                if num_samples > config.analyze_max_stream_samples:
                    sensor_stream_data = sensor_stream_data.iloc[0:config.analyze_max_stream_samples]
                    num_samples = len(sensor_stream_data)
                data_cols = [c for c in sensor_stream_data.columns if c.startswith('acc')]
                fft_df = pd.DataFrame()
                dt = sensor_stream_data['absolute_time'].diff().iloc[1]
                fft_df['freq'] = rfftfreq(num_samples, dt)
                fft_df['packet_stream'] = packet_stream
                for col in data_cols:
                    fft_df[col] = np.absolute(rfft(x=sensor_stream_data[col].values))

                sensor_ffts.append(fft_df)

            logger.info(f'Merging sensor {sensor} packet streams...')
            sensor_ffts = pd.concat(sensor_ffts)
            sensor_ffts['sensor'] = sensor
            sensor_ffts['location'] = sensor_data['location'].iloc[0]
            sensor_ffts['sensor_alias'] = sensor_data['sensor_alias'].iloc[0]
            session_ffts.append(sensor_ffts)

        session.session_analyzed = datetime.now()
        session.session_data = pd.concat(session_ffts)
        logger.info(f'Session {session.session_id} analyzed')
        if plot_result:
            self.plot_session_data(session)

        self.save_session(session)

        return session.session_data

    def plot_session_data(self, session: LoggerSession, facet_location=True, facet_alias=True, auto_open=True,
                          out_path=None):
        session_data = session.session_data
        if not isinstance(session_data, pd.DataFrame) or session_data.empty:
            logger.info(f'Session {session.session_id} has no data')
            return

        vars = [c for c in session_data.columns if c.startswith('acc')]
        num_sensors = len(session_data['sensor'].unique())
        num_alias = len(session_data['sensor_alias'].unique())
        num_locations = len(session_data['location'].unique())
        facet_col = 'sensor'
        if facet_location and num_locations == num_sensors:
            facet_col = 'location'
        elif facet_alias and num_alias == num_sensors:
            facet_col = 'sensor_alias'

        fig = px.line(session_data, x='freq', y=vars, facet_col=facet_col, facet_row='variable', color='packet_stream',
                      title=f'{session.name} - {session.session_type} - {session.created_at} - FFT Analysis')
        if out_path:
            filename = os.path.join(out_path, f'{session.session_id}_data.html')
        else:
            filename = f'{session.session_path}_data.html'
        plot_figure(fig, filename=filename, auto_open=auto_open)

    def plot_session_raw_data(self, session: LoggerSession, facet_location=True, facet_alias=True, duration=config.plot_max_seconds, auto_open=True,
                              out_path=None):

        session_data = session.session_raw_data
        if not isinstance(session_data, pd.DataFrame) or session_data.empty:
            logger.info(f'Session {session.session_id} has no raw data')
            return

        vars = [c for c in session_data.columns if c.startswith('acc')]
        num_sensors = len(session_data['sensor'].unique())
        num_alias = len(session_data['sensor_alias'].unique())
        num_locations = len(session_data['location'].unique())
        facet_row = 'sensor'
        if facet_location and num_locations == num_sensors:
            facet_row = 'location'
        elif facet_alias and num_alias == num_sensors:
            facet_row = 'sensor_alias'

        session_data = session_data[session_data['absolute_time'].le(duration)]
        fig = px.line(session_data, x='absolute_time', y=vars, facet_row=facet_row, color='variable',
                      title=f'{session.name} - {session.session_type} - {session.created_at} - Raw data')
        if out_path:
            filename = os.path.join(out_path, f'{session.session_id}_raw_data.html')
        else:
            filename = f'{session.session_path}_raw_data.html'
        plot_figure(fig, filename=filename, auto_open=auto_open)

    async def launch_capture(self, duration=config.default_session_duration, sensors=None, session=None,
                             sensor_controller: SensorController = None):

        if sensor_controller is None:
            sensor_controller = SensorController()
        sensors = sensors or sensor_controller.connected_sensors

        if not sensors:
            logger.warning('Cannot start capture, no sensors connected')
            return False

        if session is None:
            logger.info('launch_capture: no session provided, creating session with default parameters')
            session = LoggerSession()

        self._current_session = session

        sensors_list = [f'{s.address} - {s.alias}' for s in sensors]
        if duration > 0:
            logger.info(f'Launching capture with sensors {sensors_list} for {duration} seconds...')
        else:
            logger.info(f'Launching free-running capture with sensors {sensors_list}...')
        capture_start = time.time()
        running = await sensor_controller.start_capture(sensors=sensors)
        if not running:
            logger.warning(f'Failed to start capture with sensors {sensors_list}')
            return False
        else:
            logger.info(f'Capture with sensors {sensors_list} started, receiving data...')

        if duration > 0:
            remaining_time = duration
            while remaining_time > 0:
                session_duration = time.time() - capture_start
                remaining_time = duration - session_duration
                await asyncio.sleep(0.1)
                print(
                    f'\rCapturing data, duration: {session_duration:.1f} seconds, remaining time: {remaining_time:.1f} seconds...',
                    end='\r')
        else:
            async def show_progress():
                while running:
                    session_duration = time.time() - capture_start
                    print(f'\rCapturing data, duration: {session_duration:.1f} seconds... \tPress ENTER to stop',
                          end='\r')
                    await asyncio.sleep(0.1)

            asyncio.create_task(show_progress())
            await text('Capture start... Press ENTER to stop capture\n').ask_async()

        running = False

        sensors_files, sensors_packet_files = await sensor_controller.stop_capture()
        session.session_duration = time.time() - capture_start

        session.session_raw_data, session.session_packets, session.sensors_reports = sensor_controller.inflate_sensors_data(
            sensors_files=sensors_files,
            sensors_packet_files=sensors_packet_files,
            sensors=sensor_controller.known_sensors,
            keep_cache=True)

        sensor_controller.print_packet_capture_report(session.sensors_reports)
        sensor_controller.print_data_capture_report(session.sensors_reports)
        sensor_controller.print_streams_capture_report(session.sensors_reports)

        if config.analyze_data_on_capture:
            logger.info(f'Analyzing captured data...')
            self.analyze_session_data(session=session, plot_result=False)
            logger.info(f'Analyzing captured data... Done.')

        from .fsa_cli.cli_common import print_session_info # circular import
        print_session_info(session, print=logger.info)
        logger.info('Saving session data...')
        self.save_session(session)
        logger.info('Saving session data... Done.')

        return True
