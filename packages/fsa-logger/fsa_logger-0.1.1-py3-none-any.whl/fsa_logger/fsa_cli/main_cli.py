import time
import asyncio
import os

from fsa_logger.config.config import AppConfig
from fsa_logger.fsa_cli.cli_common import press_continue, print_header_msg, print_sensor_list
from fsa_logger.fsa_cli.cli_sensors import show_sensors_menu, get_sensors_menu, cmd_collect_sensors
from fsa_logger.fsa_cli.cli_sessions import get_sessions_menu, show_sessions_menu, cmd_quick_capture
from fsa_logger.session_controller import SessionController

from .labels import *

from pyfiglet import Figlet
from questionary import Choice, select, Separator

from fsa_logger.sensor_controller import SensorController

f = Figlet()
from fsa_logger.config.log_config import logger


async def launch_capture(sensor_controller, duration, export_path=None):
    duration = duration or config.default_session_duration
    print_header_msg(f'Unattended sensor capture for {duration} seconds')
    logger.info('Collecting sensors...')
    await sensor_controller.search_sensors(auto_connect=True)
    print_sensor_list(sensor_controller.connected_sensors, header=f'Collected {len(sensor_controller.connected_sensors)} sensors')
    logger.info('Collecting sensors... Done')

    logger.info('Capturing data...')
    controller = SessionController()
    await controller.launch_capture(sensor_controller=sensor_controller, duration=duration)
    logger.info('Capturing data... Done.')
    if export_path:
        session = controller.current_session
        session_export_path = os.path.join(export_path, session.session_id)

        logger.info(f'Saving session data to {session_export_path}...')
        os.makedirs(export_path, exist_ok=True)
        controller.save_session(session=session, out_path=session_export_path)
        logger.info('Saving session data to csv...')
        controller.save_session_data(session=session, out_path=session_export_path, csv=True, parquet=False)
        logger.info('Generating html reports...')
        controller.plot_session_raw_data(session=session, out_path=session_export_path, auto_open=False)
        controller.plot_session_data(session=session, out_path=session_export_path, auto_open=False)
        logger.info(f'Saving session data to {session_export_path}... Done.')


async def show_cli(sensor_controller):
    session_controller = SessionController()
    session_callbacks = {MENU_OPTION_SESSIONS: show_sessions_menu}
    session_choices = [Choice(menu) for menu in session_callbacks]

    sensor_callbacks = {MENU_OPTION_SENSORS: show_sensors_menu, MENU_OPTION_COLLECT_SENSORS: cmd_collect_sensors}
    sensor_choices = [Choice(menu) for menu in sensor_callbacks]
    if config.sensor_menu_up:
        sensor_choices, sensor_callbacks = get_sensors_menu()

    if config.collect_sensors_on_startup:
        await cmd_collect_sensors(sensor_controller)

    session_choices, session_callbacks = get_sessions_menu()

    main_choices = sensor_choices + [Separator()] + session_choices + [Choice(MENU_OPTION_EXIT)]

    while True:
        choice = await select('Select an option:', choices=main_choices).ask_async()

        if choice in session_callbacks:
            callback = session_callbacks.get(choice, None)
            if callback:
                await callback(session_controller)
            else:
                break

        elif choice in sensor_callbacks:
            callback = sensor_callbacks.get(choice, None)
            if callback:
                await callback(sensor_controller)
            else:
                break
        else:
            break


async def main_cli(capture=False, duration=config.default_session_duration, export_path=None):
    print(f.renderText("FSA Logger"))

    sensor_controller = SensorController()

    logger.info('Starting sensor controller...')
    await sensor_controller.start()
    logger.info('Starting sensor controller... Done.')
    logger.info(f'Available adapters: {sensor_controller.available_adapters}')

    if capture:
        await launch_capture(sensor_controller, duration=duration, export_path=export_path)
    else:
        await show_cli(sensor_controller)

    logger.info('Stopping sensor controller...')
    await sensor_controller.stop()
    logger.info('Stopping sensor controller... Done.')


def main():
    asyncio.run(main_cli())


if __name__ == '__main__':
    main()
