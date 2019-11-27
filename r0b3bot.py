#!/usr/bin/python3

import discord
from discord.ext import commands
import urllib.request
import random
import os
import sys
import octoapi
import homeassistant.remote as remote
import time
from datetime import datetime
import configparser
import json
from discord import FFmpegPCMAudio
from discord.utils import get
from discord.voice_client import VoiceClient
import requests

bot = commands.Bot(command_prefix='$', description='A derpy derp of a bot.')

config = configparser.RawConfigParser()
configFilePath = r'bot_config.conf'

try:
    config.read(configFilePath)
except:
    print("Error loading config!  Please check config file 'bot-config.conf'")

# Setup HomeAssistant URL and Headers
HASS_TOKEN = config.get('bot-config', 'hass_token')
HASS_URL = config.get('bot-config', 'hass_url')
HASS_LIGHT = config.get('bot-config', 'hass_light')
hassURL = HASS_URL + "/api/states/" + HASS_LIGHT
hassHEADERS = {
    'Authorization': f"Bearer {HASS_TOKEN}",
    'content-type': 'application/json',
}

OCTOPRINT_IP_ADDRESS = config.get('bot-config', 'octoprint_ip_address')

DISCORD_AUTH_TOKEN = config.get('bot-config', 'discord_auth_token')

# Printing configuration details to console
print(f"HomeAssistant URL: {hassURL}")
print(f"HomeAssistant URL HEADERS: {hassHEADERS}")
print(f"HomeAssistant Light: {HASS_LIGHT}")
print(f"OctoPrint IP Address: {OCTOPRINT_IP_ADDRESS}")

# This is now deprecated and will be replaced with using the REST
#hassapi = remote.API(HASS_IP_ADDRESS, HASS_API_KEY)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        #msg = 'This command is ratelimited, please try again in {:.2f}s'.format(error.retry_after)
        seconds = round(error.retry_after,1)
        print(f" - Error, user tried to use command while in cooldown (wait is: {seconds}")
        await ctx.send(f"This command is ratelimited per user, please try again in {seconds}s")
    if isinstance(error, commands.CommandInvokeError):
        print(" - ERROR: encountered 'CommandInvokeError'")
        print(f" - Dumping error: {error}")
        await ctx.send("Error, unable to complete your request.")
    else:
        print('Oopsie, I found an error...')
        print(f"Error: {error}")


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def greetings(ctx):
    await ctx.send(":smiley: :wave: Hello there!")

#
# Giphy Commands
#
@bot.command()
async def cat(ctx):
    await ctx.send("https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif")

@bot.command()
async def explain(ctx):
    await ctx.send("https://media.giphy.com/media/A8NNZlVuA1LoY/giphy.gif")

@bot.command()
async def holyshit(ctx):
    await ctx.send("https://media.giphy.com/media/QcGTswMKyBNgA/giphy.gif")

###

#
# Voice Commands
#

@bot.command()
@commands.cooldown(rate=1, per=30.0, type=commands.BucketType.user)
async def bitch(ctx, member : discord.Member="NONE"):
    datestring = datetime.now()
    datestring = datestring.strftime("%m/%d/%Y-%H:%M:%S")
    if ctx.message.channel.is_nsfw():
        await play_sound(ctx, member, "./sounds/monkey_bitch.mp3", "$bitch")
    else:
        print(f"[{datestring}]: {ctx.message.author.display_name} called $bitch, but is not in a NSFW channel")
        await ctx.send("This command is too explicit for you!")

@bot.command()
@commands.cooldown(rate=1, per=30.0, type=commands.BucketType.user)
async def cowbell(ctx, member : discord.Member="NONE"):
    await play_sound(ctx, member, "./sounds/More_cowbell.mp3", "$cowbell")

@bot.command()
@commands.cooldown(rate=1, per=30.0, type=commands.BucketType.user)
async def boom(ctx, member : discord.Member="NONE"):
    datestring = datetime.now()
    datestring = datestring.strftime("%m/%d/%Y-%H:%M:%S")
    if ctx.message.channel.is_nsfw():
        await play_sound(ctx, member, "./sounds/BoomBitch.mp3", "$boom")
    else:
        print(f"[{datestring}]: {ctx.message.author.display_name} called $boom, but is not in a NSFW channel")
        await ctx.send("This command is too explicit for you!")

@bot.command()
@commands.cooldown(rate=1, per=30.0, type=commands.BucketType.user)
async def oops(ctx, member : discord.Member="NONE"):
    await play_sound(ctx, member, "./sounds/Oops.mp3", "$oops")

@bot.command()
@commands.cooldown(rate=1, per=30.0, type=commands.BucketType.user)
async def trololo(ctx, member : discord.Member="NONE"):
    await play_sound(ctx, member, "./sounds/Trololo.mp3", "$trololo")

@bot.command()
@commands.cooldown(rate=1, per=30.0, type=commands.BucketType.user)
async def leeroy(ctx, member : discord.Member="NONE"):
    await play_sound(ctx, member, "./sounds/leeroy.mp3", "$leeroy")

@bot.command()
@commands.cooldown(rate=1, per=30.0, type=commands.BucketType.user)
async def promoted(ctx, member : discord.Member="NONE"):
    await play_sound(ctx, member, "./sounds/Promoted.mp3", "$promoted")

@bot.command()
@commands.cooldown(rate=1, per=30.0, type=commands.BucketType.user)
async def rs(ctx, member : discord.Member="NONE"):
    datestring = datetime.now()
    datestring = datestring.strftime("%m/%d/%Y-%H:%M:%S")
    if ctx.message.channel.is_nsfw():
        soundfiles = ["./sounds/leeroy.mp3","./sounds/monkey_bitch.mp3","./sounds/More_cowbell.mp3","./sounds/BoomBitch.mp3","./sounds/Promoted.mp3","./sounds/Trololo.mp3","./sounds/Oops.mp3"]
        await play_sound(ctx, member, random.choice(soundfiles), "$rs")
    else:
        print(f"[{datestring}]: {ctx.message.author.display_name} called $rs, but is not in a NSFW channel")
        await ctx.send("This command is too explicit for you!")

async def play_sound(ctx, member : discord.Member, soundFile, command):

    discord.opus.load_opus("libopus.so")

    datestring = datetime.now()
    datestring = datestring.strftime("%m/%d/%Y-%H:%M:%S")

    print(f"[{datestring}]: {ctx.message.author.display_name} called {command}")

    # Need to check whether or not a user has been specified.  If one has, we need to use the channel
    #  they are currently connected to instead the channel that the command issuer is in.
    if member != "NONE":
        try:
            channel = member.voice.channel
        except:
            await ctx.send(f"{member.display_name} is not in a voice channel!")
            print(f" ! {member.display_name} is not in a voice channel")
            return
        print(f" - User specified: {member.display_name}")
        print(f" - Destination channel: {channel}")

    if member == "NONE":
        try:
            channel = ctx.message.author.voice.channel
        except:
            await ctx.send("You are not connected to a voice channel.")
            print("User is not connected to a voice channel")
            return
    
    voice: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    
    # Different join actions are needed depending on whether or not the bot is already in a 
    #  voice channel.  If already in a channel, wait until disconnected, then join the requested
    #  channel.  If not already in a channel, then join requested channel immediately
    if voice and voice.is_connected():
        print(f" - Moving to channel '{channel}''")
        await ctx.send(f"Moving to '{channel}' for just a moment")
        await voice.move_to(channel)

    else:
        print(f" - Joining Channel '{channel}''")
        await ctx.send(f"Joining '{channel}' for just a moment")
        voice = await channel.connect()

    print(" - Creating Player")
    audio_source = discord.FFmpegPCMAudio(soundFile)
    print(f" - Playing {soundFile}")
    voice.play(audio_source, after=None)
    time.sleep(5)
    print(f" - Disconnecting from '{channel}'")
    await voice.disconnect()
###

#
# OctoPrint Commands
#
@bot.command()
async def printstat(ctx):

    datestring = datetime.now()
    datestring = datestring.strftime("%m/%d/%Y-%H:%M:%S")

    print(f"[{datestring}]: {ctx.message.author.display_name} called $printstat")

    #print("========== Command Called at %s ==========" % (time.strftime("%Y%m%d-%H%M%S"))) 
    # We haven't yet changed the state of the light, setting this to False
    turned_on_light = False

    # No Data from Printer?
    operational = True
    
    # Try to get the status of the 3D printer light
    print(" - Getting Printer Light Status")
    #work_lights = remote.get_state(hassapi, 'switch.work_lights')
    work_lights = requests.get(hassURL, headers=hassHEADERS)
    print(f"   JSON Response from HomeAssistant: {work_lights.text}")

    work_lights = json.loads(work_lights.text)

    # Making sure that the API request succeeded.  If it has, there will be a state attribute added to
    #  work_lights.  
    try:
        work_lights["state"]
    except:
        print("  ! Unable to get light status from Homeassistant, notifying chat channel")
        await ctx.send("Hmm, I can't tell if the light is on... oh well [Hass API error]")

        # Create empty dict w/ state of unknown
        work_lights = {'state': "unknown"}

    # If the light is off, let's turn it on before we take a picture
    if work_lights["state"] == 'off':
        print(" - Lights are off, turning on for image capture")
        turned_on_light = True

        lightMessages = ["Woah, it's pretty dark in R0b3's Basement... Give me a couple seconds to turn on a light.", \
        "Turning on a light, give me a moment...", \
        "I can't see a thing, let me get a light...", \
        "Where's that light switch?...", \
        "Uh, the lights are off.  Give me a sec...", \
        "Replacing the light bulb, just a moment..."]

        await ctx.send(f"{random.choice(lightMessages)}")

        try:
            # REST API call to home assistant to turn the light off.
            #remote.call_service(hassapi, 'switch', 'turn_on', {'entity_id':'{}'.format(HASS_LIGHT)})
            hassAPIURL = HASS_URL + "/api/services/switch/turn_on"
            payload = f'{{"entity_id": "{HASS_LIGHT}"}}'
            #print(f"  - Payload String: {payload}")
            response = requests.post(hassAPIURL, headers=hassHEADERS, data=payload)
            #print(f"  - POST Response: {response.text}")

        except Exception as e:
            print(f"  ! Unable to turn on light; ERROR: {e}")
            await ctx.send("Sorry, I was unable to turn on the light.")
            pass

        time.sleep(3)

    # Randomly generate a filename to save the image to
    file_name = random.randrange(1,10000)
    full_file_name = str(file_name) + '.jpg'

    # Get an image from OctoPrint and save it
    print(" - Getting image from Webcam")
    urllib.request.urlretrieve("http://%s:8080/?action=snapshot" % (OCTOPRINT_IP_ADDRESS), full_file_name)

    # If we turned on the light, let's be nice and turn it back off
    if turned_on_light:
        print(" - Turning Light back Off")
        try:
            # REST API call to home assistant to turn the light off.
            #remote.call_service(hassapi, 'switch', 'turn_on', {'entity_id':'{}'.format(HASS_LIGHT)})
            hassAPIURL = HASS_URL + "/api/services/switch/turn_off"
            payload = f'{{"entity_id": "{HASS_LIGHT}"}}'
            response = requests.post(hassAPIURL, headers=hassHEADERS, data=payload)
            #print(f"  - POST Response: {response.text}")

        except Exception as e:
            print(f"  ! Unable to turn on light; ERROR: {e}")
            print("  ! Unable to turn off light")
            pass

    # Send the image to the chat channel
    print(" - Uploading image to chat channel")
    file = discord.File(full_file_name, filename=full_file_name)
    await ctx.send("3D Printer Snapshot:", file=file)
    
    # Remove the Image File now that it is no longer needed
    print(" - Deleting temporary image file")
    os.remove(full_file_name)
   
    print(" - Connecting to OctoPrint API")
    # Testing OctoPrint API Status.  If printer is off, I won't receive JSON data.
    try:
        operational = json.loads(octoapi.get_printer_dict())
    except:
        # Printer is Offline
        operational = False
        
    if not operational:
        print(" - 3D Printer is on and printing, getting details")

        # Get the name of the file currently being printed
        try:
            print("  - Getting Filename")
            print_filename = octoapi.get_printFileName()
        except:
            print_filename = ""

        try:
            print("  - Getting % Completion")
            # Try to get the % of Completion
            print_completion = round(octoapi.get_completion(), 2)
        except:
            print_completion = "Unknown"

        # Get the current print time in seconds
        try:
            print("  - Getting Seconds Elapsed")
            print_seconds = octoapi.get_printTime()
        except:
            print("Unable to get Seconds data from OctoPrint")

        # Get the time remaining for current print job in seconds
        try:
            print("  - Getting Seconds Left")
            print_secondsleft = octoapi.get_printTimeLeft()
        except:
            print("  ! Unable to get Seconds Left from OctoPrint")

        try:
            print("  - Converting Seconds to Hours")
            # Try to convert seconds to hours
            print_hours = int(((print_seconds / 60) / 60))
        except:
            print_hours = "Unknown"

        try:
            print("  - Converting Seconds left to Hours left")
            # Try to convert seconds left to hours left
            print_hoursleft = int(((print_secondsleft / 60) / 60))
        except:
            print_hoursleft = "Unknown"
    
        try:
            print("  - Calculating Minutes Elapsed")
            # Using the total number of minutes minus the total number of whole hours to get the minutes remaining
            print_min = int(((print_seconds / 60) - (print_hours * 60)))
        except:
            print_min = "Unknown"
    
        try:
            print("  - Calculating Minutes Left")
            # Same as above but for the minutes left in print job
            print_minleft = int(((print_secondsleft / 60) - (print_hoursleft * 60)))
        except:
            print_minleft = "Unknown"

        time_elapsed = "%s Hours %s Minutes" % (print_hours, print_min)
        time_remaining = "%s Hours %s Minutes" % (print_hoursleft, print_minleft)

        printer_bed = "%s°C" % (octoapi.get_printer_dict()["temperature"]["bed"]["actual"])
        printer_hotend = "%s°C" % (octoapi.get_printer_dict()["temperature"]["tool0"]["actual"])

        embed = discord.Embed(title="R0b3's 3D Printer Status", description="Current Job: " + print_filename, color=0xF5A623)

        embed.add_field(name="Percent Complete: ", value=str(print_completion) + "%")
        embed.add_field(name="Time Elapsed: ", value=time_elapsed)
        embed.add_field(name="Time Remaining: ", value=time_remaining)
        embed.add_field(name="Bed Temp.: ", value=printer_bed)
        embed.add_field(name="Hotend Temp.: ", value=printer_hotend)
        print(" - Sending details to chat channel")
        await ctx.send(embed=embed)

    else:
        print(" - 3D Printer is not on or is not printing")
        embed = discord.Embed(title="Printer is Offline")
        print(" - Notifying chat channel")
        await ctx.send(embed=embed)

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="R0b3BOT", description="Derpy Derp of a Bot :P", color=0xeee657)
          
    # give info about you here
    embed.add_field(name="Author", value="R0b3")
                        
    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

    # give users a link to invite thsi bot to their server
    embed.add_field(name="Invite", value="[Invite link](https://discordapp.com/api/oauth2/authorize?client_id=416312716677087233&permissions=51264&scope=bot)")

    await ctx.send(embed=embed)

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="R0b3BOT", description="List of commands are:", color=0xeee657)
    embed.add_field(name="$printstat", value="Uploads a snapshot of Rich's 3D printer and current stats", inline=False)
    embed.add_field(name="$explain", value="Displays Dalek EXPLAIN gif", inline=False)
    embed.add_field(name="$holyshit", value="Displays Marty McFly HOLY SHIT gif", inline=False)
    embed.add_field(name="$greetings", value="Gives a nice greet message", inline=False)
    embed.add_field(name="$cat", value="Gives a cute cat gif to lighten up the mood.", inline=False)
    embed.add_field(name="$bitch @member", value="Plays 'monkey_bitch.mp3' to the users voice channel, if no user is specified it will play in your own voice channel", inline=False)
    embed.add_field(name="$boom @member", value="Plays 'BoomBitch.mp3' to the users voice channel, if no user is specified it will play in your own voice channel", inline=False)
    embed.add_field(name="$cowbell @member", value="Plays 'More_cowbell.mp3' to the users voice channel, if no user is specified it will play in your own voice channel", inline=False)
    embed.add_field(name="$oops @member", value="Plays 'Oops.mp3' to the users voice channel, if no user is specified it will play in your own voice channel", inline=False)
    embed.add_field(name="$promoted @member", value="Plays 'Promoted.mp3' to the users voice channel, if no user is specified it will play in your own voice channel", inline=False)
    embed.add_field(name="$trololo @member", value="Plays 'Trololo.mp3' to the users voice channel, if no user is specified it will play in your own voice channel", inline=False)
    embed.add_field(name="$leeroy @member", value="Plays 'leeroy.mp3' to the users voice channel, if no user is specified it will play in your own voice channel", inline=False)
    embed.add_field(name="$info", value="Gives a little info about the bot", inline=False)
    embed.add_field(name="$help", value="Gives this message", inline=False)

    await ctx.send(embed=embed)

bot.run(DISCORD_AUTH_TOKEN)