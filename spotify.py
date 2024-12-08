import click
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

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
def spotify(m, y, h, a, top) -> None:
    if m:
        fetch_data("short_term", a, top)
    elif y:
        fetch_data("long_term", a, top)
    elif h:
        fetch_data("medium_term", a, top)
    else:
        fetch_data("short_term", a, top)


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