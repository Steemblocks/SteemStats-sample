import discord
import aiohttp
import asyncio
import requests
import re
import json
import logging
import matplotlib.pyplot as plt
import io
from datetime import datetime, timedelta
from discord.ext import commands


# Set up logging to suppress PyNaCl warning
logging.basicConfig(level=logging.INFO)
# Get the discord logger
discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.ERROR)  # Suppress all warnings related to PyNaCl

# Initialize the bot
TOKEN = 'my bot token'

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

# Set up logging
logging.basicConfig(level=logging.INFO)

# Replace `discord.Client` with `commands.Bot`
bot = commands.Bot(command_prefix="!", intents=intents)

# Log all command usage
@bot.event
async def on_command(ctx):
    logging.info(f"Command '{ctx.command}' used by {ctx.author} in {ctx.guild}")

# Define client before using it
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

# Define intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

STEEM = 'STEEM'




# Fetaure 7
# Function to fetch vesting stats from the API
async def fetch_vesting_stats(session):
    try:
        url = 'https://sds0.steemworld.org/accounts_api/getVestingStats'
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
            return data['result']['defs']  # Extracting data under the 'defs' key
    except aiohttp.ClientError as e:
        print(f"Error fetching vesting stats: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}

# Function to fetch vests to SP conversion rate
async def fetch_vests_to_sp_conversion_rate(session):
    try:
        url = 'https://api.justyy.workers.dev/api/steemit/vests/?cached'
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
            return data['vests_to_sp']  # Conversion rate from vests to SP
    except aiohttp.ClientError as e:
        print(f"Error fetching conversion rate: {e}")
        return 0
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 0

# Slash command to get vesting statistics with formatted embed
@tree.command(name="vestingstats", description="Get detailed statistics of vesting accounts with SP conversion")
async def vesting_stats_command(interaction: discord.Interaction):
    print("Slash command /vestingstats received.")
    await interaction.response.defer()

    async with aiohttp.ClientSession() as session:
        vesting_data = await fetch_vesting_stats(session)
        conversion_rate = await fetch_vests_to_sp_conversion_rate(session)

    # Mapping categories to emojis, descriptions, and count
    categories = {
        'redfish': ('🐟 Redfish', '0 MV - 1 MV'),
        'minnow': ('🐠 Minnow', '1 MV - 10 MV'),
        'dolphin': ('🐬 Dolphin', '10 MV - 100 MV'),
        'orca': ('🐋 Orca', '100 MV - 1,000 MV'),
        'whale': ('🐳 Whale', '1,000 MV+')  # Handled separately
    }
    
    embed = discord.Embed(title="Steem Vesting Stats", color=0x21D19F) # teal or greenish-blue
    for category, (emoji, mv_range) in categories.items():
        count = vesting_data[category]['count']
        if category == 'whale':
            min_sp = vesting_data[category]['from'] * conversion_rate
            sp_range = f"({min_sp:,.2f} SP +)"
        else:
            min_vest, max_vest = vesting_data[category]['from'], vesting_data[category]['to']
            min_sp = min_vest * conversion_rate
            max_sp = max_vest * conversion_rate
            sp_range = f"({min_sp:,.2f} SP - {max_sp:,.2f} SP)"
        embed.add_field(name=f"{emoji} {mv_range} {sp_range}", value=f"Count: {count:,}", inline=False)

    # Adding footer to the embed
    embed.set_footer(text="API provided by @steemchiller and @justyy | developed by @dhaka.witness")

    await interaction.followup.send(embed=embed)
    print("Vesting stats SP embedded message sent.")


# Event when the bot is ready
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await tree.sync()
    print("Slash commands synced with Discord.")

# Main function to start the bot
asyncio.run(client.start(TOKEN))

# Main function to start the bot
async def main():
    try:
        await client.start(TOKEN)
    except Exception as e:
        logging.error(f"Error starting the bot: {e}")

if __name__ == "__main__":
    asyncio.run(main())
