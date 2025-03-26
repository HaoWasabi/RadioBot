from dal.server_dal import ServerDAL
from dto.server_dto import ServerDTO
from .singleton import Singleton
from typing import List, Optional
import logging

logger = logging.getLogger('server_bll')
class ServerBLL(Singleton):
    def __init__(self):
        self._server_dal = ServerDAL()
        
    def create_table(self):
        self._server_dal.create_table()
        
    def insert(self, server: ServerDTO):
        return self._server_dal.insert(server)
        
    def update(self, server: ServerDTO):
        return self._server_dal.update(server)
        
    def delete(self, server_id: int):
        return self._server_dal.delete(server_id)
        
    def select_all(self) -> List[ServerDTO]:
        return self._server_dal.select_all()
    
    def select_by_id(self, server_id: int) -> Optional[ServerDTO]:
        return self._server_dal.select_by_id(server_id)
