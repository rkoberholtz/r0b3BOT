#!/usr/bin/python3

import discord
from discord.ext import commands
import urllib.request
import random
import os
import octoapi

bot = commands.Bot(command_prefix='$', description='A bot that greets the user back.')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_command_error(error, ctx):
    print('Oopsie, I found an error...')
    print('Channel:')
    print(ctx)
    print('Error:')
    print(error)

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
# OctoPrint Commands
#
@bot.command()
async def printpic(ctx):
    file_name = random.randrange(1,10000)
    full_file_name = str(file_name) + '.jpg'
    urllib.request.urlretrieve("http://10.3.0.137:8080/?action=snapshot", full_file_name)

    file = discord.File(full_file_name, filename=full_file_name)
    await ctx.send("3D Printer Status", file=file)

    #with open(full_file_name, 'rb') as f:
    #    await client.send(ctx,f)
    os.remove(full_file_name)
   
    try:
        print_filename = octoapi.get_printFileName()
    except:
        print_filename = "Unknown"

    try:
        print_completion = round(octoapi.get_completion(), 2)
    except:
        print_completion = "Unknown"

    print_seconds = octoapi.get_printTime()
    print_secondsleft = octoapi.get_printTimeLeft()

    try:
        print_hours = int(((print_seconds / 60) / 60))
    except:
        print_hours = "Unknown"

    try:
        print_hoursleft = int(((print_secondsleft / 60) / 60))
    except:
        print_hoursleft = "Unknown"
    
    try:
        print_min = int(((print_seconds / 60) - (print_hours * 60)))
    except:
        print_min = "Unknown"
    
    try:
        print_minleft = int(((print_secondsleft / 60) - (print_hoursleft * 60)))
    except:
        print_minleft = "Unknown"

    time_elapsed = "%s Hours %s Minutes" % (print_hours, print_min)
    time_remaining = "%s Hours %s Minutes" % (print_hoursleft, print_minleft)

    embed = discord.Embed(title="R0b3's 3D Printer Status", description="File Name: " + print_filename, color=0xF5A623)
    embed.add_field(name="Percent Complete: ", value=str(print_completion) + "%")
    embed.add_field(name="Time Elapsed: ", value=time_elapsed)
    embed.add_field(name="Time Remaining: ", value=time_remaining)
    await ctx.send(embed=embed)

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="R0b3BOT", description="Derpy Derp of a Bot", color=0xeee657)
          
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
    embed.add_field(name="$printpic", value="Takes snapshot of Rich's 3D printer and uploads to channel", inline=False)
    embed.add_field(name="$explain", value="Displays Dalex EXPLAIN gif", inline=False)
    embed.add_field(name="$holyshit", value="Displays Marty McFly HOLY SHIT gif", inline=False)
    embed.add_field(name="$greetings", value="Gives a nice greet message", inline=False)
    embed.add_field(name="$cat", value="Gives a cute cat gif to lighten up the mood.", inline=False)
    embed.add_field(name="$info", value="Gives a little info about the bot", inline=False)
    embed.add_field(name="$help", value="Gives this message", inline=False)

    await ctx.send(embed=embed)

bot.run('NDE2MzEyNzE2Njc3MDg3MjMz.DXCuVg.djVGXmyd7r7XWo_NbKOVcBsv55k')
