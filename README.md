# Discord.py-Potato-Bot

A bot for Discord written in Python 3.8 as a general purpose utility bot. This bot was meant to replace my original discord.py bot after the Discord.py rewrite.

For commands, typing /help will bring up a list of commands

## Features:  type '/help' in Discord for more information
### Music player (Heavily based off vbe0201's example, see Credit for more info)
join - joins voice channel

leave - leaves voice channel

play - gets video from url or the search query provided

volume - changes volume

mute - mutes bot, but continues song. Equivalent to volume 0

info - gets inforrmation about the currently playing track

pause - pauses track

resume - resumes track

stop - stops the player and clears queue

skip - skips currently playing track

queue - shows queued up tracks

shuffle - shuffles the queue

remove - removes track at index position. Index starts at 1

loop - loops currently playing song. Trying loop untoggles it and continues the queue

### Image manipulation
fry - deepfries an image

radial - radial blurs an image

swirl - swirls an image

### Chat clearing/restore
clear - bulk delete

undo - undo bulk delete, only caches one delete per channel

restore - undo manual message deletion, configured to cache up to 50 messages per channel

### Games
Connect 4 - Self explanitory, can also change size of board

## Credit
For music integration, the code from my music.py file was built on top of [vbe0201's example here](https://gist.github.com/vbe0201/ade9b80f2d3b64643d854938d40a0a2d), with a bit modifications to most commands to handle errors, fix broken features, and add additional features

## Installation
### GNU/Linux
```
sudo apt update
sudo apt install ffmpeg 
git clone https://github.com/Winston-Lu/Discord.py-Potato-Bot
cd "Discord.py-Potato-Bot"
pip3 install -r requirements.txt
python3 "bot.py"
```

### Windows (Assumes python 3 and pip3 is installed)
```
git clone https://github.com/Winston-Lu/Discord.py-Potato-Bot
cd "Discord.py-Potato-Bot"
pip3 install -r requirements.txt
```
Then install [ffmpeg.exe from this link](https://ffmpeg.zeranoe.com/builds/), and put it in the Discord.py-Potato-Bot folder
```
python3 "bot.py"
```

### Token.txt
If you didn't know already, your bot token should be in the token.txt file. If you don't know how to get your bot token, [follow this guide here](https://www.writebots.com/discord-bot-token/) 

## To Do
- Image manipulation relies on saving the image temporarily to convert from PIL.Image format to a format pystacia supports. Should convert image through bytecode rather than taking up fileIO
- Add persistent storage for some commands such as the delete cache, volume settings for servers, etc.
- Allow for larger connect 4 board sizes (alternative shorter emoji names?)
- More games that dont require a "secret" hand/board like poker, uno, battleship, etc.
