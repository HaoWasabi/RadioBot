from dal.channel_dal import ChannelDAL
from dto.channel_dto import ChannelDTO
from .singleton import Singleton
from typing import List, Optional
import logging

logger = logging.getLogger('channel_bll')
class ChannelBLL(Singleton):
    def __init__(self):
        self._channel_dal = ChannelDAL()
        
    def create_table(self):
        self._channel_dal.create_table()
        
    def insert(self, channel: ChannelDTO):
        return self._channel_dal.insert(channel)
        
    def update(self, channel: ChannelDTO):
        return self._channel_dal.update(channel)
        
    def delete(self, channel_id: int):
        return self._channel_dal.delete(channel_id)
        
    def select_all(self) -> List[ChannelDTO]:
        return self._channel_dal.select_all()
    
    def select_by_id(self, channel_id: int) -> Optional[ChannelDTO]:
        return self._channel_dal.select_by_id(channel_id)