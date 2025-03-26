import logging
import nextcord
from nextcord.ext import commands
from utils.commands_cog import CommandsCog
from nextcord import Interaction, SlashOption
from dto.color_dto import ColorDTO
from dto.server_dto import ServerDTO
from bll.server_bll import ServerBLL
from gui.embed_custom import EmbedCustom
from gui.error_embed import ErrorEmbed


logger = logging.getLogger("CommandSetColor")

class SetColorCommand(CommandsCog):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(name='setcolor')
    async def command_set_color(self, ctx, color: str):
        '''Set the color of all embeds that you want it would send'''
        if not color:
            await ctx.send('This command must have color.')
            return

        await self._set_color(ctx, color, ctx.guild, ctx.author)

    @nextcord.slash_command(name="setcolor", description="Set the color of all embeds that you want it would send")
    async def slash_set_color(self, interaction: Interaction, 
                              color: str = SlashOption(
                                  name="color",
                                  description="Choose a color for the embeds",
                                  choices={"Red": "red", "Orange": "orange", "Yellow": "yellow", "Green": "green", 
                                           "Blue": "blue", "Purple": "purple", "Black": "black", "Gray": "gray"}
                              )):
        await interaction.response.defer()

        await self._set_color(interaction.followup, color, interaction.guild, interaction.user)

    async def _set_color(self, ctx, color: str, guild, user):
        server_id = guild.id if guild else user.id 
        server_name = guild.name if guild else user.name 
        
        try:
            server_bll = ServerBLL()
            color_dto = ColorDTO(color)
            server_dto = ServerDTO(str(server_id), server_name, color_dto.get_hex_color())

            if not server_bll.select_by_id(server_dto.get_id()):
                server_bll.insert(server_dto)
            else:
                server_bll.update(server_dto)

            hex_color = color_dto.get_hex_color()
            embed = EmbedCustom(
                id_server=server_dto.get_id(),
                description=f"✅ Set color **{color_dto.get_name_color()}** successfully.",
                color=int(hex_color, 16)
            )
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(embed = ErrorEmbed(error=e))
            logger.error(f"Error: {e}")

async def setup(bot):
    bot.add_cog(SetColorCommand(bot))
