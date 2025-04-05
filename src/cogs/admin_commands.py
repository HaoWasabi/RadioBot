import logging
from nextcord.ext import commands
from gui.embed_custom import EmbedCustom
from gui.error_embed import ErrorEmbed
from gui.ctrl_buttons import CtrlButtons
from gui.group_buttons import GroupButtons
from gui.channel_buttons import ChannelButtons
from utils.commands_cog import CommandsCog

logger = logging.getLogger("AdminCommands")

class AdminCommands(CommandsCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.color = int("0xBDB76B", 16)    
        
    @commands.command(name="shutdown")
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shut down the bot"""
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
        """Control the bot"""
        server_id =  ctx.guild.id if ctx.guild else ctx.author.id 
        
        try:
            channel = ctx.channel
            embed = EmbedCustom(
                id_server=server_id,
                title="Control Panel",
                description=f"Choose an option to control the bot.\n- 1: **Show servers**\n- 2: **Change Group**\n- 3: **Change Channel**\n- 4: **Shutdown**",
                color= self.color
            )
            await channel.send(embed=embed, view=CtrlButtons(ctx.author, self.bot))

        except Exception as e:
            await ctx.send(embed=ErrorEmbed(error=e))
            logger.error(f"'❌ Error: {e}")
            
    @commands.command(name="group")
    @commands.is_owner()
    async def group_command(self, ctx):
        """Change radio groups in database"""
        server_id =  ctx.guild.id if ctx.guild else ctx.author.id 
        
        try:
            channel = ctx.channel
            embed = EmbedCustom(
                id_server=server_id,
                title="Group Panel",
                description="Choose an option to change.",
                color= self.color
            )
            await channel.send(embed=embed, view=GroupButtons(ctx.author, self.bot))

        except Exception as e:
            await ctx.send(embed=ErrorEmbed(error=e))
            logger.error(f"'❌ Error: {e}")
            
    @commands.command(name="channel")
    @commands.is_owner()
    async def channel_command(self, ctx):
        """Change radio channels in database"""
        server_id =  ctx.guild.id if ctx.guild else ctx.author.id 
        
        try:
            channel = ctx.channel
            embed = EmbedCustom(
                id_server=server_id,
                title="Channel Panel",
                description="Choose an option to change.",
                color= self.color
            )
            await channel.send(embed=embed, view=ChannelButtons(ctx.author, self.bot))

        except Exception as e:
            await ctx.send(embed=ErrorEmbed(error=e))
            logger.error(f"'❌ Error: {e}")
        
async def setup(bot):
    bot.add_cog(AdminCommands(bot))