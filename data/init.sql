CREATE TABLE IF NOT EXISTS images (
    image_id INTEGER PRIMARY KEY AUTOINCREMENT,
    place_id INTEGER
);

CREATE TABLE IF NOT EXISTS user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    login VARCHAR(127) NOT NULL,
    password BLOB(64) NOT NULL
);

CREATE TABLE IF NOT EXISTS regions (
    region_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS cities (
    city_id INTEGER PRIMARY KEY AUTOINCREMENT,
    region_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS news (
    news_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TINYTEXT NOT NULL,
    image_id INT NOT NULL,
    creation_time TIMESTAMP NOT NULL,
    content MEDIUMTEXT
);

CREATE TABLE IF NOT EXISTS places (
    place_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TINYTEXT NOT NULL,
    city_id INTEGER NOT NULL,
    image_id INTEGER NOT NULL,
    youtube_id VARCHAR(128),
    latitude DOUBLE NOT NULL,
    longitude DOUBLE NOT NULL,
    content MEDIUMTEXT
);