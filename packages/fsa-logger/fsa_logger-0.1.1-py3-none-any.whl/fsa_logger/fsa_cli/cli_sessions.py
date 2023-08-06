from questionary import confirm, text, Choice, select, checkbox, Separator, path
import os
from fsa_logger.config.config import AppConfig
from fsa_logger.fsa_cli.cli_common import print_section_msg, press_continue, print_header_msg, print_session_info, \
    request_sensor_alias_location
from fsa_logger.fsa_cli.cli_session import show_session_menu
from .labels import *
from fsa_logger.session_controller import SessionController, LoggerSession
from ..imu_sensor_service import ImuSensorDevice
from ..sensor_controller import SensorController

config = AppConfig()


async def cmd_list_sessions(controller: SessionController):
    """
    Handles List sessions menu option
    :param controller:
    """
    print_section_msg(MENU_OPTION_LIST_SESSIONS)
    sessions = controller.load_sessions()
    if sessions:
        print(f'{len(sessions)} sessions found:')
        print(f'{"Created at":25}\t{"Name":30}\t{"session_type":15}\tSensors')
        for session in sessions:
            try:
                sensors = [s.address for s in session.sensors_reports]
            except:
                sensors = session.sensors_reports
            print(f'{str(session.created_at):25}\t{session.name:30}\t{session.session_type:15}\t{sensors}')
        press_continue()
    else:
        if await confirm(f'No existing sessions, create?', default=False).ask_async():
            await cmd_create_session(controller)


async def cmd_quick_capture(controller: SessionController):
    """
    Handles Quick capture session menu option
    :param controller:
    """
    print_section_msg(MENU_OPTION_QUICK_CAPTURE)

    result = await controller.launch_capture()
    press_continue()


async def cmd_restore_session(controller: SessionController):
    """
    Handles Restore session menu option
    :param controller:
    """

    cache_path = os.path.join(config.data_path, 'sensor_cache')
    cache_path = await path("Select cache directory", default=cache_path, only_directories=True).ask_async()
    cache_files = os.listdir(cache_path)
    cache_dates = [f[0:19] for f in cache_files]
    # remove duplicates
    cache_dates = list(dict.fromkeys(cache_dates))
    cache_dates.sort()

    cache_date_files = {}
    for cache_date in cache_dates:
        selected_files = [f for f in cache_files if f.startswith(cache_date)]
        sensors_packet_files = [f for f in selected_files if 'packets' in f]
        sensors_files = [f for f in selected_files if f not in sensors_packet_files]
        cache_date_files[cache_date] = (sensors_files, sensors_packet_files)

    choices = [Choice(value=k, title=f'{k} - {v}') for k, v in cache_date_files.items()]

    print(f'Found {len(cache_dates)} capture events in {cache_path}')
    selected_date = await select('Select desired capture event for restore session', choices=choices).ask_async()
    sensors_files, sensors_packet_files = cache_date_files[selected_date]
    sensors_files.sort()
    sensors_packet_files.sort()
    sensor_data_names = [f[20:37] for f in sensors_files]
    sensor_packet_names = [f[20:37] for f in sensors_packet_files]
    if sensor_data_names == sensor_packet_names:
        print(f'Will restore session from {sensors_files} and {sensors_packet_files}')
        if await confirm('Continue?', default=True).ask_async():
            sensor_controller = SensorController()
            sensors = []
            for sensor_name in sensor_data_names:
                sensor = ImuSensorDevice()
                sensors.append(sensor)
                sensor.address = sensor_name.replace('-', ':')
                known_sensor = sensor_controller.get_known_sensor(sensor.address)
                if known_sensor:
                    sensor.alias, sensor.location = await request_sensor_alias_location(sensor=known_sensor)
                else:
                    sensor.alias, sensor.location = await request_sensor_alias_location(sensor=sensor)

            print('Inflating sensors data...')
            sensors_files = [os.path.join(cache_path, f) for f in sensors_files]
            sensors_packet_files = [os.path.join(cache_path, f) for f in sensors_packet_files]
            session_raw_data, session_packets, sensors = sensor_controller.inflate_sensors_data(
                sensors_files=sensors_files,
                sensors_packet_files=sensors_packet_files,
                sensors=sensors,
                keep_cache=True)
            print('Inflating sensors data... Done')
            name, session_type = await ask_session_name_type()
            session = LoggerSession(name=name, session_type=session_type)
            session.session_raw_data, session.session_packets, session.sensors_reports = session_raw_data, session_packets, sensors
            session.session_duration = session.session_raw_data['absolute_time'].max()
            print('Saving session...')
            controller.save_session(session)
            print('Saving session... Done.')
            press_continue('Session restored')
    else:
        press_continue('Sensor data files and sensor packet files does not match!, cannot restore')


async def ask_session_name_type():
    name = await text('Enter session name',
                      instruction=f'Leave blank to use default session name ({config.default_session_name})').ask_async()
    session_type = await text('Enter session type',
                              instruction=f'Leave blank to use default session type ({config.default_session_type})').ask_async()
    if not name:
        name = config.default_session_name
    if not session_type:
        session_type = config.default_session_type
    return name, session_type


async def cmd_create_session(controller: SessionController):
    """
    Handles Create session menu option
    :param controller:
    """
    print_section_msg(MENU_OPTION_CREATE_SESSION)
    name, session_type = await ask_session_name_type()

    session = LoggerSession(name=name, session_type=session_type)
    controller.save_session(session)
    controller.current_session = session
    print(f'Session {session.name} saved')
    await show_session_menu(controller)


async def cmd_select_session(controller: SessionController):
    """
    Handles Select session menu option
    :param controller:
    """
    print_section_msg(MENU_OPTION_SELECT_SESSION)
    choices = []
    for session in controller.load_sessions():
        session: LoggerSession
        choices.append(Choice(title=f'{session.session_id} - {session.session_type}', value=session))

    if choices:
        selected_session = await select(message='Select sessions', choices=choices).ask_async()
        print(f'Session {selected_session.session_id} selected')
        controller.current_session = selected_session
        controller.load_session_data(selected_session)
        await show_session_menu(controller)
    elif await confirm('No sessions available, create?', default=True).ask_async():
        await cmd_create_session(controller)


async def cmd_delete_sessions(controller: SessionController):
    """
    Handles Delete sessions menu option
    :param controller:
    :return:
    """
    print_section_msg(MENU_OPTION_DELETE_SESSIONS)
    sessions = controller.load_sessions()
    if not sessions:
        press_continue('No sessions available')
        return

    choices = []
    for session in sessions:
        session: LoggerSession
        choices.append(Choice(title=f'{session.session_id} - {session.name}', value=session))

    selected_sessions = await checkbox(message='Select sessions', choices=choices).ask_async()
    if not selected_sessions:
        print('No sessions selected')
    else:
        delete_data = await confirm('Delete session(s) data?', default=True).ask_async()
        for session in selected_sessions:
            print(f'Deleting session {session.session_id}...')
            controller.delete_session(session, delete_data=delete_data)
            print(f'Deleting session {session.session_id}... Done.')

        print(f'{len(selected_sessions)} sessions deleted')

    press_continue()


async def cmd_merge_sessions(controller: SessionController):
    """
    Handles Merge sessions menu option
    :param controller:
    :return:
    """
    print_section_msg(MENU_OPTION_MERGE_SESSIONS)
    sessions = controller.load_sessions()
    if not sessions:
        press_continue('No sessions available')
        return

    choices = []
    for session in sessions:
        session: LoggerSession
        choices.append(Choice(title=f'{session.session_id} - {session.name}', value=session))

    selected_sessions = await checkbox(message='Select sessions', choices=choices).ask_async()
    if not selected_sessions:
        press_continue('No sessions selected')
    else:
        for session in selected_sessions:
            print_session_info(session)

        if await confirm('Merge selected sessions?', default=True).ask_async():
            delete = await confirm('Delete merged sessions?', default=True).ask_async()
            merged_session = controller.merge_sessions(selected_sessions, delete_sessions=delete)
            print_session_info(merged_session)
            press_continue(f'{len(selected_sessions)} sessions merged')


async def cmd_clear_sessions_data(controller: SessionController):
    """
    Handles Clear sessions data menu option
    :param controller:
    :return:
    """
    print_section_msg(MENU_OPTION_CLEAR_SESSIONS_DATA)
    sessions = controller.load_sessions()
    if not sessions:
        press_continue('No sessions available')
        return

    choices = []
    for session in sessions:
        session: LoggerSession
        choices.append(Choice(title=f'{session.session_id} - {session.name}', value=session))

    selected_sessions = await checkbox(message='Select sessions', choices=choices).ask_async()
    if not selected_sessions:
        press_continue('No sessions selected')
    else:
        for session in selected_sessions:
            print(f'Deleting session data for {session.session_id} - {session.name}...')
            controller.delete_session_data(session)
            print(f'Deleting session data for {session.session_id} - {session.name}... Done.')

        press_continue(f'Deleted data for {len(selected_sessions)} sessions')


def get_sessions_menu():
    """
    Retrieves sessions menu, to be used elsewhere
    :return:
    """
    choices = [
        Choice(MENU_OPTION_QUICK_CAPTURE),
        Choice(MENU_OPTION_CREATE_SESSION),
        Choice(MENU_OPTION_SELECT_SESSION),
        Separator(),
        Choice(MENU_OPTION_LIST_SESSIONS),
        Choice(MENU_OPTION_DELETE_SESSIONS),
        Choice(MENU_OPTION_CLEAR_SESSIONS_DATA),
        Choice(MENU_OPTION_MERGE_SESSIONS),
        Choice(MENU_OPTION_RESTORE_SESSION),
    ]

    callbacks = {
        MENU_OPTION_QUICK_CAPTURE: cmd_quick_capture,
        MENU_OPTION_CREATE_SESSION: cmd_create_session,
        MENU_OPTION_SELECT_SESSION: cmd_select_session,
        MENU_OPTION_LIST_SESSIONS: cmd_list_sessions,
        MENU_OPTION_DELETE_SESSIONS: cmd_delete_sessions,
        MENU_OPTION_MERGE_SESSIONS: cmd_merge_sessions,
        MENU_OPTION_RESTORE_SESSION: cmd_restore_session,
        MENU_OPTION_CLEAR_SESSIONS_DATA: cmd_clear_sessions_data,
    }

    return choices, callbacks


async def show_sessions_menu(controller: SessionController):
    """
    Utility to show sessions menu
    :param controller:
    """
    choices, callbacks = get_sessions_menu()
    choices.append(Choice(MENU_OPTION_BACK))

    while True:
        print_header_msg(MENU_OPTION_SESSIONS)

        choice = await select('Select an option:', choices=choices).ask_async()
        callback = callbacks.get(choice, None)
        if callback:
            await callback(controller)
        else:
            break
