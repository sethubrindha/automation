import os
import time
import random
import urllib3
import requests
from instagrapi import Client, exceptions

class InstaScraper:
    def __init__(self, username, password, directory):
        self.client = Client()
        self.username = username
        self.password = password
        self.directory = directory
        self.session_file = f"{username}_session.json"
        self.client.delay_range = [5, 15]
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

    def scrape(self, profile):
        """Fetch reels from a given profile."""
        print(f"🔍 Searching for {profile}...")
        time.sleep(random.uniform(2, 5))  # Human-like delay

        try:
            self.user_id = self.client.user_id_from_username(profile)
            print(f"✅ Found user ID: {self.user_id}")
            self.browse_profile()
            self.download_reels()
        except exceptions.UserNotFound:
            print("❌ User not found.")
            self.user_id = None
        except requests.exceptions.RetryError as e:
            print("⚠️ Too many requests! Retrying with backoff...")
            self.handle_rate_limit(profile)

        except urllib3.exceptions.MaxRetryError:
            print("🔄 Max retries exceeded. Restarting session...")
            self.reset_session()
            self.scrape(profile)  # Retry after resetting session
        except exceptions.LoginRequired:
            pass

    def browse_profile(self):
        """Simulate human-like browsing before downloading reels."""
        print("👀 Viewing profile page...")
        time.sleep(random.uniform(4, 8))  # Simulating a human checking the profile
        self.client.user_info(self.user_id)  # Fetch user details

    def ensure_directory_exists(self):
        """Ensure the target directory exists."""
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def download_reels(self):
        """Download reels only if they have high engagement."""
        if self.user_id:
            print("📥 Fetching recent reels...")
            reels = self.client.user_clips(self.user_id, 5)  # Fetch latest 5 reels
            self.ensure_directory_exists()
            time.sleep(random.uniform(2, 4))  # Simulate API call delay

            for reel in reels:
                print(f"🎥 Reel has {reel.like_count} likes.")
                
                if reel.like_count > 1500:
                    print("💾 High-engagement reel detected, downloading...")
                    try:
                        time.sleep(random.uniform(5, 10))  # Simulate a real user delay
                        media_path = self.client.video_download(reel.id, self.directory)
                        print(f"✅ Downloaded: {media_path}")
                    except Exception as e:
                        print(f"⚠️ Failed to download reel: {e}")

    def logout(self):
        """Logout safely to avoid detection."""
        print("🔒 Logging out...")
        time.sleep(random.uniform(3, 6))  # Human-like logout delay
        self.client.logout()
        print("✅ Logged out successfully.")

    def handle_rate_limit(self, profile):
        """Handles 429 rate limit by adding exponential backoff."""
        delay = random.randint(10, 30)  # Start with a 10-30 sec delay
        for attempt in range(1, 6):  # Retry up to 5 times
            print(f"⏳ Waiting {delay} seconds before retrying...")
            time.sleep(delay)
            try:
                self.scrape(profile)  # Retry scraping
                return  # If successful, exit loop
            except requests.exceptions.RetryError:
                delay *= 2  # Double the wait time for next attempt
        
        print("❌ Giving up after too many retries.")

    def reset_session(self):
        """Deletes the session file and logs in again."""
        if os.path.exists(self.session_file):
            os.remove(self.session_file)
        self.login()
