from dotenv import load_dotenv
load_dotenv()
#Environment variables
import os
import discord
from discord.ext import commands
from discord import Webhook
from discord import Activity, ActivityType
import random
import requests
import responses
import weather_api
import datetime
# import news_api
import asyncio
import youtube_dl
import currency_scraper

PREFIX = os.getenv("PREFIX")
TOKEN = os.getenv("TOKEN")
VOICE_CHANNEL_ID = os.getenv("VOICE_CHANNEL_ID")   #Enter the voice channel id where you want the bot to join
BOT_ROLE = os.getenv("BOT_ROLE")       #Enter the role with the required priveleges for the bot. Preferably, administrator privileges.

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix=PREFIX, intents=intents)
activity = Activity(name='?chelp', type=ActivityType.playing)
queue = []


@client.event
async def on_ready():
    print(f'{client.user} is now running!')
    await client.change_presence(activity=activity)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    username = str(message.author)
    user_message = str(message.content)
    channel = message.channel

    print(f"{username} said: '{user_message}'({str(channel)})")
    await client.process_commands(message)
    await channel.send(responses.handle_responses(user_message))




    
@client.command()
async def ping(ctx):
    """
    Shows the current latency.
    """
    #get latency
    latency = client.latency
    await ctx.send(latency)

@client.command()
async def choose(ctx, option1=None, option2=None):
    """Chooses between two options."""
    if option1 is None or option2 is None:
        await ctx.send("Please provide two options. Usage: ```?choose [option1] [option2]```")
    else:
        choice = random.choice([option1, option2])
        await ctx.send(f"I choose {choice}!")

@client.command()
async def time(ctx):
    info = str(datetime.datetime.utcnow())
    pretty = info[11:19]
    await ctx.send(f'UTC Time : {pretty} ')


@client.command()
async def echo(ctx, *, content:str):
    """
    Echoes the input given by the user.
    """
    await ctx.send(content)


############### WORK IN PROGRESS
# @client.command()
# async def news(topic, from_date, to_date):
#     topic_ = str(topic).lower()
#     print(topic_)
#     from_date_ = str(from_date)
#     print(from_date_)
#     to_date_ = str(to_date)
#     print(to_date_)
#     channel = topic.channel
#     data = news_api.get_news(topic_, from_date_, to_date_)
#     print(data)
#     await channel.send(f'{data} \n -------- \n')
#     embed = discord.Embed(colour=discord.Color.blurple())
#     embed.add_field(
#         name=f'News about {(topic_).capitalize()}:',
#         value=f'{data}',
#         inline=False)
#     embed.set_footer(text=f'Here is the news! {topic.message.author.name}!')
#     await channel.send(embed=embed)


@client.command()
async def weather(ctx, city) -> str:
    """
    Shows the current temperature of a city.
    """
    info = weather_api.get_weather_single(city)
    print(info)
    await ctx.send(info)

    #throws the error

#KICK FUNCTION
@client.command()
@commands.has_permissions(kick_members=True)
@commands.has_role(BOT_ROLE)
async def kick(ctx, user: discord.Member, *, reason = None):
  if not reason:
    await user.kick()
    await ctx.send(f"**{user}** has been kicked for **no reason**.")
  else:
    await user.kick(reason=reason)
    await ctx.send(f"**{user}** has been kicked for **{reason}**.")



###BAN FUNCTION
@client.command()
@commands.has_role(BOT_ROLE)
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    if reason == None:
        await ctx.send(f'{member} has been banned.')
    else:
        await ctx.send(f'{member} has been banned for {reason}')



#WARN FUNCTION
warnings = {}
@client.command()
@commands.has_role(BOT_ROLE)
async def warn(ctx, member: discord.Member, *, reason=None):
    if member.id not in warnings:
        warnings[member.id] = []

    warnings[member.id].append(reason)
    await ctx.send(f'{member.mention} has been warned for {reason}.')


#------------------------------------MUSICC------------------------------------

@client.command()  #join vc
async def play(ctx, url):

    try:
        voice_channel = client.get_channel(int(VOICE_CHANNEL_ID)) #This is the test server id.
        #953996131665326124 this is the lounge id
        if ctx.author.voice is None:
            await ctx.send("You are not in a voice channel.")
            return
        else:
            voice = await voice_channel.connect()
            await ctx.send('Commander has joined the **Music** voice channel.')
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                url = info['formats'][0]['url']

            voice.play(discord.FFmpegPCMAudio(url))
            while voice.is_playing():
                await asyncio.sleep(1)
    except discord.errors.ClientException:
        await voice_channel.disconnect()
    if commands.errors.CommandInvokeError:
        raise AttributeError(await ctx.send('Please follow the syntax: ```?play [url]```'))







@client.command()
async def stop(ctx):
    if ctx.author.voice.channel == ctx.voice_client.channel:
        voice_client = ctx.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        await ctx.send('Stopping music...')
        await voice_client.disconnect()

@client.command()
async def pause(ctx):
    voice_client = ctx.guild.voice_client

    if voice_client.is_playing():
        voice_client.pause()
        await ctx.send("Music paused.")
    else:
        await ctx.send("I am not currently playing any music.")


@client.command()
async def resume(ctx):
    if ctx.author.voice.channel == ctx.voice_client.channel:
        voice_client = ctx.guild.voice_client
    if voice_client.is_paused():
        voice_client.resume()

@client.command()
async def leave(ctx):
    # Check if the bot is in a voice channel
    voice_client = ctx.guild.voice_client
    if ctx.author.voice == voice_client:
        if voice_client is None:
            await ctx.send("I am not currently in a voice channel.")
            return
        await voice_client.disconnect()
        await ctx.send("Commander has left the voice channel.")
    else:
        await ctx.send('You are not currently in a voice channel.')


#------------------------------------MUSICC------------------------------------

@client.command()
async def convert(ctx, in_cur, out_cur, val):
    in_cur_ = str(in_cur)
    out_cur_ = str(out_cur)
    val_ = int(val)
    info = currency_scraper.get_currency(in_cur_, out_cur_, val_)
    await ctx.send(f'{val} {in_cur} = {info} {out_cur}')

@client.command()
async def currencies(ctx):
    currency_list = ['INR - Indian Rupee', 'USD - US Dollar', 'EUR - Euro', 'GBP - British Pound', 'AUD - Australian Dollar',
                     'CAD - Canadian Dollar', 'SGD - Singapore Dollar', 'AED - Emirati Dirham', 'If you want more currencies, visit: https://x-rates.com/ \n Use the link above to find out further available currency symbols.']
    for currency in currency_list:
        await ctx.send(f'*{currency}*')

@client.command()
async def chelp(ctx):
    embed = discord.Embed(title='Help', description="Use '?' prefix before entering a command.",
                          colour=discord.Color.blurple())
    embed.add_field(name = "**Moderation**", value = "*kick, ban, warn*")
    embed.add_field(name = "**Functions**", value = "*weather, convert*")
    embed.add_field(name = "**Fun**", value = "*roll, choose, kiss*")
    embed.add_field(name = "**Music**", value = "*play(url), pause, resume, stop*")
    embed.add_field(name = "**Misc**", value = "*echo, ping, time*")

    await ctx.send(embed=embed)



@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print('That\'s not a real command!')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'You missed an argument(s)!')
    elif isinstance(error, commands.errors.MissingRole):
        await ctx.send('Missing the required role to execute the function.')
    # etc
    else:
        raise error # prints the error











































client.run(TOKEN)










