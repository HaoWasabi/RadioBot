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
from gui.play_buttons import PlayButtons
import imageio_ffmpeg as ffmpeg

logger = logging.getLogger("UserCommands")

# FFmpeg setup
FFMPEG_PATH = ffmpeg.get_ffmpeg_exe()
os.environ["FFMPEG_EXECUTABLE"] = FFMPEG_PATH

class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_bll = ChannelBLL()
        self.group_bll = GroupBLL()

    async def _get_server_id(self, ctx_or_interaction):
        """Helper to get server ID from context or interaction."""
        return (ctx_or_interaction.guild.id if ctx_or_interaction.guild 
                else ctx_or_interaction.user.id)

    async def _join_voice(self, ctx_or_interaction, is_interaction=False):
        """Helper for joining voice channel."""
        server_id = await self._get_server_id(ctx_or_interaction)
        user = ctx_or_interaction.user if is_interaction else ctx_or_interaction.author
        voice_client = (ctx_or_interaction.guild.voice_client if is_interaction 
                        else ctx_or_interaction.voice_client)

        if not user.voice:
            return ErrorEmbed(error="You must join a voice channel first!")

        target_channel = user.voice.channel

        if voice_client:
            if voice_client.channel == target_channel:
                return EmbedCustom(
                    id_server=str(server_id),
                    description=f"🎧 Bot is already in **{target_channel.name}**!"
                )
            else:
                # Move the bot to the user's channel
                await voice_client.move_to(target_channel)
                return EmbedCustom(
                    id_server=str(server_id),
                    description=f"🎧 Bot has moved to **{target_channel.name}**!"
                )
        else:
            vc = await target_channel.connect()
            return EmbedCustom(
                id_server=str(server_id),
                description="🎧 Bot has joined the voice channel!"
            )

    async def _leave_voice(self, ctx_or_interaction, is_interaction=False):
        """Helper for leaving voice channel."""
        server_id = await self._get_server_id(ctx_or_interaction)
        voice_client = (ctx_or_interaction.guild.voice_client if is_interaction 
                        else ctx_or_interaction.voice_client)
        if voice_client:
            await voice_client.disconnect()
            embed = EmbedCustom(
                id_server=str(server_id),
                description="👋 Bot has left the voice channel!"
            )
        else:
            embed = ErrorEmbed(error="Bot is not in a voice channel!")
        return embed

    async def _play_channel(self, ctx_or_interaction, channel_id: int, is_interaction=False):
        """Helper for playing radio channel."""
        server_id = await self._get_server_id(ctx_or_interaction)
        voice_client = (ctx_or_interaction.guild.voice_client if is_interaction 
                        else ctx_or_interaction.voice_client)
        user = ctx_or_interaction.user if is_interaction else ctx_or_interaction.author

        channel_dto = self.channel_bll.select_by_id(channel_id)
        if not channel_dto:
            return ErrorEmbed(error="Channel not found!")

        if not voice_client:
            return ErrorEmbed(error="Bot is not in a voice channel!")

        voice_client.stop()  # Stop current audio if playing
        source = nextcord.FFmpegPCMAudio(executable=FFMPEG_PATH, source=channel_dto.get_link())
        voice_client.play(source)

        embed = EmbedCustom(
            id_server=str(server_id),
            description=f"📻 Started playing **{channel_dto.get_name()}**"
        )
        view = PlayButtons(user=user, bot=self.bot, current_channel_id=channel_id)
        return embed, view

    async def _stop_playback(self, ctx_or_interaction, is_interaction=False):
        """Helper for stopping radio playback."""
        server_id = await self._get_server_id(ctx_or_interaction)
        voice_client = (ctx_or_interaction.guild.voice_client if is_interaction 
                        else ctx_or_interaction.voice_client)
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            embed = EmbedCustom(
                id_server=str(server_id),
                description="⏹️ Stopped the radio playback."
            )
        else:
            embed = ErrorEmbed(error="No radio is currently playing!")
        return embed

    async def _show_channels(self, ctx_or_interaction, is_interaction=False):
        """Helper for showing radio channels."""
        try:
            server_id = await self._get_server_id(ctx_or_interaction)
            groups = self.group_bll.select_all()
            channels = self.channel_bll.select_all()

            if not channels:
                return ErrorEmbed(error="No radio channels available!")

            group_dict = {group.get_id(): group.get_name() for group in groups}
            grouped_channels = {}
            for channel in channels:
                group_id = channel.get_group_id()
                grouped_channels.setdefault(group_id, []).append(channel)

            message = "📻 **List of Radio Channels by Groups:**\n"
            for group_id, channel_list in grouped_channels.items():
                group_name = group_dict.get(group_id, "Unknown Group")
                message += f"\n**{group_name}**\n"
                for channel in channel_list:
                    message += f"- {channel.get_id()}: **{channel.get_name()}**\n"

            embed = EmbedCustom(
                id_server=str(server_id),
                description=f"{message}\nTotal: **{len(channels)}** channels"
            )
            return embed
        except Exception as e:
            logger.error(f"Error: {e}")
            return ErrorEmbed(error=str(e))

    async def _set_color(self, ctx_or_interaction, color: str, is_interaction=False):
        """Helper for setting embed color."""
        server_id = await self._get_server_id(ctx_or_interaction)
        guild = ctx_or_interaction.guild if is_interaction else ctx_or_interaction.guild
        user = ctx_or_interaction.user if is_interaction else ctx_or_interaction.author
        server_name = guild.name if guild else user.name

        try:
            server_bll = ServerBLL()
            color_dto = ColorDTO(color)
            server_dto = ServerDTO(str(server_id), server_name, color_dto.get_hex_color())

            if not server_bll.select_by_id(server_dto.get_id()):
                server_bll.insert(server_dto)
            else:
                server_bll.update(server_dto)

            embed = EmbedCustom(
                id_server=str(server_id),
                description=f"✅ Set color **{color_dto.get_name_color()}** successfully.",
                color=int(color_dto.get_hex_color(), 16)
            )
            return embed
        except Exception as e:
            logger.error(f"Error: {e}")
            return ErrorEmbed(error=str(e))

    # Existing Commands
    @commands.command(name="join")
    async def command_join(self, ctx):
        """Invite the bot to a voice channel."""
        embed = await self._join_voice(ctx)
        await ctx.send(embed=embed)

    @commands.command(name="leave")
    async def command_leave(self, ctx):
        """Make the bot leave the voice channel."""
        embed = await self._leave_voice(ctx)
        await ctx.send(embed=embed)

    @commands.command(name="play")
    async def play(self, ctx, channel_id: int = 1):
        """Play radio channel by ID."""
        result = await self._play_channel(ctx, channel_id)
        if isinstance(result, tuple):
            embed, view = result
            await ctx.send(embed=embed, view=view)
        else:
            await ctx.send(embed=result)

    @commands.command(name="stop")
    async def stop(self, ctx):
        """Stop the currently playing radio."""
        embed = await self._stop_playback(ctx)
        await ctx.send(embed=embed)

    @commands.command(name="show")
    async def command_show_channels(self, ctx):
        """Show list of radio channels categorized by groups."""
        embed = await self._show_channels(ctx)
        await ctx.send(embed=embed)

    @commands.command(name="setcolor")
    async def command_set_color(self, ctx, color: str):
        """Set the embed color."""
        if not color:
            await ctx.send(embed=ErrorEmbed(error="Color parameter is required!"))
            return
        embed = await self._set_color(ctx, color)
        await ctx.send(embed=embed)

    # Slash Commands
    @nextcord.slash_command(name="join", description="Invite the bot to your voice channel")
    async def slash_join(self, interaction: Interaction):
        embed = await self._join_voice(interaction, is_interaction=True)
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="leave", description="Make the bot leave the voice channel")
    async def slash_leave(self, interaction: Interaction):
        embed = await self._leave_voice(interaction, is_interaction=True)
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="play", description="Play a radio channel by ID")
    async def slash_play(
        self,
        interaction: Interaction,
        channel_id: int = SlashOption(description="Radio channel ID", default=1)
    ):
        await interaction.response.defer()  # Defer for potentially long operations
        result = await self._play_channel(interaction, channel_id, is_interaction=True)
        if isinstance(result, tuple):
            embed, view = result
            await interaction.followup.send(embed=embed, view=view)
        else:
            await interaction.followup.send(embed=result)

    @nextcord.slash_command(name="stop", description="Stop the currently playing radio")
    async def slash_stop(self, interaction: Interaction):
        embed = await self._stop_playback(interaction, is_interaction=True)
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="show", description="Show list of radio channels")
    async def slash_show_channels(self, interaction: Interaction):
        embed = await self._show_channels(interaction, is_interaction=True)
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="setcolor", description="Set the embed color")
    async def slash_set_color(
        self,
        interaction: Interaction,
        color: str = SlashOption(
            description="Choose a color",
            choices=["red", "orange", "yellow", "green", "blue", "purple", "gray", "black"]
        )
    ):
        embed = await self._set_color(interaction, color, is_interaction=True)
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(UserCommands(bot))