
import logging
import nextcord
import os
from nextcord.ext import commands
from bll.channel_bll import ChannelBLL
from gui.embed_custom import EmbedCustom
from gui.error_embed import ErrorEmbed
import imageio_ffmpeg as ffmpeg

logger = logging.getLogger("PlayCommand")

# Lấy đường dẫn của FFmpeg do imageio cung cấp
FFMPEG_PATH = ffmpeg.get_ffmpeg_exe()
os.environ["FFMPEG_EXECUTABLE"] = FFMPEG_PATH

class PlayCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="play")
    async def play(self, ctx, channel_id: int=1):
        """Command to play radio from URL"""
        channel_dto = ChannelBLL().select_by_id(channel_id)
        server_id =  ctx.guild.id if ctx.guild else ctx.author.id 
        vc = ctx.voice_client
        
        if channel_dto: 
            link = channel_dto.get_link()
            if vc:
                vc.stop()  # Dừng âm thanh hiện tại (nếu có)
                source = nextcord.FFmpegPCMAudio(executable=FFMPEG_PATH, source=link)
                vc.play(source)
                embed = EmbedCustom(
                    id_server=str(server_id),
                    description=f"📻 Started playing **{channel_dto.get_name()}**"
                )
            
            else:
                embed = ErrorEmbed(error="Bot has not been not in the voice channel!")
        
        else:
            embed = ErrorEmbed(error="Channel not found!")
            
        await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(PlayCommand(bot))