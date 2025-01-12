import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
BOT_ONLY_CHANNEL_ID = os.getenv("BOT_ONLY_CHANNEL_ID")
DEBUG_CHANNEL_ID = os.getenv("BOT_DEBUG_CHANNEL_ID")

# Ensure required variables are set
if not TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN is not set. Check your environment variables.")
if not BOT_ONLY_CHANNEL_ID:
    raise ValueError("BOT_ONLY_CHANNEL_ID is not set. Check your environment variables.")

# Set intents
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.guilds = True
intents.message_content = True

# Create the bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

# This will store the bot-only channel once the bot is ready
bot_only_channel = None
debug_channel = None

# Role name for students
STUDENT_ROLE_NAME = "Student"

@bot.event
async def on_ready():
    global bot_only_channel
    print(f'Bot is ready. Logged in as {bot.user} as of {datetime.now()}')

    # Get the bot-only channel
    bot_only_channel = bot.get_channel(int(BOT_ONLY_CHANNEL_ID))
    debug_channel = bot.get_channel(int(DEBUG_CHANNEL_ID))

    if bot_only_channel:
        await bot_only_channel.send(f'Bot is ready. Logged in as {bot.user} as of {datetime.now()}')
    else:
        print("Bot-only channel not found or cached.")


    guild = bot.guilds[0]  # Assuming the bot is in only one guild
    for member in guild.members:
        # Check if the member's nickname is None or is the same as their username
        if member.nick is None or member.nick == member.name and member.nick != "CSCE221-Bot" and member.nick!= "TeXit":
            try:
                # Send DM to the member reminding them to change their nickname
                await member.send(f"Hello {member.name}, please change your server nickname to your actual name.")
            except:
                # If the bot can't DM the member, log the failure
                if bot_only_channel:
                    await debug_channel.send(f"Could not DM {member.name} to remind them about updating their nickname.")

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name=STUDENT_ROLE_NAME)
    if role:
        await member.add_roles(role)
        if bot_only_channel:
            await bot_only_channel.send(f"Assigned {STUDENT_ROLE_NAME} role to {member.name}.")
    else:
        if debug_channel:
            await debug_channel.send(f"Role '{STUDENT_ROLE_NAME}' not found in the server.")

    try:
        await member.send("Welcome to the CSCE221-Kumar server! Please change your server nickname to your actual name.")
    except:
        if debug_channel:
            await debug_channel.send(f"Could not DM {member.name}.")

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return

#     if message.channel.name == "general" and not message.author.guild_permissions.administrator:
#         member = message.author
#         if member.nick is None or member.nick == member.name:
#             await message.channel.send(f"{member.mention}, please update your server nickname to your actual name.")

#     await bot.process_commands(message)

# Run the bot
bot.run(TOKEN)
