import logging
from nextcord.ext import commands
from nextcord import DMChannel, Color
from gui.embed_custom import EmbedCustom
from gui.error_embed import ErrorEmbed
from gui.update_buttons import UpdateButtons
from utils.commands_cog import CommandsCog

logger = logging.getLogger( "UpdateCommands")

class UpdateCommands(CommandsCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.color = int("0xBDB76B", 16)    
        
    @commands.command(name="update")
    @commands.is_owner()
    async def update_command(self, ctx):
        server_id =  ctx.guild.id if ctx.guild else ctx.author.id 
        
        try:
            channel = ctx.channel
            embed = EmbedCustom(
                id_server=server_id,
                title="Update Panel",
                description="Choose an option to update.",
                color= self.color
            )
            await channel.send(embed=embed, view=UpdateButtons(ctx.author, self.bot))

        except Exception as e:
            await ctx.send(embed=ErrorEmbed(error=e))
            logger.error(f"Error: {e}")
    
async def setup(bot):
    bot.add_cog(UpdateCommands(bot))