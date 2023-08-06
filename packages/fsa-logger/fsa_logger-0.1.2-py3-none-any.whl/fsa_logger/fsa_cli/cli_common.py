from typing import List

from questionary import Choice, select, checkbox, text

from fsa_logger.config.config import AppConfig
from fsa_logger.imu_sensor_service import ImuSensorDevice
from fsa_logger.session_controller import LoggerSession

width = 140

app_config = AppConfig()

def press_continue(message=None):
    if message:
        print(message)
    input('Press ENTER to continue...')


def print_header_msg(msg, width=width, print=print):
    line = '*' * width
    blank = '*' + ' '.center(width - 2) + '*'
    print(line)
    print(blank)
    print('*' + msg.upper().center(width - 2) + '*')
    print(blank)
    print(line)


def print_section_msg(msg, width=width, print=print):
    line = '=' * width
    print(line)
    print('=' + msg.center(width - 2) + '=')
    print(line)


def print_sensor_list(sensors: List[ImuSensorDevice], header=None, print=print):
    if header:
        print_section_msg(msg=header, print=print)
    else:
        print_section_msg(f'{len(sensors)} sensors', print=print)
    if sensors:
        print(f'{"Address":20}\t{"Alias":10}\t{"Location":15}\t{"Connected":15}\t{"Configuration"}')
        print('-' * width)
        for sensor in sensors:
            sensor_config = f'{sensor.axis.get_axis_label()}, {sensor.sample_rate.get_frequency_label()}, {sensor.scale.get_scale_label()}'
            sensor_connected = sensor.adapter_name if sensor.connected else "---"
            print(f'{sensor.address:20}\t{sensor.alias:10}\t{sensor.location:15}\t{sensor_connected:15}\t{sensor_config}')

        print('-' * width)


async def request_sensor_alias_location(sensor):
    # set alias
    sensor_alias = await text(f'Enter sensor {sensor.label} alias', default=sensor.alias).ask_async()
    # set location
    sensor_location = await select(f'Enter sensor {sensor.label} location',
                                   choices=app_config.known_locations + ['Unknown'],
                                   default=sensor.location).ask_async()
    return sensor_alias, sensor_location


def print_session_info(session: LoggerSession, header=None, print=print):
    if header:
        print_section_msg(msg=header, print=print)
    else:
        print_section_msg(f'Name: {session.name} - Type: {session.session_type} - Created at: {session.created_at}',
                          print=print)
    if session.sensors_reports:
        print(f'Last capture duration: {session.session_duration:.1f} seconds')
        print(f'Sensors: {len(session.sensors_reports)}')
        for sensor in session.sensors_reports:
            print(f'- {sensor.address} - {sensor.sample_rate:.1f} Hz {sensor.axis}')
        print('-' * width)
        for sensor in session.sensors_reports:
            print(sensor.format_sensor_packet_capture_report())
        print('-' * width)
        for sensor in session.sensors_reports:
            print(sensor.format_sensor_data_capture_report())
        print('-' * width)
        for sensor in session.sensors_reports:
            print(sensor.format_sensor_streams_summary_report())

    else:
        print(f'Session has no data')

    print('-' * width)


async def select_sensors(sensors: List[ImuSensorDevice], single_selection=False, defaults_all=True):
    """
    Utility function to mark sensors to operate with
    :param sensors: List of available sensors
    :param single_selection: whether to select a single sensor
    :param defaults_all: Select all sensors by default (when no single selection)
    :return: Selected sensors
    """
    if single_selection:
        if not sensors:
            return None
        elif len(sensors) == 1:
            return sensors[0]
        else:
            choices = []
            for sensor in sensors:
                sensor: ImuSensorDevice
                choices.append(Choice(title=sensor.label, value=sensor))

            selected_sensor = await select(message='Select sensors', choices=choices).ask_async()
            return selected_sensor

    elif sensors:
        choices = []
        for sensor in sensors:
            sensor: ImuSensorDevice
            choices.append(Choice(title=sensor.label, value=sensor, checked=defaults_all))

        selected_sensors = await checkbox(message='Select sensors', choices=choices).ask_async()
        return selected_sensors
    else:
        return []
