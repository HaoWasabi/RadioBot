import nextcord
from nextcord import Interaction
from nextcord.ui import View, Button
from nextcord.ext.commands import Bot
from .embed_custom import EmbedCustom
from .error_embed import ErrorEmbed
from .group_buttons import GroupButtons
from .channel_buttons import ChannelButtons
from utils.check_authorization import check_authorization

class CtrlButtons(View):
    def __init__(self, user, bot: Bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.author = user  # Người dùng khởi tạo tương tác
        self.color = int("0xBDB76B", 16)        
    
    @nextcord.ui.button(label="1", style=nextcord.ButtonStyle.blurple)
    async def show_servers_button(self, button: Button, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return

        try:
            id_server = str(interaction.guild.id) if interaction.guild else "Unknown"
            guild_names = [guild.name for guild in self.bot.guilds]
            num = len(guild_names)

            embed = EmbedCustom(
                id_server=id_server,
                description=f"The bot joined {num} guilds: **{', '.join(guild_names)}**",
                color=self.color
            )
            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(embed=ErrorEmbed(error=e))
            print(f"Error in show_servers_button: {e}")
            
    @nextcord.ui.button(label="2", style=nextcord.ButtonStyle.blurple)
    async def group_button(self, button: Button, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return

        try:
            server_id = str(interaction.guild.id) if interaction.guild else "Unknown"
            
            embed = EmbedCustom(
                id_server=server_id,
                title="Group Panel",
                description="Choose an option to change.",
                color= self.color
            )
            await interaction.response.send_message(embed=embed, view=GroupButtons(self.author, self.bot))

        except Exception as e:
            await interaction.response.send_message(embed=ErrorEmbed(error=e))
            print(f"'❌ Error: {e}")
            
    @nextcord.ui.button(label="3", style=nextcord.ButtonStyle.blurple)
    async def channel_button(self, button: Button, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return

        try:
            server_id = str(interaction.guild.id) if interaction.guild else "Unknown"
            
            embed = EmbedCustom(
                id_server=server_id,
                title="Channel Panel",
                description="Choose an option to change.",
                color= self.color
            )
            await interaction.response.send_message(embed=embed, view=ChannelButtons(self.author, self.bot))

        except Exception as e:
            await interaction.response.send_message(embed=ErrorEmbed(error=e))
            print(f"'❌ Error: {e}")
            
    @nextcord.ui.button(label="4", style=nextcord.ButtonStyle.danger)
    async def shutdown_button(self, button: Button, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return
            
        await interaction.response.send_message("The bot is shutting down...")
        await self.bot.close()
