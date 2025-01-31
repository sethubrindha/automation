import os
from instagrapi import Client, exceptions


class InstaScrapper:
    def __init__(self, username, password, directory):
        self.client = Client()
        self.directory = directory
        self.client.login(username, password)
        print("✅ Logged in successfully!")

    def scrape(self, profile):
        try:
            self.user_id = self.client.user_id_from_username(profile)
        except exceptions.UserNotFound: self.user_id=None
        self.download_reels()

    def ensure_directory_exists(self):
        """Ensure the directory exists, create if not."""
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def download_reels(self):
        """Download recent reels from the target user."""
        if self.user_id:
            reels = self.client.user_clips(self.user_id, 5) # Get 5 recent reels
            self.ensure_directory_exists()

            for reel in reels:
                print("reel likes", reel.like_count)
                if reel.like_count > 1500:
                    try:
                        media_path = self.client.video_download(reel.id, self.directory)
                        print(f"Downloaded reel: {media_path}")
                    except: ...

    def logout(self):
        self.client.logout()

