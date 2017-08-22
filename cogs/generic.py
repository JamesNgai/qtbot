import discord
from discord.ext import commands
import random


class Generic:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def todo(self, ctx):
        await ctx.send('[ ] Gambling bot [ ] League Match History')

    # No kicking allowed
    @commands.command()
    async def kick(self, ctx, *args):
        """ Don't use this """
        phrases = ['I would never!', 'That isn\'t very nice!',
                   'Maybe we should talk about our feelings.',
                   'Calm down.', 'Check your privileges.',
                   'Make love, not war.']
        await ctx.send(phrases[random.randint(0, len(phrases) - 1)])

    @commands.command()
    async def say(self, ctx, *, message):
        """ Make qtbot say anything ;) """
        await ctx.message.delete()
        await ctx.send(message)

    # Returns pseudo-random magic 8-ball result
    @commands.command()
    async def ball(self, ctx, *args):
        """ Ask the magic 8ball """
        responses = ['It is certain', 'It is decidedly so', 'Without a doubt',
                     'Yes definitely', 'You may rely on it', 'As I see it, yes',
                     'Most likely', 'Outlook good', 'Yes', 'Signs point to yes',
                     'Reply hazy try again', 'Ask again later', 'Better not tell you now',
                     'Cannot predict now', 'Concentrate and ask again', 'Don\'t count on it',
                     'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful']
        await ctx.send(responses[random.randint(0, len(responses) - 1)])

    # Same!
    @commands.command()
    async def same(self, ctx):
        await ctx.send('\n[✓] same\n[ ] unsame')

    # Unsame!
    @commands.command()
    async def unsame(self, ctx):
        await ctx.send('\n[ ] same\n[✓] unsame')

    # Resame!
    @commands.command()
    async def resame(self, ctx):
        await ctx.send('\n[✓] same\n [✓] re:same\n [ ] unsame')

    @commands.command()
    async def slap(self, ctx, *, target=None):
        if not target:
            return await ctx.send("You can't slap nothing.")

        member = ctx.author.nick
        await ctx.send('{} slaps {} around a bit with a large trout.'.format(member, target))

    @commands.command()
    async def love(self, ctx, *, target=None):
        member = ctx.author.nick

        if not target:
            return await ctx.send('{} loves ... nothing'.format(member))

        await ctx.send("{} gives {} some good ol' fashioned lovin'".format(member, target))


def setup(bot):
    bot.add_cog(Generic(bot))
