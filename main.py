from lib2to3.pgen2 import token
import os
from dotenv import load_dotenv
import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3

load_dotenv()
SPOTIFY_TOKEN = os.getenv('TOKEN')

pd.set_option("display.max_rows", 1000)

DB_LOCATION = "sqlite:///my_played_tracks.sqlite"
USER_ID = "amir.nrfkn"

if __name__ == "__main__":
    TOKEN = SPOTIFY_TOKEN
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token = TOKEN)
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp())*1000
    
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp), headers = headers)
    print(f"r is_______: {r.text}")

    data = r.json()
    print(f"Data is_________: {data}")

    song_names = []
    artist = []
    played_at = []
    timestamps = []

    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist.append(song["track"]["album"]["artists"][0]["name"])
        played_at.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

        song_dict = {
            "song_name" : song_names,
            "artist_name" : artist,
            "played_at" : played_at,
            "timestamp" : timestamps
        }

        song_df = pd.DataFrame(song_dict, columns=["song_name", "artist_name", "played_at", "timestamp"])

        print(song_df)
