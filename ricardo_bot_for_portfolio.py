import discord
from discord import *
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import discord.voice_client
import random
import socket
import requests
import json

client = commands.Bot(command_prefix="*")

motivate_list = [
    "Ricardo says: You are best",
    "Ricardo loves you",
    "Ricardo is proud of you",
    "Ricardo will dance to you his dance"
]

rock_paper_scissors = [
    "Rock",
    "Scissors",
    "Paper"
]

ric_dic = {
    "Ricardo": "https://media.giphy.com/media/UtcBRO8cxulRzkrVLc/giphy.gif"
}

mia_dic = {
    "Mia": "https://media.giphy.com/media/oaqA3CO6J6CRO/giphy.gif",
    "Mia2": "https://media.giphy.com/media/3o7aDdyoaef41qkn9m/giphy.gif"
}

commands_list = [
    "*hello",
    "*ping",
    "*join",
    "*play",
    "*ricardo_play",
    "*pause",
    "*stop",
    "*resume",
    "*mute",
    "*unmute",
    "*left",
    "*leave",
    "*motivate",
    "*love",
    "*gif",
    "*mia",
    "*game",
    "*star_wars",
    "*virus",
    "*commands"
]


@client.event
async def on_ready():
    print('Bot is ready!')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("This is not a command. Please use a valid command and if you don't know which "
                       "one use *commands to see full list of commands :smiley:")


@client.command()
async def hello(ctx):
    await ctx.send("Hello There ! :smiley:")


@client.command()
async def ping(ctx):
    await ctx.send(f"Here is bots ping: {round(client.latency * 1000)}ms")


@client.command()
async def kick(member: discord.Member, *, reason=None):
    await member.kick(reason=reason)


@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()


@client.command()
async def test_play(ctx):
    channel = ctx.message.author.voice.channel
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio('C:/Users/sasi1/Downloads/8 - The Mamas & The Papas - California Dreamin.mp3'),
            after=lambda e: print('Done the music is playing', e))
    vc.source = discord.PCMVolumeTransformer(vc.source)
    vc.source.volume = 0.6
    vc.is_playing()
    await ctx.send("Music starts playing")


@client.command()
async def play(ctx, n: str):
    channel = ctx.message.author.voice.channel
    vc = await channel.connect()
    song = discord.Spotify(n).artist
    vc.play(discord.FFmpegPCMAudio(song))
    vc.source = discord.PCMVolumeTransformer(vc.source)
    vc.source.volume = 0.6
    vc.is_playing()
    await ctx.send("Music starts playing")


@client.command()
async def ricardo_play(ctx):
    channel = ctx.message.author.voice.channel
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio('C:/Users/sasi1/Downloads/u-got-that.mp3'),
            after=lambda e: print('Done the music is playing', e))
    vc.source = discord.PCMVolumeTransformer(vc.source)
    vc.source.volume = 0.6
    vc.is_playing()


@client.command()
async def pause(ctx):
    vc = ctx.voice_client
    vc.pause()
    await ctx.send("Music is paused resume this to play music again")


@client.command()
async def stop(ctx):
    vc = ctx.voice_client
    vc.stop()


@client.command()
async def resume(ctx):
    vc = ctx.voice_client
    vc.resume()
    await ctx.send("Music is unpaused")


@client.command()
async def mute(ctx):
    vc = ctx.voice_client
    vc.source = discord.PCMVolumeTransformer(vc.source)
    vc.source.volume = 0
    vc.is_playing()
    await ctx.send("Music is muted")


@client.command()
async def unmute(ctx):
    vc = ctx.voice_client
    vc.source = discord.PCMVolumeTransformer(vc.source)
    vc.source.volume = 0.6
    vc.is_playing()
    await ctx.send("Music is unmuted")


@client.command()
async def left(ctx):
    server = ctx.guild.voice_client
    await server.disconnect()
    await ctx.send("I've left your room :disappointed_relieved:")


@client.command()
@commands.guild_only()
async def leave(ctx):
    voice_client = ctx.guild.voice_client
    if not voice_client:
        await ctx.send('Not connected to any voice channels.')
        return
    await voice_client.disconnect()
    await ctx.send("I've left your room :disappointed_relieved:")


@client.command()
async def motivate(ctx):
    quote = random.choice(motivate_list)
    await ctx.send(quote)


@client.command()
async def love(ctx):
    n = random.randint(1, 100)
    await ctx.send(f"Ricardo loves you on {n}%")


@client.command()
async def get_ip(ctx):
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    await ctx.send("Your Computer Name is:" + hostname)
    await ctx.send("Your Computer IP Address is:" + ip_address)


@client.command()
async def mia(ctx):
    await ctx.send("https://media.giphy.com/media/oaqA3CO6J6CRO/giphy.gif")


@client.command()
async def star_wars(ctx, number: int):
    url = f"https://swapi.dev/api/people/{number}/?format=json"
    page = requests.get(url)
    try:
        name = json.loads(page.text)["name"]
        year = json.loads(page.text)["birth_year"]
        homeworld = json.loads(requests.get(json.loads(page.text)["homeworld"]).text)
        await ctx.send(name, year, homeworld["name"])

    except KeyError:
        pass


@client.command()
async def virus(ctx, website: str):
    url = 'https://www.virustotal.com/vtapi/v2/url/report'
    api_key = "db052dd548fccdc71f1a3730ad7d532b901e6c5babeeec0a93f8ee59ce017a21"
    params = {'apikey': api_key, 'resource': website}
    response = requests.get(url, params=params)
    response_json = json.loads(response.content)

    if response_json["positives"] == 0:
        await ctx.send(
            f"I have found no problems with your website my brother look: {response_json['positives']} "
            f"scanned: {response_json['total']}")
    else:
        await ctx.send(
            f"I've found problems with your website my brother look: {response_json['positives']} "
            f"scanned: {response_json['total']}")


@client.command()
async def add(ctx, a: int, b: int):
    answer = a + b
    await ctx.send(f"Answer: {answer}")


@client.command()
async def multiply(ctx, a: int, b: int):
    answer = a * b
    await ctx.send(f"Answer: {answer}")


@client.command()
async def division(ctx, a: int, b: int):
    answer = a / b
    await ctx.send(f"Answer: {answer}")


@client.command()
async def power(ctx, a: int, b: int):
    answer = a ** b
    await ctx.send(f"Answer: {answer}")


@client.command()
async def game(ctx):
    user = random.choice(rock_paper_scissors)
    bot = random.choice(rock_paper_scissors)

    if user == "Rock":
        if bot == "Rock":
            await ctx.send(f"This is Tie, you've chose {user} and Ricardo chose {bot}")
        elif bot == "Paper":
            await ctx.send(f"Haha you lost Ricardo is best, you've chose {user} and Ricardo chose {bot}")
        else:
            await ctx.send(f"You won, you've chose {user} and Ricardo chose {bot}")

    elif user == "Paper":
        if bot == "Rock":
            await ctx.send(f"You won, you've chose {user} and Ricardo chose {bot}")
        elif bot == "Paper":
            await ctx.send(f"This is a Tie, you've chose {user} and Ricardo chose {bot}")
        else:
            await ctx.send(f"Haha you lost Ricardo is best, you've chose {user} and Ricardo chose {bot}")

    elif user == "Scissors":
        if bot == "Rock":
            await ctx.send(f"Haha you lost Ricardo is best, you've chose {user} and Ricardo chose {bot}")
        elif bot == "Paper":
            await ctx.send(f"You won, you've chose {user} and Ricardo chose {bot}")
        else:
            await ctx.send(f"This is a Tie, you've chose {user} and Ricardo chose {bot}")


@client.command()
async def commands(ctx):
    embed = discord.Embed(title="Commands for Ricardo", description="Commands shown down below:", color=0xff3657)

    embed.add_field(name="*hello", value="Will greet you", inline=False)
    embed.add_field(name="*ping", value="Show you the bot ping", inline=False)
    embed.add_field(name="*join", value="Will join the bot to your voice channel", inline=False)
    embed.add_field(name="*leave", value="Will leave the current session", inline=False)
    embed.add_field(name="*motivate", value="Ricardo will motivate you", inline=False)
    embed.add_field(name="*love", value="Show the love percentage", inline=False)
    embed.add_field(name="*gif", value="Will send you Ricardo gif", inline=False)
    embed.add_field(name="*mia", value="Will send you Mia gif", inline=False)
    embed.add_field(name="*game", value="Ricardo will play Rock, Paper, Scissors with you", inline=False)
    embed.add_field(name="*play", value="Will play song for you", inline=False)
    embed.add_field(name="*stop", value="Will stop current song", inline=False)
    embed.add_field(name="*resume", value="Will resume current song", inline=False)
    embed.add_field(name="*pause", value="Will pause current song", inline=False)
    embed.add_field(name="*ricardo_play", value="Will play U got that", inline=False)
    embed.add_field(name="*add", value="Will do a+b", inline=False)
    embed.add_field(name="*multiply", value="Will do a*b", inline=False)
    embed.add_field(name="*division", value="Will do a/b", inline=False)
    embed.add_field(name="*power", value="Will do a**b", inline=False)
    embed.add_field(name="*minus", value="Will do a-b", inline=False)
    embed.add_field(name="*star_wars",
                    value="Will give you Star Wars info about your favorite character. Try number from 1-83",
                    inline=False)
    embed.add_field(name="*virus", value="Will check any website", inline=False)

    await ctx.send(embed=embed)


client.run(secret)
