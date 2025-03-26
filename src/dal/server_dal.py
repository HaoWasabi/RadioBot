from dto.server_dto import ServerDTO
from .base_dal import BaseDAL
import logging

logger = logging.getLogger('server_dal')
class ServerDAL(BaseDAL):
    def __init__(self):
        super().__init__()
        
    def create_table(self):
        try:
            self.open_connection()
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS server (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    color_embed TEXT DEFAULT '0x2F3136',
                                    is_active INTEGER NOT NULL
                                    )""")
            self.connection.commit()
        except Exception as e:
            logger.error(f'Error creating server table: {e}')
        finally:
            self.close_connection()
            
    def insert(self, server: ServerDTO):
        try:
            self.open_connection()
            self.cursor.execute('INSERT INTO server (id, name, color_embed, is_active) VALUES (?, ?, ?, ?)',
                                (server.get_id(), server.get_name(), server.get_color_embed(), server.get_is_active()))
            self.connection.commit()
            return self.cursor.lastrowid
        except Exception as e:
            logger.error(f'Error inserting server: {e}')
            return None
        finally:
            self.close_connection()
            
    def update(self, server: ServerDTO):
        try:
            self.open_connection()
            self.cursor.execute('UPDATE server SET name=?, color_embed=?, is_active=? WHERE id=?',
                                (server.get_name(), server.get_color_embed(), server.get_is_active(), server.get_id()))
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f'Error updating server: {e}')
            return False
        finally:
            self.close_connection()
            
    def delete(self, server_id: int):
        try:
            self.open_connection()
            self.cursor.execute('UPDATE server SET is_active=0 AND is_active<>0', (server_id,))
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f'Error deleting server: {e}')
            return False
        finally:
            self.close_connection()
            
    def undelete(self, server_id: int):
        try:
            self.open_connection()
            self.cursor.execute('UPDATE server SET is_active=1 AND is_active=0', (server_id,))
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f'Error undeleting server: {e}')
            return False
        finally:
            self.close_connection()
            
    def select_all(self):
        try:
            self.open_connection()
            self.cursor.execute('SELECT * FROM server')
            return [ServerDTO(*row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f'Error selecting all servers: {e}')
        finally:
            self.close_connection()
            
    def select_by_id(self, server_id: int):
        try:
            self.open_connection()
            self.cursor.execute('SELECT * FROM server WHERE id=?', (server_id,))
            row = self.cursor.fetchone()
            return ServerDTO(*row) if row else None
        except Exception as e:
            logger.error(f'Error selecting server by id: {e}')
        finally:
            self.close_connection()
            