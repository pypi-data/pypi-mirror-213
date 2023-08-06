from typing import List

from questionary import Choice, select, confirm, text

from .labels import *
from .cli_common import print_section_msg, print_header_msg, press_continue, print_sensor_list, select_sensors, \
    request_sensor_alias_location
from ..sensor_controller import SensorController
from ..imu_sensor_service import ImuSensorDevice
from ..sensor_api import SensorScale, SensorPresetConfig, SensorAxis, SensorSampleRate

from ..config.config import AppConfig

app_config = AppConfig()


async def cmd_show_sensors(controller: SensorController):
    """
    Handles Show sensors menu option
    :param controller:
    """

    print_section_msg(MENU_OPTION_SHOW_SENSORS)
    if controller.known_sensors:
        print_sensor_list(controller.known_sensors, header=f'{len(controller.known_sensors)} sensors known')
        if len(controller.known_sensors) > len(controller.connected_sensors):
            if await confirm('Connect sensors?', default=True).ask_async():
                await cmd_connect_sensors(controller)
        else:
            press_continue()
    else:
        if await confirm(f'No sensors known, run search?', default=True).ask_async():
            await cmd_search_sensors(controller)


async def cmd_edit_sensors(controller: SensorController):
    """
    Hanldes Edit sensor menu option
    :param controller:
    """
    print_section_msg(MENU_OPTION_EDIT_SENSORS)

    if controller.known_sensors:
        selected_sensors = await select_sensors(controller.known_sensors)
        modified = 0
        for sensor in selected_sensors:
            sensor: ImuSensorDevice
            sensor_alias, sensor_location = await request_sensor_alias_location(sensor=sensor)

            if await confirm(f'Modify sensor {sensor.label}?', default=True).ask_async():
                modified += 1
                sensor.alias = sensor_alias
                sensor.location = sensor_location
                print(f'Sensor {sensor.label} modified')

        print_sensor_list(selected_sensors, header=f'{modified} sensors modified')
        press_continue()

    else:
        if await confirm(f'No sensors known, run search?', default=True).ask_async():
            await cmd_search_sensors(controller)


async def cmd_config_sensors(controller: SensorController):
    """
    Hanldes Config sensor menu option
    :param controller:
    """
    print_section_msg(MENU_OPTION_EDIT_SENSORS)

    async def request_sensor_config(sensor:ImuSensorDevice):
        # set config
        choices = {c: Choice(title=c.value, value=c) for c in SensorPresetConfig}
        sensor_config: SensorPresetConfig = await select(f'Enter sensor {sensor.label} new config',
                                                         choices=list(choices.values()),
                                                         default=choices[sensor.config]).ask_async()

        if sensor_config == SensorPresetConfig.CUSTOM:
            # select axis
            choices = {c: Choice(title=l, value=c) for c, l in SensorAxis.get_axis_labels().items()}
            sensor_axis = await select(f'Enter sensor {sensor.label} new axis', choices=list(choices.values()),
                                       default=choices[sensor.axis]).ask_async()
            # select sample_rate
            choices = {c: Choice(title=l, value=c) for c, l in SensorSampleRate.get_frequency_labels().items()}
            sample_rate = await select(f'Enter sensor {sensor.label} new sample rate',
                                       choices=list(choices.values()),
                                       default=choices[sensor.sample_rate]).ask_async()
            # select scale
            choices = {c: Choice(title=l, value=c) for c, l in SensorScale.get_scale_labels().items()}
            sensor_scale = await select(f'Enter sensor {sensor.label} new scale', choices=list(choices.values()),
                                        default=choices[sensor.scale]).ask_async()
        else:
            sensor_axis, sample_rate, sensor_scale = sensor_config.get_sensor_configs()
        return sensor_config, sensor_axis, sample_rate, sensor_scale

    def apply_sensor_config(sensor:ImuSensorDevice, sensor_config, sensor_axis, sample_rate, sensor_scale):
        sensor.config = sensor_config
        sensor.axis = sensor_axis
        sensor.sample_rate = sample_rate
        sensor.scale = sensor_scale
        if sensor.connected:
            sensor.write_configuration()
        print(f'Sensor {sensor.label} configuration modified')

    if controller.known_sensors:
        selected_sensors = await select_sensors(controller.known_sensors)

        modified = 0
        same_config = False
        for sensor in selected_sensors:
            if not same_config:
                sensor_config, sensor_axis, sample_rate, sensor_scale = await request_sensor_config(sensor)
                if await confirm(f'Modify sensor {sensor.label}?', default=True).ask_async():
                    apply_sensor_config(sensor, sensor_config, sensor_axis, sample_rate, sensor_scale)
                    modified += 1
                if len(selected_sensors) > 1 and modified == 1:
                    same_config = await confirm('Use the same config for all remaining sensors?', default=True).ask_async()
            else:
                apply_sensor_config(sensor, sensor_config, sensor_axis, sample_rate, sensor_scale)
                modified += 1

        print_sensor_list(selected_sensors, header=f'{modified} sensors configured')
        press_continue()

    else:
        if await confirm(f'No sensors known, run search?', default=True).ask_async():
            await cmd_search_sensors(controller)


async def cmd_collect_sensors(controller: SensorController):
    """
    Handles Collect sensors menu option
    :param controller:
    """
    print_section_msg(MENU_OPTION_COLLECT_SENSORS)
    print('Collecting sensors...')
    sensors = await controller.search_sensors(auto_connect=True)
    print_sensor_list(sensors, f'{len(sensors)} sensors collected')
    press_continue()


async def cmd_search_sensors(controller: SensorController, auto_connect=False):
    """
    Handles Search sensors menu option

    :param controller:
    :param auto_connect: Whether autoconnect discovered sensors
    """
    print_section_msg(MENU_OPTION_SEARCH_SENSORS)
    print('Searching sensors...')
    found_sensors = await controller.search_sensors()
    if found_sensors:
        print_sensor_list(found_sensors, header=f'{len(found_sensors)} sensors found')
        if auto_connect or await confirm('Connect sensors?', default=True).ask_async():
            await cmd_connect_sensors(controller, found_sensors, wait_continue=not auto_connect)
    else:
        press_continue('No sensors found!')


async def cmd_connect_sensors(controller: SensorController, sensors: List[ImuSensorDevice] = None, wait_continue=True):
    """
    Handles Connect sensors menu option

    :param controller:
    :param sensors: Optional list of sensors to connect (defaults to controller.known_sensors)
    :param wait_continue: True for wait user press ENTER after connecting the sensors
    :return:
    """
    print_section_msg(MENU_OPTION_CONNECT_SENSORS)

    if not controller.known_sensors:
        await cmd_search_sensors(controller)
        return

    if sensors is None:
        connectable_sensors = [s for s in controller.known_sensors if not s.connected]
        selected_sensors = await select_sensors(connectable_sensors)
    else:
        selected_sensors = sensors

    if not selected_sensors:
        press_continue('No sensors selected')
    else:
        connected_sensors = []
        for sensor in selected_sensors:
            print(f'Connecting with {sensor.address}...')
            connected = await controller.connect_sensor(sensor)
            if connected:
                print(f'Connecting with {sensor.address}... Done')
                connected_sensors.append(sensor)
            else:
                print(f'Failed to connect with sensor {sensor.address}!')

        print_sensor_list(connected_sensors, header=f'{len(connected_sensors)} sensors connected')
        if wait_continue:
            press_continue()


async def cmd_disconnect_sensors(controller: SensorController, sensors: List[ImuSensorDevice] = None):
    """
    Handles Disconnect sensors menu option

    :param controller:
    :param sensors: Optional list of sensors to disconnect (defaults to controller.connectedsensors)
    :return:
    """
    print_section_msg(MENU_OPTION_DISCONNECT_SENSORS)
    if sensors is None:

        if not controller.connected_sensors:
            press_continue('No connected sensors')
            return

        selected_sensors = await select_sensors(controller.connected_sensors)
    else:
        selected_sensors = sensors

    for sensor in selected_sensors:
        print(f'Disconnecting with {sensor.address}...')
        await controller.disconnect_sensor(sensor)
        print(f'Disconnecting with {sensor.address}... Done.')
    press_continue()


async def cmd_test_sensors(controller: SensorController):
    """
    Handles Start capture menu option
    :param controller:
    :return:
    """
    if not controller.connected_sensors:
        press_continue('No sensors connected, please get back and connect sensors')
        return

    selected_sensors = await select_sensors(controller.connected_sensors)
    if not selected_sensors:
        press_continue('No sensors selected, cancel test')
        return

    if not await confirm('Start capture?', default=True).ask_async():
        return

    running = await controller.start_capture(sensors=selected_sensors, verbose=True, collect_data=False)
    if not running:
        press_continue('Failed to start capture')
        return

    await text('Capture start... Press ENTER to stop capture\n').ask_async()

    await controller.stop_capture(discard_data=True)

    press_continue()


def get_sensors_menu():
    """
    Retrieves sensors menu, to be used elsewhere
    :return:
    """
    choices = [
        Choice(MENU_OPTION_COLLECT_SENSORS),
        Choice(MENU_OPTION_SHOW_SENSORS),
        Choice(MENU_OPTION_EDIT_SENSORS),
        Choice(MENU_OPTION_CONFIG_SENSORS),
        Choice(MENU_OPTION_SEARCH_SENSORS),
        Choice(MENU_OPTION_CONNECT_SENSORS),
        Choice(MENU_OPTION_DISCONNECT_SENSORS),
        Choice(MENU_OPTION_TEST_SENSORS),
    ]

    callbacks = {
        MENU_OPTION_COLLECT_SENSORS: cmd_collect_sensors,
        MENU_OPTION_SHOW_SENSORS: cmd_show_sensors,
        MENU_OPTION_EDIT_SENSORS: cmd_edit_sensors,
        MENU_OPTION_CONFIG_SENSORS: cmd_config_sensors,
        MENU_OPTION_SEARCH_SENSORS: cmd_search_sensors,
        MENU_OPTION_CONNECT_SENSORS: cmd_connect_sensors,
        MENU_OPTION_DISCONNECT_SENSORS: cmd_disconnect_sensors,
        MENU_OPTION_TEST_SENSORS: cmd_test_sensors,
    }

    return choices, callbacks


async def show_sensors_menu(controller: SensorController):
    """
    Utility to show sensors menu
    :param controller:
    """
    choices, callbacks = get_sensors_menu()
    choices.append(Choice(MENU_OPTION_BACK))

    while True:
        print_header_msg(MENU_OPTION_SENSORS)
        print_sensor_list(controller.known_sensors, f'{len(controller.known_sensors)} sensors known')
        choice = await select('Select an option:', choices=choices).ask_async()
        callback = callbacks.get(choice, None)
        if callback:
            await callback(controller)
        else:
            break
