import asyncio
import datetime
import discord
import random
import youtube_dl
import json
from discord.ext import commands, tasks
from lists import gifList, radioList, jazzList

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
global isPlaying

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

@bot.command()
async def startCountdown(ctx):
    countdown.start(ctx)

@tasks.loop(seconds=90)
async def countdown(ctx):
    channel = ctx.channel.id
    gif = random.choice(gifList)
    await ctx.send(gif)

@bot.command()
async def christmasGif(ctx):
    gif = None
    randomGif = random.choice(gifList)
    await ctx.send(randomGif)

def randomSong(songType):
    song = None
    if songType == "Jazz":
        song = random.choice(jazzList)
        return song
    else:
        song = random.choice(radioList)
        return song

with open('config.json') as config_file:
    config = json.load(config_file)
TOKEN = config['token']
bot.run(TOKEN)
