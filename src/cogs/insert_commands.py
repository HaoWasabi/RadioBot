import logging
from nextcord.ext import commands
from nextcord import DMChannel, Color
from gui.embed_custom import EmbedCustom
from gui.error_embed import ErrorEmbed
from gui.insert_buttons import InsertButtons
from utils.commands_cog import CommandsCog

logger = logging.getLogger( "InsertCommands")

class InsertCommands(CommandsCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.color = int("0xBDB76B", 16)    
        
    @commands.command(name="insert")
    @commands.is_owner()
    async def insert_command(self, ctx):
        server_id =  ctx.guild.id if ctx.guild else ctx.author.id 
        
        try:
            channel = ctx.channel
            embed = EmbedCustom(
                id_server=server_id,
                title="Insert Panel",
                description="Choose an option to insert.",
                color= self.color
            )
            await channel.send(embed=embed, view=InsertButtons(ctx.author, self.bot))

        except Exception as e:
            await ctx.send(embed=ErrorEmbed(error=e))
            logger.error(f"'❌ Error: {e}")
    
async def setup(bot):
    bot.add_cog(InsertCommands(bot))