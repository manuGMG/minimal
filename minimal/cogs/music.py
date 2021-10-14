import asyncio
import youtube_dl
from discord import Embed, FFmpegPCMAudio, PCMVolumeTransformer, Color
from discord.ext import commands

class Music(commands.Cog, name='Music'):
    def __init__(self):
        self.q = {} # Queue

    def embed(self, description: str, color: Color = Color.red()): 
        return Embed(title='Music Playback', description=description, color=color)

    @commands.command(name='p', description='Plays a YouTube video/song')
    @commands.guild_only()
    async def play(self, ctx, *args: str):
        if not args:
            return await ctx.send(embed=self.embed(f'{ctx.author.name}, play what?'))
            
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            return await ctx.send(embed=self.embed(f'{ctx.author.name}, join a music channel first.'))

        if ctx.voice_client is None:
            channel = await ctx.author.voice.channel.connect()
        else:
            await ctx.voice_client.move_to(ctx.author.voice.channel)
            channel = ctx.voice_client

        with youtube_dl.YoutubeDL({}) as ydl:
            vid = ydl.extract_info(f'ytsearch:{(" ").join(args)}', download=False)['entries'][0]
        
        if ctx.guild.id in self.q:
            self.q[ctx.guild.id].append({'id': vid['id'], 'title': vid['title']})
            if len(self.q[ctx.guild.id]) > 1: 
                await ctx.send(embed=self.embed(f'{ctx.author.name}, added [{vid["title"]}](https://www.youtube.com/watch?v={vid["id"]})' \
                                                f' to the queue (#{len(self.q[ctx.guild.id])}).', color=Color.blue()))
            while self.q[ctx.guild.id] and self.q[ctx.guild.id][0]['id'] is not vid['id']: 
                await asyncio.sleep(5)
            if not ctx.voice_client: return
        else:
            self.q[ctx.guild.id] = []
            self.q[ctx.guild.id].append({'id': vid['id'], 'title': vid['title']})

        channel.play(FFmpegPCMAudio(vid['formats'][0]['url'], 
                                    options={'options': '-vn', 'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 20'}))
        channel.source = PCMVolumeTransformer(ctx.guild.voice_client.source)
        channel.source.volume = 1
        await ctx.send(embed=self.embed(f'{ctx.author.name}, i\'m now playing [{vid["title"]}](https://www.youtube.com/watch?v={vid["id"]}).', color=Color.blue()))

        while ctx.voice_client and ctx.voice_client.is_playing(): await asyncio.sleep(5)

        if self.q[ctx.guild.id] and self.q[ctx.guild.id][0]['id'] is vid['id']: self.q[ctx.guild.id].pop(0)

    @commands.command(name='s', description='Skips/Stops (playing) current video/song')
    @commands.guild_only()
    async def stop(self, ctx):
        if ctx.voice_client and self.q:
            ctx.guild.voice_client.stop()
            self.q[ctx.guild.id].pop(0)
            if len(self.q[ctx.guild.id]) == 0: await ctx.send(embed=self.embed(f'{ctx.author.name}, ok i shut.'))
        else:
            await ctx.send(embed=self.embed(f'{ctx.author.name}, can\'t stop me now.'))

    @commands.command(name='q', description='Shows current queue')
    @commands.guild_only()
    async def print_queue(self, ctx):
        if ctx.guild.id in self.q and self.q[ctx.guild.id]:
            await ctx.send(embed=self.embed('**Queue:**\n'+ \
                                            '\n'.join([f'**{i+1}**. [{q["title"]}](https://www.youtube.com/watch?v={q["id"]})' \
                                            for i, q in enumerate(self.q[ctx.guild.id])]), color=Color.blue()))
        else:
            await ctx.send(embed=self.embed(f'{ctx.author.name}, there are no songs queued.'))

    @commands.command(name='d', description='Disconnects from current channel')
    @commands.guild_only()
    async def disconnect(self, ctx):
        if ctx.voice_client:
            await ctx.send(embed=self.embed(f'{ctx.author.name}, bye. :wave:'))
            self.q[ctx.guild.id] = []
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.send(embed=self.embed(f'{ctx.author.name}, i\'m in no channel.'))
            
def setup(bot):
    bot.add_cog(Music())