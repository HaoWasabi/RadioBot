from dto.group_dto import GroupDTO
from .base_dal import BaseDAL
import logging

logger = logging.getLogger('group_dal')
class GroupDAL(BaseDAL):
    def __init__(self):
        super().__init__()
        
    def create_table(self):
        try:
            self.open_connection()
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS radio_group (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name TEXT NOT NULL,
                                    description TEXT,
                                    is_active INTEGER NOT NULL
                                    )""")   
            self.connection.commit()
            self.insert_default_groups()  # Gọi hàm chèn dữ liệu mặc định
        except Exception as e:
            logger.error(f'Error creating group table: {e}')
        finally:
            self.close_connection()
            
    def insert_default_groups(self):
        """Chèn các nhóm kênh mặc định nếu bảng đang trống"""
        try:
            self.cursor.execute("SELECT COUNT(*) FROM radio_group")
            count = self.cursor.fetchone()[0]
            if count == 0:  # Nếu bảng chưa có dữ liệu
                groups = [
                    ("VOV Media", "Đài Tiếng nói Việt Nam", 1),
                ]
                self.cursor.executemany("""
                    INSERT INTO radio_group (name, description, is_active)
                    VALUES (?, ?, ?)""", groups)
                self.connection.commit()
                logger.info("Default radio groups inserted successfully.")
        except Exception as e:
            logger.error(f"Error inserting default groups: {e}")
            
    def insert(self, group: GroupDTO):
        try:
            self.open_connection()
            self.cursor.execute('INSERT INTO radio_group (name, description, is_active) VALUES (?, ?, ?)',
                                (group.get_name(), group.get_description(), group.get_is_active()))
            self.connection.commit()
            return self.cursor.lastrowid
        except Exception as e:
            logger.error(f'Error inserting group: {e}')
            return None
        finally:
            self.close_connection()
            
    def update(self, group: GroupDTO):
        try:
            self.open_connection()
            self.cursor.execute('UPDATE radio_group SET name=?, description=?, is_active=? WHERE id=? AND  is_active<>0',
                                (group.get_name(), group.get_description(), group.get_is_active(), group.get_id()))
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f'Error updating group: {e}')
            return False
        finally:
            self.close_connection()
            
    def delete(self, group_id: int):
        try:
            self.open_connection()
            self.cursor.execute('UPDATE radio_group SET is_active=0 WHERE id=? AND is_active<>0', (group_id,))
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f'Error deleting group: {e}')
            return False
        finally:
            self.close_connection()
            
    def undelete(self, group_id: int):
        try:
            self.open_connection()
            self.cursor.execute('UPDATE radio_group SET is_active=1 WHERE id=? AND is_active=0', (group_id,))
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f'Error undeleting group: {e}')
            return False
        finally:
            self.close_connection()
            
    def select_all(self):
        try:
            self.open_connection()
            self.cursor.execute('SELECT * FROM radio_group WHERE is_active<>0')
            rows = self.cursor.fetchall()
            return [GroupDTO(*row) for row in rows]
        except Exception as e:
            logger.error(f'Error selecting all groups: {e}')
        finally:
            self.close_connection()
            
    def select_by_id(self, group_id: int):
        try:
            self.open_connection()
            self.cursor.execute('SELECT * FROM radio_group WHERE id=? AND is_active<>0', (group_id,))
            row = self.cursor.fetchone()
            return GroupDTO(*row) if row else None
        except Exception as e:
            logger.error(f'Error selecting group by id: {e}')
        finally:
            self.close_connection()