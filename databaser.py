
import sqlite3
import random


class Databaser:

    def __init__(self, db_name='database.db'):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row

        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS videos (
                                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                desc TEXT,
                                likes INT,
                                author_name TEXT)''')

    def add_video(self, desc, author_name, video_id=None):
        with self.connection:
            cursor = self.connection.cursor()

            if video_id is None:
                cursor.execute('''INSERT INTO videos (desc, likes, author_name) 
                VALUES (?, 0, ?)''', (desc, author_name))

            else:
                cursor.execute('''INSERT OR REPLACE INTO videos (id, desc, likes, author_name)
                VALUES (?, ?, 0, ?)
                ''', (video_id, desc, author_name))
            
            self.connection.commit()

    def get_last_video_id(self):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id FROM videos ORDER BY id DESC LIMIT 1")
            result = cursor.fetchone()
            return result[0] if result else 0

    def get_video(self, video_id):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM videos WHERE id = ?', (video_id,))
            r = cursor.fetchone()

            if not r:
                return

            return dict(r)

    def change_video(self, video_id, desc=None, author_name=None):
        with self.connection:
            cursor = self.connection.cursor()
        
            old = self.get_video(video_id)

            if desc is None:
                desc = old['desc']
            if author_name is None:
                author_name = old['author_name']

            cursor.execute('UPDATE videos SET desc = ?, author_name = ? WHERE id = ?', (desc, author_name, video_id))
            self.connection.commit()

    def like_video(self, video_id):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('UPDATE videos SET likes = likes + 1 WHERE id = ?', (video_id,))

    def get_videos(self):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM videos ORDER BY likes')
            videos = cursor.fetchall()

            videos = list(map(dict, videos))

            return videos
    
    def get_random_video(self, history=None):
        with self.connection:
            if history is None:
                history = []

            cursor = self.connection.cursor()
            cursor.execute('SELECT Count(*) FROM videos')
            mx = cursor.fetchone()['Count(*)']

            rng = set(range(1, mx + 1)) - set(history)

            if not rng:
                return None

            print(rng, list(history))

            video_id = random.choice(list(rng))

            return self.get_video(video_id)


if __name__ == '__main__':
    db = Databaser()
    db.add_video('Тест', 'Sigma', 1)
    db.add_video('НЕ ПОВТОРЯЙТЕ ЭТО ДОЫВШГНМПДЙУЦ', 'Sigma', 2)