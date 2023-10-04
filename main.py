import asyncio

import discord
import random
import queue
import youtube_dl
import json
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
global isPlaying

def randomSong(songType):
    song = None
    if songType == "Jazz":
        jazzList = [
            'https://www.youtube.com/watch?v=t8C_sEWYKyg&t=5391s', # A Christmas Coffee Shop Ambience with Relaxing Christmas Jazz Music, Crackling Fire, and Cafe Sounds
            'https://www.youtube.com/watch?v=5tXht-NGmc0', # New York Jazz Lounge - Merry Christmas
            'https://www.youtube.com/watch?v=Eh5rrcK685k', # Christmas Jazz Intrumental Music for Good Mood🎄Cozy Christmas Coffee Shop Ambience & Warm Fireplace
            'https://www.youtube.com/watch?v=lJlEQim-yMo', # Relaxing Christmas Jazz Music 10 Hours
            'https://www.youtube.com/watch?v=DOIc3gaMBjo', # Christmas Starbucks 🎄 Christmas Jazz – Relaxing Christmas Carols and Jazz Holidays Music for Winter
            'https://www.youtube.com/watch?v=_H6nNysTQs8', # Relaxing Christmas Carol Music | 8 Hours | Quiet and Comfortable Instrumental Music | Cozy and Calm
            'https://www.youtube.com/watch?v=vVLEtZ-d1nw', # 3 Hours of Christmas Jazz Music with Snowfall and Traditional Christmas Songs & Carols
            'https://www.youtube.com/watch?v=Jo1wpKmIfEw', # Happy Christmas Jazz Instrumental Piano Music 10 Hours
        ]
        song = random.choice(jazzList)
        return song
    else:
        radioList = [
            'https://www.youtube.com/watch?v=KhqNTjbQ71A',  # Last Christmas
            'https://www.youtube.com/watch?v=wcddNN9gwiw',  # It's the Most Wonderful Time of the Year
            'https://www.youtube.com/watch?v=1qYz7rfgLWE',  # Rockin' Around The Christmas Tree
            'https://www.youtube.com/watch?v=68zIDuD0tn0',  # Winter Wonderland
            'https://www.youtube.com/watch?v=YrSEcDiedgc',  # Baby It's Cold Outside
            'https://www.youtube.com/watch?v=P_dI6fVZwd0',  # A Holly Jolly Christmas
            'https://www.youtube.com/watch?v=hwacxSnc4tI',  # The Christmas Song
            'https://www.youtube.com/watch?v=N8NcQzMQN_U',  # Feliz Navidad
            'https://www.youtube.com/watch?v=QJ5DOWPGxwg',  # It's Beginning To Look A Lot Like Christmas
        ]
    song = random.choice(radioList)
    return song

async def playMusic(ctx,channel, voice_client, musicType):
    global isPlaying
    while ctx.voice_client and ctx.voice_client.is_connected():
        if not voice_client.is_playing():
            if musicType == "Jazz":
                VIDEO_URL = randomSong("Jazz")
            else:
                VIDEO_URL = randomSong("Radio")

        if not voice_client.is_playing():
            try:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'verbose': True,
                    'extractor': 'youtube',
                    'external_downloader': 'ffmpeg',
                    'external_downloader_args': [
                        '-reconnect', '2', #maybe 1
                        '-reconnect_streamed', '2', #2
                        '-reconnect_delay_max', '10', #5
                    ],
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(VIDEO_URL, download=False)
                    url = info['formats'][0]['url']
                    voice_client.play(discord.FFmpegPCMAudio(url))
            except Exception as e:
                await ctx.send(f"An error occurred while playing audio: {str(e)}")

        isPlaying = True
        while voice_client.is_playing():
            try:
                await asyncio.sleep(1)
                if not isPlaying:
                    voice_client.stop()
                    break
            except Exception as e:
                await ctx.send(f"An error with the network occurred while playing audio: {str(e)}")
                break
@bot.command()
async def playJazz(ctx):
    channel, voice_client = await getInfo(ctx)
    if voice_client.is_playing():
        voice_client.stop()
    await playMusic(ctx,channel, voice_client,"Jazz")
@bot.command()
async def playRadio(ctx):
    channel, voice_client = await getInfo(ctx)
    if voice_client.is_playing():
        voice_client.stop()
    await playMusic(ctx,channel, voice_client,"Radio")
async def getInfo(ctx):
    channel = ctx.author.voice.channel

    if not channel:
        await ctx.send("You must be in a voice channel to use this command.")
        return

    voice_client = ctx.voice_client

    if voice_client is None:
        voice_client = await channel.connect()
    return channel, voice_client

@bot.command()
async def skip(ctx):
    global isPlaying
    isPlaying = False

@bot.command()
async def leave(ctx):
    voice_client = ctx.voice_client
    await voice_client.disconnect()

#@bot.command()
#async def countdown():
    #days = 0

with open('config.json') as config_file:
    config = json.load(config_file)
TOKEN = config['token']
bot.run(TOKEN)