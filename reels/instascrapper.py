import os
import random
import time
from instagrapi import Client, exceptions
from fake_useragent import UserAgent
import random
import json

proxies_list = [
    "188.166.30.17:8888", "37.120.133.137:3128", "37.120.222.132:3128", "89.249.65.191:3128", "144.91.118.176:3128", "95.216.17.79:3888", "85.214.94.28:3128", "185.123.143.251:3128", "167.172.109.12:39452", "176.113.73.104:3128", "51.158.68.133:8811", "185.123.143.247:3128", "95.111.226.235:3128", 
    "176.113.73.99:3128", "206.189.130.107:8080", "79.110.52.252:3128", "13.229.107.106:80", "118.99.108.4:8080", "13.229.47.109:80", "169.57.157.148:80", "51.158.68.68:8811", "167.172.109.12:40825", "119.81.189.194:80", "119.81.189.194:8123", "3.24.178.81:80", "119.81.71.27:80", "119.81.71.27:8123", 
    "185.236.203.208:3128", "193.239.86.249:3128", "159.8.114.37:80", "185.123.101.174:3128", "222.129.38.21:57114", "185.236.202.205:3128", "193.56.255.179:3128", "35.180.188.216:80", "106.45.221.168:3256", "113.121.240.114:3256", "193.34.95.110:8080", "84.17.51.235:3128", "180.183.97.16:8080", 
    "193.239.86.247:3128", "185.189.112.157:3128", "121.206.205.75:4216", "103.114.53.2:8080", "139.180.140.254:1080", "84.17.51.241:3128", "84.17.51.240:3128", "185.189.112.133:3128", "81.12.119.171:8080", "37.120.140.158:3128", "159.89.113.155:8080", "104.248.146.99:3128", "185.236.202.170:3128", 
    "67.205.190.164:8080", "46.21.153.16:3128", "51.158.172.165:8811", "84.17.35.129:3128", "85.214.244.174:3128", "104.248.59.38:80", "12.156.45.155:3128", "161.202.226.194:8123", "167.172.109.12:41491", "167.172.109.12:39533", "115.221.242.131:9999", "125.87.82.86:3256", "159.8.114.37:8123", 
    "183.164.254.8:4216", "169.57.157.146:8123", "94.100.18.111:3128", "18.141.177.23:80", "193.56.255.181:3128", "116.242.89.230:3128", "188.166.252.135:8080", "103.28.121.58:3128", "103.28.121.58:80", "119.84.215.127:3256", "217.172.122.14:8080", "79.122.230.20:8080", "167.172.109.12:46249", 
    "176.113.73.102:3128", "88.99.10.252:1080", "167.172.109.12:37355", "193.239.86.248:3128", "113.195.224.222:9999", "112.98.218.73:57658", "15.207.196.77:3128", "223.113.89.138:1080", "36.7.252.165:3256", "113.100.209.184:3128", "185.38.111.1:8080"
]


class InstaScrapper:
    def __init__(self, username, password, directory, page):
        self.client = Client()
        self.directory = directory
        self.page = page
        self.username = username
        self.password = password
        self.client.delay_range = [15, 60]
        self.session_file = f"{username}_session.json"
        self.ua = UserAgent()
        self.randomize_user_agent()
        self.proxy_list = proxies_list
        self.randomize_proxy()

        self.login()

    def login(self):
        if os.path.exists(self.session_file):
            self.client.load_settings(self.session_file)
            print("✅ Loaded previous session.")

            # Check if the session is still valid
            print("user name :", self.username)
            try:
                self.client.user_info_by_username(self.username)
            except exceptions.LoginRequired:
                print("⚠️ Session expired. Re-logging in...")
                self.client.relogin()
                self.client.dump_settings(self.session_file)  # Save the new session
                print("✅ Successfully re-+++ in!")
            except exceptions.UserNotFound:
                print('user not found')
                if os.path.exists(self.session_file):
                    os.remove(self.session_file)  # Delete the old session file
                    print("🗑️ Old session deleted. Re-logging in...")

            else:
                print("✅ Session is still active.")
                return  # No need to log in again

        # If session doesn't exist or relogin failed, do a fresh login
        print("🔑 Logging into Instagram...")
        time.sleep(random.uniform(3, 6))  # Simulate human delay
        self.client.login(self.username, self.password)
        self.client.dump_settings(self.session_file)
        print("✅ Successfully logged in!")

    def randomize_user_agent(self):
        """Set a random user-agent for every login."""
        user_agent = self.get_user_agent_from_session(self.username)
        user_agent = user_agent if user_agent else self.ua.random
        self.client.private.headers["User-Agent"] = user_agent
        print(f"🛠️ Using User-Agent: {user_agent}")

    def randomize_proxy(self):
        """Randomly select a proxy from the provided list."""
        if self.proxy_list:
            proxy = random.choice(self.proxy_list)
            proxy_dicts = [{"http": f"http://{proxy}", "https": f"http://{proxy}"} for proxy in proxies_list]
            self.client.private.proxies.update(proxy_dicts)  
            print(f"🌍 Using Proxy: {proxy}")

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
            reels = self.client.user_clips(self.user_id, 10)
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

    def get_random_proxy(self):
        return random.choice(proxies_list)

    def get_user_agent_from_session(self):
        session_file = f"{self.username}_session.json"
        
        try:
            with open(session_file, "r", encoding="utf-8") as f:
                session_data = json.load(f)

            user_agent = session_data.get('user_agent')
            if user_agent:
                return user_agent
            else:
                print("⚠️ User-Agent not found in session file.")
                return None
        except FileNotFoundError:
            print("❌ Session file not found.")
        except json.JSONDecodeError:
            print("❌ Error reading session file. Invalid JSON.")

        return None
