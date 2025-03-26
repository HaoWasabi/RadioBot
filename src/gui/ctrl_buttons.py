import nextcord
from nextcord import Interaction
from nextcord.ui import View, Button
from nextcord.ext.commands import Bot
from .embed_custom import EmbedCustom
from .error_embed import ErrorEmbed
from utils.check_authorization import check_authorization

class CtrlButtons(View):
    def __init__(self, user, bot: Bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.author = user  # Người dùng khởi tạo tương tác
        self.color = int("0xF1C40F", 16)       
    
    @nextcord.ui.button(label="show servers", style=nextcord.ButtonStyle.blurple)
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
            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(embed=ErrorEmbed(error=e), ephemeral=True)
            print(f"Error in show_servers_button: {e}")
            
    @nextcord.ui.button(label="shutdown", style=nextcord.ButtonStyle.danger)
    async def shutdown_button(self, button: Button, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return
            
        await interaction.response.send_message("The bot is shutting down...", ephemeral=True)
        await self.bot.close()
