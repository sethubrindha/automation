import os
import sqlite3
from constants import * 


def create_db_file():
    # Ensure the folder exists
    os.makedirs(FOLDER_PATH, exist_ok=True)
    
    # Full path for the new database file
    db_path = os.path.join(FOLDER_PATH, DB_NAME)
    
    # Connect to the database (will create it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    
    # Create a cursor object to interact with the database
    cursor = conn.cursor()
    
    # Example: Create a table
    cursor.execute('''
        CREATE TABLE post (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_path VARCHAR(100),
            image_path VARCHAR(100),
            post_path VARCHAR(100),
            is_posted BOOLEAN DEFAULT FALSE
        );
    ''')
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
# create_db_file()
class PostManager:
    def filter(self, **kwargs):
        os.makedirs(FOLDER_PATH, exist_ok=True)
        db_path = os.path.join(FOLDER_PATH, DB_NAME)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        sql_query = "SELECT * FROM post WHERE "
        conditions = []
        values = []

        for field, value in kwargs.items():
            conditions.append(f"{field} = ?")
            values.append(value)

        sql_query += " AND ".join(conditions) + ";"

        cursor.execute(sql_query, values)
        results = cursor.fetchall()
        conn.close()

        # Convert results into Post instances
        posts = []
        for row in results:
            post = Post(video_path=row[1], image_path=row[2], post_path=row[3], is_posted=row[4], id=row[0])
            posts.append(post)

        return posts

class Post:
    objects = PostManager()  # Attach the manager to the Post class

    def __init__(self, video_path='', image_path='', post_path='', is_posted=False, id=None):
        self.video_path = video_path
        self.image_path = image_path
        self.post_path = post_path
        self.is_posted = is_posted
        self.id = id  # To track the record for saving/updating

    @classmethod
    def create(cls, video_path='', image_path='', post_path='', is_posted=False):
        instance = cls(video_path, image_path, post_path, is_posted)
        instance.save()
        return instance

    def save(self):
        os.makedirs(FOLDER_PATH, exist_ok=True)
        db_path = os.path.join(FOLDER_PATH, DB_NAME)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        if self.id:  # Update existing record
            sql_query = f'''
                        UPDATE post
                        SET video_path = ?,
                            image_path = ?,
                            post_path = ?,
                            is_posted = ?
                        WHERE id = ?;
                        '''
            cursor.execute(sql_query, (self.video_path, self.image_path, self.post_path, self.is_posted, self.id))
        else:  # Create new record
            sql_query = f'''
                        INSERT INTO post (video_path, image_path, post_path, is_posted)
                        VALUES (?, ?, ?, ?);
                        '''
            cursor.execute(sql_query, (self.video_path, self.image_path, self.post_path, self.is_posted))
            self.id = cursor.lastrowid  # Get the ID of the newly created record

        conn.commit()
        conn.close()

    class Meta:
        table_name = 'post'

