from src.gui.helpers import read_config

# test gps jam button frequency channel 1



def test_gps_jam_button_low_1f():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    freq_1_check = parser["freq"]["freq_1"]
    assert float(freq_1_check) >= 50


def test_gps_jam_button_up_1f():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    freq_1_check = parser["freq"]["freq_1"]
    assert float(freq_1_check) <= 6400

# test gps jam button frequency channel 2


def test_gps_jam_button_low_2f():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    freq_2_check = parser["freq"]["freq_2"]
    assert float(freq_2_check) >= 50


def test_gps_jam_button_up_2f():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    freq_2_check = parser["freq"]["freq_2"]
    assert float(freq_2_check) <= 6400

# test gps jam button frequency channel 3


def test_gps_jam_button_low_3f():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    freq_3_check = parser["freq"]["freq_3"]
    assert float(freq_3_check) >= 50


def test_gps_jam_button_up_3f():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    freq_3_check = parser["freq"]["freq_3"]
    assert float(freq_3_check) <= 6400

# test gps jam button frequency channel 4


def test_gps_jam_button_low_4f():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    freq_4_check = parser["freq"]["freq_4"]
    assert float(freq_4_check) >= 50


def test_gps_jam_button_up_4f():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    freq_4_check = parser["freq"]["freq_4"]
    assert float(freq_4_check) <= 6400

# test gps jam button frequency channel 5


def test_gps_jam_button_low_5f():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    freq_5_check = parser["freq"]["freq_5"]
    assert float(freq_5_check) >= 50


def test_gps_jam_button_up_5f():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    freq_5_check = parser["freq"]["freq_5"]
    assert float(freq_5_check) <= 6400

# test gps jam button frequency channel 6


def test_gps_jam_button_low_6f():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    freq_6_check = parser["freq"]["freq_6"]
    assert float(freq_6_check) >= 50


def test_gps_jam_button_up_6f():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    freq_6_check = parser["freq"]["freq_6"]
    assert float(freq_6_check) <= 6400

# test gps jam button frequency channel 7


def test_gps_jam_button_low_7f():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    freq_7_check = parser["freq"]["freq_7"]
    assert float(freq_7_check) >= 50


def test_gps_jam_button_up_7f():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    freq_7_check = parser["freq"]["freq_7"]
    assert float(freq_7_check) <= 6400

# test gps jam button frequency channel 8


def test_gps_jam_button_low_8f():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    freq_8_check = parser["freq"]["freq_8"]
    assert float(freq_8_check) >= 50


def test_gps_jam_button_up_8f():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    freq_8_check = parser["freq"]["freq_8"]
    assert float(freq_8_check) <= 6400


#
#
# test gps jam button power channel 1
#
#

def test_gps_jam_button_low_1p():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    power_1_check = parser["power"]["power_1"]
    assert float(power_1_check) >= 0


def test_gps_jam_button_up_1p():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    power_1_check = parser["power"]["power_1"]
    assert float(power_1_check) <= 100

# test gps jam button power channel 2


def test_gps_jam_button_low_2p():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    power_2_check = parser["power"]["power_2"]
    assert float(power_2_check) >= 0


def test_gps_jam_button_up_2p():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    power_2_check = parser["power"]["power_2"]
    assert float(power_2_check) <= 100

# test gps jam button power channel 3


def test_gps_jam_button_low_3p():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    power_3_check = parser["power"]["power_3"]
    assert float(power_3_check) >= 0


def test_gps_jam_button_up_3p():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    power_3_check = parser["power"]["power_3"]
    assert float(power_3_check) <= 100

# test gps jam button power channel 4


def test_gps_jam_button_low_4p():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    power_4_check = parser["power"]["power_4"]
    assert float(power_4_check) >= 0


def test_gps_jam_button_up_4p():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    power_4_check = parser["power"]["power_4"]
    assert float(power_4_check) <= 100

# test gps jam button power channel 5


def test_gps_jam_button_low_5p():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    power_5_check = parser["power"]["power_5"]
    assert float(power_5_check) >= 0


def test_gps_jam_button_up_5p():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    power_5_check = parser["power"]["power_5"]
    assert float(power_5_check) <= 100

# test gps jam button power channel 6


def test_gps_jam_button_low_6p():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    power_6_check = parser["power"]["power_6"]
    assert float(power_6_check) >= 0


def test_gps_jam_button_up_6p():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    power_6_check = parser["power"]["power_6"]
    assert float(power_6_check) <= 100

# test gps jam button power channel 7


def test_gps_jam_button_low_7p():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    power_7_check = parser["power"]["power_7"]
    assert float(power_7_check) >= 0


def test_gps_jam_button_up_7p():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    power_7_check = parser["power"]["power_7"]
    assert float(power_7_check) <= 100

# test gps jam button power channel 8


def test_gps_jam_button_low_8p():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    power_8_check = parser["power"]["power_8"]
    assert float(power_8_check) >= 0


def test_gps_jam_button_up_8p():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    power_8_check = parser["power"]["power_8"]
    assert float(power_8_check) <= 100


#
#
# test gps jam button bandwidth channel 1
#
#

def test_gps_jam_button_low_1b():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    bandwidth_check_1 = parser["bandwidth"]["bw_1"]
    assert float(bandwidth_check_1) >= 0


def test_gps_jam_button_up_1b():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    bandwidth_check_1 = parser["bandwidth"]["bw_1"]
    assert float(bandwidth_check_1) <= 100

# test gps jam button bandwidth channel 2


def test_gps_jam_button_low_2b():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    bandwidth_check_2 = parser["bandwidth"]["bw_2"]
    assert float(bandwidth_check_2) >= 0


def test_gps_jam_button_up_2b():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    bandwidth_check_2 = parser["bandwidth"]["bw_2"]
    assert float(bandwidth_check_2) <= 100

# test gps jam button bandwidth channel 3


def test_gps_jam_button_low_3b():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    bandwidth_check_3 = parser["bandwidth"]["bw_3"]
    assert float(bandwidth_check_3) >= 0


def test_gps_jam_button_up_3b():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    bandwidth_check_3 = parser["bandwidth"]["bw_3"]
    assert float(bandwidth_check_3) <= 100

# test gps jam button bandwidth channel 4


def test_gps_jam_button_low_4b():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    bandwidth_check_4 = parser["bandwidth"]["bw_4"]
    assert float(bandwidth_check_4) >= 0


def test_gps_jam_button_up_4b():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    bandwidth_check_4 = parser["bandwidth"]["bw_4"]
    assert float(bandwidth_check_4) <= 100

# test gps jam button bandwitdth channel 5


def test_gps_jam_button_low_5b():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    bandwidth_check_5 = parser["bandwidth"]["bw_5"]
    assert float(bandwidth_check_5) >= 0


def test_gps_jam_button_up_5b():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    bandwidth_check_5 = parser["bandwidth"]["bw_5"]
    assert float(bandwidth_check_5) <= 100

# test gps jam button bandwitdth channel 6


def test_gps_jam_button_low_6b():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    bandwidth_check_6 = parser["bandwidth"]["bw_6"]
    assert float(bandwidth_check_6) >= 0


def test_gps_jam_button_up_6b():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    bandwidth_check_6 = parser["bandwidth"]["bw_6"]
    assert float(bandwidth_check_6) <= 100

# test gps jam button bandwitdth channel 7


def test_gps_jam_button_low_7b():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    bandwidth_check_7 = parser["bandwidth"]["bw_7"]
    assert float(bandwidth_check_7) >= 0


def test_gps_jam_button_up_7b():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    bandwidth_check_7 = parser["bandwidth"]["bw_7"]
    assert float(bandwidth_check_7) <= 100

# test gps jam button bandwitdth channel 8


def test_gps_jam_button_low_8b():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    bandwidth_check_8 = parser["bandwidth"]["bw_8"]
    assert float(bandwidth_check_8) >= 0


def test_gps_jam_button_up_8b():
    parser, _ = read_config(file="./src/gui/_configs/mission_alpha.ini")

    bandwidth_check_8 = parser["bandwidth"]["bw_8"]
    assert float(bandwidth_check_8) <= 100


#
#
#
#
#
#
#
#
#
#
# test zwave jam button

# test zwave jam button frequency channel 1

def test_zwave_jam_button_low_1f():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    freq_1_check = parser["freq"]["freq_1"]
    assert float(freq_1_check) >= 50


def test_zwave_jam_button_up_1f():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    freq_1_check = parser["freq"]["freq_1"]
    assert float(freq_1_check) <= 6400

# test zwave jam button frequency channel 2


def test_zwave_jam_button_low_2f():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    freq_2_check = parser["freq"]["freq_2"]
    assert float(freq_2_check) >= 50


def test_zwave_jam_button_up_2f():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    freq_2_check = parser["freq"]["freq_2"]
    assert float(freq_2_check) <= 6400

# test zwave jam button frequency channel 3


def test_zwave_jam_button_low_3f():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    freq_3_check = parser["freq"]["freq_3"]
    assert float(freq_3_check) >= 50


def test_zwave_jam_button_up_3f():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    freq_3_check = parser["freq"]["freq_3"]
    assert float(freq_3_check) <= 6400

# test zwave jam button frequency channel 4


def test_zwave_jam_button_low_4f():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    freq_4_check = parser["freq"]["freq_4"]
    assert float(freq_4_check) >= 50


def test_zwave_jam_button_up_4f():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    freq_4_check = parser["freq"]["freq_4"]
    assert float(freq_4_check) <= 6400

# test zwave jam button frequency channel 5


def test_zwave_jam_button_low_5f():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    freq_5_check = parser["freq"]["freq_5"]
    assert float(freq_5_check) >= 50


def test_zwave_jam_button_up_5f():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    freq_5_check = parser["freq"]["freq_5"]
    assert float(freq_5_check) <= 6400

# test zwave jam button frequency channel 6


def test_zwave_jam_button_low_6f():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    freq_6_check = parser["freq"]["freq_6"]
    assert float(freq_6_check) >= 50


def test_zwave_jam_button_up_6f():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    freq_6_check = parser["freq"]["freq_6"]
    assert float(freq_6_check) <= 6400

# test zwave jam button frequency channel 7


def test_zwave_jam_button_low_7f():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    freq_7_check = parser["freq"]["freq_7"]
    assert float(freq_7_check) >= 50


def test_zwave_jam_button_up_7f():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    freq_7_check = parser["freq"]["freq_7"]
    assert float(freq_7_check) <= 6400

# test zwave jam button frequency channel 8


def test_zwave_jam_button_low_8f():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    freq_8_check = parser["freq"]["freq_8"]
    assert float(freq_8_check) >= 50


def test_zwave_jam_button_up_8f():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    freq_8_check = parser["freq"]["freq_8"]
    assert float(freq_8_check) <= 6400


#
#
# test zwave jam power channel 1
#
#

def test_zwave_jam_button_low_1p():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    power_1_check = parser["power"]["power_1"]
    assert float(power_1_check) >= 0


def test_zwave_jam_button_up_1p():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    power_1_check = parser["power"]["power_1"]
    assert float(power_1_check) <= 100

# test zwave jam power channel 2


def test_zwave_jam_button_low_2p():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    power_2_check = parser["power"]["power_2"]
    assert float(power_2_check) >= 0


def test_zwave_jam_button_up_2p():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    power_2_check = parser["power"]["power_2"]
    assert float(power_2_check) <= 100

# test zwave jam power channel 3


def test_zwave_jam_button_low_3p():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    power_3_check = parser["power"]["power_3"]
    assert float(power_3_check) >= 0


def test_zwave_jam_button_up_3p():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    power_3_check = parser["power"]["power_3"]
    assert float(power_3_check) <= 100

# test zwave jam power channel 4


def test_zwave_jam_button_low_4p():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    power_4_check = parser["power"]["power_4"]
    assert float(power_4_check) >= 0


def test_zwave_jam_button_up_4p():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    power_4_check = parser["power"]["power_4"]
    assert float(power_4_check) <= 100

# test zwave jam power channel 5


def test_zwave_jam_button_low_5p():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    power_5_check = parser["power"]["power_5"]
    assert float(power_5_check) >= 0


def test_zwave_jam_button_up_5p():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    power_5_check = parser["power"]["power_5"]
    assert float(power_5_check) <= 100

# test zwave jam power channel 6


def test_zwave_jam_button_low_6p():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    power_6_check = parser["power"]["power_6"]
    assert float(power_6_check) >= 0


def test_zwave_jam_button_up_6p():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    power_6_check = parser["power"]["power_6"]
    assert float(power_6_check) <= 100

# test zwave jam power channel 7


def test_zwave_jam_button_low_7p():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    power_7_check = parser["power"]["power_7"]
    assert float(power_7_check) >= 0


def test_zwave_jam_button_up_7p():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    power_7_check = parser["power"]["power_7"]
    assert float(power_7_check) <= 100

# test zwave jam power channel 8


def test_zwave_jam_button_low_8p():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    power_8_check = parser["power"]["power_8"]
    assert float(power_8_check) >= 0


def test_zwave_jam_button_up_8p():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    power_8_check = parser["power"]["power_8"]
    assert float(power_8_check) <= 100

#
#
# test zwave jam bandwidth channel 1
#
#

def test_cell_jam_button_low_1b():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    bandwidth_check_1 = parser["bandwidth"]["bw_1"]
    assert float(bandwidth_check_1) >= 0


def test_zwave_jam_button_up_1b():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    bandwidth_check_1 = parser["bandwidth"]["bw_1"]
    assert float(bandwidth_check_1) <= 100

# test zwave jam button bandwidth channel 2


def test_zwave_jam_button_low_2b():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    bandwidth_check_2 = parser["bandwidth"]["bw_2"]
    assert float(bandwidth_check_2) >= 0


def test_zwave_jam_button_up_2b():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    bandwidth_check_2 = parser["bandwidth"]["bw_2"]
    assert float(bandwidth_check_2) <= 100

# test zwave jam button bandwidth channel 3


def test_zwave_jam_button_low_3b():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    bandwidth_check_3 = parser["bandwidth"]["bw_3"]
    assert float(bandwidth_check_3) >= 0


def test_zwave_jam_button_up_3b():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    bandwidth_check_3 = parser["bandwidth"]["bw_3"]
    assert float(bandwidth_check_3) <= 100

# test zwave jam button bandwidth channel 4


def test_zwave_jam_button_low_4b():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    bandwidth_check_4 = parser["bandwidth"]["bw_4"]
    assert float(bandwidth_check_4) >= 0


def test_zwave_jam_button_up_4b():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    bandwidth_check_4 = parser["bandwidth"]["bw_4"]
    assert float(bandwidth_check_4) <= 100

# test zwave jam button bandwitdth channel 5


def test_zwave_jam_button_low_5b():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    bandwidth_check_5 = parser["bandwidth"]["bw_5"]
    assert float(bandwidth_check_5) >= 0


def test_zwave_jam_button_up_5b():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    bandwidth_check_5 = parser["bandwidth"]["bw_5"]
    assert float(bandwidth_check_5) <= 100

# test zwave jam button bandwitdth channel 6


def test_zwave_jam_button_low_6b():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    bandwidth_check_6 = parser["bandwidth"]["bw_6"]
    assert float(bandwidth_check_6) >= 0


def test_zwave_jam_button_up_6b():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    bandwidth_check_6 = parser["bandwidth"]["bw_6"]
    assert float(bandwidth_check_6) <= 100

# test zwave jam button bandwitdth channel 7


def test_zwave_jam_button_low_7b():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    bandwidth_check_7 = parser["bandwidth"]["bw_7"]
    assert float(bandwidth_check_7) >= 0


def test_zwave_jam_button_up_7b():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    bandwidth_check_7 = parser["bandwidth"]["bw_7"]
    assert float(bandwidth_check_7) <= 100

# test zwave jam button bandwitdth channel 8


def test_zwave_jam_button_low_8b():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    bandwidth_check_8 = parser["bandwidth"]["bw_8"]
    assert float(bandwidth_check_8) >= 0


def test_zwave_jam_button_up_8b():
    parser, _ = read_config(file="./src/gui/_configs/mission_bravo.ini")

    bandwidth_check_8 = parser["bandwidth"]["bw_8"]
    assert float(bandwidth_check_8) <= 100


#
#
#
#
#
#
#
#
#
# test dect jam button

# test dect jam button frequency channel 1

def test_dect_jam_button_low_1f():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    freq_1_check = parser["freq"]["freq_1"]
    assert float(freq_1_check) >= 50



def test_dect_jam_button_up_1f():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    freq_1_check = parser["freq"]["freq_1"]
    assert float(freq_1_check) <= 6400

# test dect jam button frequency channel 2


def test_dect_jam_button_low_2f():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    freq_2_check = parser["freq"]["freq_2"]
    assert float(freq_2_check) >= 50


def test_dect_jam_button_up_2f():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    freq_2_check = parser["freq"]["freq_2"]
    assert float(freq_2_check) <= 6400

# test dect jam button frequency channel 3


def test_dect_jam_button_low_3f():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    freq_3_check = parser["freq"]["freq_3"]
    assert float(freq_3_check) >= 50


def test_dect_jam_button_up_3f():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    freq_3_check = parser["freq"]["freq_3"]
    assert float(freq_3_check) <= 6400

# test dect jam button frequency channel 4


def test_dect_jam_button_low_4f():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    freq_4_check = parser["freq"]["freq_4"]
    assert float(freq_4_check) >= 50


def test_dect_jam_button_up_4f():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    freq_4_check = parser["freq"]["freq_4"]
    assert float(freq_4_check) <= 6400

# test dect jam button frequency channel 5


def test_dect_jam_button_low_5f():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    freq_5_check = parser["freq"]["freq_5"]
    assert float(freq_5_check) >= 50


def test_dect_jam_button_up_5f():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    freq_5_check = parser["freq"]["freq_5"]
    assert float(freq_5_check) <= 6400

# test dect jam button frequency channel 6


def test_dect_jam_button_low_6f():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    freq_6_check = parser["freq"]["freq_6"]
    assert float(freq_6_check) >= 50


def test_dect_jam_button_up_6f():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    freq_6_check = parser["freq"]["freq_6"]
    assert float(freq_6_check) <= 6400

# test dect jam button frequency channel 7


def test_dect_jam_button_low_7f():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    freq_7_check = parser["freq"]["freq_7"]
    assert float(freq_7_check) >= 50


def test_dect_jam_button_up_7f():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    freq_7_check = parser["freq"]["freq_7"]
    assert float(freq_7_check) <= 6400

# test dect jam button frequency channel 8


def test_dect_jam_button_low_8f():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    freq_8_check = parser["freq"]["freq_8"]
    assert float(freq_8_check) >= 50


def test_dect_jam_button_up_8f():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    freq_8_check = parser["freq"]["freq_8"]
    assert float(freq_8_check) <= 6400

#
#
# test dect jam power channel 1
#
#


def test_dect_jam_button_low_1p():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    power_1_check = parser["power"]["power_1"]
    assert float(power_1_check) >= 0


def test_dect_jam_button_up_1p():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    power_1_check = parser["power"]["power_1"]
    assert float(power_1_check) <= 100

# test dect jam power channel 2


def test_dect_jam_button_low_2p():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    power_2_check = parser["power"]["power_2"]
    assert float(power_2_check) >= 0


def test_dect_jam_button_up_2p():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    power_2_check = parser["power"]["power_2"]
    assert float(power_2_check) <= 100

# test dect jam power channel 3


def test_dect_jam_button_low_3p():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    power_3_check = parser["power"]["power_3"]
    assert float(power_3_check) >= 0



def test_dect_jam_button_up_3p():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    power_3_check = parser["power"]["power_3"]
    assert float(power_3_check) <= 100

# test dect jam power channel 4


def test_dect_jam_button_low_4p():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    power_4_check = parser["power"]["power_4"]
    assert float(power_4_check) >= 0


def test_dect_jam_button_up_4p():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    power_4_check = parser["power"]["power_4"]
    assert float(power_4_check) <= 100

# test dect jam power channel 5


def test_dect_jam_button_low_5p():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    power_5_check = parser["power"]["power_5"]
    assert float(power_5_check) >= 0


def test_dect_jam_button_up_5p():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    power_5_check = parser["power"]["power_5"]
    assert float(power_5_check) <= 100

# test dect jam power channel 6


def test_dect_jam_button_low_6p():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    power_6_check = parser["power"]["power_6"]
    assert float(power_6_check) >= 0


def test_dect_jam_button_up_6p():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    power_6_check = parser["power"]["power_6"]
    assert float(power_6_check) <= 100

# test dect jam power channel 7


def test_dect_jam_button_low_7p():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    power_7_check = parser["power"]["power_7"]
    assert float(power_7_check) >= 0


def test_dect_jam_button_up_7p():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    power_7_check = parser["power"]["power_7"]
    assert float(power_7_check) <= 100

# test dect jam power channel 8


def test_dect_jam_button_low_8p():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    power_8_check = parser["power"]["power_8"]
    assert float(power_8_check) >= 0


def test_dect_jam_button_up_8p():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    power_8_check = parser["power"]["power_8"]
    assert float(power_8_check) <= 100

#
#
# test dect jam bandwidth channel 1
#
#


def test_dect_jam_button_low_1b():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    bandwidth_check_1 = parser["bandwidth"]["bw_1"]
    assert float(bandwidth_check_1) >= 0


def test_dect_jam_button_up_1b():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    bandwidth_check_1 = parser["bandwidth"]["bw_1"]
    assert float(bandwidth_check_1) <= 100

# test dect jam button bandwidth channel 2


def test_dect_jam_button_low_2b():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    bandwidth_check_2 = parser["bandwidth"]["bw_2"]
    assert float(bandwidth_check_2) >= 0


def test_dect_jam_button_up_2b():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    bandwidth_check_2 = parser["bandwidth"]["bw_2"]
    assert float(bandwidth_check_2) <= 100

# test dect jam button bandwidth channel 3


def test_dect_jam_button_low_3b():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    bandwidth_check_3 = parser["bandwidth"]["bw_3"]
    assert float(bandwidth_check_3) >= 0


def test_dect_jam_button_up_3b():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    bandwidth_check_3 = parser["bandwidth"]["bw_3"]
    assert float(bandwidth_check_3) <= 100

# test dect jam button bandwidth channel 4


def test_dect_jam_button_low_4b():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    bandwidth_check_4 = parser["bandwidth"]["bw_4"]
    assert float(bandwidth_check_4) >= 0


def test_dect_jam_button_up_4b():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    bandwidth_check_4 = parser["bandwidth"]["bw_4"]
    assert float(bandwidth_check_4) <= 100

# test dect jam button bandwitdth channel 5


def test_dect_jam_button_low_5b():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    bandwidth_check_5 = parser["bandwidth"]["bw_5"]
    assert float(bandwidth_check_5) >= 0


def test_dect_jam_button_up_5b():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    bandwidth_check_5 = parser["bandwidth"]["bw_5"]
    assert float(bandwidth_check_5) <= 100

# test dect jam button bandwitdth channel 6


def test_dect_jam_button_low_6b():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    bandwidth_check_6 = parser["bandwidth"]["bw_6"]
    assert float(bandwidth_check_6) >= 0


def test_dect_jam_button_up_6b():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    bandwidth_check_6 = parser["bandwidth"]["bw_6"]
    assert float(bandwidth_check_6) <= 100

# test dect jam button bandwitdth channel 7


def test_dect_jam_button_low_7b():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    bandwidth_check_7 = parser["bandwidth"]["bw_7"]
    assert float(bandwidth_check_7) >= 0


def test_dect_jam_button_up_7b():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    bandwidth_check_7 = parser["bandwidth"]["bw_7"]
    assert float(bandwidth_check_7) <= 100

# test dect jam button bandwitdth channel 8


def test_dect_jam_button_low_8b():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    bandwidth_check_8 = parser["bandwidth"]["bw_8"]
    assert float(bandwidth_check_8) >= 0


def test_dect_jam_button_up_8b():
    parser, _ = read_config(file="./src/gui/_configs/mission_charlie.ini")

    bandwidth_check_8 = parser["bandwidth"]["bw_8"]
    assert float(bandwidth_check_8) <= 100

#
#
#
#
#
#
#
#
#
#
# test zigbee bts jam button

#
#
# test zigbee bts jam frequecny channel 1
#
#


def test_zigbee_jam_button_low_1f():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    freq_1_check = parser["freq"]["freq_1"]
    assert float(freq_1_check) >= 50


def test_zigbee_jam_button_up_1f():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    freq_1_check = parser["freq"]["freq_1"]
    assert float(freq_1_check) <= 6400

# test zigbee jam button frequency channel 2


def test_zigbee_jam_button_low_2f():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    freq_2_check = parser["freq"]["freq_2"]
    assert float(freq_2_check) >= 50


def test_zigbee_jam_button_up_2f():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    freq_2_check = parser["freq"]["freq_2"]
    assert float(freq_2_check) <= 6400

# test zigbee jam button frequency channel 3


def test_zigbee_jam_button_low_3f():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    freq_3_check = parser["freq"]["freq_3"]
    assert float(freq_3_check) >= 50


def test_zigbee_jam_button_up_3f():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    freq_3_check = parser["freq"]["freq_3"]
    assert float(freq_3_check) <= 6400

# test zigbee jam button frequency channel 4


def test_zigbee_jam_button_low_4f():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    freq_4_check = parser["freq"]["freq_4"]
    assert float(freq_4_check) >= 50


def test_zigbee_jam_button_up_4f():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    freq_4_check = parser["freq"]["freq_4"]
    assert float(freq_4_check) <= 6400

# test zigbee jam button frequency channel 5


def test_zigbee_jam_button_low_5f():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    freq_5_check = parser["freq"]["freq_5"]
    assert float(freq_5_check) >= 50


def test_zigbee_jam_button_up_5f():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    freq_5_check = parser["freq"]["freq_5"]
    assert float(freq_5_check) <= 6400

# test zigbee jam button frequency channel 6


def test_zigbee_jam_button_low_6f():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    freq_6_check = parser["freq"]["freq_6"]
    assert float(freq_6_check) >= 50


def test_zigbee_jam_button_up_6f():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    freq_6_check = parser["freq"]["freq_6"]
    assert float(freq_6_check) <= 6400

# test zigbee jam button frequency channel 7


def test_zigbee_jam_button_low_7f():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    freq_7_check = parser["freq"]["freq_7"]
    assert float(freq_7_check) >= 50


def test_zigbee_jam_button_up_7f():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    freq_7_check = parser["freq"]["freq_7"]
    assert float(freq_7_check) <= 6400

# test zigbee jam button frequency channel 8


def test_zigbee_jam_button_low_8f():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    freq_8_check = parser["freq"]["freq_8"]
    assert float(freq_8_check) >= 50


def test_zigbee_jam_button_up_8f():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    freq_8_check = parser["freq"]["freq_8"]
    assert float(freq_8_check) <= 6400


#
#
# test zigbee bts jam power channel 1
#
#

def test_zigbee_jam_button_low_1p():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    power_1_check = parser["power"]["power_1"]
    assert float(power_1_check) >= 0


def test_zigbee_jam_button_up_1p():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    power_1_check = parser["power"]["power_1"]
    assert float(power_1_check) <= 100

# test zigbee jam power channel 2


def test_zigbee_jam_button_low_2p():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    power_2_check = parser["power"]["power_2"]
    assert float(power_2_check) >= 0


def test_zigbee_jam_button_up_2p():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    power_2_check = parser["power"]["power_2"]
    assert float(power_2_check) <= 100

# test zigbee jam power channel 3


def test_zigbee_jam_button_low_3p():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    power_3_check = parser["power"]["power_3"]
    assert float(power_3_check) >= 0


def test_zigbee_jam_button_up_3p():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    power_3_check = parser["power"]["power_3"]
    assert float(power_3_check) <= 100

# test zigbee jam power channel 4


def test_zigbee_jam_button_low_4p():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    power_4_check = parser["power"]["power_4"]
    assert float(power_4_check) >= 0


def test_zigbee_jam_button_up_4p():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    power_4_check = parser["power"]["power_4"]
    assert float(power_4_check) <= 100

# test zigbee jam power channel 5


def test_zigbee_jam_button_low_5p():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    power_5_check = parser["power"]["power_5"]
    assert float(power_5_check) >= 0


def test_zigbee_jam_button_up_5p():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    power_5_check = parser["power"]["power_5"]
    assert float(power_5_check) <= 100

# test rougue jam power channel 6


def test_zigbee_jam_button_low_6p():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    power_6_check = parser["power"]["power_6"]
    assert float(power_6_check) >= 0


def test_zigbee_jam_button_up_6p():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    power_6_check = parser["power"]["power_6"]
    assert float(power_6_check) <= 100

# test zigbee jam power channel 7


def test_zigbee_jam_button_low_7p():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    power_7_check = parser["power"]["power_7"]
    assert float(power_7_check) >= 0


def test_zigbee_jam_button_up_7p():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    power_7_check = parser["power"]["power_7"]
    assert float(power_7_check) <= 100

# test zigbee jam power channel 8


def test_zigbee_jam_button_low_8p():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    power_8_check = parser["power"]["power_8"]
    assert float(power_8_check) >= 0


def test_zigbee_jam_button_up_8p():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    power_8_check = parser["power"]["power_8"]
    assert float(power_8_check) <= 100


#
#
# test zigbee jam bandwidth channel 1
#
#

def test_zigbee_jam_button_low_1b():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    bandwidth_check_1 = parser["bandwidth"]["bw_1"]
    assert float(bandwidth_check_1) >= 0


def test_zigbee_jam_button_up_1b():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    bandwidth_check_1 = parser["bandwidth"]["bw_1"]
    assert float(bandwidth_check_1) <= 100

# test zigbee jam button bandwidth channel 2


def test_zigbee_jam_button_low_2b():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    bandwidth_check_2 = parser["bandwidth"]["bw_2"]
    assert float(bandwidth_check_2) >= 0


def test_zigbee_jam_button_up_2b():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    bandwidth_check_2 = parser["bandwidth"]["bw_2"]
    assert float(bandwidth_check_2) <= 100

# test zigbee jam button bandwidth channel 3


def test_zigbee_jam_button_low_3b():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    bandwidth_check_3 = parser["bandwidth"]["bw_3"]
    assert float(bandwidth_check_3) >= 0


def test_zigbee_jam_button_up_3b():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    bandwidth_check_3 = parser["bandwidth"]["bw_3"]
    assert float(bandwidth_check_3) <= 100

# test dect jam button bandwidth channel 4


def test_zigbee_jam_button_low_4b():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    bandwidth_check_4 = parser["bandwidth"]["bw_4"]
    assert float(bandwidth_check_4) >= 0


def test_zigbee_jam_button_up_4b():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    bandwidth_check_4 = parser["bandwidth"]["bw_4"]
    assert float(bandwidth_check_4) <= 100

# test zigbee jam button bandwitdth channel 5


def test_dect_jam_button_low_5b():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    bandwidth_check_5 = parser["bandwidth"]["bw_5"]
    assert float(bandwidth_check_5) >= 0


def test_zigbee_jam_button_up_5b():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    bandwidth_check_5 = parser["bandwidth"]["bw_5"]
    assert float(bandwidth_check_5) <= 100

# test zigbee jam button bandwitdth channel 6


def test_zigbee_jam_button_low_6b():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    bandwidth_check_6 = parser["bandwidth"]["bw_6"]
    assert float(bandwidth_check_6) >= 0


def test_zigbee_jam_button_up_6b():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    bandwidth_check_6 = parser["bandwidth"]["bw_6"]
    assert float(bandwidth_check_6) <= 100

# test zigbee jam button bandwitdth channel 7


def test_zigbee_jam_button_low_7b():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    bandwidth_check_7 = parser["bandwidth"]["bw_7"]
    assert float(bandwidth_check_7) >= 0


def test_zigbee_jam_button_up_7b():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    bandwidth_check_7 = parser["bandwidth"]["bw_7"]
    assert float(bandwidth_check_7) <= 100

# test zigbee jam button bandwitdth channel 8


def test_zigbee_jam_button_low_8b():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    bandwidth_check_8 = parser["bandwidth"]["bw_8"]
    assert float(bandwidth_check_8) >= 0


def test_zigbee_jam_button_up_8b():
    parser, _ = read_config(file="./src/gui/_configs/mission_delta.ini")

    bandwidth_check_8 = parser["bandwidth"]["bw_8"]
    assert float(bandwidth_check_8) <= 100


#
#
#
#
#
#
#
#
#
#
#
# test sat phone button

#
#
# test sat phone jam frequency channel 1
#
#

def test_sat_jam_button_low_1f():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    freq_1_check = parser["freq"]["freq_1"]
    assert float(freq_1_check) >= 50


def test_sat_jam_button_up_1f():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    freq_1_check = parser["freq"]["freq_1"]
    assert float(freq_1_check) <= 6400

# test sat jam button frequency channel 2


def test_sat_jam_button_low_2f():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    freq_2_check = parser["freq"]["freq_2"]
    assert float(freq_2_check) >= 50


def test_sat_jam_button_up_2f():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    freq_2_check = parser["freq"]["freq_2"]
    assert float(freq_2_check) <= 6400

# test sat jam button frequency channel 3


def test_sat_jam_button_low_3f():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    freq_3_check = parser["freq"]["freq_3"]
    assert float(freq_3_check) >= 50


def test_sat_jam_button_up_3f():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    freq_3_check = parser["freq"]["freq_3"]
    assert float(freq_3_check) <= 6400

# test sat jam button frequency channel 4


def test_sat_jam_button_low_4f():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    freq_4_check = parser["freq"]["freq_4"]
    assert float(freq_4_check) >= 50


def test_sat_jam_button_up_4f():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    freq_4_check = parser["freq"]["freq_4"]
    assert float(freq_4_check) <= 6400

# test sat jam button frequency channel 5


def test_sat_jam_button_low_5f():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    freq_5_check = parser["freq"]["freq_5"]
    assert float(freq_5_check) >= 50


def test_sat_jam_button_up_5f():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    freq_5_check = parser["freq"]["freq_5"]
    assert float(freq_5_check) <= 6400

# test sat jam button frequency channel 6


def test_sat_jam_button_low_6f():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    freq_6_check = parser["freq"]["freq_6"]
    assert float(freq_6_check) >= 50


def test_sat_jam_button_up_6f():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    freq_6_check = parser["freq"]["freq_6"]
    assert float(freq_6_check) <= 6400

# test sat jam button frequency channel 7


def test_sat_jam_button_low_7f():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    freq_7_check = parser["freq"]["freq_7"]
    assert float(freq_7_check) >= 50


def test_sat_jam_button_up_7f():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    freq_7_check = parser["freq"]["freq_7"]
    assert float(freq_7_check) <= 6400

# test sat jam button frequency channel 8


def test_sat_jam_button_low_8f():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    freq_8_check = parser["freq"]["freq_8"]
    assert float(freq_8_check) >= 50


def test_sat_jam_button_up_8f():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    freq_8_check = parser["freq"]["freq_8"]
    assert float(freq_8_check) <= 6400

#
#
# test sat jam power channel 1
#
#


def test_sat_jam_button_low_1p():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    power_1_check = parser["power"]["power_1"]
    assert float(power_1_check) >= 0


def test_sat_jam_button_up_1p():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    power_1_check = parser["power"]["power_1"]
    assert float(power_1_check) <= 100

# test sat jam power channel 2


def test_sat_jam_button_low_2p():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    power_2_check = parser["power"]["power_2"]
    assert float(power_2_check) >= 0


def test_sat_jam_button_up_2p():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    power_2_check = parser["power"]["power_2"]
    assert float(power_2_check) <= 100

# test sat jam power channel 3


def test_sat_jam_button_low_3p():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    power_3_check = parser["power"]["power_3"]
    assert float(power_3_check) >= 0


def test_sat_jam_button_up_3p():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    power_3_check = parser["power"]["power_3"]
    assert float(power_3_check) <= 100

# test sat jam power channel 4


def test_sat_jam_button_low_4p():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    power_4_check = parser["power"]["power_4"]
    assert float(power_4_check) >= 0


def test_sat_jam_button_up_4p():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    power_4_check = parser["power"]["power_4"]
    assert float(power_4_check) <= 100

# test sat jam power channel 5


def test_sat_jam_button_low_5p():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    power_5_check = parser["power"]["power_5"]
    assert float(power_5_check) >= 0


def test_sat_jam_button_up_5p():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    power_5_check = parser["power"]["power_5"]
    assert float(power_5_check) <= 100

# test sat jam power channel 6


def test_sat_jam_button_low_6p():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    power_6_check = parser["power"]["power_6"]
    assert float(power_6_check) >= 0


def test_sat_jam_button_up_6p():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    power_6_check = parser["power"]["power_6"]
    assert float(power_6_check) <= 100

# test sat jam power channel 7


def test_sat_jam_button_low_7p():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    power_7_check = parser["power"]["power_7"]
    assert float(power_7_check) >= 0


def test_sat_jam_button_up_7p():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    power_7_check = parser["power"]["power_7"]
    assert float(power_7_check) <= 100

# test sat jam power channel 8


def test_sat_jam_button_low_8p():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    power_8_check = parser["power"]["power_8"]
    assert float(power_8_check) >= 0


def test_sat_jam_button_up_8p():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    power_8_check = parser["power"]["power_8"]
    assert float(power_8_check) <= 100

#
#
# test sat jam bandwidth channel 1
#
#


def test_sat_jam_button_low_1b():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    bandwidth_check_1 = parser["bandwidth"]["bw_1"]
    assert float(bandwidth_check_1) >= 0


def test_sat_jam_button_up_1b():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    bandwidth_check_1 = parser["bandwidth"]["bw_1"]
    assert float(bandwidth_check_1) <= 100

# test sat jam button bandwidth channel 2


def test_sat_jam_button_low_2b():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    bandwidth_check_2 = parser["bandwidth"]["bw_2"]
    assert float(bandwidth_check_2) >= 0


def test_sat_jam_button_up_2b():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    bandwidth_check_2 = parser["bandwidth"]["bw_2"]
    assert float(bandwidth_check_2) <= 100

# test sat jam button bandwidth channel 3


def test_sat_jam_button_low_3b():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    bandwidth_check_3 = parser["bandwidth"]["bw_3"]
    assert float(bandwidth_check_3) >= 0


def test_sat_jam_button_up_3b():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    bandwidth_check_3 = parser["bandwidth"]["bw_3"]
    assert float(bandwidth_check_3) <= 100

# test sat jam button bandwidth channel 4


def test_sat_jam_button_low_4b():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    bandwidth_check_4 = parser["bandwidth"]["bw_4"]
    assert float(bandwidth_check_4) >= 0


def test_sat_jam_button_up_4b():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    bandwidth_check_4 = parser["bandwidth"]["bw_4"]
    assert float(bandwidth_check_4) <= 100

# test sat jam button bandwitdth channel 5


def test_sat_jam_button_low_5b():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    bandwidth_check_5 = parser["bandwidth"]["bw_5"]
    assert float(bandwidth_check_5) >= 0


def test_sat_jam_button_up_5b():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    bandwidth_check_5 = parser["bandwidth"]["bw_5"]
    assert float(bandwidth_check_5) <= 100

# test sat jam button bandwitdth channel 6


def test_sat_jam_button_low_6b():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    bandwidth_check_6 = parser["bandwidth"]["bw_6"]
    assert float(bandwidth_check_6) >= 0


def test_sat_jam_button_up_6b():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    bandwidth_check_6 = parser["bandwidth"]["bw_6"]
    assert float(bandwidth_check_6) <= 100

# test sat jam button bandwitdth channel 7


def test_sat_jam_button_low_7b():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    bandwidth_check_7 = parser["bandwidth"]["bw_7"]
    assert float(bandwidth_check_7) >= 0


def test_sat_jam_button_up_7b():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    bandwidth_check_7 = parser["bandwidth"]["bw_7"]
    assert float(bandwidth_check_7) <= 100

# test sat jam button bandwitdth channel 8


def test_sat_jam_button_low_8b():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    bandwidth_check_8 = parser["bandwidth"]["bw_8"]
    assert float(bandwidth_check_8) >= 0


def test_sat_jam_button_up_8b():
    parser, _ = read_config(file="./src/gui/_configs/mission_echo.ini")

    bandwidth_check_8 = parser["bandwidth"]["bw_8"]
    assert float(bandwidth_check_8) <= 100

#
#
#
#
#
#
#
#
#
#
#
# test ism jam button

#
#
# test ism jam frequency channel 1
#
#


def test_ism_jam_button_low_1f():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    freq_1_check = parser["freq"]["freq_1"]
    assert float(freq_1_check) >= 50


def test_ism_jam_button_up_1f():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    freq_1_check = parser["freq"]["freq_1"]
    assert float(freq_1_check) <= 6400

# test ism jam button frequency channel 2


def test_ism_jam_button_low_2f():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    freq_2_check = parser["freq"]["freq_2"]
    assert float(freq_2_check) >= 50


def test_ism_jam_button_up_2f():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    freq_2_check = parser["freq"]["freq_2"]
    assert float(freq_2_check) <= 6400

# test ism jam button frequency channel 3


def test_ism_jam_button_low_3f():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    freq_3_check = parser["freq"]["freq_3"]
    assert float(freq_3_check) >= 50


def test_ism_jam_button_up_3f():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    freq_3_check = parser["freq"]["freq_3"]
    assert float(freq_3_check) <= 6400

# test ism jam button frequency channel 4


def test_ism_jam_button_low_4f():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    freq_4_check = parser["freq"]["freq_4"]
    assert float(freq_4_check) >= 50


def test_ism_jam_button_up_4f():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    freq_4_check = parser["freq"]["freq_4"]
    assert float(freq_4_check) <= 6400

# test ism jam button frequency channel 5


def test_ism_jam_button_low_5f():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    freq_5_check = parser["freq"]["freq_5"]
    assert float(freq_5_check) >= 50


def test_ism_jam_button_up_5f():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    freq_5_check = parser["freq"]["freq_5"]
    assert float(freq_5_check) <= 6400

# test ism jam button frequency channel 6


def test_ism_jam_button_low_6f():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    freq_6_check = parser["freq"]["freq_6"]
    assert float(freq_6_check) >= 50


def test_ism_jam_button_up_6f():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    freq_6_check = parser["freq"]["freq_6"]
    assert float(freq_6_check) <= 6400

# test ism jam button frequency channel 7


def test_ism_jam_button_low_7f():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    freq_7_check = parser["freq"]["freq_7"]
    assert float(freq_7_check) >= 50


def test_ism_jam_button_up_7f():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    freq_7_check = parser["freq"]["freq_7"]
    assert float(freq_7_check) <= 6400

# test ism jam button frequency channel 8


def test_ism_jam_button_low_8f():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    freq_8_check = parser["freq"]["freq_8"]
    assert float(freq_8_check) >= 50


def test_ism_jam_button_up_8f():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    freq_8_check = parser["freq"]["freq_8"]
    assert float(freq_8_check) <= 6400

#
#
# test ism jam power channel 1
#
#


def test_ism_jam_button_low_1p():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    power_1_check = parser["power"]["power_1"]
    assert float(power_1_check) >= 0


def test_ism_jam_button_up_1p():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    power_1_check = parser["power"]["power_1"]
    assert float(power_1_check) <= 100

# test ism jam power channel 2


def test_ism_jam_button_low_2p():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    power_2_check = parser["power"]["power_2"]
    assert float(power_2_check) >= 0


def test_ism_jam_button_up_2p():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    power_2_check = parser["power"]["power_2"]
    assert float(power_2_check) <= 100

# test ism jam power channel 3


def test_ism_jam_button_low_3p():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    power_3_check = parser["power"]["power_3"]
    assert float(power_3_check) >= 0


def test_ism_jam_button_up_3p():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    power_3_check = parser["power"]["power_3"]
    assert float(power_3_check) <= 100

# test ism jam power channel 4


def test_ism_jam_button_low_4p():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    power_4_check = parser["power"]["power_4"]
    assert float(power_4_check) >= 0


def test_ism_jam_button_up_4p():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    power_4_check = parser["power"]["power_4"]
    assert float(power_4_check) <= 100

# test ism jam power channel 5


def test_ism_jam_button_low_5p():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    power_5_check = parser["power"]["power_5"]
    assert float(power_5_check) >= 0


def test_ism_jam_button_up_5p():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    power_5_check = parser["power"]["power_5"]
    assert float(power_5_check) <= 100

# test ism jam power channel 6


def test_ism_jam_button_low_6p():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    power_6_check = parser["power"]["power_6"]
    assert float(power_6_check) >= 0


def test_ism_jam_button_up_6p():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    power_6_check = parser["power"]["power_6"]
    assert float(power_6_check) <= 100

# test ism jam power channel 7


def test_ism_jam_button_low_7p():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    power_7_check = parser["power"]["power_7"]
    assert float(power_7_check) >= 0


def test_ism_jam_button_up_7p():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    power_7_check = parser["power"]["power_7"]
    assert float(power_7_check) <= 100

# test ism jam power channel 8


def test_ism_jam_button_low_8p():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    power_8_check = parser["power"]["power_8"]
    assert float(power_8_check) >= 0


def test_ism_jam_button_up_8p():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    power_8_check = parser["power"]["power_8"]
    assert float(power_8_check) <= 100


#
#
# test ism jam bandwidth channel 1
#
#

def test_ism_jam_button_low_1b():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    bandwidth_check_1 = parser["bandwidth"]["bw_1"]
    assert float(bandwidth_check_1) >= 0


def test_ism_jam_button_up_1b():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    bandwidth_check_1 = parser["bandwidth"]["bw_1"]
    assert float(bandwidth_check_1) <= 100

# test ism jam button bandwidth channel 2


def test_ism_jam_button_low_2b():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    bandwidth_check_2 = parser["bandwidth"]["bw_2"]
    assert float(bandwidth_check_2) >= 0


def test_ism_jam_button_up_2b():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    bandwidth_check_2 = parser["bandwidth"]["bw_2"]
    assert float(bandwidth_check_2) <= 100

# test ism jam button bandwidth channel 3


def test_ism_jam_button_low_3b():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    bandwidth_check_3 = parser["bandwidth"]["bw_3"]
    assert float(bandwidth_check_3) >= 0


def test_ism_jam_button_up_3b():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    bandwidth_check_3 = parser["bandwidth"]["bw_3"]
    assert float(bandwidth_check_3) <= 100

# test ism jam button bandwidth channel 4


def test_ism_jam_button_low_4b():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    bandwidth_check_4 = parser["bandwidth"]["bw_4"]
    assert float(bandwidth_check_4) >= 0


def test_ism_jam_button_up_4b():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    bandwidth_check_4 = parser["bandwidth"]["bw_4"]
    assert float(bandwidth_check_4) <= 100

# test ism jam button bandwidth channel 5


def test_ism_jam_button_low_5b():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    bandwidth_check_5 = parser["bandwidth"]["bw_5"]
    assert float(bandwidth_check_5) >= 0


def test_ism_jam_button_up_5b():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    bandwidth_check_5 = parser["bandwidth"]["bw_5"]
    assert float(bandwidth_check_5) <= 100

# test ism jam button bandwidth channel 6


def test_ism_jam_button_low_6b():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    bandwidth_check_6 = parser["bandwidth"]["bw_6"]
    assert float(bandwidth_check_6) >= 0


def test_ism_jam_button_up_6b():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    bandwidth_check_6 = parser["bandwidth"]["bw_6"]
    assert float(bandwidth_check_6) <= 100


# test ism jam button bandwitdth channel 7


def test_ism_jam_button_low_7b():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    bandwidth_check_7 = parser["bandwidth"]["bw_7"]
    assert float(bandwidth_check_7) >= 0


def test_ism_jam_button_up_7b():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    bandwidth_check_7 = parser["bandwidth"]["bw_7"]
    assert float(bandwidth_check_7) <= 100

# test ism jam button bandwitdth channel 8


def test_ism_jam_button_low_8b():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    bandwidth_check_8 = parser["bandwidth"]["bw_8"]
    assert float(bandwidth_check_8) >= 0


def test_ism_jam_button_up_8b():
    parser, _ = read_config(file="./src/gui/_configs/mission_fox.ini")

    bandwidth_check_8 = parser["bandwidth"]["bw_8"]
    assert float(bandwidth_check_8) <= 100

#
#
#
#
#
#
#
#
#
#
# test tracker tag button
