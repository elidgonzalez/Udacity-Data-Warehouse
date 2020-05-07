# Udacity-Data-Warehouse Project

## Purpose
In this first project the goal is to provide a database for library songs playing currently. From this Database, the users, songs, artist of song, and time played can be extracted. This allows for simple analysis of users using a music service to play. In addition to monitoring this information could be used to control or limit the amount of being played such as for free rather than paid user.

## Schema and ETL Pipeline
The overall structure of this a star schema. In this case the songplays table was the fact table that all the dimension tables centered around. These tables were the users, songs, artists, and time tables. It was from the songplays table that all the data could be extracted from. For example to join all the tables and see all the columns you would join by song_id, user_id, artist_id, and start_time. With this the songplays table which contained songs that were played could be used to extract the particular.

## Tables

A list of the tables for this project they are divided into two categories the staging tables which are the "raw data" of the tables in the of an input. The other tables are the actual star schema tables composed of four dimension tables centered around one fact table. Below are samples of the structures that the tables should have.

### Staging Tables

1. **staging_events**
```json
{"artist": "Pavement", "auth": "Looged In", "firstName": "Sylvie", "gender": "F", "itemInSession": 0, "lastName": "Cruz", "length": 99.16036, "level": "free", "location": "Klamath Falls, OR", "method": "PUT", "page": "NextSong", "registration": 1.540266e+12,"sessionId": 345, "song": "Mercy:TheLaundromat", "status": 200, "ts": 1541990258796, "userAgent": "Mozilla/5.0(Macintosh;Intel Mac OSX 10_9_4","userId": 53}
```
2. **staging_songs**
```json
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```

### Star Tables

#### Fact Table

1. **songplays**
```json
{"songplay_id": 1, "start_time": "11/11/2018, 6:37:39", "user_id": 53, "level": "free", "song_id": "SOUPIRU12A6D4FA1E1", "artist_id": "ARJIE2Y1187B994AB7", "session_id": 345, "location": "Klamath Falls, OR", "user_agent": "Mozilla/5.0(Macintosh;Intel Mac OSX 10_9_4"}
```

#### Dimension Tables

1. ***users**
```json
{"user_id": 53, "first_name": "Sylvie", "lastName": "Cruz", "gender": "F", "level": "free"}
```
2. **songs**
```json
{"song_id": "SOUPIRU12A6D4FA1E1", "title": "Mercy:TheLaundromat", "artist_id": "ARJIE2Y1187B994AB7", "year": 0, "duration": 152.92036}
```
3. **artists**
```json
{"artist_id": "ARJIE2Y1187B994AB7", "name": "Pavement", "location": "", "latitude": null, "longitude": null}
```
4. **time**
```json
{"start_time": "11/11/2018, 6:37:39", "hour": 6, "day": 11, "week": 48, "month": 11, "year": 2018, "weekday": 5}
```

## Files

1. **sql_queries.py:** a file holding the prepared queries for creating, dropping, and inserting to the tables. It also has queries for the staging tables, which pull that data as they are into the tables.
2. **create_tables.py:** a file that calls the queries to drop the tables if necessary for tables and then creates them.
3. **etl.py:** this file runs the queries for the staging and etl transformation of data into a star schema explained above.
4. **select.py:** a series of select statment to grab sample data and view it from the tables.
5. **test.py:** file that runs the select queries to verify data was inserted to all tables.

## Running

1. Creation of a redshift with IAM ROLE to fill in the *dwh.cfg* file.
2. A dwh.cfg file with the following info is needed:
```
[CLUSTER]
HOST=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_PORT=

[IAM_ROLE]
ARN=
[S3]
LOG_DATA='s3://udacity-dend/log_data'
LOG_JSONPATH='s3://udacity-dend/log_json_path.json'
SONG_DATA='s3://udacity-dend/song_data'
```
3. Run ```python create_tables.py``` to create the tables.
4. Run ```python etl.py``` to create etl pipeline.
5. Run ```python test.py``` to see if data was inserted.