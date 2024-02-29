#
# Migrate from Mongo db
# to postgresql db
#

import os
from dotenv import load_dotenv
from pymongo import MongoClient
import psycopg2

#
# env section
#
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWD = os.getenv('POSTGRES_PASSWD')

#
# postgres init
#
conn_pg = psycopg2.connect(
    host = POSTGRES_HOST,
    database = POSTGRES_DB,
    user = POSTGRES_USER,
    password = POSTGRES_PASSWD
)

cursor_pg = conn_pg.cursor()

#
# mongo init
#
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client["webscraper"]
smoothjazz = mongo_db["smoothjazz"]

documents = list(smoothjazz.find({}, { '_id': 0, '_class': 0 }))
print(len(documents))

for i in range(0, 6):
    currentDoc = documents[i]

    artistName = currentDoc['artistName']
    albumTitle = currentDoc['albumTitle']
    songTitle = currentDoc['songTitle']
    imgUrl = currentDoc['imgUrl']
    imgText = currentDoc['imgText']
    print(artistName)
    print(albumTitle)
    print(songTitle)
    print(imgUrl)
    print(imgText)
    print()

    insert_query_pg = '''
        INSERT INTO smoothjazz (artist_name, album_title, song_title, img_url, img_text) 
        VALUES (%s, %s, %s, %s, %s)
    '''
    cursor_pg.execute(insert_query_pg, (artistName, albumTitle, songTitle, imgUrl, imgText))
    conn_pg.commit()


cursor_pg.close()
conn_pg.close()
    