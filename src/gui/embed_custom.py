import nextcord
from bll.server_bll import ServerBLL
from dto.server_dto import ServerDTO

# Custom Embed class with default color and methods to set/get color
class EmbedCustom(nextcord.Embed):
    def __init__(self, id_server: str, **kwargs):
        # Fetch the default color from the server's settings
        server_bll = ServerBLL()
        server_dto = server_bll.select_by_id(id_server)
        
        if 'color' not in kwargs:
            # If no color is provided, use the server's wanring color
            if server_dto is None: 
                default_color = "0x2F3136"  # Default to red if server not found
            else:
                default_color = server_dto.get_color_embed()
            kwargs['color'] = nextcord.Color(int(default_color, 16))  # Convert hex to int

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

    def get_color_hex(self):
        # Returns the hex code of the embed color as a string.
        return hex(self.color.value)