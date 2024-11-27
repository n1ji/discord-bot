#Import class libraries
import os
from dotenv import load_dotenv
import discord
from ec2_metadata import ec2_metadata

# Load the .env file
load_dotenv('env.env')

#Get the token from the environment variable
token = os.getenv('TOKEN')

# Initialize the bot
client = discord.Client()

# Following commands make sure the bot has the proper permissions
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

client = discord.Bot(intents=intents)

instanceID = None
instanceRegion = None
instanceIP = None
instanceZone = None
instanceType = None

try:
    instanceID = ec2_metadata.instance_id
    instanceRegion = ec2_metadata.region
    instanceIP = ec2_metadata.public_ipv4
    instanceZone = ec2_metadata.availability_zone
    instanceType = ec2_metadata.instance_type

    print("EC2 Metadata is Available!")
except Exception as e:
    # Print to the terminal if EC2 is not running and use mock data instead.
    print(f"EC2 metadata is unavailable.\n")
    instanceID = "local-instance-id"
    instanceRegion = "ca-central-202"
    instanceIP = "52.142.124.215" #DDG Supremacy
    instanceZone = "us-neast-7c"
    instanceType = "Python Instance"

# Command that runs once when the bot starts
@client.event
async def on_ready():
    print(f"Logged into bot: {client.user}")
    await client.change_presence(status=discord.Status.online, activity=discord.CustomActivity('Type help for a list of commands.'))

@client.event
async def on_message(message):
    # Ignore messages from the bot
    if message.author == client.user:
        return

    username = str(message.author)
    dispName = str(message.author.display_name)
    userMessage = str(message.content)

    # Check if the message is in the "bot" channel or a direct message
    if isinstance(message.channel, discord.DMChannel) or (isinstance(message.channel, discord.TextChannel) and message.channel.name == "bot"):
        print(f'Message in {message.channel} from {username}: {message.content}')

        # User commands
        if userMessage.lower() in ["hi", "hello", "hola", "こんにちは"]:
            await message.reply(f'Hello {dispName}!')
        elif userMessage.lower() == "bye":
            await message.reply(f'Bye {dispName}!')
        elif userMessage.lower() == "region":
            await message.reply(f'Here is the EC2 Instance Region: {instanceRegion}')
        elif userMessage.lower() == "ip":
            await message.reply(f'Here is the public EC2 Instance IP: {instanceIP}')
        elif userMessage.lower() == "zone":
            await message.reply(f'Here is the EC2 Instance Availability Zone: {instanceZone}')
        elif userMessage.lower() == "id":
            await message.reply(f'Here is the EC2 Instance ID: {instanceID}')
        elif userMessage.lower() == "type":
            await message.reply(f'Here is the type of Instance Currently Running: {instanceType}')
        elif userMessage.lower() == "help":
            await message.reply(
                "# __Here is a list of my commands:__\n"
                "**region**: Returns the Region of the EC2 Server\n"
                "**ip**: Returns the Public IP of the EC2 Server\n"
                "**zone**: Returns the Availability Zone of the EC2 Server\n"
                "**id**: Returns the EC2 Instance ID\n"
                "**type**: Returns the type of the Current Running Instance"
            )
        else:
            await message.reply("I didn't understand that command. Type **help** for a list of my commands.")
    else:
        print(f"Ignored message in {message.channel} from {username}: {message.content}")

# Run the bot
client.run(token)