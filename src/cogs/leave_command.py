
import logging
from nextcord.ext import commands
from gui.embed_custom import EmbedCustom
from gui.error_embed import ErrorEmbed

logger = logging.getLogger("LeaveCommand")

class LeaveCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="leave")
    async def command_leave(self, ctx):
        """Command to make the bot leave the voice channel of Discord"""
        server_id =  ctx.guild.id if ctx.guild else ctx.author.id 
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            embed = EmbedCustom(
                id_server=str(server_id),
                description="👋 Bot has left the voice channel!"
            )

        else:
            embed = ErrorEmbed(error="Bot has not been in the voice channel!")
        
        await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(LeaveCommand(bot))
