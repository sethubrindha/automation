from instabot import Bot
import os
from constants import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD

def upload_reel(video_path='', caption=''):
    # Initialize bot and login
    bot = Bot()
    bot.login(username=INSTAGRAM_USERNAME, password=INSTAGRAM_PASSWORD)

    # Upload the video as a reel
    bot.upload_video(video_path, caption=caption)

    # Logout
    bot.logout()
