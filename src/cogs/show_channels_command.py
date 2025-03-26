import logging
from nextcord.ext import commands
from bll.channel_bll import ChannelBLL
from bll.group_bll import GroupBLL
from gui.embed_custom import EmbedCustom
from gui.error_embed import ErrorEmbed

logger = logging.getLogger("ShowChannelsCommand")

class ShowChannelsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_bll = ChannelBLL()
        self.group_bll = GroupBLL()

    @commands.command(name="show")
    async def command_show_channels(self, ctx):
        """Command to show list of radio channels categorized by groups"""
        try:
            server_id = ctx.guild.id if ctx.guild else ctx.author.id
            num = 0
            
            groups = self.group_bll.select_all()
            channels = self.channel_bll.select_all()

            if not channels:
                await ctx.send(embed=ErrorEmbed(error= "No radio channels available!"))
                return
            
            message = "📻 **List of Radio Channels by Groups:**\n"
            group_dict = {group.get_id(): group.get_name() for group in groups}
            
            grouped_channels = {}
            for channel in channels:
                group_id = channel.get_group_id()
                if group_id not in grouped_channels:
                    grouped_channels[group_id] = []
                grouped_channels[group_id].append(channel)
            
            for group_id, channel_list in grouped_channels.items():
                group_name = group_dict.get(group_id, "Unknown Group")
                message += f"\n**{group_name}**\n"
                for channel in channel_list:
                    message += f"- {channel.get_id()}: **{channel.get_name()}**\n"
                    num += 1
            
            embed = EmbedCustom(
                id_server=str(server_id),
                description=f"{message}\nTotal: **{num}** channels"
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(embed=ErrorEmbed(error=e))
            logger.error(f"Error: {e}")


def setup(bot):
    bot.add_cog(ShowChannelsCommand(bot))
