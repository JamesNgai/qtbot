#!/bin/env python

import discord
import json
import aiohttp
import aredis
import asyncpg
from datetime import datetime
from discord.ext import commands

# Init bot
des = 'qtbot is a big qt written in python3 and love.'
bot = commands.Bot(command_prefix='.', description=des, pm_help=True)

# Get bot's token
with open('data/apikeys.json') as f:
    discord_bot_token = json.load(f)['discord']

# Create bot aiohttp session
bot.aio_session = aiohttp.ClientSession

# Create bot redis client
bot.redis_client = aredis.StrictRedis(host='localhost', decode_responses=True)

# Create connection to postgresql server using pools
async def create_db_pool():
    with open('data/apikeys.json') as f:
        pg_pw = json.load(f)['postgres']
    bot.pg_con = await asyncpg.create_pool(user='james', password=pg_pw, database='discord_testing')
bot.loop.run_until_complete(create_db_pool())

# Choose default cogs
bot.startup_extensions = (
    'cogs.admin',
    'cogs.generic',
    'cogs.weather',
    'cogs.comics',
    'cogs.dictionary',
    'cogs.osrs',
    'cogs.tmdb',
    'cogs.gif',
    'cogs.calc',
    'cogs.league',
    'cogs.ask',
    'cogs.meme',
    'cogs.error',
    'cogs.eval',
    'cogs.timer',
    'cogs.yt',
    'cogs.news',
    'cogs.wiki',
    'cogs.isup')

# Get current time for uptime
start_time = datetime.now()
start_time_str = start_time.strftime('%B %d %H:%M:%S')

@bot.event
async def on_ready():
    """ Basic information printed via stdout """
    print(f'Client logged in at {start_time_str}')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(aliases=['up'])
async def uptime(ctx):
    """ Get current bot uptime """
    current_time = datetime.now()
    current_time_str = current_time.strftime('%B %d %H:%M:%S')

    await ctx.send(
        f'Initialized: `{start_time_str}`\nCurrent Time: `{current_time_str}`\nUptime: `{str(current_time - start_time).split(".")[0]}`')


if __name__ == '__main__':
    for ext in bot.startup_extensions:
        try:
            bot.load_extension(ext)
        except Exception as e:
            exc = f'{type(e).__name__}: {e}'
            print(u'failed to load extension {ext}\n{exc}')

    bot.run(discord_bot_token)
