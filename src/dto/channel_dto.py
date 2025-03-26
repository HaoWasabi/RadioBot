class ChannelDTO:
    def __init__(self, id_: int, group_id: int, name: str, description: str, link: str, is_active: int=1):
        self.id = id_
        self.group_id = group_id
        self.name = name
        self.description = description
        self.link = link
        self.is_active = is_active
        
    def __str__(self):
        return f'ChannelDTO(id={self.id}, group_id={self.group_id}, name={self.name}, description={self.description}, is_premium={self.is_premium}, is_active={self.is_active})'
    
    def set_id(self, id_: int):
        self.id = id_
        
    def set_group_id(self, group_id: int):
        self.group_id = group_id
        
    def set_name(self, name: str):
        self.name = name
        
    def set_description(self, description: str):
        self.description = description
        
    def set_link(self, link: str):
        self.link = link
        
    def set_is_active(self, is_active: int):
        self.is_active = is_active
        
    def get_id(self) -> int:
        return self.id
    
    def get_group_id(self) -> int:
        return self.group_id
    
    def get_name(self) -> str:
        return self.name
    
    def get_description(self) -> str:
        return self.description
    
    def get_link(self) -> str:
        return self.link
    
    def get_is_active(self) -> int:
        return self.is_active
    
