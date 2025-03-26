from dal.group_dal import GroupDAL
from dto.group_dto import GroupDTO
from .singleton import Singleton
from typing import List, Optional
import logging

logger = logging.getLogger('group_bll')
class GroupBLL(Singleton):
    def __init__(self):
        self._group_dal = GroupDAL()
        
    def create_table(self):
        self._group_dal.create_table()
        
    def insert(self, group: GroupDTO):
        return self._group_dal.insert(group)
        
    def update(self, group: GroupDTO):
        return self._group_dal.update(group)
        
    def delete(self, group_id: int):
        return self._group_dal.delete(group_id)
        
    def select_all(self) -> List[GroupDTO]:
        return self._group_dal.select_all()
    
    def select_by_id(self, group_id: int) -> Optional[GroupDTO]:
        return self._group_dal.select_by_id(group_id)