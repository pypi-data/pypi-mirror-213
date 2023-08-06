import requests
import time
import titlecase

artist = ""
title = ""

def currently_playing(ctime, stop_event):
    """
    Function to get the currently playing track (every 10 seconds).
    """
    while not stop_event.is_set():
        response = requests.get("https://www.grrif.ch/live/covers.json")

        # Check if the request was successful
        if response.status_code == 200:
            ltime = response.json()[3].get("Hours")
            if ctime == 0 or ctime != ltime:
                data = response.json()[3]
                title = titlecase.titlecase(data.get("Title"))
                artist = titlecase.titlecase(data.get("Artist"))
                ctime = ltime
                print(f"Currently playing {title} by {artist}.")
            else:
                pass
        else:
            print("Failed to retrieve data from the URL.")

        time.sleep(10)

#currently_playing(ctime)