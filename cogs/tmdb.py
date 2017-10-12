#!/bin/env python

import discord
import json
from discord.ext import commands
import tmdbsimple as tmdb


# TMDb key
with open('data/apikeys.json') as f:
    tmdb.API_KEY = json.load(f)['tmdb']


class MyTMDb:
    def __init__(self, bot):
        self.bot = bot

    def sync_get_tmdb(query, type_search):
        """ Non async tmdb library function """

        # Initialize the search
        search = tmdb.Search()

        # TMDb response & store
        if type_search == 'tv':
            response = None or search.tv(query=query)['results'][0]
        elif type_search == 'movie':
            response = None or search.movie(query=query)['results'][0]
        else:
            raise NameError('type_search must be "tv" or "movie".')

        return response

    @commands.command(name='show', aliases=['ss', 'tv'])
    async def get_show(self, ctx, *, query):
        """ Get TV show information """

        # Must run_in_executor for blocking libraries
        result = await self.bot.loop.run_in_executor(None, MyTMDb.sync_get_tmdb, query, 'tv')

        # If no result are found
        if not result:
            return await ctx.send("Sorry, couldn't find that one.")

        # Get qtbot rating
        rating = float(result['vote_average'])
        if (rating > 7.0):
            rec = 'This is a qtbot™ recommended show.'
        else:
            rec = 'This is not a qtbot™ recommmended show.'

        # For getting poster
        base_image_uri = 'https://image.tmdb.org/t/p/w185{}'

        # Create embed
        em = discord.Embed(color=discord.Color.greyple())
        em.title = f'{result["name"]} ({result["first_air_date"].split("-")[0]})'
        em.description = result['overview']
        em.set_thumbnail(url=base_image_uri.format(
            result['poster_path']))
        em.add_field(name='Rating', value=str(rating))
        em.set_footer(text=rec)

        await ctx.send(embed=em)

    @commands.command(name='movie', aliases=['mov'])
    async def get_movie(self, ctx, *, query):
        """ Get movie information """

        # Must run_in_executor for blocking libraries
        result = await self.bot.loop.run_in_executor(None, MyTMDb.sync_get_tmdb, query, 'movie')

        if not result:
            return await ctx.send("Sorry, couldn't find that one.")

        rating = float(result['vote_average'])
        if (rating < 7.0):
            rec = 'This is not a qtbot™ recommmended film.'
        else:
            rec = 'This is a qtbot™ recommended film.'

        # For getting poster
        base_image_uri = 'https://image.tmdb.org/t/p/w185{}'

        # Create embed
        em = discord.Embed(color=discord.Color.greyple())
        em.title = f'{result["title"]} ({result["release_date"].split("-")[0]})'
        em.description = result['overview']
        em.set_thumbnail(url=base_image_uri.format(
            result['poster_path']))
        em.add_field(name='Rating', value=str(rating))
        em.set_footer(text=rec)

        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(MyTMDb(bot))
