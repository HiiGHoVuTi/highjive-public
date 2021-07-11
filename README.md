
Contrary to the main game's code, the dependency control and installation process are totally open-source, along with anything community-made that will be here. We thus encourage you to contribute if you want to make High Jive a better experience !

# High Jive public files

High Jive is a heavily WIP game, so don't expect more than a crude demo. You are however encouraged to enjoy it and report any feedback to the creator over on [discord](https://discord.gg/7rWGcmxE8F).
The full game will be released the [TBD] and will include the OST along with custom track support.
There will be free updates, along with one-purchase DLC including online services like user-made maps, leaderboards and much more !

Enjoy !

## Installation

### Main Game
This game is pretty light, so it can be downloaded whole in a zip file [here](https://github.com/HiiGHoVuTi/highjive-public/releases). Pick the appropriate Operating System.

However, on the first install, you need to have a few dependencies on your system, including:
```yaml
- SDL
- SDL-Mixer
- Python (for packages)
- Aubio
```
Thankfully, we made an installation tool that should take care of most of the annoying work for you. You can pick it up from this repo. All you need to run it is python.

To get the installation tool, just use curl:
```sh
# In an empty folder
$ curl https://raw.githubusercontent.com/HiiGHoVuTi/highjive-public/main/install.py > install.py
$ python3 install.py
```

## Gameplay
There is no tutorial at the moment, although the gameplay is simple. You have to guide the cursor to click on the white circles as they reach their full size. To do that, you can use the arrow keys (recommended) or a mouse (if you own a trackpad).

## Custom Tracks
To add your own songs to the game, you simply have to drop them in the `assets/songs/` folder. Most popular formats are supported, including `.mp3`, `.ogg`, and `.wav`.
You should see up to 6 songs in the selection menu.
