import discord
import json
import datetime
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

TOKEN = "OI! ENTER YOUR FOCKING TOKEN HERE"  # Your bot token

with open('config.json') as config_file:
    config = json.load(config_file)
    server_ids_to_scrape = config.get("servers", [])

bot = commands.Bot(command_prefix="!", intents=intents)

banner = r"""
        _ _  _ ____ ___ ____ _  _ ___ _  _ ____ _  _ ____
        | |\ | [__   |  |__| |\ |  |  |\ | |__| |\/| |___
        | | \| ___]  |  |  | | \|  |  | \| |  | |  | |___
"""

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    if not os.path.exists('scraped_messages.json'):
        await scrape_existing_messages()
        print("        =================================================")
        print(f"{banner}")
        print("=====================================================================")
        print("          Time format: Year-Month-Day Hour:Minute:Second")
        print("=====================================================================")
    else:
        print('scraped_messages.json already exists. Skipping historical scraping.')
        print("        =================================================")
        print(f"{banner}")
        print("=====================================================================")
        print("          Time format: Year-Month-Day Hour:Minute:Second")
        print("=====================================================================")

async def scrape_existing_messages():
    for guild in bot.guilds:
        if str(guild.id) in server_ids_to_scrape:
            print(f'Scraping messages in server: {guild.name}')
            for channel in guild.text_channels:
                print(f'  Channel: {channel.name}')
                try:
                    async for message in channel.history(limit=None):
                        save_message(message)
                except Exception as e:
                    print(f'Failed to scrape messages in {channel.name}: {e}')
        else:
            print(f'Skipping server: {guild.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if str(message.guild.id) in server_ids_to_scrape:
        print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {message.author.name} -> {message.content}')
        save_message(message)

def save_message(message):
    data = {
        'server': message.guild.name,
        'channel': message.channel.name,
        'author': message.author.name,
        'content': message.content,
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open('scraped_messages.json', 'a') as f:
        json.dump(data, f)
        f.write('\n')

bot.run(TOKEN)
