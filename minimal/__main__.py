import sys, json, pathlib
from discord import Game, Embed, Color
from discord.ext import commands

def main(config_path: str):
    try:
        # Load configuration file.
        with open(config_path / 'config.json') as f:
            config = json.load(f)
        print('Loaded config.json')
    except:
        # Create configuration file.
        with open(config_path / 'config.json', 'w') as f:
            json.dump({'token': 'YOUR_TOKEN_HERE', 'prefixes': ['min '], 'cogs': ['owner']}, f, indent=4)
        print('Created "config.json" file. Edit it with your token and rerun the bot.')
        return

    # Set token and prefix.
    TOKEN  = config['token']
    PREFIX = config['prefixes']

    # Init bot.
    bot = commands.Bot(command_prefix=PREFIX, help_command=None, activity=Game(name=f'{PREFIX[0]}help'))
    bot.hidden = [] # Hidden cogs
    bot.config_path = config_path # Pass config path in case the config file needs to be changed by a cog. (e.g. owner cog)

    # Load cogs from configuration file.
    for c in config['cogs']:
        try:
            bot.load_extension(f'cogs.{c}')
            print(f'Loaded cog: {c}')
        except commands.errors.ExtensionNotFound as e:
            print(f'[NOT FOUND] Couldn\'t load cog: {c}')

    # Help command.
    @bot.command(name='help')
    async def help(ctx, cog: str = ''):
        if not cog: # Print categories.
            await ctx.send(embed=Embed(title='Help Categories', 
                                    description=f'Type: `{PREFIX[0]}help [category]`\n\n'+ '\n'.join([f':star: **{cog}**' \
                                                                                                    for cog in bot.cogs if not cog in bot.hidden]),
                                    color=Color.blue()))
        elif cog.capitalize() in bot.cogs and not cog.capitalize() in bot.hidden: # Print cog commands.
            await ctx.send(embed=Embed(title=cog.capitalize(), 
                                    description='\n'.join([f':star: **{PREFIX[0]}{c.name}** - {c.description}.' \
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

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).parent)