import time
import serial as sr
from colorama import Fore as F


R = F.RESET


def translate(
    value: int | float,
    leftMin: int | float,
    leftMax: int | float,
    rightMin: int | float,
    rightMax: int | float,
):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


class E_UTRA:
    """Table 5.7.3-1 E-UTRA channel numbers"""

    TABLE: dict[str, tuple[float, int]] = {
        # Band: (FDL_low, NOffs_DL)
        "1": (2100, 0),
        "2": (1930, 600),
        "3": (1805, 1200),
        "4": (2110, 1950),
        "5": (869, 2400),
        "6": (875, 2650),
        "7": (2620, 2750),
        "8": (925, 3450),
        "9": (1844.9, 3800),
        "10": (2110, 4150),
        "11": (1475.9, 4750),
        "12": (729, 5010),
        "13": (746, 5180),
        "14": (758, 5280),
        "17": (734, 5730),
        "18": (860, 5850),
        "19": (875, 6000),
        "20": (791, 6150),
        "21": (1495.9, 6450),
        "24": (1525, 7700),
        "25": (1900, 8040),
        "26": (859, 8690),
        "27": (852, 9040),
        "28": (758, 9210),
        "29": (717, 9660),
        "30": (2350, 9770),
        "31": (462.5, 9870),
        "32": (1900, 9920),
        "33": (1900, 36000),
        "34": (2010, 36200),
        "35": (1850, 36350),
        "36": (1930, 36950),
        "37": (1910, 37550),
        "38": (2570, 37750),
        "39": (1880, 38250),
        "40": (2300, 38650),
        "41": (2496, 39650),
        "42": (3400, 41590),
        "43": (3600, 43590),
        "44": (3700, 45590),
        "66": (2100, 66436),
        "71": (617, 66436),
    }

    US_BANDS = [
        2,
        4,
        5,
        10,
        12,
        13,
        14,
        25,
        26,
        30,
        41,
        66,
        71,
    ]  # US bands we want to use

    @classmethod
    def quectel_band(self, bands: int) -> int:
        """Convert the desired band for use in Quectel command"""

        new_band = sum([2 ** (int(band) - 1) for band in bands])

        return new_band

    @classmethod
    def _band_ranges(self) -> dict[list[int]]:
        """Define the ranges of earfcns for each band"""

        band_1 = [i for i in range(0, 600)]
        band_2 = [i for i in range(600, 1200)]
        band_3 = [i for i in range(1200, 1950)]
        band_4 = [i for i in range(1950, 2400)]
        band_5 = [i for i in range(2400, 2650)]
        band_6 = [i for i in range(2650, 2750)]
        band_7 = [i for i in range(2750, 3450)]
        band_8 = [i for i in range(3450, 3800)]
        band_9 = [i for i in range(3800, 4150)]
        band_10 = [i for i in range(4150, 4750)]
        band_11 = [i for i in range(4750, 4950)]
        band_12 = [i for i in range(5010, 5180)]
        band_13 = [i for i in range(5180, 5280)]
        band_14 = [i for i in range(5280, 5380)]
        band_17 = [i for i in range(5730, 5850)]
        band_18 = [i for i in range(5850, 6000)]
        band_19 = [i for i in range(6000, 6150)]
        band_20 = [i for i in range(6150, 6450)]
        band_21 = [i for i in range(6450, 6600)]
        band_24 = [i for i in range(7700, 8040)]
        band_25 = [i for i in range(8040, 8690)]
        band_26 = [i for i in range(8690, 9040)]
        band_27 = [i for i in range(9040, 9210)]
        band_28 = [i for i in range(9210, 9660)]
        band_29 = [i for i in range(9660, 9770)]  # Downlink only
        band_30 = [i for i in range(9770, 9870)]
        band_31 = [i for i in range(9870, 9920)]
        band_32 = [i for i in range(9920, 10360)]  # Downlink only
        band_33 = [i for i in range(36000, 36200)]
        band_34 = [i for i in range(36200, 36350)]
        band_35 = [i for i in range(36350, 36950)]
        band_36 = [i for i in range(36950, 37550)]
        band_37 = [i for i in range(37550, 37750)]
        band_38 = [i for i in range(37750, 38250)]
        band_39 = [i for i in range(38250, 38650)]
        band_40 = [i for i in range(38650, 39650)]
        band_41 = [i for i in range(39650, 41590)]
        band_42 = [i for i in range(41590, 43590)]
        band_43 = [i for i in range(43590, 45590)]
        band_44 = [i for i in range(45590, 46590)]
        band_66 = [i for i in range(66436, 67336)]
        band_71 = [i for i in range(68586, 68936)]

        return {
            "1": band_1,
            "2": band_2,
            "3": band_3,
            "4": band_4,
            "5": band_5,
            "6": band_6,
            "7": band_7,
            "8": band_8,
            "9": band_9,
            "10": band_10,
            "11": band_11,
            "12": band_12,
            "13": band_13,
            "14": band_14,
            "17": band_17,
            "18": band_18,
            "19": band_19,
            "20": band_20,
            "21": band_21,
            "24": band_24,
            "25": band_25,
            "26": band_26,
            "27": band_27,
            "28": band_28,
            "29": band_29,
            "30": band_30,
            "31": band_31,
            "32": band_32,
            "33": band_33,
            "34": band_34,
            "35": band_35,
            "36": band_36,
            "37": band_37,
            "38": band_38,
            "39": band_39,
            "40": band_40,
            "41": band_41,
            "42": band_42,
            "43": band_43,
            "44": band_44,
            "66": band_66,
            "71": band_71,
        }

    @classmethod
    def convert_to_frequency(cls, earfcn: list[int]) -> float | None:
        """Convert the earfcn to a center band frequency"""

        for band in E_UTRA._band_ranges().items():
            # print(band[1])
            for i in band[1]:
                try:
                    if i == earfcn:
                        FDL_low, NOffs_DL = (
                            cls.TABLE.get(band[0])[0],
                            cls.TABLE.get(band[0])[1],
                        )
                        return FDL_low + 0.1 * (earfcn - NOffs_DL)
                    else:
                        print(f"{F.RED}Earfcn not found{R}")
                        return None
                except TypeError:
                    print("No band found for earfcn: {}".format(earfcn))
                    return None


class EG25G:
    """Get the neighborhood list of local celluar towers"""

    POWER_DOWN = "AT+QPOWD"
    DATA_CARRIER_DETECTION_MODE = "AT&C0"  # Always ON
    REQUEST_MODEL_IDENTIFICATION = "AT+GMM"
    UE_CONFIG = "AT+QCFG"
    ENGINEERING_MODE = "AT+QENG"
    BAND_SCAN = "AT+QCOPS"
    SIGNAL_QUALITY = "AT+CSQ"

    def __init__(self, port):
        self.port = port
        self.ser = sr.Serial(port, 115_200, timeout=2)

    def power_down(self):
        key_word = f"{self.POWER_DOWN}\r"
        self.ser.write(key_word.encode())
        self.ser.flush()
        print(self.ser.readlines())
        self.ser.close()

    def data_carrier_detection_mode(self):
        key_word = f"{self.DATA_CARRIER_DETECTION_MODE}\r"
        self.ser.write(key_word.encode())
        self.ser.flush()

    def check_connection(self) -> str:
        key_word = f"{self.REQUEST_MODEL_IDENTIFICATION}\r"
        self.ser.write(key_word.encode())
        self.ser.flush()

        return str(self.ser.readlines()[1:]
                   [0].decode().strip("\n").strip("\r"))

    def get_signal_strength(self) -> int | str:
        key_word = f"{self.SIGNAL_QUALITY}\r"
        self.ser.write(key_word.encode())
        self.ser.flush()

        rssi = int(
            self.ser.readlines()[1]
            .decode()
            .strip("\n")
            .strip("\r")
            .split(":")[1]
            .split(",")[0]
        )

        match rssi:
            case 0:
                return -113
            case 1:
                return -111
            case val if 2 <= val < 31:
                return int(
                    translate(
                        value=val, leftMin=2, leftMax=31, rightMin=-109, rightMax=-52
                    )
                )
            case 31:
                return -51
            case 99:
                return "Undetectable"
            case 100:
                return -116
            case 101:
                return -115
            case val if 102 <= val < 190:
                return int(
                    translate(
                        value=val, leftMin=102, leftMax=191, rightMin=-114, rightMax=-25
                    )
                )
            case 199:
                return "Undetectable"
            case _:
                return "Undetectable"

    def get_neighborcell(self):
        key_word = f"{self.BAND_SCAN}\r"
        self.ser.write(key_word.encode())
        self.ser.flush()

        return self.ser.readlines()[1:][0].decode().strip("\n").strip("\r")

    def ue_config(self):
        key_word = f"{self.UE_CONFIG}\r"
        self.ser.write(key_word.encode())
        self.ser.flush()

        return self.ser.readlines()[1:][0].decode().strip("\n").strip("\r")

    def engineering_mode(self):
        key_word = f"{self.ENGINEERING_MODE}\r"
        self.ser.write(key_word.encode())
        self.ser.flush()

        return self.ser.readlines()[1:][0].decode().strip("\n").strip("\r")

    def set_band(self, bands_in_int: list) -> bool:
        """Set the bands to scan"""

        key_word = (
            f'{self.UE_CONFIG}="band",0,{E_UTRA.quectel_band(bands=bands_in_int)},0\r'
        )
        self.ser.write(key_word.encode())
        self.ser.flush()
        return True

    def check_current_band(self):
        """Check the band that is presently set"""

        key_word = f'{self.UE_CONFIG}="band"\r'
        self.ser.write(key_word.encode())
        self.ser.flush()

        band = self.ser.readlines()[1].decode().strip(
            "\n").strip("\r").split(",")[2]
        band = int(band, base=16)

        return band

    def is_ser_open(self) -> bool:
        return self.ser.isOpen()

    def get_neighborcell_list(self) -> list[int]:
        key_word = f'{self.ENGINEERING_MODE}="neighbourcell"\r'
        self.ser.write(key_word.encode())
        self.ser.flush()

        neighborcell = [
            line.decode().strip("\n").strip("\r").split("',")
            for line in self.ser.readlines()
        ][1:-2]

        earfcns = [
            neighborcell[i][0][35:].split(",")[0] for i in range(len(neighborcell))
        ]  # Get the earfcn

        return [int(earfcn) for earfcn in earfcns]

    def get_band_scan(self) -> list[str]:
        start = (
            time.time()
        )  # 4: 4G only, 1: Most information, 0: show PSID, 1: seconds per scan
        key_word = f"{self.BAND_SCAN}=4,1,0,1\r"
        self.ser.write(key_word.encode())
        self.ser.flush()

        band_scan = self.ser.readlines()

        end = time.time()

        # show time taken in colorama red
        print(f"{F.BLUE}Time taken to scan bands{R}: {F.RED}{str(end - start)}{R} secs")

        return band_scan


def main():
    us_band = EG25G("/dev/ttyUSB3")

    # [print(f"Signal Strength: {F.BLUE}{us_band.get_signal_strength()}{R} {F.YELLOW}dBm{R}")
    #  for i in range(20)]
    # print(f"Current Band: {F.BLUE}{us_band.check_current_band()}{R}")

    # [print(f"Signal Strength: {F.BLUE}{us_band.get_signal_strength()}{R} {F.YELLOW}dBm{R}") for i in range(20)]

    print(
        f"Neighbor Cell List: {F.YELLOW}{us_band.get_neighborcell_list()}{R}")
    # get signal strength
    print(
        f"Signal Strength: {F.BLUE}{us_band.get_signal_strength()}{R} {F.YELLOW}dBm{R}"
    )

    # Set the band to band 2
    us_band.set_band([71])

    # print signal strength
    print(f"Checking Connections: {F.BLUE}{us_band.check_connection()}{R}")
    print(
        f"Signal Strength: {F.BLUE}{us_band.get_signal_strength()}{R} {F.YELLOW}dBm{R}"
    )
    print(
        f"Neighbor Cell List: {F.YELLOW}{us_band.get_neighborcell_list()}{R}")
    print(f"Current Band: {F.GREEN}{us_band.check_current_band()}{R}")

    us_band.set_band([13])

    print(f"Checking Connections: {F.BLUE}{us_band.check_connection()}{R}")
    print(
        f"Signal Strength: {F.BLUE}{us_band.get_signal_strength()}{R} {F.YELLOW}dBm{R}"
    )
    print(f"Neighbor Cell List: {F.BLUE}{us_band.get_neighborcell_list()}{R}")
    print(f"Current Band: {F.GREEN}{us_band.check_current_band()}{R}")

    us_band.set_band([5])

    print(f"Checking Connections: {F.BLUE}{us_band.check_connection()}{R}")
    print(
        f"Signal Strength: {F.BLUE}{us_band.get_signal_strength()}{R} {F.YELLOW}dBm{R}"
    )
    print(f"Neighbor Cell List: {F.GREEN}{us_band.get_neighborcell_list()}{R}")
    print(f"Current Band: {F.GREEN}{us_band.check_current_band()}{R}")

    us_band.set_band([4])

    print(f"Checking Connections: {F.BLUE}{us_band.check_connection()}{R}")
    print(
        f"Signal Strength: {F.BLUE}{us_band.get_signal_strength()}{R} {F.YELLOW}dBm{R}"
    )
    print(f"Neighbor Cell List: {F.CYAN}{us_band.get_neighborcell_list()}{R}")
    print(f"Current Band: {F.GREEN}{us_band.check_current_band()}{R}")

    us_band.set_band([30])

    print(f"Checking Connections: {F.BLUE}{us_band.check_connection()}{R}")
    print(
        f"Signal Strength: {F.BLUE}{us_band.get_signal_strength()}{R} {F.YELLOW}dBm{R}"
    )
    print(f"Neighbor Cell List: {F.BLACK}{us_band.get_neighborcell_list()}{R}")
    print(f"Current Band: {F.GREEN}{us_band.check_current_band()}{R}")

    us_band.set_band([12])

    print(f"Checking Connections: {F.BLUE}{us_band.check_connection()}{R}")
    print(
        f"Signal Strength: {F.BLUE}{us_band.get_signal_strength()}{R} {F.YELLOW}dBm{R}"
    )
    print(
        f"Neighbor Cell List: {F.MAGENTA}{us_band.get_neighborcell_list()}{R}")
    print(f"Current Band: {F.GREEN}{us_band.check_current_band()}{R}")

    us_band.set_band(bands_in_int=[66])

    # print the neighbor cell list
    print(f"Checking Connections: {F.BLUE}{us_band.check_connection()}{R}")
    print(
        f"Signal Strength: {F.BLUE}{us_band.get_signal_strength()}{R} {F.YELLOW}dBm{R}"
    )
    print(
        f"Neighbor Cell List: {F.YELLOW}{us_band.get_neighborcell_list()}{R}")
    print()
    # get current band
    print(f"Current Band: {F.GREEN}{us_band.check_current_band()}{R}")

    # print the band scan results in colorama yellow
    # us_band.power_down()


if __name__ == "__main__":
    main()
