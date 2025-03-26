class ServerDTO:
    def __init__(self, id_: int, name: str, color_embed: str, is_active: int=1):
        self.id = id_
        self.name = name
        self.color_embed = color_embed
        self.is_active = is_active
        
    def __str__(self):
        return f'ServerDTO(id={self.id}, name={self.name}, color_embed={self.color_embed}, is_active={self.is_active})'
    
    def set_id(self, id_: int):
        self.id = id_
        
    def set_name(self, name: str):
        self.name = name
        
    def set_color_embed(self, color_embed: str):
        self.color_embed = color_embed
        
    def set_is_active(self, is_active: int):
        self.is_active = is_active
        
    def get_id(self) -> int:
        return self.id
    
    def get_name(self) -> str:
        return self.name
    
    def get_color_embed(self) -> str:
        return self.color_embed
    
    def get_is_active(self) -> int:
        return self.is_active