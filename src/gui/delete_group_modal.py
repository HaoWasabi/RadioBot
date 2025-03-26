from nextcord import Interaction
from nextcord.ui import TextInput, Modal
from dto.group_dto import GroupDTO
from bll.group_bll import GroupBLL
from utils.check_authorization import check_authorization
from .embed_custom import EmbedCustom
from .error_embed import ErrorEmbed

class DeleteGroupModal(Modal):
    def __init__(self, user):
        super().__init__(title="Delete Group Radio")
        self.color = int("0xBDB76B", 16)  
        self.author = user
        self.id_ = TextInput(label="Group radio id", placeholder="Enter the group radio id", required=True)
        self.add_item(self.id_)
        
    async def callback(self, interaction: Interaction):
        server_id =  interaction.guild.id if interaction.guild else interaction.user.id 
        
        if not await check_authorization(interaction, self.author):
            return
        
        await interaction.response.defer()
        try:
            group_bll = GroupBLL()
            if group_bll.delete(int(self.id_.value)):
                embed = EmbedCustom(
                    id_server=str(server_id),
                    description=f"✅ Successfully delete group radio (`{self.id_.value}`).",
                    color=self.color
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.followup.send(embed=ErrorEmbed(error=e), ephemeral=True)
