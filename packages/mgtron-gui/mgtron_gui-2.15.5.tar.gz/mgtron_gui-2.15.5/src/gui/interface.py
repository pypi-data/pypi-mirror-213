from dataclasses import dataclass
import pathlib
import platform
from time import sleep
import time
from typing import Any, Callable
import serial
import subprocess
import logging


ROOT = pathlib.Path(__file__).resolve().parent.parent.parent


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s :: %(name)s :: %(message)s :: %(levelname)s",
    datefmt="%d-%b-%y %H:%M:%S",
    filename=f"{ROOT}/mg.log",
    filemode="w",
)

logger = logging.getLogger(__name__)

BAUDRATE = 115_200
DEVICE_PORT: int = int()


def find_device(DEVICE_NUMBER: int = DEVICE_PORT) -> tuple[str, list[str]]:
    """Find the Megatron device plugged into the Linux computer."""
    global PORT

    results: list[str] = list()
    win_str: str = "COM3"
    not_found: str = "Device not found"

    # Determine if system is Linux or WIN
    if platform.system().lower() == "linux":
        # Search Linux filesystem for device
        find = ["find /dev -iname 'ttyACM*'"]
        try:
            logger.info(
                msg=f"{find_device.__name__} function executing\
 linux shell command to get device file names"
            )
            results_ = subprocess.run(
                args=find,
                shell=True,
                stdout=subprocess.PIPE,
                universal_newlines=True,
                encoding="utf-8",
                capture_output=False,
            )
            results = sorted(results_.stdout.strip().splitlines())

            try:
                PORT = results[DEVICE_NUMBER]
            except IndexError:
                logger.error(not_found)
                return not_found, results

            logger.info(msg=f"Connected Devices: {results}")
            logger.debug(msg=f"Chosen Device: {PORT}")
            return PORT, results
        except IndexError:
            logger.exception(not_found)
            print(not_found)
            return not_found, results

    elif platform.system().lower() == "windows":
        logger.info(f"{platform.system()} discovered")
        # global PORT
        # Search Windows filesystem for device
        # filename = "COM3"
        # devices = [os.path.join(root, filename) for root, dir,
        #           files in os.walk("/user/") if filename in files]

        return win_str, [win_str]

    return ("", [""])


def serial_call(*args, PORT: str = find_device(0)[0][0]) -> None:
    """Call the serial device and send the command to the device."""
    logger.debug(msg="Serial call to device initiated")

    NAME: str = serial_call.__name__

    sleep(0.095)  # Allow time to read and execute via serial *REQUIRED*

    try:
        # If the teensy is corrupted the GUI freezes here
        logger.debug(msg=f"Attempting to open serial connection {NAME}()")
        with serial.Serial() as ser:
            ser.port = PORT.strip()
            logger.debug(msg=f"Serial device set | {NAME}()")

            ser.baudrate = BAUDRATE
            logger.debug(msg=f"baudrate set | {NAME}()")

            ser.timeout = 0.8  # seconds
            logger.debug(msg=f"timeout set | {NAME}()")

            ser.open()
            logger.debug(msg=f"serial connection open | {NAME}()")

            print(" ".join([arg for arg in args]).encode("utf-8"))
            ser.write(" ".join([arg for arg in args]).encode("utf-8"))
            ser.write("\n".encode("utf-8"))

            logger.debug(msg=f"info sent via serial protocol | {NAME}()")
            ser.flush()

    except (serial.SerialException, NameError):
        logger.error(msg="No response from device or no device | {NAME}()")

    logger.debug(msg=f"Contextually closed serial connection | {NAME}()")


def read_output(PORT: str) -> list[str]:
    """Read the raw serial output from the serial terminal."""
    NAME: str = read_output.__name__
    output_holder: list[str] = list()
    stopper: bool = bool()

    with serial.Serial() as ser:
        ser.baudrate = BAUDRATE
        logger.debug(msg=f"baudrate set | {NAME}()")

        ser.port = str(PORT).strip()
        logger.debug(msg=f"Serial device set | {NAME}()")

        ser.timeout = 0.2  # seconds
        logger.debug(msg=f"timeout set | {NAME}()")

        try:
            ser.open()
        except serial.SerialException:
            logger.error(msg=f"No device found | {NAME}()")
            return ["No device found"]
        logger.debug(msg=f"opening serial connection | {NAME}()")

        logger.debug(msg=f"Starting loop to read card output |  {NAME}()")
        start_time = time.time()
        while not stopper:
            for i, val in enumerate(ser.read()):
                output_holder.append(chr(val))

                if output_holder[-1].__contains__("$"):
                    output_holder = output_holder[:-1]
                    stopper = True
                    break
            continue_time = time.time() - start_time

            if continue_time > 0.2:
                logger.error(msg=f"Timeout reached | {NAME}()")
                break
            ser.flush()

    logger.debug(msg=f"Contextually closed serial connection from {NAME}()")

    return output_holder


def format_output(
    PORT: str = find_device(0)[0],
        output_holder: Callable[[str],
                                list[str]] = read_output
) -> dict[str, list[float | int]]:
    """Take in the raw output from the serial terminal and format it."""
    init_data: dict[str, list[float | int]] = {
        "channel": list(),
        "freq": list(),
        "power": list(),
        "bandwidth": list(),
    }

    body: list = list()
    channel_data: list = list()
    power_data: list[Any] = list()
    freq_data: list = list()
    bw_data: list[Any] = list()

    # Store the output in a digestible format
    body.append("".join(j for j in output_holder(PORT)))

    # split the output into a list of strings
    body = body[0].split("\r\n")

    channel_data.append(list(filter(lambda a: "Channel" in a, body)))

    freq_data.append(list(filter(lambda a: "Frequency" in a, body)))

    power_data.append(list(filter(lambda a: "Power" in a, body)))

    bw_data.append(list(filter(lambda a: "Bandwidth" in a, body)))

    # Parse the fortmatted data into a list of floats
    init_data["channel"] = [
        int(j.strip("Status-").
            strip("-Channel").strip()) for j in channel_data[0]
    ]

    init_data["freq"] = [
        float(j.strip("MHz").strip("Frequency: ")) for j in freq_data[0]
    ]

    init_data["power"] = [float(j.strip()
                                .strip("Power: ")) for j in power_data[0]]

    init_data["bandwidth"] = [
        float(j.strip("%").strip("Bandwidth: ")) for j in bw_data[0]
    ]

    return init_data


@dataclass(slots=True)
class Megatron:
    """Class to organize the manipulation of 8 channels."""

    logger.debug(msg="\n\nGUI LAUNCHED\n\n")

    try:
        logger.info(msg="Getting the port name of device")
        PORT = find_device(DEVICE_PORT)[0]  # type: ignore
        logger.info(msg=f"Connected device path: {PORT}")
    except TypeError:
        logger.exception(msg="No device found on system")

    @classmethod
    def status(cls, PORT: str) -> None:
        """Check the status of the board."""
        logger.info(f"{Megatron.status.__name__} function executed")
        serial_call("s", PORT=PORT)

    def change_power(self, channel: int, power_level: int, PORT: str):
        """Change the power level of a channel Range: 0 - 63."""
        print(f"Change power: PORT === {PORT}")
        logger.info(f"{Megatron.change_power.__name__} function executed")
        logger.info(msg=f"Connected device path: {PORT}")
        return serial_call("p", str(channel), str(power_level), PORT=PORT)

    def change_freq(self, channel: int, frequency: float, PORT: str):
        """Change the frequency of a channel Range: 50 - 6400 MHz."""
        logger.info(f"{Megatron.change_freq.__name__} function executed")
        print()
        return serial_call("f", str(channel), str(frequency), PORT=PORT)

    def change_bandwidth(self, channel: int, percentage: int, PORT: str):
        """
        Change the bandwidth of a channel
        Range: 0 - 100
        """

        logger.info(f"{Megatron.change_bandwidth.__name__} function executed")
        return serial_call("b", str(channel), str(percentage), PORT=PORT)

    def save_state(self, state: bool, PORT: str) -> None:
        """Save each settings made by the user into memory for next startup"""

        state = 1 if state else 0  # type: ignore
        try:
            serial_call("x", str(state), PORT=PORT)
            logger.info(f"{Megatron.save_state.__name__} function executed")
        except TypeError:
            logger.exception(msg="No device assigned")

    def amplification(self, channel: int, state: bool, PORT: str) -> None:
        """Output HIGH or LOW logic level out of a chosen channel"""

        state = 1 if state else 0  # type: ignore
        serial_call("a", str(channel), str(state), PORT=PORT)
        logger.info(f"{Megatron.amplification.__name__} function executed")

    def stability(self, state: bool, PORT: str) -> None:
        """Boolean a second
        filtering stage of capacitors for further stability"""

        state = 1 if state else 0  # type: ignore
        serial_call("~", str(state), PORT=PORT)
        logger.info(f"{Megatron.stability.__name__} function executed")

    def noise_control(self, state: bool, percentage: int, PORT: str) -> None:
        """
        Optimal settings hardcoded; Input @ %100 Output @ %85
        state 0: Output stage
        state 1: Input stage
        """

        state = 1 if state else 0  # type: ignore
        serial_call("n", str(state), str(percentage), PORT=PORT)
        logger.info(f"{Megatron.noise_control.__name__} function executed")

    def reset_board(self, PORT: str) -> None:
        """Reset the parameters of the board"""

        [
            (
                serial_call("p", str(i), "0", PORT=PORT),
                # serial_call("b", str(i), "0", PORT=PORT),
                # serial_call("f", str(i), "50.00", PORT=PORT),
            )
            for i in range(1, 9)
        ]

        logger.info(f"{Megatron.reset_board.__name__} function executed")

    logger.info(msg="class Megatron initialized")


logger.debug(msg=f"EOF: {__name__}")


def main() -> None:
    # import random

    # find_device("linux")
    # test_1 = Megatron()
    pass

    # for i in range(8):
    # test_1.change_power(i+1, random.randint(a=10, b=63))
    # sleep(1)
    # test_1.change_freq(i+1, random.randint(a=50, b=6300))
    # sleep(1)
    # test_1.change_bandwidth(i+1, random.randint(a=10, b=100))
    # sleep(1)
    # sleep(1)
    # test_1.reset_board()

    # test_1.change_freq(1, 2545.54)
    # test_1.change_power(1, 63)

    # test_1.status(PORT=PORT)
    # print("\n", format_output())

    # test_1.amplification(3, True)
    # test_1.stability(True)
    # test_1.save_state(True)


if __name__ == "__main__":
    main()

# q: how to delete a local git branch
# a: git branch -d <branch_name>
