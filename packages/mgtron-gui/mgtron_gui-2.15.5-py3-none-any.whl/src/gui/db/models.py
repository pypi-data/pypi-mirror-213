"""Database communicatation and execution of the SQL commands."""

from pathlib import Path
import pathlib
import sqlite3
from datetime import datetime


ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
WORKING = ROOT / "gui"

# Define the input values
date_accessed_value = datetime.now().strftime("%Y-%m-%d")

# If the file does not exist create it
db_path: Path = Path(f"{WORKING}/db/mgtron_db.db")
init_path: Path = Path(f"{WORKING}/db/init_db.sql")


def read_sql_query(sql_path: pathlib.Path) -> str:
    """Read an SQL query from a file and returns it as a string."""
    return pathlib.Path(sql_path).read_text()


print("initializing the db")

# init the database
init_db = read_sql_query(init_path)

print("db initialized")

# Populate db if it does not exist
with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.executescript(init_db)
    conn.commit()
    # conn.close()


def save_to_database(
        input_data: list[dict[str, str]],
        db_path: str | Path = db_path):
    """Save the input data to the database."""
    # Open a connection to the database and create a cursor
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.executescript(init_db)
        conn.commit()

        # Insert into the save_name table and get the ID of the newly
        # inserted row
        try:
            cursor.execute(
                "INSERT INTO save_name (datetime, date_added,\
                    date_accessed, name) VALUES (?, ?, ?, ?)",
                (
                    input_data[0]["date"],
                    input_data[0]["date"],
                    input_data[0]["date"],
                    input_data[0]["save_name"],
                ),
            )
        except sqlite3.IntegrityError as e:
            # modal popup a dearpygui window
            print(e)
            # return

        save_name_id = input_data[0]["save_name"]

        # Insert into the channel tables using the save_name_id as a
        # foreign key
        cursor.execute(
            "INSERT INTO channel_1 (save_name_id, frequency,\
                 power, bandwidth) VALUES (?, ?, ?, ?)",
            (
                save_name_id,
                input_data[0]["frequency"],
                input_data[0]["power"],
                input_data[0]["bandwidth"],
            ),
        )
        cursor.execute(
            "INSERT INTO channel_2 (save_name_id, frequency,\
                 power, bandwidth) VALUES (?, ?, ?, ?)",
            (
                save_name_id,
                input_data[1]["frequency"],
                input_data[1]["power"],
                input_data[1]["bandwidth"],
            ),
        )
        cursor.execute(
            "INSERT INTO channel_3 (save_name_id, frequency,\
                 power, bandwidth) VALUES (?, ?, ?, ?)",
            (
                save_name_id,
                input_data[2]["frequency"],
                input_data[2]["power"],
                input_data[2]["bandwidth"],
            ),
        )
        cursor.execute(
            "INSERT INTO channel_4 (save_name_id, frequency,\
                 power, bandwidth) VALUES (?, ?, ?, ?)",
            (
                save_name_id,
                input_data[3]["frequency"],
                input_data[3]["power"],
                input_data[3]["bandwidth"],
            ),
        )
        cursor.execute(
            "INSERT INTO channel_5 (save_name_id, frequency,\
                power, bandwidth) VALUES (?, ?, ?, ?)",
            (
                save_name_id,
                input_data[4]["frequency"],
                input_data[4]["power"],
                input_data[4]["bandwidth"],
            ),
        )
        cursor.execute(
            "INSERT INTO channel_6 (save_name_id, frequency,\
                 power, bandwidth) VALUES (?, ?, ?, ?)",
            (
                save_name_id,
                input_data[5]["frequency"],
                input_data[5]["power"],
                input_data[5]["bandwidth"],
            ),
        )
        cursor.execute(
            "INSERT INTO channel_7 (save_name_id, frequency,\
                 power, bandwidth) VALUES (?, ?, ?, ?)",
            (
                save_name_id,
                input_data[6]["frequency"],
                input_data[6]["power"],
                input_data[6]["bandwidth"],
            ),
        )
        cursor.execute(
            "INSERT INTO channel_8 (save_name_id, frequency,\
                 power, bandwidth) VALUES (?, ?, ?, ?)",
            (
                save_name_id,
                input_data[7]["frequency"],
                input_data[7]["power"],
                input_data[7]["bandwidth"],
            ),
        )

        # Commit the changes to the database
        conn.commit()


def get_sql_details(
    save_name: str, db_path: str | Path = db_path
) -> tuple[
    float,
    int,
    int,
    float,
    int,
    int,
    float,
    int,
    int,
    float,
    int,
    int,
    float,
    int,
    int,
    float,
    int,
    int,
    float,
    int,
    int,
    float,
    int,
    int,
]:
    """Load the data from the database and return it as a tuple."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
            channel_1.frequency,
            channel_1.power,
            channel_1.bandwidth,
            channel_2.frequency,
            channel_2.power,
            channel_2.bandwidth,
            channel_3.frequency,
            channel_3.power,
            channel_3.bandwidth,
            channel_4.frequency,
            channel_4.power,
            channel_4. bandwidth,
            channel_5.frequency,
            channel_5.power,
            channel_5.bandwidth,
            channel_6.frequency,
            channel_6.power,
            channel_6.bandwidth,
            channel_7.frequency,
            channel_7.power,
            channel_7.bandwidth,
            channel_8.frequency,
            channel_8.power,
            channel_8.bandwidth,
            channel_1.save_name_id,
            channel_2.save_name_id,
            channel_3.save_name_id,
            channel_4.save_name_id,
            channel_5.save_name_id,
            channel_6.save_name_id,
            channel_7.save_name_id,
            channel_8.save_name_id
            FROM save_name
            JOIN channel_1 ON channel_1.save_name_id = save_name.name
            JOIN channel_2 ON channel_2.save_name_id = save_name.name
            JOIN channel_3 ON channel_3.save_name_id = save_name.name
            JOIN channel_4 ON channel_4.save_name_id = save_name.name
            JOIN channel_5 ON channel_5.save_name_id = save_name.name
            JOIN channel_6 ON channel_6.save_name_id = save_name.name
            JOIN channel_7 ON channel_7.save_name_id = save_name.name
            JOIN channel_8 ON channel_8.save_name_id = save_name.name
            WHERE save_name.name = ?
            """,
            (save_name,),
        )

        result = cursor.fetchall()

    return result[0]  # type: ignore


def get_sql_save_names(db_path: str | Path = db_path) -> list[str]:
    """Get the save names from the database"""

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM save_name")
        result = cursor.fetchall()
        result = [i[0] for i in result]
        return result


def delete_sql_save_data(save_name: str, db_path: str | Path = db_path):
    """Delete a save name from the database"""

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute("DELETE FROM save_name WHERE name = ?", (save_name,))
        cursor.execute(
            "DELETE FROM\
            channel_1 WHERE save_name_id = ?",
            (save_name,),
        )
        cursor.execute(
            "DELETE FROM\
            channel_2 WHERE save_name_id = ?",
            (save_name,),
        )
        cursor.execute(
            "DELETE FROM\
            channel_3 WHERE save_name_id = ?",
            (save_name,),
        )
        cursor.execute(
            "DELETE FROM\
            channel_4 WHERE save_name_id = ?",
            (save_name,),
        )
        cursor.execute(
            "DELETE FROM\
            channel_5 WHERE save_name_id = ?",
            (save_name,),
        )
        cursor.execute(
            "DELETE FROM\
            channel_6 WHERE save_name_id = ?",
            (save_name,),
        )
        cursor.execute(
            "DELETE FROM\
            channel_7 WHERE save_name_id = ?",
            (save_name,),
        )
        cursor.execute(
            "DELETE FROM\
            channel_8 WHERE save_name_id = ?",
            (save_name,),
        )

        conn.commit()
