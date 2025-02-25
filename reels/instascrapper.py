import os
import random
import time
from instagrapi import Client, exceptions

class InstaScrapper:
    def __init__(self, username, password, directory, page):
        self.client = Client()
        self.directory = directory
        self.page = page
        self.username = username
        self.password = password
        self.client.delay_range = [15, 60]
        self.session_file = f"{username}_session.json"
        self.login()


    def login(self):
        if os.path.exists(self.session_file):
            self.client.load_settings(self.session_file)
            print("✅ Loaded previous session.")
        else:
            print("🔑 Logging into Instagram...")
            time.sleep(random.uniform(3, 6))  # Simulate human delay
            self.client.login(self.username, self.password)
            self.client.dump_settings(self.session_file)
            print("✅ Successfully logged in!")

    def Ingester(self):
        """Main function to download and upload reels."""
        try:
            self.user_id = self.client.user_id_from_username(self.page)
        except exceptions.UserNotFound:
            self.user_id = None
            print("❌ User not found!")
            return
        
        self.download_reels()
        
        # Random sleep to evade detection
        sleep_time = random.randint(10, 60)
        print(f"⏳ Sleeping for {sleep_time} seconds before upload...")
        time.sleep(sleep_time)

        self.upload_reels()
        
        # Longer sleep to prevent frequent activity
        sleep_time = random.randint(240, 360)
        print(f"⏳ Sleeping for {sleep_time} seconds before clearing files...")
        time.sleep(sleep_time)

        self.clear_files()

    def ensure_directory_exists(self):
        """Ensure the directory exists, create if not."""
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def download_reels(self):
        """Download recent reels from the target user."""
        if self.user_id:
            reels = self.client.user_clips(self.user_id, 25)
            if reels:
                random_clip = random.choice(reels)  # Randomly choose a reel
                self.ensure_directory_exists()
                print("🎥 Downloading reel:", random_clip.id)
                self.caption = random_clip.caption_text or "🔥 Amazing video!"
                self.media_path = self.client.video_download(random_clip.id, self.directory)
                print(f"✅ Downloaded reel: {self.media_path}")
            else:
                print("⚠️ No reels found!")

    def upload_reels(self):
        """Upload the downloaded reel."""
        if hasattr(self, 'media_path') and os.path.exists(self.media_path):
            # Random delay before upload
            sleep_time = random.randint(30, 90)
            print(f"⏳ Sleeping {sleep_time}s before uploading...")
            time.sleep(sleep_time)

            print("🚀 Uploading reel...")
            self.client.clip_upload(self.media_path, caption=self.caption)
            print("✅ Upload successful!")
        else:
            print("❌ No media found to upload.")

    def logout(self):
        """Logout safely to avoid detection."""
        self.client.logout()
        print("🔒 Logged out successfully!")

    def clear_files(self):
        """Delete downloaded reels to free up space."""
        if hasattr(self, 'media_path') and os.path.exists(self.media_path):
            os.remove(self.media_path)
            print(f"🗑️ File '{self.media_path}' deleted.")
        else:
            print("⚠️ No file found to delete.")

