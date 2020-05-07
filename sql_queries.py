import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events
(
    artist text,
    auth text,
    firstName text,
    gender text,
    itemInSession int,
    lastName text,
    length numeric,
    level text,
    location text,
    method text,
    page text,
    registration numeric,
    sessionId int,
    song text,
    status int,
    ts bigint,
    userAgent text,
    userId int
);
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs
(
    num_songs int,
    artist_id text,
    artist_latitude numeric,
    artist_longitude numeric,
    artist_location text,
    artist_name text,
    song_id text,
    title text,
    duration numeric,
    year int 
);
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays
(
    songplay_id INTEGER IDENTITY (1, 1) Primary Key,
    start_time timestamp, 
    user_id int, 
    level text,  
    song_id text, 
    artist_id text, 
    session_id int, 
    location text, 
    user_agent text
)
DISTSTYLE KEY
DISTKEY ( start_time )
SORTKEY ( start_time );
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users
(
    user_id int Primary Key,
    first_name text, 
    last_name text, 
    gender text, 
    level text
)
SORTKEY (user_id);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs
(
    song_id text Primary Key, 
    title text, 
    artist_id text, 
    year int, 
    duration numeric
)
SORTKEY (song_id);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists
(
    artist_id text Primary Key, 
    name text, 
    location text, 
    latitude text, 
    longitude text
)
SORTKEY (artist_id);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time
(
    start_time timestamp without time zone Primary Key, 
    hour int, 
    day int, 
    week int, 
    month int, 
    year int, 
    weekday int
)
DISTSTYLE KEY
DISTKEY ( start_time )
SORTKEY (start_time);
""")

# STAGING TABLES

staging_events_copy = ("""
COPY staging_events
FROM {}
iam_role {}
FORMAT as json {}
region 'us-west-2'
""").format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""
COPY staging_songs
FROM {}
iam_role {}
FORMAT AS json 'auto'
region 'us-west-2'
""").format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN'])

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) 
    SELECT DISTINCT 
                    TIMESTAMP 'epoch' + (se.ts / 1000) * INTERVAL '1 second' as start_time,
                    se.userId,
                    se.level,
                    ss.song_id,
                    ss.artist_id,
                    se.sessionId,
                    se.location,
                    se.userAgent
    FROM staging_events se
    INNER JOIN staging_songs ss ON (se.song = ss.title AND se.artist = ss.artist_name)
    WHERE se.page = 'NextSong' AND start_time IS NOT NULL;
""")

user_table_insert = ("""
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    SELECT DISTINCT
                    userId,
                    firstName,
                    lastName,
                    gender,
                    level
    FROM staging_events
    WHERE userId IS NOT NULL;
""")

song_table_insert = ("""
    INSERT INTO songs (song_id, title, artist_id, year, duration)
    SELECT DISTINCT
                    song_id,
                    title,
                    artist_id,
                    year,
                    duration
    FROM staging_songs
    WHERE song_id IS NOT NULL;
""")

artist_table_insert = ("""
    INSERT INTO artists (artist_id, name, location, latitude, longitude)
    SELECT DISTINCT
                    artist_id,
                    artist_name,
                    artist_location,
                    artist_latitude,
                    artist_longitude
    FROM staging_songs
    WHERE artist_id IS NOT NULL;
""")

time_table_insert = ("""
    INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT DISTINCT
                    TIMESTAMP 'epoch' + (ts/1000) * INTERVAL '1 second' as start_time,
                    EXTRACT(HOUR FROM start_time) AS hour,
                    EXTRACT(DAY FROM start_time) AS day,
                    EXTRACT(WEEKS FROM start_time) AS week,
                    EXTRACT(MONTH FROM start_time) AS month,
                    EXTRACT(YEAR FROM start_time) AS year,
                    EXTRACT(dayofweek FROM start_time) AS weekday          
    FROM staging_events
    WHERE start_time IS NOT NULL;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
