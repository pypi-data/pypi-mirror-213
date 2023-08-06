from __future__ import annotations

from pydantic import BaseSettings, Field, SecretStr, validator

from fsa_logger.sensor_api import SensorSampleRate, SensorScale, SensorAxis


class AppConfig(BaseSettings):
    data_path: str = 'data'
    use_parquet_partition: bool = False
    save_raw_acc: bool = False

    language: str = 'EN'
    sensor_menu_up: bool = True
    known_locations: list = ['POSITION_UP', 'POSITION_DOWN', 'POSITION_LEFT', 'POSITION_RIGHT']

    max_adapters: int = 4
    max_sensors_connected: int = 4
    max_sensors_per_adapter: int = 1
    collect_sensors_on_startup: bool = False

    background_save_period: int = 10
    keep_sensor_cache_files: bool = True
    default_session_name: str = 'New session'
    default_session_type: str = 'Test'
    default_session_duration: int = 10
    analyze_data_on_capture: bool = False

    sensor_use_default_configuration: bool = True
    default_sensor_sample_rate: SensorSampleRate = SensorSampleRate.SAMPLE_RATE_3200HZ_HF
    default_sensor_scale: SensorScale = SensorScale.SCALE_16G
    default_sensor_axis: SensorAxis = SensorAxis.AXIS_ONLY_YZ

    plot_max_seconds: int = 60
    analyze_min_stream_samples: int = 2 ** 12
    analyze_max_stream_samples: int = 2 ** 14

    @validator('default_sensor_sample_rate', pre=True)
    def parse_sensor_sample_rate(cls, v, values, **kwargs):
        if isinstance(v, str):
            try:
                return SensorSampleRate[v]
            except Exception as e:
                pass
        return values

    @validator('default_sensor_scale', pre=True)
    def parse_sensor_scale(cls, v, values, **kwargs):
        if isinstance(v, str):
            try:
                return SensorScale[v]
            except Exception as e:
                pass
        return values

    @validator('default_sensor_axis', pre=True)
    def parse_sensor_axis(cls, v, values, **kwargs):
        if isinstance(v, str):
            try:
                return SensorAxis[v]
            except Exception as e:
                pass
        return values

    class Config:
        use_enum_values = False
        env_prefix = 'logger_config_'
        env_file = '.env'
        env_file_encoding = 'utf-8'
