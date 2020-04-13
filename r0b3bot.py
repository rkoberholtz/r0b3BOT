#!/usr/bin/python3

import discord
from discord.ext import commands
import urllib.request
import random
import os
import sys
import octoapi
import time
from datetime import datetime
import configparser
import json
from discord import FFmpegPCMAudio
from discord.utils import get
from discord.voice_client import VoiceClient
import requests
import asyncio
#from aiofile import AIOFile
import aiofiles as aiof
import pickle


#Record the time the bot started
start_time = time.time() 

config = configparser.RawConfigParser()
configFilePath = r'bot_config.conf'

# Last error message variable used by $last_error command to display in discord
global last_error
last_error = "No errors have been recorded."

try:
    config.read(configFilePath)
except:
    print("Error loading config!  Please check config file 'bot-config.conf'")

#
# Read in bot configurations
#

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
BOT_COMMAND_PREFIX = config.get('bot-config', 'bot_command_prefix')
STATPING_URL = config.get('bot-config', 'statping_url')
STATPING_API_KEY = config.get('bot-config', 'statping_api_key')
statpingURL = STATPING_URL + "/api/services"
statpingHEADERS = {
    'Authorization': f"Bearer {STATPING_API_KEY}",
    'content-type': 'application/json',
}

# Configure bot
bot = commands.Bot(command_prefix=BOT_COMMAND_PREFIX, description='A derpy derp of a bot.')

# Printing configuration details to console
print(f"HomeAssistant URL: {hassURL}")
print(f"HomeAssistant URL HEADERS: {hassHEADERS}")
print(f"HomeAssistant Light: {HASS_LIGHT}")
print(f"OctoPrint IP Address: {OCTOPRINT_IP_ADDRESS}")
print(f"StatPing Server: {STATPING_URL}")
print(f"StatPing API Key: {STATPING_API_KEY}")
print(f"StatPing URL Headers: {statpingHEADERS}")

# On Ready
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    print("Setting activity to 'Listenting to your commands'")
    activity = discord.Activity(name="your $commands",type=discord.ActivityType.listening)
    await bot.change_presence(activity=activity)

    #Run StatPing_Monitor
    await StatPing_Monitor()

@bot.command()
async def greetings(ctx):
    await ctx.send(":smiley: :wave: Hello there!")


@bot.event
async def on_command_error(ctx, error):
    global last_error
    if isinstance(error, commands.CommandOnCooldown):
        seconds = round(error.retry_after,1)
        print(f" - Error, user tried to use command while in cooldown (wait is: {seconds}")
        await ctx.send(f"This command is ratelimited per user, please try again in {seconds}s")
    if isinstance(error, commands.CommandInvokeError):
        print(" - ERROR: encountered 'CommandInvokeError'")
        print(f" - Dumping error: {error}")
        last_error = error
        await ctx.send("Error, unable to complete your request.")
    else:
        print('Oopsie, I found an error...')
        print(f"Error: {error}")
        last_error = error

#
# Debug commands
#
@bot.command()
async def last_error(ctx):
    await ctx.send(f"Last error recorded: {last_error}")

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
# Image Commands
#
@bot.command()
async def smudge(ctx):
    print(" - Uploading Smudge to chat channel")
    file = discord.File("./images/smudge.png", filename="smudge.png")
    await ctx.send(file=file)

#
# Voice Commands
#

@bot.command()
@commands.cooldown(rate=1, per=30.0, type=commands.BucketType.user)
async def bitch(ctx, member : discord.Member="NONE"):
    datestring = datetime.now()
    datestring = datestring.strftime("%m/%d/%Y-%H:%M:%S")
    if ctx.message.channel.is_nsfw():
        await play_sound(ctx, member, "./sounds/monkey_bitch.mp3", "$bitch", 5)
    else:
        print(f"[{datestring}]: {ctx.message.author.display_name} called $bitch, but is not in a NSFW channel")
        await ctx.send("This command is too explicit for you!")

@bot.command()
@commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
async def cowbell(ctx, member : discord.Member="NONE"):
    await play_sound(ctx, member, "./sounds/More_cowbell.mp3", "$cowbell", 5)

@bot.command()
@commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
async def boom(ctx, member : discord.Member="NONE"):
    datestring = datetime.now()
    datestring = datestring.strftime("%m/%d/%Y-%H:%M:%S")
    if ctx.message.channel.is_nsfw():
        await play_sound(ctx, member, "./sounds/BoomBitch.mp3", "$boom", 5)
    else:
        print(f"[{datestring}]: {ctx.message.author.display_name} called $boom, but is not in a NSFW channel")
        await ctx.send("This command is too explicit for you!")

@bot.command()
@commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
async def oops(ctx, member : discord.Member="NONE"):
    await play_sound(ctx, member, "./sounds/Oops.mp3", "$oops", 5)

@bot.command()
@commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
async def trololo(ctx, member : discord.Member="NONE"):
    await play_sound(ctx, member, "./sounds/Trololo.mp3", "$trololo", 5)

@bot.command()
@commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
async def leeroy(ctx, member : discord.Member="NONE"):
    await play_sound(ctx, member, "./sounds/leeroy.mp3", "$leeroy", 5)

@bot.command()
@commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
async def promoted(ctx, member : discord.Member="NONE"):
    await play_sound(ctx, member, "./sounds/Promoted.mp3", "$promoted", 5)

@bot.command()
@commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
async def wow(ctx, member : discord.Member="NONE"):
    await play_sound(ctx, member, "./sounds/wow.mp3", "$wow", 5)

@bot.command()
@commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
async def aww(ctx, member : discord.Member="NONE"):
    await play_sound(ctx, member, "./sounds/Awww_Bitch.mp3", "$aww", 5)

@bot.command()
@commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
async def eia(ctx, member : discord.Member="NONE"):
    await play_sound(ctx, member, "./sounds/awesome.mp3", "$eia", 11)

@bot.command()
@commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
async def yaw(ctx, member : discord.Member="NONE"):
    await play_sound(ctx, member, "./sounds/yaw.mp3", "$yaw", 6)

@bot.command()
@commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
async def heavy(ctx, member : discord.Member="NONE"):
    await play_sound(ctx, member, "./sounds/heavy.mp3", "$heavy", 6)

@bot.command()
@commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
async def rs(ctx, member : discord.Member="NONE"):
    datestring = datetime.now()
    datestring = datestring.strftime("%m/%d/%Y-%H:%M:%S")
    if ctx.message.channel.is_nsfw():
        soundfiles = ["./sounds/leeroy.mp3","./sounds/monkey_bitch.mp3","./sounds/More_cowbell.mp3","./sounds/BoomBitch.mp3","./sounds/Promoted.mp3","./sounds/Trololo.mp3","./sounds/Oops.mp3"]
        await play_sound(ctx, member, random.choice(soundfiles), "$rs")
    else:
        print(f"[{datestring}]: {ctx.message.author.display_name} called $rs, but is not in a NSFW channel")
        await ctx.send("This command is too explicit for you!")

async def play_sound(ctx, member : discord.Member, soundFile, command, playtime):

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
    time.sleep(1)
    voice.play(audio_source, after=None)
    time.sleep(playtime)
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
        activity = discord.Activity(name=f"3D Print @ {str(print_completion)}%",type=discord.ActivityType.watching)
        await bot.change_presence(activity=activity)
        await updateStatus()

    else:
        print(" - 3D Printer is not on or is not printing")
        embed = discord.Embed(title="Printer is Offline")
        print(" - Notifying chat channel")
        await ctx.send(embed=embed)

async def updateStatus():

    # Initialize variables
    print_completion = 0
    unknowns = 0
    #While the print status is less than 100 % complete, keep updating
    while print_completion < 100:
        try:
            print("  - Getting % Completion")
            # Try to get the % of Completion
            print_completion = round(octoapi.get_completion(), 2)
        except:
            print_completion = 999
            unknowns += 1
        
        #Set the activity to the new percent complete value
        if print_completion != 999:
            activity = discord.Activity(name=f"3D Print @ {str(print_completion)}%",type=discord.ActivityType.watching)
        else:
            activity = discord.Activity(name=f"3D Print @ ERROR",type=discord.ActivityType.watching)

        await bot.change_presence(activity=activity)

        if (unknowns >= 5):
            break
        await asyncio.sleep(30)
    
    # Flash the status @ 100% before changing back to listening to your commands, only if uknowns !5.
    if unknowns != 5:
        for x in range(20):
            activity = discord.Activity(name="-",type=discord.ActivityType.watching)
            await bot.change_presence(activity=activity)
            await asyncio.sleep(1)
            activity = discord.Activity(name=f"3D Print @ {str(print_completion)}%",type=discord.ActivityType.watching)
            await bot.change_presence(activity=activity)
            await asyncio.sleep(1)

    print(" - Done watching 3D Printer status")
    await asyncio.sleep(3)
    activity = discord.Activity(name="your commands",type=discord.ActivityType.listening)
    await bot.change_presence(activity=activity)


@bot.command()
async def info(ctx):
    embed = discord.Embed(title="R0b3BOT", description="Derpy Derp of a Bot :P", color=0xeee657)
          
    # give info about you here
    embed.add_field(name="Author", value="R0b3")
                        
    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

    # give users a link to invite thsi bot to their server
    embed.add_field(name="Invite", value="[Invite link](https://discordapp.com/api/oauth2/authorize?client_id=416312716677087233&permissions=51264&scope=bot)")

    # Bot Uptime
    second = time.time() - start_time
    minute, second = divmod(second, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)
    week, day = divmod(day, 7)
    week = int(week)
    day = int(day)
    hour = int(hour)
    minute = int(minute)
    second = int(second)
    embed.add_field(name="Uptime [WW:DD:HH:MM:SS]:", value=f"{week:02d}:{day:02d}:{hour:02d}:{minute:02d}:{second:02d}", inline=False)


    # Gitlab link to source
    embed.add_field(name="Source Code:", value="[R0b3Bot on Gitlab](https://gitlab.rickelobe.com/Bots/r0b3BOT)", inline=False)
    await ctx.send(embed=embed)

bot.remove_command('help')

@bot.command()
async def spalert(ctx, service = "NONE"):
#async def spalert(ctx, cmd = "NONE", arg = "NONE"):

    # if cmd != "NONE":
    #    if cmd == "add":
    #        spalert +=
    if service != "NONE":
        
        #await get_stp_status(ctx, service.lower())
        result = await get_stp_status(service.lower())

        if result == "service not found":
            await ctx.send(f"'{service}' was not found")
        elif result['online']:
            await ctx.send(f"{result['name']} is Online")
        elif not result['online']:
            await ctx.send(f"{result['name']} is Offline")
        else:
            await ctx.send(f"Received an unexpected result '{result}' querying '{service}'")

    else:
        await ctx.send("Please speficy a service name to query.")

    
    
@bot.command()
async def spsub(ctx, service = "NONE"):

    currentsub_request = []
    datestring = datetime.now()
    datestring = datestring.strftime("%m/%d/%Y-%H:%M:%S")
    print(f"[{datestring}]: {ctx.message.author.display_name} called '$spsub {service}'")

    if service != "NONE":

        print(f"Querying status of '{service}' to see if it exists")
        service_state = await get_stp_status(service)

        if service_state != "service not found":
        
            print(f"'{service}' exists, starting monitor")
            await ctx.send(f"'{service_state['name']}' added to monitored services")
            currentsub_request.append(ctx)
            currentsub_request.append(service)
            currentsub_request.append("online")

            await sp_monitor(currentsub_request)
        
        else:
            print(f"'{service}' does not exist, cancelling subscription")
            await ctx.send(f"{service} was not found")

@bot.command()
async def spsub_T(ctx, service = "NONE"):

    spsublist = {} # Statping Subscription list to be read in from file
    #  Structure of spsublist nested dictionary
    #   spsublist[service name][list of channel ids][a state value]
    #   dict = {'Plex': {'state' : 'online', 'channels' : ['1232', '43234']}
    #           'Space Eingineers' : {'state' : online', 'channels' : ['2343', '54563']}}
    #
    currentsub_request = [] # list of elements detailing the current sub request
    datestring = datetime.now()
    datestring = datestring.strftime("%m/%d/%Y-%H:%M:%S")

    print(f"[{datestring}]: {ctx.message.author.display_name} called '$spsub {service}'")

    # Only work on this if the user has supplied a service name to monitor, a value of NONE
    #  means nothing was specified.
    if service != "NONE":

        # Verify that the service name requested acutally exists
        print(f">> Querying status of '{service}' to see if it exists")
        service_state = await get_stp_status(service)

        # If the service exists, proceed with adding it to the list.
        if service_state != "service not found":
        
            print(f">> '{service}' exists, adding to StatPing Monitor")
            await ctx.send(f"'{service_state['name']}' added to monitored services")
            currentsub_request.append(ctx.message.channel.id)
            print(f">> channel ID: {ctx.message.channel}")
            #currentsub_request.append(ctx)
            currentsub_request.append(service_state['name'])
            currentsub_request.append("online")

            # read in data file containing dict of subscriptions
            print(">> Reading in spsublist.dat")
            if os.path.exists('spsublist.dat'):

                # Read in spsublist
                async with aiof.open('spsublist.dat', 'rb') as datafile:
                    pickled_spsublist = await datafile.read()
                    spsublist = pickle.loads(pickled_spsublist)
                
                for service, info in spsublist.keys():
                    # service = service_names
                    # info = dict of service information

                    if service == currentsub_request[1]:
                        # This service matched what the user is trying to subscribe to
                        # Now we need to check if this is for the same channel
                        for channels in service['channels']:
                            if channel == currentsub_request[0]:
                                print(">> Subscribed Already")
                            else:
                                # Append the current channel id to the list for this service
                                print(f">> Appending {currentsub_request[1]} to {channel}")
                                spsublist[service]['channels'].append(currentsub_request[1])
                    
            else:

                print(">> spsublist.dat does not exist, new file will be created")
            
                # append new subscription to dict
                print(">> Creating new dictionary")
                spsublist[currentsub_request[1]] = {'state' : 'online', 'channels' : (currentsub_request[0])}

            #Write updated array to data file
            print(">> Saving dictionary to spsublist.dat")
            async with aiof.open('spsublist.dat', 'wb') as datafile:
                pickled_spsublist = pickle.dumps(spsublist, protocol=4)
                await datafile.write(pickled_spsublist)
                #await datafile.fsync()
                await datafile.flush()
            
            print(">> Done")
            await ctx.send(f"'{service_state['name']}' added to monitored services")
        
        else:
            print(f">> '{service}' does not exist, cancelling subscription")
            await ctx.send(f"{service} was not found")

async def StatPing_Monitor():

    # reads in "spsublist.dat" every 60 seconds then iterates
    # through to check for service status changes.  This function will need to check
    # that "spsublist.dat" exists and is not empty.  This function should be called
    # in bot.on_ready

    #new_spsublist = {}

    # read in data file containing list of subscriptions
    while True:
        print("Statping Monitor: Reading in spsublist.dat")
        if os.path.exists('spsublist.dat'):
            async with aiof.open('spsublist.dat', 'rb') as datafile:
                pickled_spsublist = await datafile.read()
                spsublist = pickle.loads(pickled_spsublist)
        
            for service in spsublist.keys():
                # service used to be subscription

                status = await get_stp_status(service)

                if status['online'] and service['state'] == 'online':

                    # nothing has changed, no alert needed
                    await asyncio.sleep(1)
                elif not status['online'] and service['state'] == "offline":

                    # again, nothing has changed no alert needed
                    await asyncio.sleep(1)
                else:
                    
                    print(f"Status of {service}' has changed, notifying subscribed channels")

                    if status['online']:
                        for channel in service['channels']:
                            ctx = bot.get_channel(channel)
                            embed = discord.Embed(title=f"Service Alert", description=f"{service} is Online!", color=0x00ff40)
                            await ctx.send(embed=embed)
                            spsublist[service]['state'] = 'online'

                    elif not status['online']:
                        for channel in service['channels']:
                            ctx = bot.get_channel(channel)
                            embed = discord.Embed(title=f"Service Alert", description=f"{service} is Offline!", color=0xff2200)
                            await ctx.send(embed=embed)
                            spsublist[service]['state'] = 'offline'

                    else:
                        for channel in service['channels']:
                            ctx = bot.get_channel(channel)
                            embed = discord.Embed(title=f"Service Alert", description=f"{service} is in an unknown state!", color=0xffff00)
                            await ctx.send(embed=embed)
                
                new_spsublist.append(subscription)
            
            # Write status changes to spsublist.dat
            async with aiof.open('spsublist.dat', 'wb') as datafile:
                pickled_spsublist = pickle.dumps(spsublist)
                await datafile.write(pickled_spsublist)
                #await datafile.fsync()
                await datafile.flush()
                    
        else:
            print(">> spsublist.dat does not exist, nothing to do.")
        
        await asyncio.sleep(60)
 

async def sp_monitor(sublist):

    # Checks the services listed in spsublist for status change
    # Sublist is a list of 3 items:
    #    - ctx (used to send alert to channel)
    #    - service (the name of the service to check)
    #    - status string (last status of the service, either 'online' or 'offline')

    ctx = sublist[0]


    while True:

        status = await get_stp_status(spsublist[1])
        if status['online'] and spsublist[2] == "online":
            # nothing has changed, no alert needed
            await asyncio.sleep(1)
        elif not status['online'] and spsublist[2] == "offline":
            # again, nothing has changed no alert needed
            await asyncio.sleep(1)
        else:
            print(f"Status of {status['name']}' has changed")
            if status['online']:
                embed = discord.Embed(title=f"{status['name']} Service Alert", description=f"{spsublist[1]} is Online!", color=0x00ff40)
                await ctx.send(embed=embed)
                #await ctx.send(f"{spsublist[1]} is Online!")
                spsublist[2] = "online"
            elif not status['online']:
                embed = discord.Embed(title=f"{status['name']} Service Alert", description=f"{spsublist[1]} is Offline!", color=0xff2200)
                await ctx.send(embed=embed)
                #await ctx.send(f"{spsublist[1]} is Offline!")
                spsublist[2] = "offline"
            else:
                embed = discord.Embed(title=f"{status['name']} Service Alert", description=f"{spsublist[1]} is in an unknown state!", color=0xffff00)
                await ctx.send(embed=embed)
                #await ctx.send(f"Unknown state for service {spsublist[1]}")
        await asyncio.sleep(60)

async def get_stp_status(service):

    # Get StatPing status via REST API
    spservice_array = requests.get(statpingURL, headers=statpingHEADERS)
    found = False

    # spservice_array is json data, need to treat it as such
    for spservice in spservice_array.json():

        # using lower() to eliminate any case mismatch problems
        if spservice['name'].lower() == service:
            
                found = True
                return spservice

    # Want to alert user if the service was not found
    if not found:  
        return "service not found"  


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="R0b3BOT", description="List of commands are:", color=0xeee657)
    embed.add_field(name="$printstat", value="Uploads a snapshot of Rich's 3D printer and current stats", inline=False)
    embed.add_field(name="$explain", value="Displays Dalek EXPLAIN gif", inline=False)
    embed.add_field(name="$holyshit", value="Displays Marty McFly HOLY SHIT gif", inline=False)
    embed.add_field(name="$greetings", value="Gives a nice greet message", inline=False)
    embed.add_field(name="$cat", value="Gives a cute cat gif to lighten up the mood.", inline=False)
    embed.add_field(name="$bitch @member", value="Plays clip of BigEric420 saying 'maybe you shouldn't be such a bitch.mp3'", inline=False)
    embed.add_field(name="$boom @member", value="Plays 'Boom Bitch' sound clip", inline=False)
    embed.add_field(name="$cowbell @member", value="Plays 'SNL More Cowbell' sound clip", inline=False)
    embed.add_field(name="$oops @member", value="Plays 'Oops.mp3'", inline=False)
    embed.add_field(name="$promoted @member", value="Plays Battlefield Friends 'PROMOTED!' sound clip", inline=False)
    embed.add_field(name="$trololo @member", value="Plays a clip of Trololo song", inline=False)
    embed.add_field(name="$leeroy @member", value="Plays Leeeerrroooyyy Jenkins clip", inline=False)
    embed.add_field(name="$eia @member", value="Plays 'Everything is Awesome' song clip")
    embed.add_field(name="$info", value="Gives a little info about the bot", inline=False)
    embed.add_field(name="$help", value="Gives this message", inline=False)
    embed.add_field(name="$last_error", value="Will display the real error message the bot has last encountered for additional debugging info")
    embed.add_field(name="$spalert servicename", value="Retrieves status of service from StatPing")
    await ctx.send(embed=embed)

    embed = discord.Embed(title="A note about sound clips:", description="Sound clips are only played in voice channels.  If a user is not specified when calling the command, the sound will played in the channel of that issuing user is currently joined to.  When a username is specified, the bot will play the sound in the channel that user is currently in.")
    await ctx.send(embed=embed)

bot.run(DISCORD_AUTH_TOKEN)
