import discord
import random
import queue
import youtube_dl
import json
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


def randomSong():
    song = None;
    songList = [
        'https://www.youtube.com/watch?v=KhqNTjbQ71A',
        'https://www.youtube.com/watch?v=wcddNN9gwiw',
        'https://www.youtube.com/watch?v=1qYz7rfgLWE',
        'https://www.youtube.com/watch?v=68zIDuD0tn0',
        'https://www.youtube.com/watch?v=YrSEcDiedgc',
        'https://www.youtube.com/watch?v=P_dI6fVZwd0',
        'https://www.youtube.com/watch?v=hwacxSnc4tI',
        'https://www.youtube.com/watch?v=N8NcQzMQN_U',
        'https://www.youtube.com/watch?v=QJ5DOWPGxwg'


    ]
    song = random.choice(songList)
    return song

@bot.command()
async def play(ctx):
    channel = ctx.author.voice.channel

    if not channel:
        await ctx.send("You must be in a voice channel to use this command.")
        return

    voice_client = ctx.voice_client

    if voice_client is None:
        voice_client = await channel.connect()

    if not voice_client.is_playing():
        VIDEO_URL = randomSong()

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
    else:
        await ctx.send("The bot is already playing.")
    print("Hi")

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