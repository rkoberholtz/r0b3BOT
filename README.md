*** This project lives @ https://gitlab.rickelobe.com/Bots/R0b3BOT ***

[![pipeline status](http://gitlab.rickelobe.com/Bots/r0b3BOT/badges/master/pipeline.svg)](http://gitlab.rickelobe.com/Bots/r0b3BOT/commits/master)

# Description
This is R0b3's Discord Bot.  It's creation was basically a challenge posed a coworker who said "Hey, you can write Discord Bots in Python... Make one to display your 3D printer status!".  But as time went on, a few more features were added.  Aside from being able to query and monitor your 3D printer, it can also fetch the current status of a service monitroed by your [StatPing](https://github.com/statping/statping) instance.  In addition to just fetching the current status of a service, you can subscribe to receive alerts for any StatPing service state change.  All subscriptions are persistent and will remain even after the bot is restarted.

# Features
*  Query & Monitor 3D Printer Status using `$printstat` command(Requires that your printer is connected to [Octoprint](https://octoprint.org/))<br>
![](images/Discord_Printstat_Command.png)
*  Query serivces states on StatPing using the `$spstatus`
*  Use `$spsub` to "Subscribe" to service change alerts for StatPing services.  Subscribed alerts are persistent and are not lost on bot restart.<br>
![Example service alert](images/Service_alert.png)
*  Play a selection of sound clips to voice channel members using the various commands (`$torololo`, `$oops`, `$promoted`, etc)

# Commands
![Screenshot of $help](images/command_list.png)

# Requirements
1. discord.py version 1.2.4 or greater<br>
    <code> pip install discord.py </code>

# Configuration
1. Create a Discord Bot via Developer tools<br>
2. Enter configuration parameters in bot_config.conf.example<br>
3. Enter OctoPrint config parameters in octoapi.conf.example<br>
4. Rename *.example files as *.conf<br>