import configparser


# CONFIG
config = configparser.ConfigParser()
config.read("dwh.cfg")

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create = """
CREATE TABLE IF NOT EXISTS staging_events(
    event_id integer NOT NULL IDENTITY(0,1),
    artist varchar,
    auth varchar,
    firstName varchar,
    gender varchar,
    itemInSession integer,
    lastName varchar,
    length double precision,
    level varchar,
    location varchar,
    method varchar,
    page varchar,
    registration double precision,
    sessionId integer,
    song varchar,
    status integer,
    ts bigint,
    userAgent varchar,
    user_id varchar
"""

staging_songs_table_create = """
CREATE TABLE IF NOT EXISTS staging_songs(
    song_id varchar,
    artist_id varchar,
    artist_latitude double precision,
    artist_location varchar,
    artist_longitude double precision,
    artist_name varchar,
    duration double precision,
    num_songs integer,
    song_id varchar,
    title varchar,
    year integer
)
"""

songplay_table_create = """
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id integer NOT NULL IDENTITY(0,1),
    start_time timestamp NOT NULL SORTKEY,
    user_id varchar NOT NULL,
    level varchar,
    song_id varchar DISTKEY,
    artist_id varchar,
    session_id integer SORTKEY,
    location varchar,
    user_agent varchar,
    PRIMARY KEY (songplay_id),
);
"""

user_table_create = """
CREATE TABLE IF NOT EXISTS users(
    user_id varchar NOT NULL,
    first_name varchar,
    last_name varchar,
    gender varchar,
    level varchar NOT NULL,
    PRIMARY KEY (user_id)
)
diststyle all;
"""

song_table_create = """
CREATE TABLE IF NOT EXISTS songs(
    song_id varchar NOT NULL DISTKEY,
    title varchar,
    artist_id varchar NOT NULL,
    year integer SORTKEY,
    duration double precision,
    PRIMARY KEY (song_id),
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
);
"""

artist_table_create = """
CREATE TABLE IF NOT EXISTS artists(
    artist_id varchar NOT NULL,
    name varchar NOT NULL,
    location varchar,
    latitude double precision,
    longitude double precision,
    PRIMARY KEY (artist_id)
)
diststyle all;
"""

time_table_create = """
CREATE TABLE IF NOT EXISTS time(
    start_time bigint NOT NULL,
    hour integer,
    day integer,
    week integer,
    month integer,
    year integer,
    weekday integer,
    PRIMARY KEY (start_time)
);
"""

# STAGING TABLES

staging_events_copy = (
    """
copy staging_events
from {}
iam_role {}
json {};
"""
).format(
    config.get("S3", "LOG_DATA"),
    config.get("IAM_ROLE", "ARN"),
    config.get("S3", "LOG_JSONPATH"),
)

staging_songs_copy = (
    """
copy staging_songs
from {}
iam_role {}
json 'auto';
"""
).format(config.get("S3", "SONG_DATA"), config.get("IAM_ROLE", "ARN"))

# FINAL TABLES

songplay_table_insert = """
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT
    TIMESTAMP 'epoch' + e.ts * interval '0.001 seconds' as start_time,
    e.user_id,
    e.user_level,
    s.song_id,
    s.artist_id,
    e.session_id,
    e.location,
    e.user_agent
FROM staging_events e
    INNER JOIN staging_songs s
        ON(e.song_title = s.title
            AND e.artist_name = s.artist_name
            AND e.song_length = s.duration)
WHERE e.page = 'NextSong';
"""

user_table_insert = """
INSERT INTO users (user_id, first_name, last_name, gender, level)
SELECT DISTINCT
    user_id,
    user_first_name,
    user_last_name,
    user_gender,
    user_level
FROM staging_events;
"""

song_table_insert = """
INSERT INTO songs (song_id, title, artist_id, year, duration)
SELECT DISTINCT
    song_id,
    title,
    artist_id,
    year,
    duration
FROM staging_songs;
"""

artist_table_insert = """
INSERT INTO artists (artist_id, name, location, latitude, longitude)
SELECT DISTINCT
    artist_id,
    artist_name,
    artist_location,
    artist_latitude,
    artist_longitude
FROM staging_songs;
"""

time_table_insert = """
INSERT INTO time(start_time, hour, day, week, month, year, weekDay)
SELECT start_time,
    extract(hour from start_time),
    extract(day from start_time),
    extract(week from start_time),
    extract(month from start_time),
    extract(year from start_time),
    extract(dayofweek from start_time)
FROM songplays
"""

# QUERY LISTS

create_table_queries = [
    staging_events_table_create,
    staging_songs_table_create,
    songplay_table_create,
    user_table_create,
    song_table_create,
    artist_table_create,
    time_table_create,
]
drop_table_queries = [
    staging_events_table_drop,
    staging_songs_table_drop,
    songplay_table_drop,
    user_table_drop,
    song_table_drop,
    artist_table_drop,
    time_table_drop,
]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [
    songplay_table_insert,
    user_table_insert,
    song_table_insert,
    artist_table_insert,
    time_table_insert,
]
