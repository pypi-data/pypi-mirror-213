import asyncio
import os
import time

import pandas as pd
from questionary import Choice, select, checkbox, confirm, text, Separator, path

from .labels import *
from .cli_common import print_section_msg, print_header_msg, press_continue, select_sensors, print_session_info, \
    print_sensor_list
from ..sensor_controller import SensorController
from ..session_controller import SessionController


async def cmd_delete_session(controller: SessionController):
    """
    Handles Delete session menu option
    :param controller:
    """
    print_section_msg(MENU_OPTION_DELETE_SESSION)
    if await confirm('Delete current session?', default=False).ask_async():
        session = controller.current_session
        delete_data = await confirm('Delete session data?', default=True).ask_async()
        print(f'Deleting session {session.session_id}...')
        controller.delete_session(session, delete_data=delete_data)
        print(f'Deleting session {session.session_id}... Done.')
        controller.current_session = None
        press_continue()


async def cmd_edit_session(controller: SessionController):
    """
    Handles Edit session menu option
    :param controller:
    """
    print_section_msg(MENU_OPTION_EDIT_SESSION)
    session = controller.current_session
    name = await text('Enter session name',
                      instruction=f'Leave blank to use current session name ({session.name})').ask_async()
    session_type = await text('Enter session type',
                              instruction=f'Leave blank to use current session type ({session.session_type})').ask_async()
    if not name:
        name = session.name
    if not session_type:
        session_type = session.session_type

    session_notes = await text('Enter session notes').ask_async()

    if await confirm(f'Modify session {session.name}', default=True).ask_async():
        if session.name != name:
            controller.delete_session(session=session)

        session.name = name
        session.session_type = session_type
        session.session_notes = session_notes
        controller.save_session(session=session)
        press_continue('Session modified')


async def cmd_clear_session_data(controller: SessionController):
    """
    Handles Clear session data menu option
    :param controller:
    """
    print_section_msg(MENU_OPTION_CLEAR_SESSION_DATA)
    if await confirm('Delete current session data?', default=True).ask_async():
        session = controller.current_session
        print(f'Deleting session {session.session_id} data...')
        controller.delete_session_data(session)
        session.sensors_reports.clear()
        print(f'Deleting session {session.session_id} data... Done.')
        press_continue()


async def cmd_start_capture(controller: SessionController):
    """
    Handles Start capture menu option
    :param controller:
    :return:
    """
    print_section_msg(MENU_OPTION_START_SESSION_CAPTURE)
    session = controller.current_session
    sensor_controller = SensorController()
    if not sensor_controller.connected_sensors:
        press_continue('No sensors connected, please get back and connect sensors')
        return

    if session.sensors_reports and await confirm('Use the same sensors than previous capture?',
                                                 default=True).ask_async():
        try:
            session_sensors = [s.address for s in session.sensors_reports]
        except Exception as e:
            session_sensors = session.sensors_reports
        selected_sensors = [s for s in sensor_controller.connected_sensors if s.address in session_sensors]
        if not selected_sensors:
            press_continue(f'None of {session.sensors_reports} are connected, please get back and connect them')
            return
    else:
        selected_sensors = await select_sensors(sensor_controller.connected_sensors)
        if not selected_sensors:
            press_continue('No sensors selected, cancel capture')
            return

    duration_choices = [
        Choice(title='Free running', value=0),
        Choice(title='30 seconds', value=30),
        Choice(title='1 minute', value=60),
        Choice(title='5 minutes', value=60 * 5),
        Choice(title='10 minutes', value=60 * 10),
        Choice(title='30 minutes', value=60 * 30),
        Choice(title='1 hour', value=60 * 60),
        Choice(title='Custom', value='custom'),
    ]
    duration = await select('Select duration of capture', choices=duration_choices).ask_async()
    if duration == 'custom':
        while True:
            try:
                duration = int(await text('Enter duration in seconds').ask_async())
                break
            except Exception as e:
                print('Enter valid number')
    elif duration == 0:
        print('No fixed duration selected, capture will end with user input')

    if not await confirm('Start capture?', default=True).ask_async():
        return

    result = await controller.launch_capture(duration=duration, sensors=selected_sensors, session=session,
                                             sensor_controller=sensor_controller)
    if result:
        press_continue('Capture ends')
    else:
        press_continue()


async def cmd_show_session_data(controller: SessionController):
    """
    Handles Show session data menu option
    :param controller:
    """

    print_section_msg(MENU_OPTION_SHOW_SESSION_DATA)
    session = controller.current_session
    print('Session details')
    print('---------------')
    print(f'Name: {session.name}')
    print(f'Type: {session.session_type}')
    print(f'Duration: {session.session_duration}')
    print(f'Notes: {session.session_notes}')
    print(f'Analyzed: {session.session_analyzed}')
    if session.sensors_reports:
        print('Sensors:')
        for sensor_report in session.sensors_reports:
            print(
                f'- {sensor_report.address} - [{sensor_report.alias} - Location: {sensor_report.location} - {sensor_report.axis}- {sensor_report.sample_rate}')
        print('-' * 240)
        print('Packets:')
        for sensor_report in session.sensors_reports:
            print(sensor_report.format_sensor_packet_capture_report())
        print('-' * 240)
        print('Samples:')
        for sensor_report in session.sensors_reports:
            print(sensor_report.format_sensor_data_capture_report())
        print('-' * 240)
        print('Streams:')
        for sensor_report in session.sensors_reports:
            print(sensor_report.format_sensor_streams_summary_report())

    if isinstance(session.session_raw_data, pd.DataFrame):
        print(f'Session Raw Data:')
        print(session.session_raw_data)

    if isinstance(session.session_data, pd.DataFrame):
        print(f'Session Data:')
        print(session.session_data)

    if await confirm('Plot session data?', default=False).ask_async():
        controller.plot_session_raw_data(session=session)
        controller.plot_session_data(session=session)
        press_continue()


async def cmd_analyze_session_data(controller: SessionController):
    """
    Handles Analyze session data menu option
    :param controller:
    """
    print_section_msg(MENU_OPTION_ANALYZE_SESSION_DATA)
    session = controller.current_session
    plot_result = await confirm('Plot analysis result', default=False).ask_async()
    controller.analyze_session_data(session, plot_result=plot_result)
    press_continue()


async def cmd_export_session_data(controller: SessionController):
    """
    Handles Export session menu option
    :param controller:
    """

    print_section_msg(MENU_OPTION_EXPORT_SESSION_DATA)

    export_path = await path(message='Enter export directory', only_directories=True).ask_async()
    export_choices = [
        Choice(title='Raw data (parquet)', value='parquet', checked=True, disabled='Will be exported by default'),
        Choice(title='Raw data (csv) - ~x7 parquet size', value='csv'),
        Choice(title='Raw data (excel) - ~x2.5 parquet size, slow', value='excel'),
        Choice(title='Raw data (html)', value='html'),
    ]
    outputs = await checkbox('Select data to export', choices=export_choices).ask_async()
    session = controller.current_session
    session_export_path = os.path.join(export_path, session.session_id)
    if not await confirm('Continue?', default=True).ask_async():
        return

    print(f'Exporting session {session.session_id} to {session_export_path}...')
    os.makedirs(session_export_path, exist_ok=True)
    controller.save_session(session=session, out_path=session_export_path)
    if 'csv' in outputs:
        print('Saving csv...')
        controller.save_session_data(session=session, parquet=False, csv=True, out_path=session_export_path)

    if 'excel' in outputs:
        print('Saving excel...')
        controller.save_session_data(session=session, parquet=False, excel=True, out_path=session_export_path)

    if 'html' in outputs:
        print('Saving html...')
        controller.plot_session_raw_data(session=session, out_path=session_export_path, auto_open=False)
        controller.plot_session_data(session=session, out_path=session_export_path, auto_open=False)

    print(f'Exporting session {session.session_id} to {session_export_path}... Done.')

    press_continue()


def get_session_menu():
    """
    Retrieves current session menu, to be used elsewhere
    :return:
    """
    choices = [
        Choice(MENU_OPTION_SHOW_SESSION_DATA),
        Choice(MENU_OPTION_START_SESSION_CAPTURE),
        Choice(MENU_OPTION_ANALYZE_SESSION_DATA),
        Choice(MENU_OPTION_EXPORT_SESSION_DATA),
        Separator(),
        Choice(MENU_OPTION_EDIT_SESSION),
        Choice(MENU_OPTION_DELETE_SESSION),
        Choice(MENU_OPTION_CLEAR_SESSION_DATA),
    ]

    callbacks = {
        MENU_OPTION_SHOW_SESSION_DATA: cmd_show_session_data,
        MENU_OPTION_START_SESSION_CAPTURE: cmd_start_capture,
        MENU_OPTION_ANALYZE_SESSION_DATA: cmd_analyze_session_data,
        MENU_OPTION_EXPORT_SESSION_DATA: cmd_export_session_data,
        MENU_OPTION_DELETE_SESSION: cmd_delete_session,
        MENU_OPTION_EDIT_SESSION: cmd_edit_session,
        MENU_OPTION_CLEAR_SESSION_DATA: cmd_clear_session_data,
    }

    return choices, callbacks


async def show_session_menu(controller: SessionController):
    """
    Utility to show current session menu
    :param controller:
    """
    choices, callbacks = get_session_menu()
    choices.append(Choice(MENU_OPTION_BACK))
    sensor_controller = SensorController()
    while True:
        if not controller.current_session:
            break

        print_header_msg(MENU_OPTION_SESSION)
        print_session_info(controller.current_session)
        print_sensor_list(sensor_controller.connected_sensors,
                          header=f'{len(sensor_controller.connected_sensors)} sensors connected')

        choice = await select('Select an option:', choices=choices).ask_async()
        callback = callbacks.get(choice, None)
        if callback:
            await callback(controller)
        else:
            break
