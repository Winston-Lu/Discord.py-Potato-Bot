# **Discord.py-Potato-Bot**

A bot for Discord written for Python 3.7.3+ as a general purpose utility bot. This bot was meant to replace my original discord.<i></i>py bot after the [Discord.py](https://github.com/Rapptz/discord.py) rewrite.

Discord slash seems to be the way to go, but would require a major rewrite of many modules. This is likely going to be done in a future project. This will serve as a legacy bot until I get around to rewriting a bot for discord slash

## **Features:  type '/help' in Discord for more information**
### Music player (Heavily based off JohnDavids's example, see Credit for more info)
* join - joins voice channel
* leave - leaves voice channel
* play - gets video from url or the search query provided
* volume - changes volume
* song-info - gets inforrmation about the currently playing track
* pause - pauses track
* resume - resumes track
* stop - stops the player and clears queue
* skip - skips currently playing track
* queue - shows queued up tracks
* repeat - loops currently playing song. Trying loop untoggles it and continues the queue

### Image manipulation
* fry - deepfries an image
* radial - radial blurs an image
* swirl - swirls an image
* warp -  randomly warps an image through random effects

### Chat clearing/restore
* clear - bulk delete
* undo - undo bulk delete, only caches one delete per channel
* restore - undo manual message deletion, configured to cache up to 50 messages per channel

### Games
* Connect 4 - Self explanitory, can also change size of board
* Chess - Self explanitry. Works by inputting 2 sets of coordinates. Still a work in progress

### General
* Ping - Responds with latency to Discord servers
* say - Makes bot say something

## Credit
For music integration, the code from music.py file was almost entirely ripped from [JohnDavid's repo here](https://github.com/MrrVit665/Discord-Bot-Music-python/).

## **Installation**
### GNU/Linux
```sh
sudo apt update
sudo apt install -y ffmpeg python-skimage libatlas-base-dev libjasper-dev libqtgui4 python3-pyqt5 build-essential cmake unzip pkg-config libjpeg-dev libpng-dev libtiff-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran python3-dev libgtk2.0-dev libqtwebkit4
git clone https://github.com/Winston-Lu/Discord.py-Potato-Bot
cd "Discord.py-Potato-Bot"
pip3 install -r requirements.txt
python3 "bot.py"
```
If you are running this on a Raspberry Pi, run this:
```sh
sudo apt install libhdf5-103
```
Note If you are using a Raspberry Pi, the image module will only work for versions of Raspbian Buster or higher (Skikit-image will not install on any earlier versions). This means the Image module in COGS will not work with prior raspbian versions including Stretch and Jessie. Everything else should work fine on earlier raspbian versions.

If you are still getting errors relating to missing packages, [follow this guide.](https://blog.piwheels.org/how-to-work-out-the-missing-dependencies-for-a-python-package/)

### Windows (Assumes Python 3 and pip3 is installed)
```sh
git clone https://github.com/Winston-Lu/Discord.py-Potato-Bot
cd "Discord.py-Potato-Bot"
pip3 install -r requirements.txt
```
Then install [ffmpeg.exe from this link](https://ffmpeg.zeranoe.com/builds/), and put it in the Discord.py-Potato-Bot folder
```sh
python3 "bot.py"
```

### **Token.txt**
If you didn't know already, your bot token should be in the token.txt file. If you don't know how to get your bot token, [follow this guide here](https://www.writebots.com/discord-bot-token/) 

## **To Do**
### Games
- More games that dont require a "secret" hand/board like poker, uno, battleship, etc. Games like minesweeper, solitare, but multiplayer
- Chess only supports moving and capturing. Game doesn't know when a player is in check, checkmate, or stalemate. Work on checking for "checks"
### Image to Braille Converter
- Convert an image to ASCII-like art using braille characters
### Google Translate Bug
- Ongoing bug with NoneType object has no attribute 'group'. Fix is documented here. https://stackoverflow.com/questions/52455774/googletrans-stopped-working-with-error-nonetype-object-has-no-attribute-group, but doesnt seem to work at the moment. Seems like an ongoing issue
