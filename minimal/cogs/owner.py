import json
from discord.ext import commands
from discord import Embed, Color

class Owner(commands.Cog, name='Owner'):
    def __init__(self, bot):
        self.bot = bot

    def embed(self, description: str, color: Color = Color.red()): 
        return Embed(title='Configuration', description=description, color=color)

    @commands.command(name='cog', aliases=['cogs'])
    @commands.is_owner()
    async def manage_cogs(self, ctx, command: str = '', cog: str = ''):
        if not command:
            await ctx.send(embed=self.embed('Missing command.'))
            return
        
        with open(self.bot.config_path / 'config.json') as f:
            config = json.load(f)
        
        if not cog:
            if command == 'list':
                await ctx.send(embed=self.embed(f'**Loaded cogs:**\n' +
                                                '\n'.join([f':star: {cog}' for cog in self.bot.cogs]),
                                                color=Color.teal()))
        elif command == 'load':
            try:
                self.bot.load_extension(f'cogs.{cog}')
                config['cogs'].append(cog)
                await ctx.send(embed=self.embed(f'Loaded `{cog}`.', color=Color.teal()))
                print(f'Loaded cog: {cog}')
            except Exception as e:
                await ctx.send(embed=self.embed(f'**Error**:\n```{e}```'))
                return
        elif command == 'unload':
            try:
                self.bot.unload_extension(f'cogs.{cog}')
                config['cogs'].remove(cog)
                await ctx.send(embed=self.embed(f'Unloaded `{cog}`.', color=Color.teal()))
                print(f'Unloaded cog: {cog}')
            except Exception as e:
                await ctx.send(embed=self.embed(f'**Error**:\n```{e}```'))
                return
        elif command == 'reload':
            try:
                self.bot.reload_extension(f'cogs.{cog}')
                await ctx.send(embed=self.embed(f'Reloaded `{cog}`.', color=Color.teal()))
                print(f'Reloaded cog: {cog}')
                return
            except Exception as e:
                await ctx.send(embed=self.embed(f'**Error**:\n```{e}```'))
                return

        with open(self.bot.config_path / 'config.json', 'w') as f:
            json.dump(config, f, indent=4)

def setup(bot):
    bot.add_cog(Owner(bot))
    bot.hidden.append('Owner')