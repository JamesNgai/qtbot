import json
import traceback
from datetime import datetime
from pathlib import Path

import aiohttp
import aredis
import asyncpg
from discord.ext import commands

from utils.custom_context import CustomContext


class QTBot(commands.Bot):
    def __init__(self, config_file, *args, **kwargs):
        self.config_file = config_file
        self.description = 'qtbot is a big qt written in python3 and love.'
        self.do_not_load = ('league')

        with open(self.config_file) as f:
            self.api_keys = json.load(f)

        self.token = self.api_keys['discord']

        super().__init__(command_prefix=self.get_prefix, description=self.description,
                         pm_help=None, case_insensitive=True, *args, **kwargs)

        self.aio_session = aiohttp.ClientSession(loop=self.loop)
        # self.rune_client = lolrune.AioRuneClient()
        self.redis_client = aredis.StrictRedis(host='localhost', decode_responses=True)
        self.startup_extensions = [x.stem for x in Path('cogs').glob('*.py')]
        self.loop.run_until_complete(self.create_db_pool())
        self.loop.run_until_complete(self.load_all_prefixes())

    def run(self):
        super().run(self.token)

    async def load_all_prefixes(self):
        pres = await self.pg_con.fetch('SELECT * from custom_prefix')
        # Load custom prefixes into a dict
        self.pre_dict = {r['guild_id']: r['prefix'] for r in pres}

    async def get_prefix(self, message):
        try:
            return ('qt.', self.pre_dict[message.guild.id])
        except (KeyError, AttributeError):
            return 'qt.'

    async def create_db_pool(self):
        with open(self.config_file) as f:
            self.pg_pw = json.load(f)['postgres']
        self.pg_con = await asyncpg.create_pool(user='james', password=self.pg_pw, database='discord_testing')

    async def on_message(self, message):
        ctx = await self.get_context(message, cls=CustomContext)
        await self.invoke(ctx)

    async def on_ready(self):
        if not hasattr(self, 'start_time'):
            self.start_time = datetime.now()
            self.start_time_str = self.start_time.strftime('%B %d %H:%M:%S')

        for extension in self.startup_extensions:
            if extension not in self.do_not_load:
                try:
                    self.load_extension(f'cogs.{extension}')
                except:
                    print(f'Failed Extension: {extension}')
                    traceback.print_exc()
                else:
                    print(f'Loaded Extension: {extension}')

        print(f'Client logged in at {self.start_time_str}')
        print(self.user.name)
        print(self.user.id)
        print('----------')
