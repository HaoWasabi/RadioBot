import logging
from nextcord.ext import commands
from nextcord import DMChannel, Color
from gui.embed_custom import EmbedCustom
from gui.error_embed import ErrorEmbed
from gui.ctrl_buttons import CtrlButtons
from utils.commands_cog import CommandsCog

logger = logging.getLogger( "AdminBotCommands")

class CtrlCommands(CommandsCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.color = int("0xBDB76B", 16)    
        
    @commands.command(name="shutdown")
    @commands.is_owner()
    async def shutdown(self, ctx):
        server_id =  ctx.guild.id if ctx.guild else ctx.author.id 
        
        try:
            channel = ctx.channel
            embed = EmbedCustom(
                id_server=server_id,
                description="⚠️ The bot is shutting down...",
                color = self.color
            )
            await channel.send(embed=embed)
            await self.bot.close()
            
        except Exception as e:
            await ctx.send(embed=ErrorEmbed(e))
            logger.error(f"'❌ Error: {e}")

    @commands.command(name="ctrl")
    @commands.is_owner()
    async def ctrl_command(self, ctx):
        server_id =  ctx.guild.id if ctx.guild else ctx.author.id 
        
        try:
            channel = ctx.channel
            embed = EmbedCustom(
                id_server=server_id,
                title="Control Panel",
                description="Choose an option to control the bot.",
                color= self.color
            )
            await channel.send(embed=embed, view=CtrlButtons(ctx.author, self.bot))

        except Exception as e:
            await ctx.send(embed=ErrorEmbed(error=e))
            logger.error(f"'❌ Error: {e}")
        
async def setup(bot):
    bot.add_cog(CtrlCommands(bot))