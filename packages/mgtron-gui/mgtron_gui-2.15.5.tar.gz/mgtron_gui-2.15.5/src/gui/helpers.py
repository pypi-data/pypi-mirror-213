"""Helper functions for the GUI. Intended design is functional programming."""
#!/usr/bin/env python

import configparser
import itertools
import json
import logging
import pathlib
import platform
import sqlite3

import subprocess
import sys
import requests
from datetime import datetime

import dearpygui.dearpygui as dpg
from interface import Megatron, format_output
from neighborhood_list import EG25G

from src.gui.db.models import delete_sql_save_data, get_sql_details
from src.gui.db.models import get_sql_save_names
from src.gui.db.models import save_to_database

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
WORKING = ROOT / "src" / "gui"


# datetime object containing current date and time
now = datetime.now()

loggey = logging.getLogger(name=__name__)

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

loggey.info(msg="class Megatron instatiated")
data_vehicle: Megatron = Megatron()

loggey.info(msg="Remote colors initialized")
dpg.create_context()


FREQ: dict[str, int] = {
    "chan_1": 0,
    "chan_2": 3,
    "chan_3": 6,
    "chan_4": 9,
    "chan_5": 12,
    "chan_6": 15,
    "chan_7": 18,
    "chan_8": 21,
}

POWS: dict[str, int] = {
    "chan_1": 1,
    "chan_2": 4,
    "chan_3": 7,
    "chan_4": 10,
    "chan_5": 13,
    "chan_6": 16,
    "chan_7": 19,
    "chan_8": 22,
}

BANDS: dict[str, int] = {
    "chan_1": 2,
    "chan_2": 5,
    "chan_3": 8,
    "chan_4": 11,
    "chan_5": 14,
    "chan_6": 17,
    "chan_7": 20,
    "chan_8": 23,
}

NAME: dict[str, int] = {
    "chan_1": 24,
    "chan_2": 25,
    "chan_3": 26,
    "chan_4": 27,
    "chan_5": 28,
    "chan_6": 29,
    "chan_7": 30,
    "chan_8": 31,
}

# Green Button Theme
with dpg.theme() as grn_btn_theme, dpg.theme_component(dpg.mvAll):
    dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 255, 0, 255))  # GREEN
# Red Button Theme
with dpg.theme() as red_btn_theme, dpg.theme_component(dpg.mvAll):
    dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 0, 0, 255))  # RED
# Blue Button Theme
with dpg.theme() as blue_btn_theme, dpg.theme_component(dpg.mvAll):
    dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 0, 255, 255))  # BLUE
# Grey Button Theme
with dpg.theme() as grey_btn_theme, dpg.theme_component(dpg.mvAll):
    dpg.add_theme_color(dpg.mvThemeCol_Button, (105, 105, 105, 255))  # GREY
# Orange Button Theme
with dpg.theme() as orng_btn_theme, dpg.theme_component(dpg.mvAll):
    dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 165, 0, 255))  # ORANGE

# load the intial contents of the database for comparison upon new save
loggey.info(msg="inital loading database")


def version_getter() -> str | None:
    """Get the latest version from the CHANGELOG file."""
    with open(ROOT / "CHANGELOG.md") as f:
        for line in f:
            if line.__contains__("##") and not line.__contains__(
                    "YEAR MONTH DAY"):
                correct_line = line.split("-")[0].strip()
                version = correct_line.split("[")[1]

                return version.strip("]")
        return None


VERSION: str | None = version_getter()


def device_names() -> list[str]:
    """Use a bash script to list connected microarchitectures."""
    if platform.system().lower != "windows":
        # Avoid crashing program if there are no devices detected
        try:
            listing_script = [
                # f'#!/bin/bash\n'
                f'for sysdevpath in $(find /sys/bus/usb/devices/usb*/ -name dev | grep "ACM"); do\n'
                f'(syspath={"${sysdevpath%/dev}"}\n'
                f'devname={"$(udevadm info -q name -p $syspath)"}\n'
                f'[[ {"$devname"} == "bus/"* ]] && exit\n'
                f'eval "$(udevadm info -q property --export -p $syspath)"\n'
                f'[[ -z "$ID_SERIAL" ]] && exit\n'
                f'echo "/dev/$devname - $ID_SERIAL"\n'
                f") done"
            ]
            devices: subprocess.CompletedProcess[str] = subprocess.run(
                args=listing_script,
                shell=True,
                stdout=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                capture_output=False,
            )
        except TypeError:
            loggey.warning(
                msg=f"No devices detected | {device_names.__name__}")
            devices = subprocess.CompletedProcess(
                args="",
                returncode=1,
                stdout="",
                stderr="",
            )

    _devices: list = list(
        devices.stdout.strip().split(
            sep="\n"))  # type: ignore

    loggey.info(msg=f"Devices found: {_devices} | {device_names.__name__}")

    # If there is only one device skip the hooplah
    if len(_devices) == 1:
        return _devices
    return sorted(_devices)


DEVICE: list[str] = device_names()

def card_state(channel: int) -> None:
    """Get the present state of the card."""
    # Refresh indicators; this grants state of the card
    card_stats = get_card_status()

    try:  # If the card is not connected, then skip
        card_stats["power"][channel - 1]
    except IndexError:
        dpg.set_value(
            item=f"power_{channel}_indicator",
            value="N/A",
        )
        dpg.set_value(
            item=f"bandwidth_{channel}_indicator",
            value="N/A",
        )

        return

    # Power state
    if int(
        dpg.get_value(item=f"power_{channel}"),
    ) != int(card_stats["power"][channel - 1]):
        dpg.set_value(
            item=f"power_{channel}_indicator",
            value=f"{int(card_stats['power'][channel-1])} pwr",
        )

    # frquency state
    if int(
        dpg.get_value(item=f"freq_{channel}"),
    ) != int(card_stats["freq"][channel - 1]):
        dpg.set_value(
            item=f"frequency_{channel}_indicator",
            value=f"{card_stats['freq'][channel-1]} MHz",
        )

    # bandwidth state
    if int(
        dpg.get_value(item=f"bandwidth_{channel}"),
    ) != int(card_stats["bw"][channel - 1]):
        dpg.set_value(
            item=f"bandwidth_{channel}_indicator",
            value=f"{int(card_stats['bw'][channel-1])} %",
        )

    # Clear the card state if field is the same as the input
    if int(
        dpg.get_value(item=f"power_{channel}"),
    ) == int(card_stats["power"][channel - 1]):
        dpg.configure_item(
            item=f"power_{channel}_indicator",
            default_value="",
        )

    if int(
        dpg.get_value(item=f"freq_{channel}"),
    ) == int(card_stats["freq"][channel - 1]):
        dpg.configure_item(
            item=f"frequency_{channel}_indicator",
            default_value="",
        )

    if int(
        dpg.get_value(item=f"bandwidth_{channel}"),
    ) == int(card_stats["bw"][channel - 1]):
        dpg.configure_item(
            item=f"bandwidth_{channel}_indicator",
            default_value="",
        )


def start_up_card_state() -> None:
    """Specialized function to display card state at startup."""
    # Refresh indicators; this grants state of the card
    card_stats = get_card_status()

    for i in range(1, 9):
        try:  # If the card is not connected, then skip
            card_stats["power"][i - 1]
        except (IndexError, KeyError):
            dpg.set_value(
                item=f"power_{i}_indicator",
                value="N/A",
            )
            dpg.set_value(
                item=f"bandwidth_{i}_indicator",
                value="N/A",
            )

            continue

        # check if the input value is different from the card state
        if int(dpg.get_value(item=f"power_{i}")) != int(
                card_stats["power"][i - 1]):
            dpg.set_value(
                item=f"power_{i}_indicator",
                value=f"{int(card_stats['power'][i-1])} pwr",
            )

        if int(dpg.get_value(item=f"freq_{i}")) != int(
                card_stats["freq"][i - 1]):
            dpg.set_value(
                item=f"frequency_{i}_indicator",
                value=f"{card_stats['freq'][i-1]} MHz",
            )

        if int(dpg.get_value(item=f"bandwidth_{i}")) != int(
                card_stats["bw"][i - 1]):
            dpg.set_value(
                item=f"bandwidth_{i}_indicator",
                value=f"{int(card_stats['bw'][i-1])} %",
            )


def return_teensy(device_list: list[str] = DEVICE) -> dict[str, str]:
    """Return the device path and serial of the name Teensy."""
    teensy_info: dict[str, str] = {}

    # Initial process the device names
    device = [device.split(sep="_") for device in device_list]

    # filter and return only Teensy devices
    desired_device = [device for device in device if "Teensy" in device[0]]

    # Create the dictionary of the Teensy path and serial number
    for _i, val in enumerate(desired_device):
        teensy_info[val[-1]] = val[0].split(sep="-")[0]

    # if teensy_info == {}:
    #     loggey.error(msg="No Teensy device found")
    #     return {"0": "0"}

    return teensy_info


def get_device_path_from_serial_number() -> str:
    """Get the device path from the serial number."""
    loggey.debug(msg=f"{get_device_path_from_serial_number.__name__}()")
    # Get the serial number from the GUI
    try:
        serial_number: str = str(dpg.get_value(
            item="device_indicator"
        )).split(sep=":")[
            1
        ]
    except IndexError:
        loggey.error(
            msg=f"No serial number found |{get_device_path_from_serial_number.__name__}()"
        )
        return "/dev/ttyACM0"

    # Get the list of devices in a list of dictionaries
    devices = return_teensy(DEVICE).items()

    # Loop through the list of devices and compare to serial number
    for device in devices:
        if int(device[0]) == int(serial_number):
            device_path = device[1]
            loggey.debug(msg=f"Device path: {device_path}")

            loggey.info(
                f"Device path: {device_path} | {get_device_path_from_serial_number.__name__}()"
            )

            return device_path

    return "No Match"

TEENSY_DETAILS: dict() = return_teensy()


def compare_device_serial_to_config(serial_num: str) -> bool:
    """Compare the selected serial to the serial in the config."""
    # Get the device serial number directly from the GUI

    # Get the list of devices in a list of dictionaries
    parser, _ = read_config(file=f"{WORKING}/_configs/card_config.ini")

    # print(parser["mgtron"])

    devices = []

    try:
        devices: list[int] = [
            int(parser["mgtron"][f"card_{i}"]) for i in range(1, 9)]
    except KeyError:
        loggey.warning(msg="No serial number found")

    # Loop through the list of devices and compare to serial number
    for device in devices:
        # print(device)
        if device == int(serial_num):
            serial_number = device
            loggey.debug(
                msg=f"Serial Number: {serial_number} matched | {compare_device_serial_to_config.__name__}()"
            )

            return True

    return False

def validate_user_input(
    channel: int
):
    power_input = dpg.get_value(item=f"power_{channel}")
    band_input = dpg.get_value(item=f"bandwidth_{channel}")
    freq_input = dpg.get_value(item=f"freq_{channel}")
    is_powerValid = True
    is_bandValid = True
    is_freqValid = True
    forbidden = ["*", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "=", """/""", "-", "?", ".."]
    # Checks if user input is blank, or has invalid characters
    for invalid in forbidden:
        match power_input, invalid:
            case ("", invalid):
                dpg.set_value(item=f"power_{channel}", value="0")
            case (powerString, invalid) if invalid in powerString:
                dpg.set_value(item=f"power_{channel}", value="0")
                is_powerValid = False
        match band_input, invalid:
            case ("", invalid):
                dpg.set_value(item=f"bandwidth_{channel}", value="0")
            case (bandString, invalid) if invalid in bandString:
                dpg.set_value(item=f"bandwidth_{channel}", value="0")
                is_bandValid = False
        match freq_input, invalid:
            case ("", invalid):
                dpg.set_value(item=f"freq_{channel}", value="50")
            case (freqString, invalid) if invalid in freqString:
                dpg.set_value(item=f"freq_{channel}", value="50")
                is_freqValid = False
    # Checks if user inputs numbers past max value or below minimum value for all inputs
    match is_powerValid, int(dpg.get_value(item=f"power_{channel}")):
        case (True, value) if value > 100:
            dpg.set_value(item=f"power_{channel}", value="100")
        case (True, value) if value < 0:
            dpg.set_value(item=f"power_{channel}", value="0")
    match is_bandValid, int(dpg.get_value(item=f"bandwidth_{channel}")):
        case (True, value) if value > 100:
            dpg.set_value(item=f"bandwidth_{channel}", value="100")
        case (True, value) if value < 0:
            dpg.set_value(item=f"bandwidth_{channel}", value="0")    
    match is_freqValid, float(dpg.get_value(item=f"freq_{channel}")):
        case (True, value) if value > 6400:
            dpg.set_value(item=f"freq_{channel}", value="6400")
        case (True, value) if value < 50:
            dpg.set_value(item=f"freq_{channel}", value="50")

def callstack_helper(
    channel: int,
    freq_value: float = float(),
    pwr_value: int = int(),
    bw_value: int = int(),
):
    """Send the command to the microcontroller."""
    loggey.info(msg=f"{callstack_helper.__name__}() executed")

    dpg.bind_item_theme(
        item=f"stats_{channel}",
        theme=orng_btn_theme,  # type: ignore
    )

    loggey.info(f"Channel {channel} Information Sent")

    data_vehicle.change_power(
        channel=channel,
        power_level=convert_power(dpg.get_value(f"power_{channel}")),
        PORT=get_device_path_from_serial_number(),
    )

    data_vehicle.change_bandwidth(
        channel=channel,
        percentage=dpg.get_value(f"bandwidth_{channel}"),
        PORT=get_device_path_from_serial_number(),
    )

    data_vehicle.change_freq(
        channel=channel,
        frequency=dpg.get_value(f"freq_{channel}"),
        PORT=get_device_path_from_serial_number(),
    )

    loggey.info("Ready for next command.\n")

    # Automatically turn the indicators green after command is sent
    # if the power level is zero turn the indicator from green to grey
    [
        dpg.bind_item_theme(
            item=f"stats_{channel}",
            theme=grn_btn_theme,  # type: ignore
        )
        if dpg.get_value(f"power_{channel}")
        else dpg.bind_item_theme(
            item=f"stats_{channel}",
            theme=grey_btn_theme,  # type: ignore
        ),
    ]
    no_power()

def send_vals(sender, app_data, user_data) -> None:
    """Relational connection between GUI and Megatron class."""
    loggey.info(msg=f"{send_vals.__name__}() executed")

    match user_data:
        case 1:
            validate_user_input(channel=1)
            callstack_helper(channel=1)
        case 2:
            validate_user_input(channel=2)
            callstack_helper(channel=2)
        case 3:
            validate_user_input(channel=3)
            callstack_helper(channel=3)
        case 4:
            validate_user_input(channel=4)
            callstack_helper(channel=4)
        case 5:
            validate_user_input(channel=5)
            callstack_helper(channel=5)
        case 6:
            validate_user_input(channel=6)
            callstack_helper(channel=6)
        case 7:
            validate_user_input(channel=7)
            callstack_helper(channel=7)
        case 8:
            validate_user_input(channel=8)
            callstack_helper(channel=8)
        case _:
            loggey.warning("Unrecognized GUI report of a channel: \n")
            loggey.debug(
                f"Sender: {sender}\n"
                f"App data: {app_data}\n"
                f"User data: {user_data}\n",
            )


def reset_button(sender, app_data, user_data) -> None:
    """Reset all channel power levels to zero."""
    loggey.info("Kill All command Sent")

    [
        dpg.bind_item_theme(f"stats_{i+1}", orng_btn_theme)  # type: ignore
        for i in range(8)
    ]

    # data_vehicle.save_state(
    # state=True,
    # PORT=get_device_path_from_serial_number(),
    # )
    data_vehicle.reset_board(
        PORT=get_device_path_from_serial_number(),
    )

    [
        # Only change the Power to 0; No longer change the power level to 0
        (
            dpg.bind_item_theme(
                f"stats_{i+1}",
                grey_btn_theme),
            # type: ignore
            # dpg.set_value(item=f"power_{i+1}", value=0),
        )
        for i in range(8)
    ]

    loggey.info("Ready for next command.\n")


def send_all_channels(sender=None, app_data=None, user_data=None) -> None:
    """Send the data from all channels at once."""
    loggey.info(f"{send_all_channels.__name__}() executed")
    for i in range(1, 9):
        validate_user_input(channel=i)
    callstack_helper(channel=1)
    callstack_helper(channel=2)
    callstack_helper(channel=3)
    callstack_helper(channel=4)
    callstack_helper(channel=5)
    callstack_helper(channel=6)
    callstack_helper(channel=7)
    callstack_helper(channel=8)

    no_power()

    loggey.info("Ready for next command.\n")


def quick_save(sender, app_data, user_data) -> None:
    """Save the present inputs of the fields."""
    prelim_data: list[dict[str, dict[str, str]]] = [
        {
            f"channel {channel}": {
                "Power": dpg.get_value(f"power_{channel}"),
                "Bandwidth": dpg.get_value(f"bandwidth_{channel}"),
                "Frequency": dpg.get_value(f"freq_{channel}"),
                "Date": dt_string,
            },
        }
        for channel in range(1, 9)
    ]

    with open(file=f"{WORKING}/db/quick_save.json", mode="w") as file:
        file.write(json.dumps(obj=prelim_data, indent=2))
        loggey.info("Save Complete")


def quick_load(sender, app_data, user_data) -> None:
    """Load the last daved data."""
    saved_data: list = []
    try:
        loggey.info("Opening the quick save file: quick_save.json")
        with open(file=f"{WORKING}/db/quick_save.json") as file:
            saved_data = json.loads(file.read())
            [
                (
                    dpg.set_value(
                        item=f"power_{channel}",
                        value=saved_data[channel -
                                         1][f"channel {channel}"]["Power"],
                    ),
                    dpg.set_value(
                        item=f"bandwidth_{channel}",
                        value=saved_data[channel -
                                         1][f"channel {channel}"]["Bandwidth"],
                    ),
                    dpg.set_value(
                        item=f"freq_{channel}",
                        value=saved_data[channel -
                                         1][f"channel {channel}"]["Frequency"],
                    ),
                )
                for channel in range(1, 9)
            ]
            loggey.info("Quick load complete")

    except SystemError:
        loggey.error("No saved data found")
        return


def custom_save(sender, app_data, user_data) -> None:
    """Save config w/ a custom name."""
    loggey.debug(f"{custom_save.__name__}() executed")

    try:
        input_data = (get_save_data(),)
        # print(f"input_data: {list(input_data[0])}")
        save_to_database(input_data=list(input_data[0]))

    except (
            TypeError,
            IndexError,
            KeyError,
            AttributeError,
            ValueError,
    ):
        loggey.warning(msg=f"database failure | {custom_save.__name__}()")

    # Clear input and close input
    dpg.set_value(item="save_custom_input", value="")
    dpg.configure_item(item="modal_save", show=False)


def get_save_data() -> list[dict[str, str]]:
    """Get the save data."""
    return [
        {
            "save_name": dpg.get_value(item="save_custom_input"),
            "power": dpg.get_value(f"power_{channel}"),
            "bandwidth": dpg.get_value(f"bandwidth_{channel}"),
            "frequency": dpg.get_value(f"freq_{channel}"),
            "date": dt_string,
        }
        for channel in range(1, 9)
    ]


def custom_load(sender, app_data=None, user_data=None) -> None:
    """Load config /w a custom name."""

    loggey.info(f"{custom_load.__name__}() executed")

    loggey.debug(msg="Attempting to load custom save data")

    custom_load_to_sql: list[str] = []
    try:
        custom_load_to_sql = get_sql_save_names()
        # print(f"custom_load_to_sql: {custom_load_to_sql}")
    except sqlite3.DatabaseError:
        loggey.warning(msg="No custom save file found")
        print("No custom save file found")

    init_save_data_length = custom_load_to_sql.__len__()

    live_refresh(alias=["load", "delete"])
    loggey.info(msg=f"Sender: {sender}")
    with dpg.window(
            modal=True,
            popup=True,
            tag="modal_loaded",
            pos=(
                0,  # dpg.get_viewport_client_width() // 2 - 100,
                0,  # dpg.get_viewport_client_height() // 2 - 100,
            ),
    ):
        {
            (
                dpg.add_menu_item(
                    parent="modal_loaded",
                    label=unique,
                    tag=f"load_{itera + init_save_data_length}",
                    callback=load_chosen,
                    user_data=(unique, itera + init_save_data_length),
                ),
            )
            if sender == "custom_load_button" or sender == 210
            else (
                dpg.add_menu_item(
                    parent="modal_delete",
                    label=unique,
                    callback=delete_chosen,
                    user_data=(unique, itera + init_save_data_length),
                    tag=f"delete_{itera + init_save_data_length}",
                    show=True,
                )
            )
            for itera, unique in enumerate(custom_load_to_sql, start=0)
        }
        dpg.add_button(
            label="Close",
            parent="modal_loaded",
            tag="close_modal_loaded",
            callback=lambda: dpg.configure_item(
                item="modal_loaded", show=False),
        )


def load_chosen(
        sender=None, app_data=None, user_data: tuple[str, int] = ("", 0)
) -> None:
    """Take in the chosen file to be loaded into the input fields of the gui"""

    loggey.info(f"{load_chosen.__name__}() executed")

    _custom_load = get_sql_details(save_name=user_data[0])
    _ret_data: tuple = _custom_load
    # print(f"_ret_data: {_ret_data}")
    loggey.info(f"Loaded {_ret_data[NAME['chan_1']]}")

    [
        (
            dpg.set_value(item=f"freq_{itera}",
                          value=_ret_data[FREQ[f"chan_{itera}"]]),
            dpg.set_value(
                item=f"power_{itera}", value=_ret_data[POWS[f"chan_{itera}"]]
            ),
            dpg.set_value(
                item=f"bandwidth_{itera}", value=_ret_data[BANDS[f"chan_{itera}"]]
            ),
        )
        for itera in range(1, 9)
    ]


def delete_chosen(
        sender=None,
        app_data=None,
        user_data: tuple[str, int] = (str(), int()),
) -> None:
    """Delete a saved file."""

    # Get the list of saved objects
    _custom_load = get_sql_save_names()

    # Get primary key for every name in the database matching the chosen name
    if user_data[0] in _custom_load:
        # Delete the chosen name and data from the database
        loggey.info(f"Deleting {user_data[0]} | {delete_chosen.__name__}()")
        delete_sql_save_data(save_name=user_data[0])

    loggey.info(
        f"Live update of delete and load menu items complete\
            | {delete_chosen.__name__}()"
    )


def auto_fill_freq(
        sender=None,
        app_data=None,
        user_data=None,
        freq_val: float = 0.0,
        freq_constant: float = 5.0,
) -> None:
    """Auto fill the frequency column based on the first input."""

    [
        dpg.set_value(
            item=f"freq_{i}",
            value=(
                abs(
                    float(dpg.get_value(f"freq_{i-2}"))
                    - float(dpg.get_value(f"freq_{i-1}"))
                )
                + float(dpg.get_value(f"freq_{i-1}"))
            )
            if float(dpg.get_value(item=f"freq_{i}")) <= 6400
            else 6400.00,
        )
        for i in range(3, 9)
        if not freq_constant
    ]

    [
        dpg.set_value(
            item=f"freq_{i}",
            value=freq_val + freq_constant * (i - 1)
        )
        for i in range(1, 9)
        if freq_constant
    ]


def auto_fill_power() -> None:
    """Auto fill the power column based on the first input."""

    power_1 = dpg.get_value(item="power_1")

    # Ensure power_1 is greater than 0 and less than 100
    if int(power_1) <= 0:
        power_1 = 0
    elif int(power_1) >= 100:
        power_1 = 100

    [
        dpg.set_value(item=f"power_{i}", value=power_1)
        for i in range(1, 9)
    ]


def auto_fill_bandwidth() -> None:
    """Auto fill the bandwidth column based on the first input."""

    bandwidth_1 = dpg.get_value(item="bandwidth_1")

    # Ensure bandwidth_1 is greater than 0 and less than 100
    if int(bandwidth_1) <= 0:
        bandwidth_1 = 0
    elif int(bandwidth_1) >= 100:
        bandwidth_1 = 100

    [
        dpg.set_value(
            item=f"bandwidth_{i}",
            value=bandwidth_1,
        )
        for i in range(1, 9)
    ]


def change_inputs(sender, app_data, user_data) -> None:
    """Use the mouse wheel to change the field inputs."""
    loggey.info(f"app data: {app_data}")

    if dpg.is_item_focused(item="power_1"):
        loggey.debug(dpg.get_value("power_1"))


def read_config(file: str) -> tuple[configparser.ConfigParser, list[str]]:
    """Read the config file and return the contents."""
    devices = DEVICE
    parser = configparser.ConfigParser()
    parser.read(filenames=file, encoding="utf-8")
    loggey.info(msg=f"file {file} read | {read_config.__name__}()")

    return parser, devices


def auto_send(sender, app_data, user_data) -> None:
    """Set a flag to indicate when mission buttons should auto send"""

    loggey.debug(msg=f"{auto_send.__name__}()")

    # Set the button to green
    dpg.bind_item_theme(
        theme=grn_btn_theme if not dpg.get_item_theme(
            item=sender) == grn_btn_theme else None,
        item=sender,
    )

    global AUTO_SEND_FLAG

    # Set the flag
    AUTO_SEND_FLAG = True if dpg.get_item_theme(
        item=sender) == grn_btn_theme else False

    loggey.debug(msg=f"Auto send flag: {AUTO_SEND_FLAG}")


def mission(sender, app_data, user_data) -> None:
    """Mission alpha user facing button configuration."""
    name = sender.split("\n")[0].lower()

    # print(f"tag name: {dpg.get_item_configuration(item=sender)['label']}")

    label_name = dpg.get_item_configuration(item=sender)['label']

    # Capture only the first part of the button name
    loggey.info(msg="{}() executed".format(sender.split("\n")[0]))

    # Check against the database for the name of the config button as the name
    # of the saved config
    input_vals: dict[str, list] = check_and_load_config(button_name=label_name)

    try:
        # Check if the config file exists and if it does, read it
        parser, _ = read_config(
            file=f"{WORKING}/_configs/{mission.__name__ + '_' + name}.ini"
        )

        [
            (
                dpg.set_value(
                    item=f"freq_{config}",
                    value=float(parser["freq"][f"freq_{config}"])
                    if not input_vals
                    else input_vals["freq"][config - 1],
                ),
                dpg.set_value(
                    item=f"power_{config}",
                    value=int(parser["power"][f"power_{config}"])
                    if not input_vals
                    else input_vals["power"][config - 1],
                ),
                dpg.set_value(
                    item=f"bandwidth_{config}",
                    value=int(
                        parser["bandwidth"][f"bw_{config}"]
                        if not input_vals
                        else input_vals["bw"][config - 1]
                    ),
                ),
            )
            for config in range(1, 9)
        ]

        loggey.debug(msg="Send all flag checking")

        global AUTO_SEND_FLAG

        # If SEND_AUTO_FLAG then SEND_ALL
        if AUTO_SEND_FLAG:
            loggey.info(msg=f"auto send flag: {AUTO_SEND_FLAG}")
            send_all_channels()
        else:
            loggey.info(msg=f"auto send flag: {AUTO_SEND_FLAG}")

    except (KeyError, SystemError, NameError) as e:
        loggey.warning(msg=f"Error: {e}")


def kill_channel(sender, app_data, user_data: int) -> None:
    """Kill channel w/out resetting power on user facing screen."""
    data_vehicle.change_power(
        channel=user_data,
        power_level=0,
        PORT=get_device_path_from_serial_number(),
    )

    dpg.bind_item_theme(
        item=f"stats_{user_data}",
        theme=grey_btn_theme)  # type: ignore


def device_finder(sender=None, app_data=None, user_data: int = int()) -> None:
    """Filter all connected devices and present only Teensy devices."""
    loggey.info(msg=f"{device_finder.__name__}() executed")
    teensy_info: dict[str, str] = {}

    # Initial process the device names
    device = [device.split(sep="_") for device in device_names()]

    # filter and return only Teensy devices
    desired_device = [device for device in device if "Teensy" in device[0]]
    loggey.info(msg=f"Devices filtered check: {desired_device} | {device_names.__name__}")

    # Create the dictionary of the Teensy path and serial number
    for _i, val in enumerate(desired_device):
        teensy_info[val[-1]] = val[0].split(sep="-")[0]
    loggey.info(msg=f"Teensy info: {teensy_info} | {device_names.__name__}")
    # Can only choose a 'Teensy' device
    for _i, dev in enumerate(teensy_info, start=1):
        # * Source of truth for chosen device
        if user_data == dev:
            # Set the device indicator to the chosen device
            dpg.set_value(
                item="device_indicator",
                value=f"Device:{dev}",
            )

            # Disappear the menu after choosing a device
            dpg.configure_item(item="modal_device_config", show=False)

            # Turn the card select button green when you switch devices
            # and turn the other buttons blue
            (
                dpg.bind_item_theme(
                    item=f"card_{_i}", theme=grn_btn_theme  # type: ignore
                ),
                [
                    dpg.bind_item_theme(
                        # type: ignore
                        item=f"card_{_j}",
                        theme=blue_btn_theme,  # type: ignore
                    )
                    for _j, _ in enumerate(dev, start=1)
                    if _j != _i and dpg.does_item_exist(item=f"card_{_j}")
                ],
            ) if compare_device_serial_to_config(
                serial_num=str(
                    dpg.get_value(
                        item="device_indicator")).split(
                    sep=":")[1]
            ) else dpg.bind_item_theme(
                # Theoretically, this should never happen
                item=f"card_{_i}",
                theme=grey_btn_theme,  # type: ignore
            )

    device_refresh()
    return desired_device


def populate_right_side_buttons() -> list[bool]:
    """Detect if up to eight Teensy devices are connected."""

    # Get the number of connected devices
    num_devices = device_finder().__len__()

    match num_devices:
        # If there are less than 1 device connected, return False
        case x if x < 1:
            return [False]

        # If there are more than 8 devices connected, return True
        # case x if x > 8:
            # return [True]

        # If there are less than 8 devices connected, populate the buttons
        case _:
            # Return true for each device connected and false until 8
            truth = [True] * num_devices
            false = [False] * (8 - len(truth))

            # Append the false values to the truth values
            truth.extend(false)
            print(len(truth))

            # Return the list of booleans
            return truth


def device_refresh(sender=None, app_data=None, user_data=None) -> None:
    """Update the present status of the card."""

    card_stats = get_card_status()

    for i in range(1, 9):
        try:
            if str(
                    dpg.get_value(item=f"power_{i}"),
            ) != str(card_stats["power"][i - 1]):
                dpg.set_value(
                    item=f"power_{i}",
                    value=rev_convert_power(int(card_stats["power"][i - 1])),
                )
                dpg.bind_item_theme(item=f"stats_{i}", theme=grey_btn_theme) if str(
                    dpg.get_value(item=f"power_{i}")
                ) == "0" else dpg.bind_item_theme(
                    item=f"stats_{i}", theme=grn_btn_theme
                )  # type: ignore

            if str(
                    dpg.get_value(item=f"freq_{i}"),
            ) != str(card_stats["freq"][i - 1]):
                dpg.set_value(
                    item=f"freq_{i}",
                    value=float(card_stats["freq"][i - 1]),
                )

            if str(
                    dpg.get_value(item=f"bandwidth_{i}"),
            ) != str(card_stats["bw"][i - 1]):
                dpg.set_value(
                    item=f"bandwidth_{i}",
                    value=int(card_stats["bw"][i - 1]),
                )

        except IndexError:
            loggey.warning(msg=f"Index error in {device_refresh.__name__}()")
            dpg.set_value(item=f"power_{i}", value="")
            dpg.set_value(item=f"freq_{i}", value="")
            dpg.set_value(item=f"bandwidth_{i}", value="")
            dpg.bind_item_theme(
                item=f"stats_{i}",
                theme=grey_btn_theme)  # type: ignore


def fill_config():
    """Automatically fill the config file with devices detected."""

    parser, devices = read_config(file=f"{WORKING}/_configs/card_config.ini")
    devices = TEENSY_DETAILS
    serial_list= list(devices.keys())
    loggey.info(msg="Populating config file with detected devices")
    loggey.info(msg=f"Devices: {devices}")
    loggey.info(msg=f"length of device: {len(devices)}")
    [
        serial_list.append(str(0)) for _ in range(8 - len(serial_list))
    ]
    try:

        # Ensure eight spots in the config file are filled in if there are
        # not eight devices
        # {
        #     "0": "0" for i in range(8 - len(devices))
        # }
        loggey.info(msg=(devices))
        # Automatically fill in an empty config file
        # parser["mgtron"] = {
        #     f"card_{i+1}": str(dev.split(sep="_")[-1]) 
        #     for i, dev in enumerate(devices) if len(
        #         str(dev.split(sep="_")[-1])
        #     ) <= 8 
        # }
        parser["mgtron"] = {
        f"card_{i+1}": str(dev.split(sep="_")[-1]) if len(
            str(dev.split(sep="_")[-1])) <= 8 else str(0)
        for i, dev in enumerate(serial_list)
        }
    
        with open(
                file=f"{WORKING}/_configs/card_config.ini",
                mode="w"
        ) as config_file:
            parser.write(config_file)
            loggey.info(msg="Config file has been automatically filled")

    except (KeyError, IndexError):
        loggey.warning(msg="Config file error")
        with open(
                file=f"{WORKING}/_configs/card_config.ini",
                mode="w"
        ) as config_file:
            config_file.write("[mgtron]\n")
            config_file.write("card_1=\n")
            fill_config()


def config_intake() -> None:
    """Read a config file and assign card buttons."""

    parser, devices = read_config(file=f"{WORKING}/_configs/card_config.ini")

    if len(devices) > 1:
        try:
            for dev_count, _ in enumerate(parser["mgtron"], start=1):
                for _, card in enumerate(devices):
                    match card.split(sep="_")[-1] == parser["mgtron"][
                        f"card_{dev_count}"
                    ]:
                        case True if len(card) > 1:
                            dpg.bind_item_theme(
                                item=f"card_{dev_count}",
                                theme=blue_btn_theme,  # type: ignore
                            )
                            dpg.configure_item(
                                item=f"card_{dev_count}", enabled=True)
                            loggey.debug(
                                f"{card} is assigned to {parser['mgtron'][f'card_{dev_count}']}"
                            )
                        case False if len(card) == 1:
                            loggey.info(
                                msg=f"No device filled in on this line {platform.machine()} | {config_intake.__name__}"
                            )
                        case False:
                            loggey.warning(
                                msg=f"Device ID not detected in order OR not at all on {platform.machine()} | {config_intake.__name__}"
                            )
        except (KeyError, SystemError):
            loggey.warning(
                msg=f"No config file error | {config_intake.__name__}")


def find_signals_and_frequencies() -> dict[int, float]:
    """Use the linux host to scan for wifi signals and frequencies."""

    output: subprocess.CompletedProcess = subprocess.run(
        [
            "nmcli",
            "-g",
            "FREQ",
            "-c",
            "no",
            "dev",
            "wifi",
            "list",
            "--rescan",
            "yes",
        ],
        capture_output=True,
        encoding="utf-8",
    )

    output_2: subprocess.CompletedProcess = subprocess.run(
        [
            "nmcli",
            "-g",
            "SIGNAL",
            "-c",
            "no",
            "dev",
            "wifi",
            "list",
        ],
        capture_output=True,
        encoding="utf-8",
    )

    signal_column: set[str] = set(output_2.stdout.split(sep="\n"))

    freq_column: set[str] = set(output.stdout.split(sep="\n"))

    matched_sigs_and_freqs: dict[int, float] = {
        int(sig): float(freq.strip("MHz"))
        for sig, freq in zip(signal_column, freq_column)
        if sig != "" and freq != ""
    }

    # Sort the dictionary by the signal strength
    matched_sigs_and_freqs = dict(
        sorted(
            matched_sigs_and_freqs.items(),
            key=lambda item: item[0],
            reverse=True)
    )

    # print the ordered dictionary
    print(
        f"All matches: {matched_sigs_and_freqs}\nnumber of matches: {len(matched_sigs_and_freqs)}"
    )

    loggey.info(
        msg=f"Freq and Strength: {matched_sigs_and_freqs} | {find_signals_and_frequencies.__name__}"
    )

    # reduce the dictionary to the top 8 strongest signals
    matched_sigs_and_freqs = dict(
        itertools.islice(
            matched_sigs_and_freqs.items(), 8))

    # if the dictionry is not eight items long, fill it with zeros
    if len(matched_sigs_and_freqs) < 8:
        [
            matched_sigs_and_freqs.update({1 + i: 50}) for i in range(8 - len(matched_sigs_and_freqs))
        ]
        loggey.warning(
            msg=f"Dictionary is not eight items long | {find_signals_and_frequencies.__name__}"
        )

    return matched_sigs_and_freqs


def find_bluetooth_and_frequencies() -> bool:
    """Use the linux host to scan for bluetooth signals and frequencies."""
    # send the command: bluetootctl scan on
    subprocess.run(
        ["bluetoothctl", "scan", "on"],
        capture_output=True,
        encoding="utf-8",
    )

    output: subprocess.CompletedProcess = subprocess.run(
        [
            "bluetoothctl",
            "scan",
            "on",
        ],
        capture_output=True,
        encoding="utf-8",
    )

    hardware_column: set[str] = set(output.stdout.split(sep="\n"))

    hardware_ids = {
        int(hardware.split(sep=" ")[0]): int(hardware.split(sep=" ")[-1])
        for hardware in hardware_column
        if hardware != ""
    }

    # print the ordered dictionary
    print(f"hardware_ids: {hardware_ids}")

    loggey.info(
        msg=f"Freq and Strength: {hardware_ids} | {find_bluetooth_and_frequencies.__name__}"
    )

    return len(hardware_ids) > 0


def card_config(card_number: int = int()) -> None:
    """Read the config file and set the values in the GUI."""
    try:
        parser, _ = read_config(
            file=f"{WORKING}/_configs/card_{card_number}.ini")

        [
            (
                dpg.set_value(
                    item=f"freq_{config}", value=float(parser["freq"][f"freq_{config}"])
                ),
                dpg.set_value(
                    item=f"power_{config}",
                    value=int(parser["power"][f"power_{config}"]),
                ),
                dpg.set_value(
                    item=f"bandwidth_{config}",
                    value=float(parser["bandwidth"][f"bw_{config}"]),
                ),
            )
            for config in range(1, 9)
        ]

    except KeyError:
        loggey.warning(
            msg="Error in reading the config file OR config file does not exist"
        )

    except SystemError:
        loggey.warning(msg="Invalid data type;  Expected floating point value")


def card_selection(sender=None, app_data=None, user_data: int = int()) -> None:
    """Load the selected cards prefix when selected."""

    parser, _ = read_config(file=f"{WORKING}/_configs/card_config.ini")

    loggey.info(msg=f"selected card: {user_data} | {card_selection.__name__}")
    loggey.info(msg=parser["mgtron"][f"card_{user_data}"])

    # Manipulate the set to accomplish a loop without the currently selected
    # button
    card_list: set[int] = {1, 2, 3, 4, 5, 6, 7, 8}
    match user_data:
        case 1:
            dpg.bind_item_theme(
                item=f"card_{user_data}", theme=grn_btn_theme  # type: ignore
            )
            dpg.set_value(
                item="device_indicator",
                value=f"Device:{parser['mgtron']['card_1']}"
            )
            try:
                device_finder(user_data=int(parser["mgtron"]["card_1"]))
            except ValueError:
                loggey.error(msg="No devices detected")
                dpg.bind_item_theme(
                    item=f"card_{user_data}", theme=red_btn_theme
                )
                return

            # Blue all other active card buttons and make this one green when
            # clicked
            card_list.remove(1)

            # Turn only this button blue
            try:
                [
                    dpg.bind_item_theme(
                        item=f"card_{greyed_card}",
                        theme=blue_btn_theme,  # type: ignore
                    )
                    for greyed_card in card_list
                ]
            except SystemError:
                loggey.warning(msg="Other cards not found")
                return

            # card_config(card_number=1)
            loggey.info(
                msg=f"Card 1 config loaded | {card_selection.__name__}")

        case 2:
            dpg.bind_item_theme(
                item=f"card_{user_data}", theme=grn_btn_theme  # type: ignore
            )
            dpg.set_value(
                item="device_indicator", value=f"Device:{parser['mgtron']['card_2']}"
            )
            device_finder(user_data=int(parser["mgtron"]["card_2"]))

            card_list.remove(2)

            try:
                [
                    dpg.bind_item_theme(
                        item=f"card_{greyed_card}",
                        theme=blue_btn_theme,  # type: ignore
                    )
                    for greyed_card in card_list
                ]

            except SystemError:
                loggey.warning(msg="Other cards not found")
                return

            # card_config(card_number=2)
            loggey.info(
                msg=f"Card 2 config loaded | {card_selection.__name__}")

        case 3:
            card_list.remove(3)
            dpg.bind_item_theme(
                item=f"card_{user_data}", theme=grn_btn_theme  # type: ignore
            )
            dpg.set_value(
                item="device_indicator", value=f"Device:{parser['mgtron']['card_3']}"
            )
            device_finder(user_data=int(parser["mgtron"]["card_3"]))

            try:
                [
                    dpg.bind_item_theme(
                        item=f"card_{greyed_card}",
                        theme=blue_btn_theme,  # type: ignore
                    )
                    for greyed_card in card_list
                ]
            except SystemError:
                loggey.warning(msg="Other cards not found")
                return

            # card_config(card_number=3)
            loggey.info(
                msg=f"Card 3 config loaded | {card_selection.__name__}")

        case 4:
            card_list.remove(4)
            dpg.bind_item_theme(
                item=f"card_{user_data}", theme=grn_btn_theme  # type: ignore
            )
            dpg.set_value(
                item="device_indicator", value=f"Device:{parser['mgtron']['card_4']}"
            )
            device_finder(user_data=int(parser["mgtron"]["card_4"]))

            try:
                [
                    dpg.bind_item_theme(
                        item=f"card_{greyed_card}",
                        theme=blue_btn_theme,  # type: ignore
                    )
                    for greyed_card in card_list
                ]
            except SystemError:
                loggey.warning(msg="Other cards not found")
                return

            # card_config(card_number=4)
            loggey.info(
                msg=f"Card 4 config loaded | {card_selection.__name__}")

        case 5:
            card_list.remove(5)
            dpg.bind_item_theme(
                item=f"card_{user_data}", theme=grn_btn_theme  # type: ignore
            )
            dpg.set_value(
                item="device_indicator", value=f"Device:{parser['mgtron']['card_4']}"
            )
            device_finder(user_data=int(parser["mgtron"]["card_4"]))

            try:
                [
                    dpg.bind_item_theme(
                        item=f"card_{greyed_card}",
                        theme=blue_btn_theme,  # type: ignore
                    )
                    for greyed_card in card_list
                ]
            except SystemError:
                loggey.warning(msg="Other cards not found")
                return

            # card_config(card_number=5)
            loggey.info(
                msg=f"Card 5 config loaded | {card_selection.__name__}")

        case 6:
            card_list.remove(6)
            dpg.bind_item_theme(
                item=f"card_{user_data}", theme=grn_btn_theme  # type: ignore
            )
            dpg.set_value(
                item="device_indicator", value=f"Device:{parser['mgtron']['card_6']}"
            )
            device_finder(user_data=int(parser["mgtron"]["card_6"]))

            try:
                [
                    dpg.bind_item_theme(
                        item=f"card_{greyed_card}",
                        theme=blue_btn_theme,  # type: ignore
                    )
                    for greyed_card in card_list
                ]
            except SystemError:
                loggey.warning(msg="Other cards not found")
                return

            # card_config(card_number=6)
            loggey.info(
                msg=f"Card 6 config loaded | {card_selection.__name__}")

        case 7:
            card_list.remove(7)
            dpg.bind_item_theme(
                item=f"card_{user_data}", theme=grn_btn_theme  # type: ignore
            )
            dpg.set_value(
                item="device_indicator", value=f"Device:{parser['mgtron']['card_7']}"
            )
            device_finder(user_data=int(parser["mgtron"]["card_7"]))

            try:
                [
                    dpg.bind_item_theme(
                        item=f"card_{greyed_card}",
                        theme=blue_btn_theme,  # type: ignore
                    )
                    for greyed_card in card_list
                ]
            except SystemError:
                loggey.warning(msg="Other cards not found")
                return

            # card_config(card_number=7)
            loggey.info(
                msg=f"Card 7 config loaded | {card_selection.__name__}")

        case 8:
            card_list.remove(8)
            dpg.bind_item_theme(
                item=f"card_{user_data}", theme=grn_btn_theme  # type: ignore
            )
            dpg.set_value(
                item="device_indicator", value=f"Device:{parser['mgtron']['card_8']}"
            )
            device_finder(user_data=int(parser["mgtron"]["card_8"]))

            try:
                [
                    dpg.bind_item_theme(
                        item=f"card_{greyed_card}",
                        theme=blue_btn_theme,  # type: ignore
                    )
                    for greyed_card in card_list
                ]
            except SystemError:
                loggey.warning(msg="Other cards not found")
                return

            # card_config(card_number=8)
            loggey.info(
                msg=f"Card 8 config loaded | {card_selection.__name__}")

        case _:
            loggey.warning(msg=f"No card selected: {user_data}")
        # card_l
        #           try:ist.remove(user_data)

            try:
                [
                    dpg.bind_item_theme(
                        item=f"card_{greyed_card}",
                        theme=blue_btn_theme,  # type: ignore
                    )
                    for greyed_card in card_list
                ]
                loggey.error(
                    msg=f"No card data loaded | {card_selection.__name__}")
            except SystemError:
                loggey.warning(msg="Other cards not found")
                return


def wifi_scan_jam(sender, app_data, user_data) -> None:
    """Scan the local wifi channels and jam them."""
    loggey.info(msg="Scan jammer method called")

    dpg.configure_item(item=sender, label="SCANNING...")
    dpg.bind_item_theme(item=sender, theme=red_btn_theme)  # type: ignore

    loggey.info(msg="SCANNING...")
    freq_and_strength: dict[int, float] = find_signals_and_frequencies()

    loggey.warning(msg=f"Freq & Strength sorted: {freq_and_strength}")

    [
        (
            dpg.set_value(
                item=f"freq_{i}", value=float(freq) if isinstance(
                    freq, float
                ) else 50.0
            ),
            dpg.set_value(
                item=f"power_{i}",
                value=100 if int(freq) != 50 else 0),
            dpg.set_value(
                item=f"bandwidth_{i}",
                value=10 if int(freq) != 50 else 0),
            loggey.debug(  # type: ignore
                msg=f"Frequency, in sig strength order, discovered: {freq}"
            ),
            # Automatically send the command to the MGTron board
        )
        for i, freq in enumerate(freq_and_strength.values(), start=1)
    ]

    # # Stop looping scan jam if 'KILL ALL' is pressed and hovered over
    # if dpg.is_item_focused(test
    #         item="Stop_all_channels"):

    # Change the button back to blue
    dpg.bind_item_theme(
        item=sender,
        theme=blue_btn_theme,  # type: ignore
    )

    # Change the button text back to normal
    dpg.configure_item(
        item=sender,
        label="WIFI",
    )

    loggey.debug(msg="Scan jammer method finished")


def bluetooth_scan_jam(sender, app_data, user_data) -> None:
    """Scan the local bluetooth channels and jam them."""
    loggey.info(msg="Scan jammer method called")

    # Conditional lgic to determine if the scan is in progress
    if dpg.get_item_theme(item=sender) == orng_btn_theme:
        dpg.bind_item_theme(
            item=sender,
            theme=blue_btn_theme,  # type: ignore
        )
        dpg.configure_item(
            item=sender,
            label="  BLUETOOTH\n   SCAN",
        )
        loggey.debug(msg="Bluetooth scan button disabled")

        # Delete the open bluetooth scan window
        dpg.delete_item(item=12)

    else:
        dpg.bind_item_theme(
            item=sender,
            theme=orng_btn_theme,  # type: ignore
        )
        dpg.configure_item(
            item=sender,
            label="  CLOSE\n  BLUETOOTH\n   SCAN",
        )
        loggey.debug(msg="Bluetooth scan button enabled")

        with dpg.window(
            tag=12,
            no_scrollbar=True,
            no_collapse=True,
            no_resize=True,
            no_title_bar=True,
            no_move=True,
            pos=(0, 0),
            width=880,
            height=735,
        ):
            with dpg.child_window(
                tag="ble_labels",
                pos=(0, 0),
                width=880,
                height=715,
            ):
                dpg.add_text(
                    default_value=" " * 10 + "MAC" + " " * 5 + "|" + " " * 3 +
                    "MANUFACTURER" + " " * 3 + "|" + " " +
                    "RSSI" + " " * 1 + "|" + " " * 12 + "DATE",
                    label="BLUETOOTH LIST",
                )
                dpg.add_text(
                    default_value='-'*89
                )

            with dpg.child_window(
                tag="ble_list",
                no_scrollbar=True,
                pos=(0, 60),
                width=880,
                height=680,
            ):

                company = True

                # Get the BLE information and print to GUI

                all_data: dict = ble_data_complete()
                for i, macs in enumerate(all_data.keys(), start=1):

                    dpg.add_text(
                        default_value=f"{i}. {macs} | {all_data[macs][0]} | {all_data[macs][1]} | {datetime.now().strftime('%H:%M:%S')}"
                    )
                    dpg.add_text(
                        default_value='-' * 78
                    )

        no_power()


def neighborhood_list(sender, app_data, user_data) -> None:
    """Mission celluar neighborhood list facing button config."""
    [
        (
            dpg.set_value(item=f"freq_{i}", value=float(freq)),
            dpg.set_value(item=f"power_{i}", value=40),
            dpg.set_value(item=f"bandwidth_{i}", value=100),
            loggey.debug(  # type: ignore
                msg=f"Frequency, in sig strength order, discovered: {freq}"
            ),
            # recently filled fields
        )
        for i, freq in enumerate(
            sorted(
                EG25G.earfcn_frequencies,  # type: ignore
            ),
            start=1,
        )
    ]


def get_card_status() -> dict[str, list]:
    """Grab the status of the card
    so the GUI has an idea of the state of the card."""

    card_data: dict[str, list] = {}

    # Get the path of the presently selected device
    path = get_device_path_from_serial_number()

    # print(f"Path: {path} | {get_card_status.__name__}")

    try:
        data_vehicle.status(
            PORT=str(path),
        )

        data = format_output(PORT=path)

        loggey.debug(msg=f"raw card status: {data}")

        # Get the channel, frequency, power, and bandwidth
        channel: list[int] = [int(i) for i in data["channel"]]
        frequency: list[float] = [float(i) for i in data["freq"]]
        power: list[float] = [float(i) for i in data["power"]]
        bandwidth: list[float] = [float(i) for i in data["bandwidth"]]

    except IndexError:
        loggey.warning(msg=f"{get_card_status.__name__} failed")
        # Log the line number
        loggey.error(
            # type: ignore
            msg=f"Line number: {sys.exc_info()[-1].tb_lineno} - No device found"
        )

        return card_data

    # if not channel:

    card_data["channel"] = channel
    card_data["freq"] = frequency
    card_data["power"] = power
    card_data["bw"] = bandwidth

    return card_data


loggey.debug(msg="EOF")


def reset_status_text(channel: int) -> None:
    """Remove the text above the input fields."""
    # Reset the text above the input after every send command
    dpg.configure_item(item=f"power_{channel}_indicator", show=False)
    dpg.configure_item(item=f"frequency_{channel}_indicator", show=False)
    dpg.configure_item(item=f"bandwidth_{channel}_indicator", show=False)


def db_error(sender=None, app_data=None, user_data=None) -> None:
    """Display a modal popup with the error message."""


def check_and_load_config(button_name: str) -> dict[str, list]:
    """Check database for config button as the name of the saved config."""
    loggey.debug(msg=f"{check_and_load_config}()")
    config_data: dict[str, list] = {}

    # Check the sql database for the name of the button
    save_names = get_sql_save_names()

    # Remove new lines and rejoin sentence; this is ! robust
    button_name = button_name.replace("  ", " ").replace("\n", "")

    loggey.info(f"DB names: {save_names}")
    loggey.info(f"Button name: '{button_name}'")

    if button_name in save_names:
        loggey.debug(f"Button name: {button_name} found in DB")

        # Get the config from the database
        config = get_sql_details(save_name=button_name)

        loggey.debug(config)

        # Get the channel, frequency, power, and bandwidth
        channel: list[int] = [int(i) for i in range(1, 9)]
        frequency: list[float] = [
            float(config[FREQ[
                f"chan_{i}"]]) for i, _ in enumerate(FREQ, start=1)
        ]
        power: list[int] = [
            int(config[POWS[
                f"chan_{i}"]]) for i, _ in enumerate(POWS, start=1)
        ]
        bandwidth: list[int] = [
            int(config[BANDS[
                f"chan_{i}"]]) for i, _ in enumerate(BANDS, start=1)
        ]

        # Store the config in a dictionary
        config_data: dict[str, list] = {
            "channel": channel,
            "freq": frequency,
            "power": power,
            "bw": bandwidth,
        }

    return config_data


def convert_power(power: int) -> int:
    """Map the input from 0 to 100 and convert to 0 to 63."""
    loggey.debug(msg=f"{convert_power.__name__}()")

    loggey.info(msg=f"Power prior to conversion: {power}")
    # Map the input from 0 to 100 and convert to 0 to 63
    try:
        power = int(
            round(
                map_range(
                    x=int(power),
                    in_min=0,
                    in_max=100,
                    out_min=0,
                    out_max=63,
                ),
            ),
        )
    except ValueError:
        loggey.warning(msg=f"{convert_power.__name__} failed")
        # Log the line number
        loggey.error(
            # type: ignore
            msg=f"Line number: {sys.exc_info()[-1].tb_lineno} - No input found"
        )

        return 0

    loggey.info(msg=f"Power after conversion: {power}")

    # Limit the power to 63
    if power > 63:
        power = 63

    return power


def rev_convert_power(power: int) -> int:
    """Map the input from 0 to 63 and convert to 0 to 100"""

    loggey.debug(msg=f"{rev_convert_power.__name__}()")

    loggey.info(msg=f"Power prior to conversion: {power}")

    # Map the input from 0 to 63 and convert to 0 to 100
    power = int(
        round(
            map_range(
                x=int(power),
                in_min=0,
                in_max=63,
                out_min=0,
                out_max=100,
            ),
        ),
    )

    loggey.info(msg=f"Power after conversion: {power}")

    return power


def map_range(
    x: int,
    in_min: int,
    in_max: int,
    out_min: int,
    out_max: int,
) -> float:
    """Map the input from 0 to 100 and convert to 0 to 63"""

    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def change_card_name(sender, app_data, user_data) -> None:
    """Change the name of the card select button that is currently selected."""

    # Parse the sender to get the card select button
    # by splitting the sender string on the underscore
    card_select_button = sender.split("_")[1]

    card_item = f"card_{card_select_button}"

    # If user selected name is too long, add a new line

    len_cap = 6
    max_cap = 10

    if len(app_data) > len_cap:
        app_data = app_data[:len_cap] + "\n" + app_data[len_cap:]

    # Truncate the name if it is too long
    if len(app_data) > max_cap:
        app_data = app_data[:max_cap]

    # Change the name of the card select button
    dpg.configure_item(item=card_item, label=app_data)


def save_init():
    """Saves the current config to the init file"""

    loggey.debug(msg="Saving init file")

    dpg.save_init_file("dpg.ini")


def live_refresh(alias: list[str]):
    """For as many aliases passed in, remove the alias from the dpg registry"""

    loggey.debug(msg=f"{live_refresh.__name__}()")

    for i in dpg.get_aliases():
        for j in alias:
            if i.__contains__(j):
                dpg.remove_alias(alias=i)
                loggey.debug(f"Removed alias: {i}")
                loggey.debug(msg=f"Removed alias: {i}")


def connect_device(sender, app_data, user_data) -> None:
    """Connect to the device and send the config to the GUI"""

    try:
        # Grab the list of Teensy devices connected
        devices: dict[str, str] = return_teensy(DEVICE)

        if len(devices) == 1:
            dpg.add_menu_item(
                parent="modal_device_config",
                label=f"{devices.popitem()[0].upper()}",
            )

        elif len(devices) > 1:
            [
                (
                    dpg.configure_item(
                        item="modal_device_config",
                        children=[
                            dpg.add_menu_item(
                                parent="modal_device_config",
                                label=f"{device.upper()}",
                                callback=device_finder,
                                user_data=device,
                            )
                        ],
                    )
                    # dpg.add_menu_item(
                    #     parent="modal_device_config",
                    #     label=f"{device.upper()}",
                    #     callback=device_finder,
                    #     user_data=device,
                    # )
                )
                for device in devices
            ]
        else:
            pass  # Error handled elsewhere

    except (TypeError, NameError, KeyError, SystemError, ValueError):
        dpg.add_menu_item(
            parent="choose_device",
            label="DEVICE NUMBER: NOT FOUND",
            callback=lambda: dpg.configure_item(
                item="modal_device_config", show=False),
        )
        loggey.error(msg="No device detected")

        [
            dpg.bind_item_theme(
                item=f"stats_{channel}",
                theme=red_btn_theme,  # type: ignore
            )
            for channel in range(1, 9)
        ]
        dpg.add_text(
            parent="device_config",
            tag="device_indicator",
            default_value="",
            pos=(5, 35),
        )


def no_power():
    """If the power input field is 0 then turn the stats indicator grey."""
    # loggey.debug(msg=f"{no_power.__name__}()")

    current_power = [
        str(dpg.get_value(item=f"power_{i}")) for i in range(1, 9)]

    # print(current_power)

    for i in range(1, 9):
        dpg.bind_item_theme(
            item=f"stats_{i}",
            theme=grey_btn_theme,  # type: ignore
        ) if current_power[i - 1].isdigit() and current_power[i - 1] == "0" else None
        # dpg.bind_item_theme(
        #     item=f"stats_{i}",
        #     theme=grn_btn_theme,  # type: ignore
        # )  # if dpg.get_item_theme(item=f"stats_{i}") != red_btn_theme else None


def numpad(sender, app_data, user_data):
    """Open the numpad for the power input field"""

    loggey.debug(msg=f"{numpad.__name__}()")
    loggey.debug(msg=f"Sender: {sender}")

    if dpg.is_item_focused(item="freq_1") and dpg.is_item_hovered(
        item="freq_1"
    ):

        # Open the numpad
        with dpg.window(
            modal=True,
                pos=(100, 100),
                parent=sender,
                tag="numpad",
                label="NUMPAD",
                show=True,
                width=200,
                height=300,
        ):

            dpg.add_text(
                default_value="Enter Power",
                parent="numpad",
                tag="numpad_text",
                pos=(5, 5),
            )

        # Grab the number from the numpad


def ble_rs(target: str):
    """Call the BLE RS API and return the data."""
    loggey.debug(msg=f"{ble_rs.__name__}()")

    port = 8080

    # Grab the target from the API
    try:
        data = requests.get(
            url=f"http://localhost:{port}/{target}",
            headers={"Content-Type": "application/json"},
        )

        if data.status_code != 200:
            loggey.error(msg=f"BLE API returned {data.status_code}")
            return {}

        loggey.info(msg=f"BLE API raw response: {data}")

        # Convert the data to a dict
        data = data.json()

        # Convert the dict to a list
        # data = list(data)

        # Return the data
        return data

    except requests.exceptions.ConnectionError:
        loggey.error(msg="BLE API not running")
        return {}


def ble_data(company: bool) -> tuple:
    """Collate the da from the BLE API and return it."""
    loggey.debug(msg=f"{ble_data.__name__}()")

    target: tuple[str, str] = "rssi", "company"

    # Grab the data from the API
    data = ble_rs(target=target[0]) if not company else ble_rs(target=target[1])

    loggey.info(msg=data)

    # If the data is empty, return an empty dict
    if not data:
        return {}

    # Grab the data from the dict
    if not company:
        macs, rssi = (data.keys(), data.values())
    else:
        macs, companies = (data.keys(), data.values())

    return (
        list(macs),
        list(rssi)
    ) if not company else (
        list(macs),
        list(companies)
    )


def ble_data_complete() -> dict:
    """Get the MAC address, Manufacturer, and RSSI."""

    company = True, False

    ble = ble_data(company=company[0])
    ble_rssi = ble_data(company=company[1])

    for i, mac in enumerate(ble_rssi):
        mac = mac[0].split(']')[1]
        for mac_2 in ble[0]:
            print(f"mac: {mac}, mac_2: {mac_2}")
            if mac_2 == mac:
                # Insert the RSSI from mac_2  into the ble's third index
                list(ble).append(ble_rssi[-1][i])
                print(f"ble_rssi: {ble_rssi}")
                print(f"ble: {ble}")

                print("Match!")
    print(f"ble_1: {ble}")
    print(f"ble_rssi: {ble_rssi}")

    try:
        for mac, mac_2 in zip(ble[0], ble_rssi[0]):
            print(mac, mac_2)
            ble_rssi[0].remove(mac_2)
            ble_rssi[1].remove(ble_rssi[1][ble_rssi[0].index(mac_2)])
    except KeyError:
        loggey.warning(msg="Rust webserver not running")

    return {}


def main():
    """In file main function."""
    print(version_getter())

    # if not compressed_data:

    # store the 'freq_dl' column in a df variable


if __name__ == "__main__":
    main()
