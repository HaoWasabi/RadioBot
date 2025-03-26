from dto.channel_dto import ChannelDTO
from .base_dal import BaseDAL
from .group_dal import GroupDAL
import logging

logger = logging.getLogger('channel_dal')
class ChannelDAL(BaseDAL):
    def __init__(self):
        super().__init__()
        
    def create_table(self):
        try:
            self.open_connection()
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS radio_channel (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    group_id INTEGER NOT NULL,
                                    name TEXT NOT NULL,
                                    description TEXT,
                                    link TEXT NOT NULL,
                                    is_active INTEGER NOT NULL,
                                    FOREIGN KEY(group_id) REFERENCES radio_group(id)
                                    )""")
            self.connection.commit()
            self.insert_default_channels()  # Gọi hàm chèn dữ liệu mặc định
        except Exception as e:
            logger.error(f'Error creating channel table: {e}')
        finally:
            self.close_connection()
            
    def insert_default_channels(self):
        """Chèn các kênh mặc định nếu bảng đang trống"""
        try:
            GroupDAL() # Khởi tạo nhóm để chèn nhóm mặc định trước
            self.cursor.execute("SELECT COUNT(*) FROM radio_channel")
            count = self.cursor.fetchone()[0]
            if count == 0:  # Nếu bảng chưa có dữ liệu
                channels = [
                    (1, "VOV1", "VOV1 tần số 100MHz, nghe VOV1 trực tuyến trên website vovmedia.vn, VOV1 online cập nhật tình hình thời sự, chính trị, kinh tế, văn hóa xã hội, quốc phòng an ninh của đất nước", "http://media.kythuatvov.vn:7001/;stream/", 1),
                    (1, "VOV2", "VOV2 tần số 96.5MHz, nghe VOV2 trực tuyến trên website vovmedia.vn, VOV2 online cung cấp thông tin về các lĩnh vực văn hóa, đời sống - xã hội, khoa học - giáo dục, các chương trình văn học nghệ thuật, ca nhạc, giải trí.", "http://media.kythuatvov.vn:7003/;stream/", 1),
                    (1, "VOV3", "VOV3 tần số 102.7MHz, Nghe VOV3 trực tuyến trên website vovmedia.vn, VOV3 online cung cấp thông tin về lĩnh vực âm nhạc, giải trí trong nước và quốc tế.", "http://media.kythuatvov.vn:7005/;stream/", 1),
                    (1, "VOV GT Thành Phố Hồ Chí Minh 91Mhz", "VOV Giao thông tần số 91MHz, nghe VOV Giao Thông HCM trực tuyến trên website vovmedia.vn, VOV Giao thông online cập nhật thông tin giao thông trực tiếp tại Hồ Chí Minh", "http://media.kythuatvov.vn:7023/;stream/", 1),
                    (1, "VOV5", "Nghe VOV5 English 247 trực tuyến trên website vovmedia.vn, VOV5 English 247 online", "https://stream.vovmedia.vn/vov5", 1),
                ]
                self.cursor.executemany("""
                    INSERT INTO radio_channel (group_id, name, description, link, is_active)
                    VALUES (?, ?, ?, ?, ?)""", channels)
                self.connection.commit()
                logger.info("Default radio channels inserted successfully.")
        except Exception as e:
            logger.error(f"Error inserting default channels: {e}")
            
    def insert(self, channel: ChannelDTO):
        try:
            self.open_connection()
            self.cursor.execute('INSERT INTO radio_channel (group_id, name, description, link, is_active) VALUES (?, ?, ?, ?, ?)',
                                (channel.get_group_id(), channel.get_name(), channel.get_description(), channel.get_link(), channel.get_is_active()))
            self.connection.commit()
            return self.cursor.lastrowid
        except Exception as e:
            logger.error(f'Error inserting channel: {e}')
            return None
        finally:
            self.close_connection()
            
    def update(self, channel: ChannelDTO):
        try:
            self.open_connection()
            self.cursor.execute('UPDATE radio_channel SET group_id=?, name=?, description=?, link=?, is_active=? WHERE id=? AND is_active<>0',
                                (channel.get_group_id(), channel.get_name(), channel.get_description(), channel.get_link(), channel.get_is_active(), channel.get_id()))
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f'Error updating channel: {e}')
            return False
        finally:
            self.close_connection()
            
    def delete(self, channel_id: int):
        try:
            self.open_connection()
            self.cursor.execute('UPDATE radio_channel SET is_active=0 WHERE id=? AND is_active<>0', (channel_id,))
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f'Error deleting channel: {e}')
            return False
        finally:
            self.close_connection()
            
    def undelete(self, channel_id: int):
        try:
            self.open_connection()
            self.cursor.execute('UPDATE radio_channel SET is_active=1 WHERE id=? AND is_active=0', (channel_id,))
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f'Error undeleting channel: {e}')
            return False
        finally:
            self.close_connection()
            
    def select_all(self):
        try:
            self.open_connection()
            self.cursor.execute('SELECT * FROM radio_channel WHERE is_active<>0')
            return [ChannelDTO(*row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f'Error selecting all channels: {e}')
        finally:
            self.close_connection()
            
    def select_by_id(self, channel_id: int):
        try:
            self.open_connection()
            self.cursor.execute('SELECT * FROM radio_channel WHERE id=? AND is_active<>0', (channel_id,))
            row = self.cursor.fetchone()
            return ChannelDTO(*row) if row else None
        except Exception as e:
            logger.error(f'Error selecting channel by id: {e}')
        finally:
            self.close_connection()
            