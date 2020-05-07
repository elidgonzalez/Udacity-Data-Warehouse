# users_select = ("""
# SELECT table_name FROM information_schema.tables
#        WHERE table_schema = 'public'

# ss_select = ("""
# select column_name, data_type from information_schema.columns
# where table_name = 'staging_songs'
# """)

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