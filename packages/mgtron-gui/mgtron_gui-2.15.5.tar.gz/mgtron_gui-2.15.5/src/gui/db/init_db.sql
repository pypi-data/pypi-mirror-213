CREATE TABLE IF NOT EXISTS save_name (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datetime TEXT NOT NULL,
    date_accessed TEXT NOT NULL,
    date_added TEXT NOT NULL,
    name TEXT NOT NULL UNIQUE,
    channel_1 TEXT,
    channel_2 TEXT,
    channel_3 TEXT,
    channel_4 TEXT,
    channel_5 TEXT,
    channel_6 TEXT,
    channel_7 TEXT,
    channel_8 TEXT,
    FOREIGN KEY (channel_1) REFERENCES channel_1(save_name_id),
    FOREIGN KEY (channel_2) REFERENCES channel_2(save_name_id),
    FOREIGN KEY (channel_3) REFERENCES channel_3(save_name_id),
    FOREIGN KEY (channel_4) REFERENCES channel_4(save_name_id),
    FOREIGN KEY (channel_5) REFERENCES channel_5(save_name_id),
    FOREIGN KEY (channel_6) REFERENCES channel_6(save_name_id),
    FOREIGN KEY (channel_7) REFERENCES channel_7(save_name_id),
    FOREIGN KEY (channel_8) REFERENCES channel_8(save_name_id)
);

CREATE TABLE IF NOT EXISTS channel_1 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    save_name_id TEXT NOT NULL,
    frequency REAL NOT NULL,
    power INTEGER NOT NULL,
    bandwidth INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS channel_2 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    save_name_id TEXT NOT NULL,
    frequency REAL NOT NULL,
    power INTEGER NOT NULL,
    bandwidth INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS channel_3 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    save_name_id TEXT NOT NULL,
    frequency REAL NOT NULL,
    power INTEGER NOT NULL,
    bandwidth INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS channel_4 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    save_name_id TEXT NOT NULL,
    frequency REAL NOT NULL,
    power INTEGER NOT NULL,
    bandwidth INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS channel_5 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    save_name_id TEXT NOT NULL,
    frequency REAL NOT NULL,
    power INTEGER NOT NULL,
    bandwidth INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS channel_6 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    save_name_id TEXT NOT NULL,
    frequency REAL NOT NULL,
    power INTEGER NOT NULL,
    bandwidth INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS channel_7 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    save_name_id TEXT NOT NULL,
    frequency REAL NOT NULL,
    power INTEGER NOT NULL,
    bandwidth INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS channel_8 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    save_name_id TEXT NOT NULL,
    frequency REAL NOT NULL,
    power INTEGER NOT NULL,
    bandwidth INTEGER NOT NULL
);