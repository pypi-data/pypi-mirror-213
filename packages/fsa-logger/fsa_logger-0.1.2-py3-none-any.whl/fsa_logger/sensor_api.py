from __future__ import annotations

from enum import Enum

SERVICE_UUID = '00000000-cc7a-482a-984a-7f2ed5b3e58f'
SENSOR_STREAMING_CHARACTERISTIC_UUID = '00000000-8e22-4541-9d4c-21edae82ed19'
CONTROL_POINT_CHARACTERISTIC_UUID = '00000001-8e22-4541-9d4c-21edae82ed19'

MAX_PACKET_NUMBER = 32000
ACC_DATA_LENGTH = 240
IMU_SENSOR_NAME = 'bt_ad_name'

class ControlPointApi(Enum):
    COMMAND_GET = 0x00
    COMMAND_SET = 0x01
    PARAM_SAMPLE_RATE = 0x01
    CP_PARAM_SCALE = 0x02
    CP_PARAM_AXIS = 0x03

    COMMAND_SET_RESPONSE_OK = 0x1F
    COMMAND_SET_RESPONSE_ERROR = 0xFF


class SensorSampleRate(Enum):
    SAMPLE_RATE_OFF = 0x00
    SAMPLE_RATE_1HZ_LP = 0x08
    SAMPLE_RATE_12HZ5_LP = 0x09
    SAMPLE_RATE_25HZ_LP = 0x0A
    SAMPLE_RATE_50HZ_LP = 0x0B
    SAMPLE_RATE_100HZ_LP = 0x0C
    SAMPLE_RATE_200HZ_LP = 0x0D
    SAMPLE_RATE_400HZ_LP = 0x0E
    SAMPLE_RATE_800HZ_LP = 0x0F
    SAMPLE_RATE_12HZ5_HR = 0x01
    SAMPLE_RATE_25HZ_HR = 0x02
    SAMPLE_RATE_50HZ_HR = 0x03
    SAMPLE_RATE_100HZ_HR = 0x04
    SAMPLE_RATE_200HZ_HR = 0x05
    SAMPLE_RATE_400HZ_HR = 0x06
    SAMPLE_RATE_800HZ_HR = 0x07
    SAMPLE_RATE_1600HZ_HF = 0x15
    SAMPLE_RATE_3200HZ_HF = 0x16
    SAMPLE_RATE_6400HZ_HF = 0x17

    def get_frequency_label(self):
        FREQ_LABELS = self.get_frequency_labels()
        return FREQ_LABELS.get(self)

    @staticmethod
    def get_frequency_labels():
        FREQ_LABELS = {
            SensorSampleRate.SAMPLE_RATE_OFF: 'OFF',
            SensorSampleRate.SAMPLE_RATE_1HZ_LP: '1Hz (LP)',
            SensorSampleRate.SAMPLE_RATE_12HZ5_LP: '12.5Hz (LP)',
            SensorSampleRate.SAMPLE_RATE_25HZ_LP: '25Hz (LP)',
            SensorSampleRate.SAMPLE_RATE_50HZ_LP: '50Hz (LP)',
            SensorSampleRate.SAMPLE_RATE_100HZ_LP: '100Hz (LP)',
            SensorSampleRate.SAMPLE_RATE_200HZ_LP: '200Hz (LP)',
            SensorSampleRate.SAMPLE_RATE_400HZ_LP: '400Hz (LP)',
            SensorSampleRate.SAMPLE_RATE_800HZ_LP: '800Hz (LP)',
            SensorSampleRate.SAMPLE_RATE_12HZ5_HR: '12.5Hz (HR)',
            SensorSampleRate.SAMPLE_RATE_25HZ_HR: '25Hz (HR)',
            SensorSampleRate.SAMPLE_RATE_50HZ_HR: '50Hz (HR)',
            SensorSampleRate.SAMPLE_RATE_100HZ_HR: '100Hz (HR)',
            SensorSampleRate.SAMPLE_RATE_200HZ_HR: '200Hz (HR)',
            SensorSampleRate.SAMPLE_RATE_400HZ_HR: '400Hz (HR)',
            SensorSampleRate.SAMPLE_RATE_800HZ_HR: '800Hz (HR)',
            SensorSampleRate.SAMPLE_RATE_1600HZ_HF: '1600Hz (HF)',
            SensorSampleRate.SAMPLE_RATE_3200HZ_HF: '3200Hz (HF)',
            SensorSampleRate.SAMPLE_RATE_6400HZ_HF: '6400Hz (HF)',
        }
        return FREQ_LABELS

    def get_frequency(self):
        FREQ_VALUES = self.get_frequencies()
        return FREQ_VALUES.get(self)

    @staticmethod
    def get_frequencies():
        FREQ_VALUES = {
            SensorSampleRate.SAMPLE_RATE_OFF: 0,
            SensorSampleRate.SAMPLE_RATE_1HZ_LP: 1,
            SensorSampleRate.SAMPLE_RATE_12HZ5_LP: 12.5,
            SensorSampleRate.SAMPLE_RATE_25HZ_LP: 25,
            SensorSampleRate.SAMPLE_RATE_50HZ_LP: 50,
            SensorSampleRate.SAMPLE_RATE_100HZ_LP: 10,
            SensorSampleRate.SAMPLE_RATE_200HZ_LP: 200,
            SensorSampleRate.SAMPLE_RATE_400HZ_LP: 400,
            SensorSampleRate.SAMPLE_RATE_800HZ_LP: 800,
            SensorSampleRate.SAMPLE_RATE_12HZ5_HR: 12.5,
            SensorSampleRate.SAMPLE_RATE_25HZ_HR: 25,
            SensorSampleRate.SAMPLE_RATE_50HZ_HR: 50,
            SensorSampleRate.SAMPLE_RATE_100HZ_HR: 100,
            SensorSampleRate.SAMPLE_RATE_200HZ_HR: 200,
            SensorSampleRate.SAMPLE_RATE_400HZ_HR: 400,
            SensorSampleRate.SAMPLE_RATE_800HZ_HR: 800,
            SensorSampleRate.SAMPLE_RATE_1600HZ_HF: 1600,
            SensorSampleRate.SAMPLE_RATE_3200HZ_HF: 3200,
            SensorSampleRate.SAMPLE_RATE_6400HZ_HF: 6400,
        }
        return FREQ_VALUES


class SensorScale(Enum):
    SCALE_2G = 0x00
    SCALE_16G = 0x01
    SCALE_4G = 0x02
    SCALE_8G = 0x03

    def get_scale_label(self):
        SCALE_LABELS = self.get_scale_labels()
        return SCALE_LABELS.get(self)

    @staticmethod
    def get_scale_labels():
        SCALE_LABELS = {
            SensorScale.SCALE_2G: '2G',
            SensorScale.SCALE_4G: '4G',
            SensorScale.SCALE_8G: '8G',
            SensorScale.SCALE_16G: '16G',
        }
        return SCALE_LABELS

    def get_scale_factor(self):
        SCALE_FACTORS = self.get_scale_factors()
        return SCALE_FACTORS.get(self)

    @staticmethod
    def get_scale_factors():
        SCALE_FACTORS = {
            SensorScale.SCALE_2G: 1 / 2 ** 14,
            SensorScale.SCALE_4G: 1 / 2 ** 13,
            SensorScale.SCALE_8G: 1 / 2 ** 12,
            SensorScale.SCALE_16G: 1 / 2 ** 11,
        }
        return SCALE_FACTORS


class SensorAxis(Enum):
    AXIS_XYZ = 0x10
    AXIS_ONLY_YZ = 0x11
    AXIS_ONLY_X = 0x12
    AXIS_ONLY_Y = 0x13
    AXIS_ONLY_Z = 0x14

    def get_axis_label(self):
        AXIS_LABELS = self.get_axis_labels()
        return AXIS_LABELS.get(self)

    @staticmethod
    def get_axis_labels():
        AXIS_LABELS = {
            SensorAxis.AXIS_XYZ: 'Three axis (X, Y, Z)',
            SensorAxis.AXIS_ONLY_YZ: 'Two axis (Y, Z)',
            SensorAxis.AXIS_ONLY_X: 'One axis (X)',
            SensorAxis.AXIS_ONLY_Y: 'One axis (Y)',
            SensorAxis.AXIS_ONLY_Z: 'One axis (Z)',
        }
        return AXIS_LABELS

    def get_axis_names(self):
        AXIS_NAMES = {
            SensorAxis.AXIS_XYZ: ['x', 'y', 'z'],
            SensorAxis.AXIS_ONLY_YZ: ['y', 'z'],
            SensorAxis.AXIS_ONLY_X: ['x'],
            SensorAxis.AXIS_ONLY_Y: ['y'],
            SensorAxis.AXIS_ONLY_Z: ['z'],
        }
        return AXIS_NAMES.get(self)


class SensorPresetConfig(Enum):
    XYZ_6_4_KHZ = 'Three axis (X, Y, Z) - 6.4 KHz - 16G'
    XYZ_3_2_KHZ = 'Three axis (X, Y, Z) - 3.2 KHz - 16G'
    XYZ_1_6_KhZ = 'Three axis (X, Y, Z) - 1.6 KHz - 16G'
    YZ_6_4_KHZ = 'Two axis (Y, Z) - 6.4 KHz - 16G'
    YZ_3_2_KHZ = 'Two axis (Y, Z) - 3.2 KHz - 16G'
    YZ_1_6_KHZ = 'Two axis (Y, Z) - 1.6 KHz - 16G'
    X_6_4_KHZ = 'One axis (X) - 6.4 KHz - 16G'
    Y_6_4_KHZ = 'One axis (Y) - 6.4 KHz - 16G'
    Z_6_4_KHZ = 'One axis (Z) - 6.4 KHz - 16G'
    X_3_2_KHZ = 'One axis (X) - 3.2 KHz - 16G'
    Y_3_2_KHZ = 'One axis (Y) - 3.2 KHz - 16G'
    Z_3_2_KHZ = 'One axis (Z) - 3.2 KHz - 16G'
    X_1_6_KHZ = 'One axis (X) - 1.6 KHz - 16G'
    Y_1_6_KHZ = 'One axis (Y) - 1.6 KHz - 16G'
    Z_1_6_KHZ = 'One axis (Z) - 1.6 KHz - 16G'
    CUSTOM = 'Custom'

    def get_sensor_configs(self):
        configs = self.get_configs()
        return configs.get(self)

    @staticmethod
    def get_configs():
        sensor_preset_configs = {
            SensorPresetConfig.XYZ_6_4_KHZ: (
            SensorAxis.AXIS_XYZ, SensorSampleRate.SAMPLE_RATE_6400HZ_HF, SensorScale.SCALE_16G),
            SensorPresetConfig.XYZ_3_2_KHZ: (
            SensorAxis.AXIS_XYZ, SensorSampleRate.SAMPLE_RATE_3200HZ_HF, SensorScale.SCALE_16G),
            SensorPresetConfig.XYZ_1_6_KhZ: (
            SensorAxis.AXIS_XYZ, SensorSampleRate.SAMPLE_RATE_1600HZ_HF, SensorScale.SCALE_16G),
            SensorPresetConfig.YZ_6_4_KHZ: (
            SensorAxis.AXIS_ONLY_YZ, SensorSampleRate.SAMPLE_RATE_6400HZ_HF, SensorScale.SCALE_16G),
            SensorPresetConfig.YZ_3_2_KHZ: (
            SensorAxis.AXIS_ONLY_YZ, SensorSampleRate.SAMPLE_RATE_3200HZ_HF, SensorScale.SCALE_16G),
            SensorPresetConfig.YZ_1_6_KHZ: (
            SensorAxis.AXIS_ONLY_YZ, SensorSampleRate.SAMPLE_RATE_1600HZ_HF, SensorScale.SCALE_16G),
            SensorPresetConfig.X_6_4_KHZ: (
            SensorAxis.AXIS_ONLY_X, SensorSampleRate.SAMPLE_RATE_6400HZ_HF, SensorScale.SCALE_16G),
            SensorPresetConfig.Y_6_4_KHZ: (
            SensorAxis.AXIS_ONLY_Y, SensorSampleRate.SAMPLE_RATE_6400HZ_HF, SensorScale.SCALE_16G),
            SensorPresetConfig.Z_6_4_KHZ: (
            SensorAxis.AXIS_ONLY_Z, SensorSampleRate.SAMPLE_RATE_6400HZ_HF, SensorScale.SCALE_16G),
            SensorPresetConfig.X_3_2_KHZ: (
            SensorAxis.AXIS_ONLY_X, SensorSampleRate.SAMPLE_RATE_3200HZ_HF, SensorScale.SCALE_16G),
            SensorPresetConfig.Y_3_2_KHZ: (
            SensorAxis.AXIS_ONLY_Y, SensorSampleRate.SAMPLE_RATE_3200HZ_HF, SensorScale.SCALE_16G),
            SensorPresetConfig.Z_3_2_KHZ: (
            SensorAxis.AXIS_ONLY_Z, SensorSampleRate.SAMPLE_RATE_3200HZ_HF, SensorScale.SCALE_16G),
            SensorPresetConfig.X_1_6_KHZ: (
            SensorAxis.AXIS_ONLY_X, SensorSampleRate.SAMPLE_RATE_1600HZ_HF, SensorScale.SCALE_16G),
            SensorPresetConfig.Y_1_6_KHZ: (
            SensorAxis.AXIS_ONLY_Y, SensorSampleRate.SAMPLE_RATE_1600HZ_HF, SensorScale.SCALE_16G),
            SensorPresetConfig.Z_1_6_KHZ: (
            SensorAxis.AXIS_ONLY_Z, SensorSampleRate.SAMPLE_RATE_1600HZ_HF, SensorScale.SCALE_16G),
            SensorPresetConfig.CUSTOM: (None, None, None),
        }
        return sensor_preset_configs

