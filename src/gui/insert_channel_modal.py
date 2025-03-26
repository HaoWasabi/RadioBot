from nextcord import Interaction
from nextcord.ui import TextInput, Modal
from dto.channel_dto import ChannelDTO
from bll.channel_bll import ChannelBLL
from utils.check_authorization import check_authorization
from .embed_custom import EmbedCustom
from .error_embed import ErrorEmbed

class InsertChannelModal(Modal):
    def __init__(self, user):
        super().__init__(title="Insert Channel Radio")
        self.color = int("0xBDB76B", 16)  
        self.author = user
        self.group_id = TextInput(label="Group radio id", placeholder="Enter the group radio id", required=True)
        self.name = TextInput(label="Channel radio name", placeholder="Enter the channel radio name", required=True)
        self.description = TextInput(label="Channel radio description", placeholder="Enter the channel radio description", required=False)
        self.link = TextInput(label="Channel radio link", placeholder="Enter the channel radio link", required=True)
        self.add_item(self.group_id)
        self.add_item(self.name)
        self.add_item(self.description)
        self.add_item(self.link)
        
    async def callback(self, interaction: Interaction):
        server_id =  interaction.guild.id if interaction.guild else interaction.user.id 
        
        if not await check_authorization(interaction, self.author):
            return
        
        await interaction.response.defer()
        try:
            channel_bll = ChannelBLL()
            channel_dto = ChannelDTO(
                id_=0,
                group_id= int(self.group_id.value), # type: ignore
                name=self.name.value, # type: ignore
                description=self.description.value, # type: ignore)
                link=self.link.value, # type: ignore)
            )
            
            real_id = channel_bll.insert(channel_dto)
            if real_id:
                embed = EmbedCustom(
                    id_server=str(server_id),
                    description=f"✅ Successfully insert channel radio **{self.name.value}** (`{real_id}`).",
                    color=self.color
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.followup.send(embed=ErrorEmbed(error=e), ephemeral=True)
