import sqlite3

class GreetingsDatabase:
    def __init__(self, db_path: str = 'little_friend_db.db'):
        self.db_path = db_path
        connection = self._get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS greeting_data 
                    (guild_id TEXT PRIMARY KEY, welcome_channel_id TEXT, welcome_message TEXT)
                    """)

        connection.commit()
        connection.close()
        print("Greetings Database Initialized!")

    def _get_db_connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        return connection

    def set_guild_welcome_channel(self, guild_id: int, welcome_channel_id: int):
        connection = self._get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
                INSERT OR IGNORE INTO greeting_data(guild_id) 
                VALUES (?)""", (str(guild_id),)
                )

        cursor.execute("""
                UPDATE greeting_data 
                SET welcome_channel_id = ? 
                WHERE guild_id = ?""", (str(welcome_channel_id), str(guild_id)))

        connection.commit()
        connection.close()

    def get_guild_welcome_channel(self, guild_id: int) -> int | None:
        connection = self._get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
                SELECT welcome_channel_id FROM greeting_data 
                WHERE guild_id = ?""", (str(guild_id),))

        result = cursor.fetchone()
        connection.close()

        return int(result[0]) if result else None

    def set_guild_welcome_message(self, guild_id: int, welcome_message: str) -> None:
        connection = self._get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
                INSERT OR IGNORE INTO greeting_data(guild_id) 
                VALUES (?)""", (str(guild_id),)
               )

        cursor.execute("""
                UPDATE greeting_data 
                SET welcome_message = ? 
                WHERE guild_id = ?""", (welcome_message, str(guild_id)))

        connection.commit()
        connection.close()

    def get_guild_welcome_message(self, guild_id: int) -> str | None:
        connection = self._get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
                SELECT welcome_message FROM greeting_data 
                WHERE guild_id = ?""", (str(guild_id),))

        result = cursor.fetchone()
        connection.close()

        return result[0] if result else None

    def remove_guild_data(self, guild_id: int) -> None:
        connection = self._get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
                DELETE FROM greeting_data 
                WHERE guild_id = ?""", (str(guild_id),))

        connection.commit()
        connection.close()