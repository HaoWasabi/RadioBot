import os
import logging
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from dto.color_dto import ColorDTO
from dto.server_dto import ServerDTO
from bll.group_bll import GroupBLL
from bll.channel_bll import ChannelBLL
from bll.server_bll import ServerBLL
from gui.embed_custom import EmbedCustom
from gui.error_embed import ErrorEmbed
import imageio_ffmpeg as ffmpeg

logger = logging.getLogger("UserCommands")

# Lấy đường dẫn của FFmpeg do imageio cung cấp
FFMPEG_PATH = ffmpeg.get_ffmpeg_exe()
os.environ["FFMPEG_EXECUTABLE"] = FFMPEG_PATH

class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_bll = ChannelBLL()
        self.group_bll = GroupBLL()

    @commands.command(name="join")
    async def command_join(self, ctx):
        """Invite the bot to a voice channel of Discord"""
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
            
    @commands.command(name="leave")
    async def command_leave(self, ctx):
        """Make the bot leave the voice channel of Discord"""
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
        
    @commands.command(name="play")
    async def play(self, ctx, channel_id: int=1):
        """Play radio channel by id"""
        channel_dto = ChannelBLL().select_by_id(channel_id)
        server_id =  ctx.guild.id if ctx.guild else ctx.author.id 
        vc = ctx.voice_client
        
        if channel_dto: 
            link = channel_dto.get_link()
            if vc:
                vc.stop()  # Dừng âm thanh hiện tại (nếu có)
                source = nextcord.FFmpegPCMAudio(executable=FFMPEG_PATH, source=link)
                vc.play(source)
                embed = EmbedCustom(
                    id_server=str(server_id),
                    description=f"📻 Started playing **{channel_dto.get_name()}**"
                )
            
            else:
                embed = ErrorEmbed(error="Bot has not been not in the voice channel!")
        
        else:
            embed = ErrorEmbed(error="Channel not found!")
            
        await ctx.send(embed=embed)
        
    @commands.command(name="stop")
    async def stop(self, ctx):
        """Stop the currently playing radio"""
        vc = ctx.voice_client
        server_id = ctx.guild.id if ctx.guild else ctx.author.id

        if vc and vc.is_playing():
            vc.stop()
            embed = EmbedCustom(
                id_server=str(server_id),
                description="⏹️ Stopped the radio playback."
            )
        else:
            embed = ErrorEmbed(error="There's no radio playing to stop.")

        await ctx.send(embed=embed)

        
    @commands.command(name="show")
    async def command_show_channels(self, ctx):
        """Show list of radio channels categorized by groups"""
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

    @commands.command(name='setcolor')
    async def command_set_color(self, ctx, color: str):
        '''Set the embed color'''
        if not color:
            await ctx.send('This command must have color.')
            return

        await self._set_color(ctx, color, ctx.guild, ctx.author)

    # @nextcord.slash_command(name="setcolor", description="Set the embed color")
    # async def slash_set_color(self, interaction: Interaction, 
    #                           color: str = SlashOption(
    #                               name="color",
    #                               description="Choose a color for the embeds",
    #                               choices={"Red": "red", "Orange": "orange", "Yellow": "yellow", "Green": "green", 
    #                                        "Blue": "blue", "Purple": "purple", "Black": "black", "Gray": "gray"}
    #                           )):
    #     await interaction.response.defer()

        # await self._set_color(interaction.followup, color, interaction.guild, interaction.user)

    async def _set_color(self, ctx, color: str, guild, user):
        server_id = guild.id if guild else user.id 
        server_name = guild.name if guild else user.name 
        
        try:
            server_bll = ServerBLL()
            color_dto = ColorDTO(color)
            server_dto = ServerDTO(str(server_id), server_name, color_dto.get_hex_color())

            if not server_bll.select_by_id(server_dto.get_id()):
                server_bll.insert(server_dto)
            else:
                server_bll.update(server_dto)

            hex_color = color_dto.get_hex_color()
            embed = EmbedCustom(
                id_server=server_dto.get_id(),
                description=f"✅ Set color **{color_dto.get_name_color()}** successfully.",
                color=int(hex_color, 16)
            )
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(embed = ErrorEmbed(error=e))
            logger.error(f"Error: {e}")
        
def setup(bot):
    bot.add_cog(UserCommands(bot))

