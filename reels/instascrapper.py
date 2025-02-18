import os
import random
from time import sleep
from constants import PAGE_LIST
from instagrapi import Client, exceptions


class InstaScrapper:
    def __init__(self, username, password, directory, page):
        self.client = Client()
        self.directory = directory
        self.page = page
        self.client.login(username, password)
        print("✅ Logged in successfully!")

    def Ingester(self):
        try: self.user_id = self.client.user_id_from_username(self.page)
        except exceptions.UserNotFound: self.user_id=None
        self.download_reels()
        self.upload_reels()
        self.logout()
        sleep(300)
        self.clear_files()

    def ensure_directory_exists(self):
        """Ensure the directory exists, create if not."""
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def download_reels(self):
        """Download recent reels from the target user."""
        if self.user_id:
            reels = self.client.user_clips(self.user_id, 25)  
            if reels: random_clip = random.choice(reels)
            self.ensure_directory_exists()
            print("random_clip_id : ", random_clip.id)
            self.caption = random_clip.caption_text
            print("self.caption : ", self.caption)
            self.media_path = self.client.video_download(random_clip.id, self.directory)
            print(f"Downloaded reel: {self.media_path}")
            
    
    def upload_reels(self):
        self.client.clip_upload(self.media_path, caption=self.caption)

    def logout(self):
        self.client.logout()

    def clear_files(self):
        os.remove(self.media_path)
        print(f"File '{self.media_path}' has been deleted.")

