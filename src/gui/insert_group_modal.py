from nextcord import Interaction
from nextcord.ui import TextInput, Modal
from dto.group_dto import GroupDTO
from bll.group_bll import GroupBLL
from utils.check_authorization import check_authorization
from .embed_custom import EmbedCustom
from .error_embed import ErrorEmbed

class InsertGroupModal(Modal):
    def __init__(self, user):
        super().__init__(title="Insert Group Radio")
        self.color = int("0xBDB76B", 16)  
        self.author = user
        self.name = TextInput(label="Group radio name", placeholder="Enter the group radio name", required=True)
        self.description = TextInput(label="Group radio description", placeholder="Enter the group radio description", required=False)
        self.add_item(self.name)
        self.add_item(self.description)
        
    async def callback(self, interaction: Interaction):
        server_id =  interaction.guild.id if interaction.guild else interaction.user.id 
        
        if not await check_authorization(interaction, self.author):
            return
        
        await interaction.response.defer()
        try:
            group_bll = GroupBLL()
            group_dto = GroupDTO(
                id_=0,
                name=self.name.value, # type: ignore
                description=self.description.value, # type: ignore)
            )
            
            real_id = group_bll.insert(group_dto)
            if real_id:
                embed = EmbedCustom(
                    id_server=str(server_id),
                    description=f"✅ Successfully insert group radio **{self.name.value}** (`{real_id}`).",
                    color=self.color
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.followup.send(embed=ErrorEmbed(error=e), ephemeral=True)
