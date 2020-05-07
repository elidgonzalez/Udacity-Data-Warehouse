'''
Sample grabbing file this is used to select 10 entries from each table.
'''

se_select = ("""
SELECT * from staging_events LIMIT 10;
""")
ss_select = ("""
SELECT * from staging_songs LIMIT 10;
""")
songplays_select = ("""
SELECT * from songplays LIMIT 10;
""")
users_select = ("""
SELECT * from users LIMIT 10;
""")
songs_select = ("""
SELECT * from songs LIMIT 10;
""")
artists_select = ("""
SELECT * from artists LIMIT 10;
""")
time_select = ("""
SELECT * from time LIMIT 10;
""")
select_queries = [se_select, ss_select, users_select, songs_select, artists_select, time_select]

# A select statement use for gathering info about a table.
table_info = ("""
SELECT column_name, data_type from information_schema.columns
WHERE table_name = 'staging_songs'
""")