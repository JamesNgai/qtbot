#!/bin/env python

import discord
from discord.ext import commands


class Admin:
    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, ctx):
        await ctx.send('Welcome to the server! For a complete list of commands, type `.help`.')

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension_name: str):
        """ Loads an extension """
        try:
            self.bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            return await ctx.send(f'```py\n{type(e).__name__}: {str(e)}\n```')
        await ctx.send('Cog `{}` loaded successfully.'.format(extension_name))


    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension_name: str):
        """ Unloads an extension. """
        self.bot.unload_extension(extension_name)
        await ctx.send('Cog `{}` has been unloaded.'.format(extension_name))


    @commands.command(name='reload', aliases='r')
    @commands.is_owner()
    async def _reload(self, ctx, extension_name: str):
        """ Reloads an extension """
        try:
            self.bot.unload_extension(extension_name)
            self.bot.load_extension(extension_name)
        except Exception as e:
            return await ctx.send(f'```py\n{type(e).__name__}: {str(e)}\n```')
        await ctx.send(f'Cog `{extension_name}` has been reloaded.')

    @commands.command(name='reload_all', aliases=['ra'])
    @commands.is_owner()
    async def reload_all(self, ctx):
        """ Reloads all extensions """

        # Gets cog list and pops admin cog (can't reload without it)
        ext_list = []
        for extension in self.bot.startup_extensions:
            ext_list.append(extension)
        ext_list.pop(ext_list.index('cogs.admin'))

        # Reloads all cogs
        for extension in ext_list:
            try:
                self.bot.unload_extension(extension)
                self.bot.load_extension(extension)
            except Exception as e:
                return await ctx.send(f'```py\n{type(e).__name__}: {str(e)}\n```')

        await ctx.send('All cogs have been reloaded.')


def setup(bot):
    bot.add_cog(Admin(bot))
