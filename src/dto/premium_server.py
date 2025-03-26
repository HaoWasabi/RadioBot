class PremiumServerDTO:
    def __init__(self, id_: int, server_id: int, start_date: str, end_date: str, is_active: int=1):
        self.id = id_
        self.server_id = server_id
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = is_active
        
    def __str__(self):
        return f'PremiumServerDTO(id={self.id}, server_id={self.server_id}, start_date={self.start_date}, end_date={self.end_date}, is_active={self.is_active})'
    
    def set_id(self, id_: int):
        self.id = id_
        
    def set_server_id(self, server_id: int):
        self.server_id = server_id
        
    def set_start_date(self, start_date: str):
        self.start_date = start_date
        
    def set_end_date(self, end_date: str):
        self.end_date = end_date
        
    def set_is_active(self, is_active: int):
        self.is_active = is_active
        
    def get_id(self) -> int:
        return self.id
    
    def get_server_id(self) -> int:
        return self.server_id
    
    def get_start_date(self) -> str:
        return self.start_date
    
    def get_end_date(self) -> str:
        return self.end_date
    
    def get_is_active(self) -> int:
        return self.is_active