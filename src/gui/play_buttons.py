import os
import nextcord
from nextcord import Interaction
from nextcord.ui import View, Button
from nextcord.ext import commands  # Thay vì import Bot trực tiếp
import imageio_ffmpeg as ffmpeg
from .error_embed import ErrorEmbed
from .embed_custom import EmbedCustom
from bll.channel_bll import ChannelBLL
from utils.check_authorization import check_authorization

# Lấy đường dẫn của FFmpeg do imageio cung cấp
FFMPEG_PATH = ffmpeg.get_ffmpeg_exe()
os.environ["FFMPEG_EXECUTABLE"] = FFMPEG_PATH

class PlayButtons(View):
    def __init__(self, user, bot: commands.Bot, current_channel_id: int = 1):
        super().__init__(timeout=None)
        self.bot = bot
        self.author = user
        self.current_channel_id = current_channel_id
        self.channel_list = ChannelBLL().select_all()

        for item in self.children:
            if isinstance(item, Button) and item.custom_id == "start_button":
                item.disabled = True

    @nextcord.ui.button(label="⏮️ Previous", style=nextcord.ButtonStyle.secondary, row=1)
    async def previous_button(self, button: Button, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return

        prev_id = self._get_adjacent_channel_id(-1)
        await self._play_channel(interaction, prev_id)

    @nextcord.ui.button(label="⏹️ Stop", style=nextcord.ButtonStyle.danger, custom_id="stop_button", row=1)
    async def stop_button(self, button: Button, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return

        try:
            vc = interaction.guild.voice_client
            server_id = interaction.guild.id if interaction.guild else interaction.user.id

            if vc and vc.is_playing():
                vc.stop()
                embed = EmbedCustom(
                    id_server=str(server_id),
                    description="⏹️ Stopped the radio playback."
                )
            else:
                embed = ErrorEmbed(error="There's no radio playing to stop.")

            new_view = PlayButtons(self.author, self.bot, current_channel_id=self.current_channel_id)
            for child in new_view.children:
                if isinstance(child, Button):
                    if child.custom_id == "stop_button":
                        child.disabled = True
                    elif child.custom_id == "start_button":
                        child.disabled = False

            await interaction.response.edit_message(embed=embed, view=new_view)

        except Exception as e:
            await interaction.response.send_message(embed=ErrorEmbed(error=e))
            print(f"Error: {e}")

    @nextcord.ui.button(label="▶️ Start", style=nextcord.ButtonStyle.success, custom_id="start_button", row=1)
    async def start_button(self, button: Button, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return

        await self._play_channel(interaction, self.current_channel_id)

    @nextcord.ui.button(label="⏭️ Next", style=nextcord.ButtonStyle.secondary, row=1)
    async def next_button(self, button: Button, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return

        next_id = self._get_adjacent_channel_id(1)
        await self._play_channel(interaction, next_id)

    def _get_adjacent_channel_id(self, offset: int) -> int:
        ids = [c.get_id() for c in self.channel_list]
        if self.current_channel_id not in ids:
            return ids[0]
        index = ids.index(self.current_channel_id)
        new_index = (index + offset) % len(ids)
        return ids[new_index]

    async def _play_channel(self, interaction: Interaction, new_channel_id: int):
        try:
            channel_dto = ChannelBLL().select_by_id(new_channel_id)
            vc = interaction.guild.voice_client

            if not vc:
                await interaction.response.send_message(embed=ErrorEmbed("Bot is not in a voice channel"))
                return

            link = channel_dto.get_link()
            vc.stop()
            source = nextcord.FFmpegPCMAudio(executable=FFMPEG_PATH, source=link)
            vc.play(source)

            embed = EmbedCustom(
                id_server=str(interaction.guild.id),
                description=f"📻 Switched to **{channel_dto.get_name()}**"
            )

            new_view = PlayButtons(self.author, self.bot, current_channel_id=new_channel_id)
            await interaction.response.edit_message(embed=embed, view=new_view)

        except Exception as e:
            await interaction.response.send_message(embed=ErrorEmbed(error=e))
            print(f"Error: {e}")
