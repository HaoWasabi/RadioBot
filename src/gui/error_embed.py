import nextcord
from bll.server_bll import ServerBLL
from dto.server_dto import ServerDTO
from typing import Union

# Custom Embed class with default color and methods to set/get color
class ErrorEmbed(nextcord.Embed):
    def __init__(self, error: Union[str,Exception], **kwargs):
        # Fetch the default color from the server's settings
        kwargs['description'] = f"❌ Error: {error}"
        kwargs['color'] = int("0xFF0000", 16)  # Convert hex to int

        # Set a default footer if not already set
        if 'footer' not in kwargs:
            self.set_footer(text="GCdev Solo Project 2025")
            
        super().__init__(**kwargs)

    def set_color(self, color):
        # Set the color of the embed. Color should be a nextcord.Color instance.
        if isinstance(color, nextcord.Color):
            self.color = color
        else:
            raise ValueError("Color must be an instance of nextcord.Color")
