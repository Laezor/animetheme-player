# Table of Contents

- [Table of Contents](#table-of-contents)
  - [showcase](#showcase)
  - [Introduction](#introduction)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Limitations](#limitations)
  - [Credits](#credits)
  
## showcase

[animethemes_compressed.webm](https://user-images.githubusercontent.com/32393101/229285478-f8077f5d-c109-4423-b1dc-13daef15310c.webm)


## Introduction

This is a Python script that lets you search for an anime and play its opening or ending theme songs using the mpv media player. The script uses the AnimeThemes API to get the available theme songs and the pyfzf library to prompt the user for selections.

## Requirements

- Python 3.x
- requests module (can be installed via pip)
- pyfzf module (can be installed via pip)
- mpv media player (must be installed separately)
- install fzf as well (depending on your OS)


## Installation

- For linux


## Using git

Alternatively, you can "git clone" this repository to any directory and run
[install](https://github.com/junegunn/fzf/blob/master/install) script.

```sh
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
```

## Using Linux package managers

| Package Manager | Linux Distribution      | Command                            |
| ---             | ---                     | ---                                |
| APK             | Alpine Linux            | `sudo apk add fzf`                 |
| APT             | Debian 9+/Ubuntu 19.10+ | `sudo apt install fzf`             |
| Conda           |                         | `conda install -c conda-forge fzf` |
| DNF             | Fedora                  | `sudo dnf install fzf`             |
| Nix             | NixOS, etc.             | `nix-env -iA nixpkgs.fzf`          |
| Pacman          | Arch Linux              | `sudo pacman -S fzf`               |
| pkg             | FreeBSD                 | `pkg install fzf`                  |
| pkgin           | NetBSD                  | `pkgin install fzf`                |
| pkg_add         | OpenBSD                 | `pkg_add fzf`                      |
| Portage         | Gentoo                  | `emerge --ask app-shells/fzf`      |
| XBPS            | Void Linux              | `sudo xbps-install -S fzf`         |
| Zypper          | openSUSE                | `sudo zypper install fzf`          |

- Install the script

```
sudo curl -sL https://raw.githubusercontent.com/Laezor/animetheme-player/main/animethemes -o /$HOME/.local/bin/animethemes &&
sudo chmod +x /$HOME/.local/bin/animethemes
```

- For windows

| Package manager | Command              |
| ---             | ---                  |
| Chocolatey      | `choco install fzf`  |
| Scoop           | `scoop install fzf`  |
| Winget          | `winget install fzf` |

- Install the script

```
iwr "https://raw.githubusercontent.com/Laezor/animetheme-player/main/animethemes-win.py" -OutFile "%userprofile%/Downloads/animethemes-win.py"
```

## Usage

To use the script, follow these steps:

1. Clone the repository to your local machine.
2. Open a terminal window and navigate to the directory where the script is located.
3. Run the script by typing the following command and pressing Enter:

For windows

```python
python animethemes-win.py
```
For linux
```
animethemes
```

4. When prompted, enter the title of the anime you want to search for and whether you want to play its opening or ending theme songs.
5. Select the anime you want to play theme songs for from the list of search results that appear.
6. Select the theme song you want to play from the list of available theme songs.
7. The script will automatically launch the mpv media player and play the selected theme song. Press Q to quit mpv.
8. After the theme song has finished playing, you will be prompted to choose whether to exit the selection or play another theme song from the current anime.
9. If you choose to play another theme song, the available theme songs for the current anime will be displayed and you can select another one to play.
10. If you choose to exit the selection, you will be prompted to choose whether to search for a new anime or exit the script.
11. If you choose to search for a new anime, the script will start over and prompt you for a new anime title and theme type.
12. If you choose to exit the script, the script will terminate.

## Limitations

- The script only searches for TV and OVA anime titles.
- The script only supports playing opening and ending theme songs.
- The script only plays one theme song at a time.
- The script requires an active internet connection to function properly.

## Credits

- AnimeThemes for providing the API used by the script.
- pyfzf for providing the FzfPrompt library used by the script.
- The creators and contributors of the requests and mpv modules used by the script.
