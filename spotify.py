import click
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from datetime import datetime

import os
import json

today = datetime.today()

load_dotenv()
scope = "user-top-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, 
                                               client_id=os.getenv("CLIENT_ID"), 
                                               client_secret=os.getenv("CLIENT_SECRET"), 
                                               redirect_uri="http://localhost:8080"))

@click.command()
@click.option("-m", is_flag=True, default=False, help="Show past months top played")
@click.option("-y", is_flag=True, default=False, help="Show past years top played")
@click.option("-h", is_flag=True, default=False, help="Show past 6 months top played")
@click.option("-a", is_flag=True, default=False, help="Display artists instead of songs")
@click.option("--top", default=5, show_default=True, help="Number of top items to display")
@click.option("--store", is_flag=True, default=False, help="Store top played data")
def spotify(m, y, h, a, top, store) -> None:
    if store:
        store_month_data("december", "2024")
    if m:
        fetch_data("short_term", a, top)
    elif y:
        fetch_data("long_term", a, top)
    elif h:
        fetch_data("medium_term", a, top)
    else:
        fetch_data("short_term", a, top)

def store_month_data() -> bool:
    top_artists = sp.current_user_top_artists(time_range="short_term", limit=5)
    top_tracks = sp.current_user_top_tracks(time_range="short_term", limit=5)
    if not top_artists or not top_tracks:
        print("Error getting spotify data")
        return False
    
    artists = []
    tracks = []
    for artist in top_artists['items']:
        artists.append(artist['name'])
    for track in top_tracks['items']:
        tracks.append({"name": track['name'], "artist": track['artists'][0]['name']})

    with open(f"data/{today.year}_spotify.json", "r+") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}
            f.seek(0)
            json.dump(data, f, indent=4)
        data[today.month] = {"artists": artists, "tracks": tracks}
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
        return True



def fetch_data(time_range, artist, num_items) -> None:
    if artist:
        results = sp.current_user_top_artists(time_range=time_range, limit=num_items)
        if results:
            for i, item in enumerate(results['items']):
                print(f"{i+1}. {item['name']}")
        else:
            click.echo("No top artists found")
    else:
        top_tracks = sp.current_user_top_tracks(time_range=time_range, limit=num_items)
        if top_tracks:
            for i, item in enumerate(top_tracks['items']):
                print(f"{i+1}. {item['name']} - {item['artists'][0]['name']}")
        else:
            click.echo("No top tracks found")