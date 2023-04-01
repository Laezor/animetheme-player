import requests
from pyfzf.pyfzf import FzfPrompt
import subprocess


def play_anime_theme():
    fzf = FzfPrompt()

    animetitle = input("Give an anime title: ")
    themetype = input("Opening or Ending [OP/ED]: ")

    res = requests.get(f" https://myanimelist.net/search/prefix.json?type=anime&keyword={animetitle}&v=1").json()

    animeinfo = res['categories'][0]['items']

    animes = {
        f"{gotanimeid['name']}": str(gotanimeid["id"])
        for gotanimeid in animeinfo
        if gotanimeid.get("payload", {}).get('media_type') in ["TV", "OVA"]
    }

    selectedtitle = fzf.prompt(animes)

    selectedid = animes.get(selectedtitle[0])
    if selectedid is None:
        print("Invalid selection.")
        return

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; MSIE 8.0; Windows 98; Win 9x 4.90; Trident/4.0)"
    }

    resp = requests.get(
        f"https://api.animethemes.moe/anime?include=animesynonyms,series,animethemes,animethemes.animethemeentries.videos,animethemes.song,animethemes.song.artists,studios,images,resources&fields%5Banime%5D=id,name,slug,year&filter%5Bhas%5D=resources&filter%5Bsite%5D=myanimelist&filter%5Bexternal_id%5D={selectedid}",
        headers=headers,
    )

    if resp.status_code != 200:
        print(f"Error occurred: {resp.status_code} {resp.text}")
        return

    resp = resp.json()

    if not resp["anime"]:
        print("Not found, probably not added yet!")
        return

    animethemes = resp["anime"][0]["animethemes"]
    animename = resp["anime"][0]["name"]

    # Initialize a list to store the available theme songs
    available_themes = []

    # Iterate over the anime themes and gather all matching theme song titles and links
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
    while True:
        # Use fzf.prompt to let the user select a theme song
        selected_theme = fzf.prompt([theme["title"] for theme in available_themes])

        if not selected_theme:
            # If the user chose to exit, break out of the loop
            break

        if selected_link := next(
            (
                theme["link"]
                for theme in available_themes
                if theme["title"] == selected_theme[0]
            ),
            None,
        ):
            print(f"Now playing... {selected_theme[0]}")
            subprocess.run(["mpv", selected_link])
        else:
            print("Invalid selection.")

        askuser = fzf.prompt(["Play another theme from this anime",
                              "Search for another anime",
                              "Exit"
                              ])

        if askuser[0] == "Play another theme from this anime":
            continue
        elif askuser[0] == "Search for another anime":
            play_anime_theme()
        else:
            quit()
            
    #     askuser = input("Do you want to exit the selection? [Y/N]")
        
    #     if askuser.upper() == "Y":
    #         break
    #     elif askuser.upper() == "N":
    #         continue
        
    # while True:
    #     searchagain = input("Do you want to Search a new anime? [Y/N]")
    
    #     if searchagain.upper() == "Y":
    #         play_anime_theme()
    #     else:
    #         quit()


if __name__ == "__main__":
    play_anime_theme()
    
    