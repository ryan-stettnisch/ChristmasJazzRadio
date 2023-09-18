import discord
import responses
import youtube_dl
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

VIDEO_URL = 'https://www.youtube.com/watch?v=1qYz7rfgLWE'
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

def randomSongs():
    song = None;

bot.run('MTE1MjcxMzc2MTYwMjQyMDgxNw.GmHZBK.ON5io1VVUZ7CxvvTKVe 4mdrYDbhDHmGb9vchYg')