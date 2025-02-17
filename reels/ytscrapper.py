import os
from instagrapi import Client, exceptions
import random
import requests
import subprocess
from constants import CHANNEL_IDS
from pytube import YouTube
import yt_dlp


class YTScrapper:
        def __init__(self, download_path, apikeys):
             self.path = download_path
             self.apikeys = apikeys
             
        def scrape(self):
            video_data = self.get_random_short()
            if not video_data:
                exit()
            video_id, video_title = video_data
            print("video_id, video_title ", video_id, video_title)
            self.download_youtube_short(video_id)
            return video_title

        def get_random_short(self):
            url = f"https://www.googleapis.com/youtube/v3/search?key={self.apikeys}&channelId={random.choice(CHANNEL_IDS)}&part=snippet&type=video&videoDuration=short"
            response = requests.get(url)
            videos = response.json().get("items", [])

            if not videos:
                print("No shorts found for this channel.")
                return None

            random_video = random.choice(videos)
            video_id = random_video["id"]["videoId"]
            title = random_video["snippet"]["title"]
            return video_id, title

        def download_youtube_short(self, video_id):
            try:
                url = f'https://www.youtube.com/shorts/{video_id}'
                options = {
                    'format': 'best',
                    'outtmpl': self.path,
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                }
                with yt_dlp.YoutubeDL(options) as ydl:
                    ydl.download([url])
                print("Video downloaded successfully.")
            
            except Exception as e:
                print(f"Error: {e}")

        #     command = [
        #         "yt-dlp", "-f", "mp4", "-o", self.path, video_url
        #     ]
        #     subprocess.run(command, check=True)

        # Download video using requests



