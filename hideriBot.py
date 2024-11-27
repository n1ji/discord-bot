                                        #Importing Libraries

# os library to use environment variables
# discord and ec2_metadata because that's pretty much the whole point of this project. (They allow us to interact with AWS EC2 & Discord)
# dotenv so we can import the .env file into python
# commands from discord.ext which allows us to use the bot with a command prefix.
# pytz converts time
# datetime to get the time

import os
import discord
from ec2_metadata import ec2_metadata
from dotenv import load_dotenv
from discord.ext import commands
import pytz
from datetime import datetime

# Load the .env file
load_dotenv('myra.env')

# Get the token from the environment variable
token = os.getenv('TOKEN')

# Ensure that the bot has the proper gateway intents, otherwise we can't read user messages.
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

#This tells the bot to look for ! when we want to invoke a command.
hideriBot = commands.Bot(command_prefix="!", intents=intents)



                                        #EC2 Things

        # Declare EC2 metadata variables as none, otherwise the program will not run.
        # If you set these variables = ec2_metadata.* they will try to pull data that doesn't exist when you run this program outside of EC2.
instanceID = None
instanceRegion = None
instanceIP = None
instanceZone = None
instanceType = None

        # Exception handler to get EC2 metadata and print that the EC2 data is available.
try:
    instanceID = ec2_metadata.instance_id
    instanceRegion = ec2_metadata.region
    instanceIP = ec2_metadata.public_ipv4
    instanceZone = ec2_metadata.availability_zone
    instanceType = ec2_metadata.instance_type
    print("EC2 Metadata is Available!")

        # If the exception handler can't find any data, then use faux data and print that EC2 data is unavailable.
except Exception:
    instanceID = "i-dsgc6f4g33ehwhl6p"
    instanceRegion = "ca-bc-south-202"
    instanceIP = "52.142.124.215"
    instanceZone = "ca-bc-northwest-7c"
    instanceType = "Python Instance"
    print("EC2 metadata is unavailable.")



                                        # Event that runs when the program is run
        # This prints to let us know that we logged into the bot account and sets a custom status.

@hideriBot.event
async def on_ready():
    print(f"Logged into bot: {hideriBot.user}")
    await hideriBot.change_presence(
        status=discord.Status.online,
        activity=discord.CustomActivity('Type !help for commands.')
    )


                                        # Event that is run every time a message is sent.
        #This converts discord time into Pacific time and prints the message sent by the user. Also ignores bot messages as they tend to fill up the terminal with redundant information.
@hideriBot.event
async def on_message(message):

    # Ignore messages from the bot
    if message.author == hideriBot.user:
        return
    
    # Convert Discord UTC timestamp to PST. Discord provides message timestamps in UTC so we take this to use later.
    utc_time = message.created_at

    # Set the timezone we want the timestamp to display.
    timezone = pytz.timezone("US/Pacific")

    # Convert to timezone set above.
    local_time = utc_time.astimezone(timezone)
    
    # Format the timestamp to the best format AKA day, month, year.
    timestamp = local_time.strftime('%d-%m-%Y %H:%M:%S')
    
    # Print every message the bot reads including the user that sent it and the time it was sent.
    print(f'Message in {message.channel} from {message.author}: "{message.content}" @ [{timestamp}]')

    # This has to be added for ! prefix commands to continue working outside the event
    await hideriBot.process_commands(message)



                                        ### Commands ###

# Restrict all the commands to only bot channels and direct messages using a function.
def botChannel(ctx):
    return ctx.channel.type == discord.ChannelType.private or (
        isinstance(ctx.channel, discord.TextChannel) and ctx.channel.name.lower() == "bot"
    )

# Every command runs the channel checker function before replying and then runs a function to reply to the user.

# Hi
@hideriBot.command(name="hi", aliases=["hello", "hey", "hola"]) # Hi Command with Aliases
@commands.check(botChannel)
async def hiCommand(ctx):
    await ctx.reply(f"Hello {ctx.author.display_name}!")

# Bye
@hideriBot.command(name="bye", aliases=["goodbye", "see ya", "adios"]) # Bye Command with Aliases
@commands.check(botChannel)
async def byeCommand(ctx):
    await ctx.reply(f"Bye {ctx.author.display_name}!")

# Region
@hideriBot.command(name="region")
@commands.check(botChannel)
async def regionCommand(ctx):
    await ctx.reply(f"Here is the EC2 Instance Region: {instanceRegion}")

# IP
@hideriBot.command(name="ip")
@commands.check(botChannel)
async def ipCommand(ctx):
    await ctx.reply(f"Here is the public EC2 Instance IP: {instanceIP}")

# Zone
@hideriBot.command(name="zone")
@commands.check(botChannel)
async def zoneCommand(ctx):
    await ctx.reply(f"Here is the EC2 Instance Availability Zone: {instanceZone}")

# ID
@hideriBot.command(name="id")
@commands.check(botChannel)
async def idCommand(ctx):
    await ctx.reply(f"Here is the EC2 Instance ID: {instanceID}")

# Type
@hideriBot.command(name="type")
@commands.check(botChannel)
async def typeCommand(ctx):
    await ctx.reply(f"Here is the type of Instance Currently Running: {instanceType}")

# There is a help command already built into discord, so we remove it to add our own custom help command.
hideriBot.remove_command("help")

# Custom help command that gives a list of commands.
@hideriBot.command(name="help")
@commands.check(botChannel)
async def helpCommand(ctx):
    help_text = (
        "# __Here is a list of my commands:__\n"
        "**!hi**: Greets the user\n"
        "**!bye**: Says goodbye\n"
        "**!region**: Returns the Region of the EC2 Server\n"
        "**!ip**: Returns the Public IP of the EC2 Server\n"
        "**!zone**: Returns the Availability Zone of the EC2 Server\n"
        "**!id**: Returns the EC2 Instance ID\n"
        "**!type**: Returns the type of the Current Running Instance"
    )
    await ctx.reply(help_text)

# Error handling for any channel we didn't specify above
@hiCommand.error
@byeCommand.error
@regionCommand.error
@ipCommand.error
@zoneCommand.error
@idCommand.error
@typeCommand.error
@helpCommand.error

# If the command is used in the wrong channel, then send the user a message letting them know they are in the wrong channel.
async def command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.reply("This command can only be used in the #bot channel or in direct messages.")
    else:
        # If the command doesn't exist, print the error message.
        raise error

# Run the bot
hideriBot.run(token)
