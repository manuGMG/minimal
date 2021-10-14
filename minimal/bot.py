import json, pathlib
from discord import Game, Embed, Color
from discord.ext import commands

# Load configuration file.
with open(pathlib.Path(__file__).parent / 'config.json') as f:
    config = json.load(f)
    print('Loaded config.json')

# Set token and prefix.
TOKEN  = config['token']
PREFIX = config['prefix']

# Init bot.
bot = commands.Bot(command_prefix=PREFIX, help_command=None, activity=Game(name=f'{PREFIX}help'))

# Load cogs from configuration file.
for c in config['cogs']:
    bot.load_extension(f'cogs.{c}')
    print(f'Loaded cog: {c}')

# Help command.
@bot.command(name='help')
async def help(ctx, cog: str = ''):
    if not cog: # Print categories.
        await ctx.send(embed=Embed(title='Help Categories', 
                                   description=f'Type: `{PREFIX}help [category]`\n\n'+ '\n'.join([f':star: **{cog}**' for cog in bot.cogs]), 
                                   color=Color.blue()))
    elif cog.capitalize() in bot.cogs: # Print cog commands.
        await ctx.send(embed=Embed(title=cog.capitalize(), 
                                   description='\n'.join([f':star: **{PREFIX}{c.name}** - {c.description}.' \
                                                          for c in bot.commands if c.description and c.cog.qualified_name == cog.capitalize()]), 
                                   color=Color.blue()))
    else: # Print error.
        await ctx.send(embed=Embed(title='Help', description='You\'re wasting my time.', color=0xFF5733))

# Bot is ready.
@bot.event
async def on_ready():
    print('Up and running!')

# Run the bot.
bot.run(TOKEN)