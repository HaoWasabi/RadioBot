import nextcord
from nextcord import Interaction
from nextcord.ui import View, Button
from nextcord.ext.commands import Bot
from .error_embed import ErrorEmbed
from .insert_channel_modal import InsertChannelModal
from .update_channel_modal import UpdateChannelModal
from .delete_channel_modal import DeleteChannelModal
from utils.check_authorization import check_authorization

class ChannelButtons(View):
    def __init__(self, user, bot: Bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.author = user  # Người dùng khởi tạo tương tác
        self.color = int("0xBDB76B", 16)       
            
    @nextcord.ui.button(label="insert", style=nextcord.ButtonStyle.secondary)
    async def insert_channel_button(self, button: Button, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return

        try:
            await interaction.response.send_modal(modal=InsertChannelModal(self.author))

        except Exception as e:
            await interaction.response.send_message(embed=ErrorEmbed(error=e), ephemeral=True)
            print(f"Error: {e}")
            
    @nextcord.ui.button(label="update", style=nextcord.ButtonStyle.secondary)
    async def update_channel_button(self, button: Button, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return

        try:
            await interaction.response.send_modal(modal=UpdateChannelModal(self.author))

        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)
            print(f"Error: {e}")
            
    @nextcord.ui.button(label="delete", style=nextcord.ButtonStyle.danger)
    async def delete_channel_button(self, button: Button, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return

        try:
            await interaction.response.send_modal(modal=DeleteChannelModal(self.author))

        except Exception as e:
            await interaction.response.send_message(embed=ErrorEmbed(error=e), ephemeral=True)
            print(f"Error: {e}")
            
            