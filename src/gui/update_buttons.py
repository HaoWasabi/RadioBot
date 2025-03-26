import nextcord
from nextcord import Interaction
from nextcord.ui import View, Button
from nextcord.ext.commands import Bot
from .embed_custom import EmbedCustom
from .update_channel_modal import UpdateChannelModal
from .update_group_modal import UpdateGroupModal
from utils.check_authorization import check_authorization

class UpdateButtons(View):
    def __init__(self, user, bot: Bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.author = user  # Người dùng khởi tạo tương tác
        self.color = int("0xBDB76B", 16)       
    
    @nextcord.ui.button(label="channel", style=nextcord.ButtonStyle.secondary)
    async def update_channel_button(self, button: Button, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return

        try:
            await interaction.response.send_modal(modal=UpdateChannelModal(self.author))

        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)
            print(f"Error: {e}")
            
    @nextcord.ui.button(label="group", style=nextcord.ButtonStyle.secondary)
    async def update_group_button(self, button: Button, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return

        try:
            await interaction.response.send_modal(modal=UpdateGroupModal(self.author))

        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)
            print(f"Error: {e}")
            