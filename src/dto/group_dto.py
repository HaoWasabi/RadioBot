class GroupDTO:
    def __init__(self, id_: int, name: str, description: str, is_active: int=1):
        self.id = id_
        self.name = name
        self.description = description
        self.is_active = is_active
        
    def __str__(self):
        return f'GroupDTO(id={self.id}, name={self.name}, description={self.description}, is_active={self.is_active})'
    
    def set_id(self, id_: int):
        self.id = id_
        
    def set_name(self, name: str):
        self.name = name
        
    def set_description(self, description: str):
        self.description = description
        
    def set_is_active(self, is_active: int):
        self.is_active = is_active
        
    def get_id(self) -> int:
        return self.id
    
    def get_name(self) -> str:
        return self.name
    
    def get_description(self) -> str:
        return self.description
    
    def get_is_active(self) -> int:
        return self.is_active