from pathlib import Path
import sqlite3
import pytest
from src.gui.db.models import delete_sql_save_data, get_sql_details
from src.gui.db.models import get_sql_save_names
from src.gui.db.models import save_to_database
from src.gui.helpers import BANDS, convert_power
from src.gui.helpers import FREQ
from src.gui.helpers import NAME
from src.gui.helpers import POWS
from src.gui.helpers import kill_channel
from src.gui.helpers import version_getter
from src.gui.interface import format_output

scan_results: dict = {}  # find_signals_and_frequencies()

test_db_path: str | Path = Path("test.db")


def test_kill_channel() -> None:
    assert kill_channel.__name__


@pytest.mark.skip
def test_wifi_scanner():
    assert isinstance(scan_results, dict)


@pytest.mark.skip
def test_frequency_and_signal_value_exists():
    x = scan_results
    assert len(x) != 0, "Dictionary should not be empty"


@pytest.mark.skip
def test_frequency_for_string():
    assert "Infra" not in scan_results.items()


@pytest.mark.skip
def test_frequency_value():
    assert 2412 or 5220 in scan_results.values()


@pytest.mark.skip
def test_frequency_value2():
    assert 2437 or 2462 in scan_results.values()


@pytest.mark.skip
def test_signal_string():
    assert "MHz" not in scan_results


def test_version_getter():
    assert isinstance(version_getter(), str)


def test_version_are_numbers():
    # parse the version string
    version: str = str(version_getter())
    version = version.split(".")  # type: ignore

    # check if the version is a number
    assert version[0].isdigit()
    assert version[1].isdigit()
    assert version[2].isdigit()


def test_format_output_returns_tuple():
    assert isinstance(
        format_output(
            lambda x: [
                """Command: 's'\r\n-Channel 1 Status-\r\nFrequency: 650.00MHz\r\nPower: 0\r\nBandwidth: 0.00%\r\n\r\n-Channel 2 Status-\r\nFrequency: 1300.00MHz\r\nPower: 0\r\nBandwidth: 0.00%\r\n\r\n-Channel 3 Status-\r\nFrequency: 1950.00MHz\r\nPower: 0\r\nBandwidth: 0.00%\r\n\r\n-Channel 4 Status-\r\nFrequency: 2600.00MHz\r\nPower: 0\r\nBandwidth: 0.00%\r\n\r\n-Channel 5 Status-\r\nFrequency: 3250.00MHz\r\nPower: 0\r\nBandwidth: 0.00%\r\n\r\n-Channel 6 Status-\r\nFrequency: 3900.00MHz\r\nPower: 0\r\nBandwidth: 0.00%\r\n\r\n-Channel 7 Status-\r\nFrequency: 4550.00MHz\r\nPower: 0\r\nBandwidth: 0.00%\r\n\r\n-Channel 8 Status-\r\nFrequency: 5200.00MHz\r\nPower: 0\r\nBandwidth: 0.00%\r\n\r\nNew command: $"""  # noqa: E501
            ]  # type: ignore
        ),
        dict,
    )


# @pytest.mark.skip
def test_save_to_database_1():
    # Call the function to save data to the database
    test_data: list[dict[str, str]] = [
        {
            "save_name": "Test save 1",
            "power": "100",
            "bandwidth": "10",
            "frequency": "1000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 1",
            "power": "200",
            "bandwidth": "20",
            "frequency": "2000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 1",
            "power": "300",
            "bandwidth": "30",
            "frequency": "3000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 1",
            "power": "400",
            "bandwidth": "40",
            "frequency": "4000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 1",
            "power": "500",
            "bandwidth": "50",
            "frequency": "5000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 1",
            "power": "600",
            "bandwidth": "60",
            "frequency": "6000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 1",
            "power": "700",
            "bandwidth": "70",
            "frequency": "7000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 1",
            "power": "800",
            "bandwidth": "80",
            "frequency": "8000",
            "date": "2023-04-07 12:00:00",
        },
    ]
    save_to_database(test_data, test_db_path)

    data = get_sql_details("Test save 1", test_db_path)

    # Connect to the database using a context manager

    with sqlite3.connect(test_db_path) as conn:
        # Get a cursor object
        cursor = conn.cursor()

        # Cleanup: Delete the test record from the tables
        cursor.execute("DELETE FROM save_name WHERE name = 'Test save 1'")
        cursor.execute(
            "DELETE FROM\
                channel_1 WHERE save_name_id = 'Test save 1'"
        )
        cursor.execute(
            "DELETE FROM\
                channel_2 WHERE save_name_id = 'Test save 1'"
        )
        cursor.execute(
            "DELETE FROM\
                channel_3 WHERE save_name_id = 'Test save 1'"
        )
        cursor.execute(
            "DELETE FROM\
                channel_4 WHERE save_name_id = 'Test save 1'"
        )
        cursor.execute(
            "DELETE FROM\
                channel_5 WHERE save_name_id = 'Test save 1'"
        )
        cursor.execute(
            "DELETE FROM\
                channel_6 WHERE save_name_id = 'Test save 1'"
        )
        cursor.execute(
            "DELETE FROM\
                channel_7 WHERE save_name_id = 'Test save 1'"
        )
        cursor.execute(
            "DELETE FROM\
                channel_8 WHERE save_name_id = 'Test save 1'"
        )

        # Check frequency data
        assert data[FREQ["chan_1"]] == 1000.0
        assert data[FREQ["chan_2"]] == 2000.0
        assert data[FREQ["chan_3"]] == 3000.0
        assert data[FREQ["chan_4"]] == 4000.0
        assert data[FREQ["chan_5"]] == 5000.0
        assert data[FREQ["chan_6"]] == 6000.0
        assert data[FREQ["chan_7"]] == 7000.0
        assert data[FREQ["chan_8"]] == 8000.0

        # Check power data
        assert data[POWS["chan_1"]] == 100.0
        assert data[POWS["chan_2"]] == 200.0
        assert data[POWS["chan_3"]] == 300.0
        assert data[POWS["chan_4"]] == 400.0
        assert data[POWS["chan_5"]] == 500.0
        assert data[POWS["chan_6"]] == 600.0
        assert data[POWS["chan_7"]] == 700.0
        assert data[POWS["chan_8"]] == 800.0

        # Check bandwidth data
        assert data[BANDS["chan_1"]] == 10.0
        assert data[BANDS["chan_2"]] == 20.0
        assert data[BANDS["chan_3"]] == 30.0
        assert data[BANDS["chan_4"]] == 40.0
        assert data[BANDS["chan_5"]] == 50.0
        assert data[BANDS["chan_6"]] == 60.0
        assert data[BANDS["chan_7"]] == 70.0
        assert data[BANDS["chan_8"]] == 80.0

        # Check name data
        # assert data[NAME["save_name"]] == "Test save 1"


# @pytest.mark.skip
def test_save_to_database_2():
    # Call the function to save data to the database
    test_data: list[dict[str, str]] = [
        {
            "save_name": "Test save 2",
            "power": "100",
            "bandwidth": "10",
            "frequency": "1000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 2",
            "power": "200",
            "bandwidth": "20",
            "frequency": "2000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 2",
            "power": "300",
            "bandwidth": "30",
            "frequency": "3000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 2",
            "power": "400",
            "bandwidth": "40",
            "frequency": "4000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 2",
            "power": "500",
            "bandwidth": "50",
            "frequency": "5000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 2",
            "power": "600",
            "bandwidth": "60",
            "frequency": "6000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 2",
            "power": "700",
            "bandwidth": "70",
            "frequency": "7000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 2",
            "power": "800",
            "bandwidth": "80",
            "frequency": "8000",
            "date": "2023-04-07 12:00:00",
        },
    ]

    save_to_database(test_data, test_db_path)

    data = get_sql_details("Test save 2", test_db_path)

    # Connect to the database using a context manager
    with sqlite3.connect(test_db_path) as conn:
        # Get a cursor object
        cursor = conn.cursor()

        # Cleanup: Delete the test record from the tables
        cursor.execute("DELETE FROM save_name WHERE name = 'Test save 2'")
        cursor.execute(
            "DELETE FROM\
                channel_1 WHERE save_name_id = 'Test save 2'"
        )
        cursor.execute(
            "DELETE FROM\
                channel_2 WHERE save_name_id = 'Test save 2'"
        )
        cursor.execute(
            "DELETE FROM\
                channel_3 WHERE save_name_id = 'Test save 2'"
        )
        cursor.execute(
            "DELETE FROM\
                channel_4 WHERE save_name_id = 'Test save 2'"
        )
        cursor.execute(
            "DELETE FROM\
                channel_5 WHERE save_name_id = 'Test save 2'"
        )
        cursor.execute(
            "DELETE FROM\
                channel_6 WHERE save_name_id = 'Test save 2'"
        )
        cursor.execute(
            "DELETE FROM\
                channel_7 WHERE save_name_id = 'Test save 2'"
        )
        cursor.execute(
            "DELETE FROM\
                channel_8 WHERE save_name_id = 'Test save 2'"
        )

        # Check frequency data
        assert data[FREQ["chan_1"]] == 1000.0
        assert data[FREQ["chan_2"]] == 2000.0
        assert data[FREQ["chan_3"]] == 3000.0
        assert data[FREQ["chan_4"]] == 4000.0
        assert data[FREQ["chan_5"]] == 5000.0
        assert data[FREQ["chan_6"]] == 6000.0
        assert data[FREQ["chan_7"]] == 7000.0
        assert data[FREQ["chan_8"]] == 8000.0

        # Check power data
        assert data[POWS["chan_1"]] == 100
        assert data[POWS["chan_2"]] == 200
        assert data[POWS["chan_3"]] == 300
        assert data[POWS["chan_4"]] == 400
        assert data[POWS["chan_5"]] == 500
        assert data[POWS["chan_6"]] == 600
        assert data[POWS["chan_7"]] == 700
        assert data[POWS["chan_8"]] == 800

        # Check bandwidth data
        assert data[BANDS["chan_1"]] == 10
        assert data[BANDS["chan_2"]] == 20
        assert data[BANDS["chan_3"]] == 30
        assert data[BANDS["chan_4"]] == 40
        assert data[BANDS["chan_5"]] == 50
        assert data[BANDS["chan_6"]] == 60
        assert data[BANDS["chan_7"]] == 70
        assert data[BANDS["chan_8"]] == 80

        # Check NAME data
        assert data[NAME["chan_1"]] == "Test save 2"
        assert data[NAME["chan_2"]] == "Test save 2"
        assert data[NAME["chan_3"]] == "Test save 2"
        assert data[NAME["chan_4"]] == "Test save 2"
        assert data[NAME["chan_5"]] == "Test save 2"
        assert data[NAME["chan_6"]] == "Test save 2"
        assert data[NAME["chan_7"]] == "Test save 2"
        assert data[NAME["chan_8"]] == "Test save 2"


def test_get_all_names():
    """Test that the get_all_names function returns a list of all save names"""

    test_data: list[dict[str, str]] = [
        {
            "save_name": "Test save 2",
            "power": "100",
            "bandwidth": "10",
            "frequency": "1000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 2",
            "power": "200",
            "bandwidth": "20",
            "frequency": "2000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 2",
            "power": "300",
            "bandwidth": "30",
            "frequency": "3000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 2",
            "power": "400",
            "bandwidth": "40",
            "frequency": "4000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 2",
            "power": "500",
            "bandwidth": "50",
            "frequency": "5000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 2",
            "power": "600",
            "bandwidth": "60",
            "frequency": "6000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 2",
            "power": "700",
            "bandwidth": "70",
            "frequency": "7000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 2",
            "power": "800",
            "bandwidth": "80",
            "frequency": "8000",
            "date": "2023-04-07 12:00:00",
        },
    ]
    save_to_database(test_data, test_db_path)

    test_data: list[dict[str, str]] = [
        {
            "save_name": "Test save 3",
            "power": "100",
            "bandwidth": "10",
            "frequency": "1000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 3",
            "power": "200",
            "bandwidth": "20",
            "frequency": "2000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 3",
            "power": "300",
            "bandwidth": "30",
            "frequency": "3000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 3",
            "power": "400",
            "bandwidth": "40",
            "frequency": "4000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 3",
            "power": "500",
            "bandwidth": "50",
            "frequency": "5000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 3",
            "power": "600",
            "bandwidth": "60",
            "frequency": "6000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 3",
            "power": "700",
            "bandwidth": "70",
            "frequency": "7000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 3",
            "power": "800",
            "bandwidth": "80",
            "frequency": "8000",
            "date": "2023-04-07 12:00:00",
        },
    ]
    save_to_database(test_data, test_db_path)

    names = get_sql_save_names(test_db_path)

    # Connect to the database using a context manager
    with sqlite3.connect(test_db_path) as conn:
        # Get a cursor object
        cursor = conn.cursor()

        # Cleanup: Delete the test record from the tables
        cursor.execute("DELETE FROM save_name WHERE name = 'Test save 2'")
        cursor.execute(
            "DELETE FROM\
             channel_1 WHERE save_name_id = 'Test save 2'"
        )
        cursor.execute(
            "DELETE FROM\
             channel_2 WHERE save_name_id = 'Test save 2'"
        )
        cursor.execute(
            "DELETE FROM\
             channel_3 WHERE save_name_id = 'Test save 2'"
        )
        cursor.execute(
            "DELETE FROM\
             channel_4 WHERE save_name_id = 'Test save 2'"
        )
        cursor.execute(
            "DELETE FROM\
             channel_5 WHERE save_name_id = 'Test save 2'"
        )
        cursor.execute(
            "DELETE FROM\
             channel_6 WHERE save_name_id = 'Test save 2'"
        )
        cursor.execute(
            "DELETE FROM\
             channel_7 WHERE save_name_id = 'Test save 2'"
        )
        cursor.execute(
            "DELETE FROM\
             channel_8 WHERE save_name_id = 'Test save 2'"
        )

        # Cleanup: Delete the test record from the tables
        cursor.execute(
            "DELETE FROM\
             save_name WHERE name = 'Test save 3'"
        )
        cursor.execute(
            "DELETE FROM\
             channel_1 WHERE save_name_id = 'Test save 3'"
        )
        cursor.execute(
            "DELETE FROM\
             channel_2 WHERE save_name_id = 'Test save 3'"
        )
        cursor.execute(
            "DELETE FROM\
             channel_3 WHERE save_name_id = 'Test save 3'"
        )
        cursor.execute(
            "DELETE FROM\
             channel_4 WHERE save_name_id = 'Test save 3'"
        )
        cursor.execute(
            "DELETE FROM\
             channel_5 WHERE save_name_id = 'Test save 3'"
        )
        cursor.execute(
            "DELETE FROM\
             channel_6 WHERE save_name_id = 'Test save 3'"
        )
        cursor.execute(
            "DELETE FROM\
             channel_7 WHERE save_name_id = 'Test save 3'"
        )
        cursor.execute(
            "DELETE FROM\
             channel_8 WHERE save_name_id = 'Test save 3'"
        )

    assert names == ["Test save 2", "Test save 3"]


# @pytest.mark.skip(reason="Memory leak")
def test_delete_db():
    """Test the delete_db function."""

    test_data: list[dict[str, str]] = [
        {
            "save_name": "Test save 4",
            "power": "100",
            "bandwidth": "10",
            "frequency": "1000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 4",
            "power": "200",
            "bandwidth": "20",
            "frequency": "2000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 4",
            "power": "300",
            "bandwidth": "30",
            "frequency": "3000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 4",
            "power": "400",
            "bandwidth": "40",
            "frequency": "4000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 4",
            "power": "500",
            "bandwidth": "50",
            "frequency": "5000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 4",
            "power": "600",
            "bandwidth": "60",
            "frequency": "6000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 4",
            "power": "700",
            "bandwidth": "70",
            "frequency": "7000",
            "date": "2023-04-07 12:00:00",
        },
        {
            "save_name": "Test save 4",
            "power": "800",
            "bandwidth": "80",
            "frequency": "8000",
            "date": "2023-04-07 12:00:00",
        },
    ]

    save_to_database(test_data, test_db_path)

    data = get_sql_save_names(test_db_path)

    assert data[-1] == "Test save 4"

    delete_sql_save_data("Test save 4", test_db_path)

    assert data[-1] != ["Test save 4"]


def test_convert_power_min():
    assert convert_power(power=0) == 0


def test_convert_power_max():
    assert convert_power(power=100) == 63


def test_convert_power_mid():
    assert convert_power(power=50) == 32


def test_convert_power_mid2():
    assert convert_power(power=25) == 16


def test_convert_power_mid3():
    assert convert_power(power=75) == 47
