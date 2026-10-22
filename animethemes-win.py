# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
import time

import requests
from pyfzf.pyfzf import FzfPrompt


def find_vlc():
    """Find VLC on PATH or in its default Windows install locations."""
    found = shutil.which("vlc")
    if found:
        return found

    candidates = [
        os.path.join(os.environ.get("ProgramFiles", r"C:\Program Files"), "VideoLAN", "VLC", "vlc.exe"),
        os.path.join(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"), "VideoLAN", "VLC", "vlc.exe"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    return None


def get_player_command(link):
    """Return the command to play `link` with mpv, or vlc if mpv isn't installed."""
    mpv = shutil.which("mpv")
    if mpv:
        return [mpv, link]

    vlc = find_vlc()
    if vlc:
        return [vlc, "--play-and-exit", link]

    return None


def fetch_themes(mal_id, retries=3, timeout=20):
    """Fetch themes from AnimeThemes, retrying on timeouts / 5xx errors."""
    url = "https://api.animethemes.moe/anime"
    params = {
        "include": "animethemes.animethemeentries.videos,animethemes.song",
        "fields[anime]": "id,name,slug,year",
        "filter[has]": "resources",
        "filter[site]": "myanimelist",
        "filter[external_id]": mal_id,
    }
    headers = {"User-Agent": "animetheme-player/1.0"}

    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=timeout)
            if resp.status_code == 200:
                return resp.json()
            print(f"Attempt {attempt}/{retries}: HTTP {resp.status_code}")
        except requests.RequestException as e:
            print(f"Attempt {attempt}/{retries}: {e}")
        if attempt < retries:
            time.sleep(2 * attempt)

    return None


def play_anime_theme():
    fzf = FzfPrompt()

    animetitle = input("Give an anime title: ")
    themetype = input("Opening or Ending [OP/ED]: ").upper()

    try:
        res = requests.get(
            "https://myanimelist.net/search/prefix.json",
            params={"type": "anime", "keyword": animetitle, "v": 1},
            timeout=20,
        ).json()
    except (requests.RequestException, ValueError) as e:
        print(f"MyAnimeList search failed: {e}")
        return

    animeinfo = res["categories"][0]["items"]

    animes = {
        f"{gotanimeid['name']}": str(gotanimeid["id"])
        for gotanimeid in animeinfo
        if gotanimeid.get("payload", {}).get("media_type") in ["TV", "OVA"]
    }

    if not animes:
        print("No anime found.")
        return

    selectedtitle = fzf.prompt(animes)
    if not selectedtitle:
        return

    selectedid = animes.get(selectedtitle[0])
    if selectedid is None:
        print("Invalid selection.")
        return

    resp = fetch_themes(selectedid)
    if resp is None:
        print("The AnimeThemes API isn't responding right now. Try again later.")
        return

    if not resp["anime"]:
        print("Not found, probably not added yet!")
        return

    animethemes = resp["anime"][0]["animethemes"]

    # Gather all matching theme song titles and links
    available_themes = []
    for theme in animethemes:
        if theme["type"] == themetype:
            for entry in theme["animethemeentries"]:
                available_themes.extend(
                    {
                        "title": f"{theme['song']['title']} - {video['filename']}",
                        "link": video["link"],
                    }
                    for video in entry["videos"]
                )

    if not available_themes:
        print(f"No {themetype} themes found.")
        return

    while True:
        selected_theme = fzf.prompt([theme["title"] for theme in available_themes])

        if not selected_theme:
            break

        selected_link = next(
            (
                theme["link"]
                for theme in available_themes
                if theme["title"] == selected_theme[0]
            ),
            None,
        )

        if selected_link:
            command = get_player_command(selected_link)
            if command is None:
                print("Neither mpv nor vlc was found. Please install one of them.")
                return

            print(f"Now playing with {os.path.basename(command[0])}... {selected_theme[0]}")
            subprocess.run(command)
        else:
            print("Invalid selection.")

        askuser = fzf.prompt(
            [
                "Play another theme from this anime",
                "Search for another anime",
                "Exit",
            ]
        )

        if not askuser or askuser[0] == "Exit":
            quit()
        elif askuser[0] == "Search for another anime":
            play_anime_theme()
            return
        # otherwise: "Play another theme from this anime" -> loop again


if __name__ == "__main__":
    play_anime_theme()