import discord
from discord.ext import commands
import youtube_dl
import contextlib
import asyncio
import time
import wave
import os

## Class Timer
class Timer:
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._callback()

    def cancel(self):
        self._task.cancel()

## Class Player
class Player:
    ### __init__(self)
    def __init__(self):
        print("LOG Initialized..")

        for file in os.listdir("music"):
            if file.endswith(".wav"):
                os.remove("music\\{0}".format(file))

        self.current_track = None
        self.id_current_track = 0
        self.is_connected = False
        self.timer = None
        self.player = None
        self.loop = True
        self.mus_list = list(list())

    ### __del__(self)
    def __del__(self):
        for i in self.mus_list:
            os.remove(i)

        self.timer.cancel()
        self.mus_list.clear()
        self.current_track = None
        self.id_current_track = 0
        self.is_connected = False
        self.timer = None
        self.player = None
        self.loop = True

    ### Download Youtube Content
    async def download(self, url):
        opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            'outtmpl': '\\music\\%(id)s.%(ext)s',      
            'noplaylist' : True,        
            'progress_hooks': [self.my_hook]
        }
        with youtube_dl.YoutubeDL(opts) as ydl:
            ydl.download([url])

        await self.play()

    ### Youtube download's hook
    def my_hook(self, d):
        if d['status'] == 'finished':
            filename = "{0}.wav".format(d['filename'].split('.')[0])
            try:
                self.mus_list.index(filename)
            except:    
                self.mus_list.append(filename)
            print('Done downloading, now converting ...')

    ### 'Play music' function definition
    async def play(self):
        if self.player.is_playing() != False:
            return

        if len(self.mus_list) < 1:
            return

        self.current_track = self.mus_list[self.id_current_track]

        with contextlib.closing(wave.open(self.current_track,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
        print("Duration: {0}".format(duration))

        source = discord.FFmpegPCMAudio(self.current_track)
        self.player.play(source)

        self.timer = Timer(duration, self.next)

    ### 'Next track' function
    async def next(self):
        try:
            self.player.stop()

            self.id_current_track = self.id_current_track + 1

            if len(self.mus_list) <= self.id_current_track:
                self.id_current_track = 0
            
            if self.loop != True:
                return

            print('LOG: Current track id: {0}. Current track dir: {1}'.format(self.id_current_track, self.mus_list[self.id_current_track]))

            await self.play()
        except:
            print("ERROR: Cannot call 'next' function.")
            return

    ### remove one song from current playlist
    async def remove(self):
        try:
            for i in self.mus_list:
                print(i)

            temp = self.current_track
            self.timer.cancel()
            self.player.stop()

            if len(self.mus_list) > 0:
                await self.next()
                time.sleep(1)
                os.remove(temp)
                self.mus_list.remove(temp)
            else:
                await self.player.disconnect()
                self.__del__()
        except:
            print("ERROR: 'remove' function is not callable.")