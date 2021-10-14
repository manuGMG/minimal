import aiohttp
from discord.ext import commands

# Quick cog example
# github.com/manuGMG/minimal

class Hello(commands.Cog, name='Hello'):
    @commands.command(name='hello', description='Sends hello world')
    async def hello(self, ctx):
        await ctx.send('Hello world :wave:')

def setup(bot):
    bot.add_cog(Hello())