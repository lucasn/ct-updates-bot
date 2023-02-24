import sqlite3
import logging

class Database:
    def __init__(self, database_name: str = 'bot.db') -> None:
        self.connection = sqlite3.connect(database_name)
        init_cursor = self.connection.cursor()
        init_cursor.execute('CREATE TABLE IF NOT EXISTS chat (chat_id INT PRIMARY KEY);')
        init_cursor.execute('CREATE TABLE IF NOT EXISTS news (title VARCHAR(100), url VARCHAR(100));')
        init_cursor.close()

    def register_chat_if_is_not_registered(self, chat_id: int) -> None:
        cursor = self.connection.cursor()
        res = cursor.execute(f'SELECT * FROM chat WHERE chat_id={chat_id}')

        if len(res.fetchall()) == 0: 
            logging.info(f'Chat {chat_id} has been registered')
            cursor.execute(f'INSERT INTO chat VALUES ({chat_id});')
            self.connection.commit()

        cursor.close() 

    def check_news_entry(self, url: str) -> bool:
        cursor = self.connection.cursor()
        entries = cursor.execute(f"SELECT * FROM news WHERE url='{url}'").fetchall()
        cursor.close()

        return len(entries) != 0 # return True if entry already exists
    
    def insert_news_entry(self, title: str, url: str) -> None:
        logging.info(f'Inserting entry with title "{title}"')
        cursor = self.connection.cursor()
        cursor.execute(f"INSERT INTO news VALUES ('{title}', '{url}')")
        cursor.close()
        self.connection.commit()