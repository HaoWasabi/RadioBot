import nextcord
from nextcord import Interaction
from nextcord.ui import View, Button
from nextcord.ext.commands import Bot
from .embed_custom import EmbedCustom
from .error_embed import ErrorEmbed
from .insert_channel_modal import InsertChannelModal
from .insert_group_modal import InsertGroupModal
from utils.check_authorization import check_authorization

class InsertButtons(View):
    def __init__(self, user, bot: Bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.author = user  # Người dùng khởi tạo tương tác
        self.color = int("0xBDB76B", 16)       
    
    @nextcord.ui.button(label="channel", style=nextcord.ButtonStyle.secondary)
    async def insert_channel_button(self, button: Button, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return

        try:
            await interaction.response.send_modal(modal=InsertChannelModal(self.author))

        except Exception as e:
            await interaction.response.send_message(embed=ErrorEmbed(error=e), ephemeral=True)
            print(f"Error: {e}")
            
    @nextcord.ui.button(label="group", style=nextcord.ButtonStyle.secondary)
    async def insert_group_button(self, button: Button, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return

        try:
            await interaction.response.send_modal(modal=InsertGroupModal(self.author))

        except Exception as e:
            await interaction.response.send_message(embed=ErrorEmbed(error=e), ephemeral=True)
            print(f"Error: {e}")
            