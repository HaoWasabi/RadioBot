import logging
from nextcord.ext import commands
from gui.embed_custom import EmbedCustom
from gui.error_embed import ErrorEmbed

logger = logging.getLogger("JoinCommand")

class JoinCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="join")
    async def command_join(self, ctx):
        """Command to invite the bot to a voice channel of Discord"""
        server_id =  ctx.guild.id if ctx.guild else ctx.author.id 
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            vc = await channel.connect()
            embed = EmbedCustom(
                id_server=str(server_id),
                description="🎧 Bot has joined the voice channel!"
            )
            
        else:
            embed = ErrorEmbed(error="You must join the channel first!")
            
        await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(JoinCommand(bot))

