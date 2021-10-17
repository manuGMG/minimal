from discord.ext import commands

# Quick cog example
# github.com/manuGMG/minimal

class Hello(commands.Cog, name='Hello'): #-> name must be in capitals.
    
    # Need to use a JSON file?
    # def __init__(self, bot):
    #   self.config_path = bot.config_path

    @commands.command(name='hello', description='Sends hello world')
    async def hello(self, ctx):
        await ctx.send(f'Hello {ctx.author.name} :wave:')

def setup(bot):
    bot.add_cog(Hello())

    # Exclude from help command?
    # bot.hidden.append('Hello')