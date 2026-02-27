import sqlite3
from core.setup import BASE_DIR

class SQliteDB:
    
    def __init__(self, db_path=BASE_DIR / "syncord.db"):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.setup()
    
    def close(self):
        self.connection.close()
        
    def setup(self):
        # Example setup method to create a table
        self.cursor.execute('''CREATE TABLE if not exists syncord(parition_number integer, parition_uuid text, message_id text primary key, file_name text, folder_name text, file_size_bytes integer)''')
        self.connection.commit()
        
    def add_file(
        self,
        partition_number: int,
        partition_uuid: str,
        message_id: str,
        file_name: str,
        folder_name: str,
        file_size_bytes: int
    ):
        
        #
        self.cursor.execute(
            '''INSERT INTO syncord (parition_number, parition_uuid, message_id, file_name, folder_name, file_size_bytes) VALUES (?, ?, ?, ?, ?, ?)''', 
            (partition_number, partition_uuid, message_id, file_name, folder_name, file_size_bytes)
        )

        #
        self.connection.commit()
    
    def get_file_by_message_id(self, message_id: str):
        self.cursor.execute('''SELECT * FROM syncord WHERE message_id = ?''', (message_id,))
        return self.cursor.fetchone()

    def get_file_by_parition_id(self, partition_uuid: str):
        self.cursor.execute('''SELECT * FROM syncord WHERE parition_uuid = ? ORDER BY parition_number''', (partition_uuid,))
        return self.cursor.fetchall()
    
    def get_file_by_file_path(self, folder_name: str, file_name: str):
        self.cursor.execute('''SELECT * FROM syncord WHERE folder_name = ? AND file_name = ?''', (folder_name, file_name))
        return self.cursor.fetchall()

    def delete_file_by_file_path(self, folder_name:str, file_name:str):
 
        self.cursor.execute(
            """DELETE FROM syncord WHERE file_name = ? AND folder_name = ?""", 
            (file_name, folder_name)
        )
        
        self.connection.commit()

    def delete_file_by_message_id(self, message_id: str):
        self.cursor.execute('''DELETE FROM syncord WHERE message_id = ?''', (message_id,))
        self.connection.commit()
    
    def delete_file_by_parition_id(self, partition_number: int, partition_uuid: str):
        self.cursor.execute('''DELETE FROM syncord WHERE parition_number = ? AND parition_uuid = ?''', (partition_number, partition_uuid))
        self.connection.commit()
    
    def get_all_folder_files(self, folder_name: str):
        self.cursor.execute('''SELECT * FROM syncord WHERE folder_name = ?''', (folder_name,))
        return self.cursor.fetchall()

    def get_all_files(self):
        self.cursor.execute('''SELECT * FROM syncord''')
        return self.cursor.fetchall()
        
    def clear_database(self):
        self.cursor.execute('''DELETE FROM syncord''')
        self.connection.commit()
    
    def get_all_folders(self):
        self.cursor.execute('''SELECT DISTINCT folder_name FROM syncord''')
        return [row[0] for row in self.cursor.fetchall()]
        
    
if __name__ == "__main__":
    db = SQliteDB("syncord.db")
    # db.setup()
    db.close()