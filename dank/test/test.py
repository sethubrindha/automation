
# # from utils import timer
# # # ******** Undetected chrome***********#
# # # from undetected_chromedriver import Chrome, ChromeOptions
# # # print("inside chrome >>>>>>>")

# # # options = ChromeOptions()
# # # # options.add_argument("--headless")
# # # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
# # # options.add_argument("--blink-settings=imagesEnabled=false")


# # # with Chrome(options=options) as driver:
# # #     driver.get("https://whatismyipaddress.com/")
# # #     # Perform your automated actions here

# # # ******** generate useragent***********#
# # from user_agent import generate_user_agent, generate_navigator
# # import requests
# # from bs4 import BeautifulSoup



# # #***********change ip***********#
# # # import requests
# # # from bs4 import BeautifulSoup
# # import random


# # def get_proxies():
# #     url = 'https://free-proxy-list.net/'
# #     response = requests.get(url)
# #     if response.status_code != 200:
# #         raise Exception(f"Failed to retrieve proxies. Status code: {response.status_code}")

# #     soup = BeautifulSoup(response.text, 'html.parser')
# #     proxies_table = soup.find('table')
    
# #     if proxies_table is None:
# #         raise Exception("Failed to find the proxy list table on the page.")
    
# #     proxies = []
# #     for row in proxies_table.tbody.find_all('tr'):
# #         ip = row.find_all('td')[0].text
# #         port = row.find_all('td')[1].text
# #         proxy = f"{ip}:{port}"
# #         proxies.append(proxy)
    
# #     return proxies




# # # import google.auth
# # # from googleapiclient.discovery import build

# # # # Load credentials from the JSON file you downloaded
# # # credentials, project = google.auth.default()

# # # # Create a Gmail API service
# # # service = build('gmail', 'v1', credentials=credentials)

# # # # Define the account information
# # # account_info = {
# # #     'emailAddress': 'newuser@example.com',
# # #     'password': 'securepassword123'
# # # }

# # # # Use the Gmail API to create the account
# # # created_account = service.users().create(body=account_info).execute()

# # # print(f'Account created: {created_account}')
# # from selenium.common.exceptions import NoSuchElementException
# # from selenium.webdriver.common.by import By
# # from webdriver_manager.chrome import ChromeDriverManager
# # from selenium import webdriver
# # from moviepy.editor import VideoFileClip, concatenate_videoclips
# # from selenium.webdriver.chrome.service import Service
# # from upload_youtube import uploadYtvid
# # import os
# # import time
# # import random
# # import instaloader

# # # Instagram credentials
# # INSTAGRAM_USERNAME = 'sethu.emedhub@gmail.com'
# # INSTAGRAM_PASSWORD = 'sethupathi@123'
# # L = instaloader.Instaloader()
# # LIST_OF_PAGES = [
# #     'https://www.instagram.com/uchiha_veeran/reels/',
# #     'https://www.instagram.com/the_veeraraghavan._.supremacy_/reels/',
# #     'https://www.instagram.com/dankkagee/reels/',
# #     'https://www.instagram.com/tele_telepathy/reels/',
# #     'https://www.instagram.com/vana.cumm/reels/',
# #     'https://www.instagram.com/abdul_la_s/reels/',
# #     'https://www.instagram.com/vaazhai_pazham/reels/',
# #     'https://www.instagram.com/mokkapagesir/reels/'
# # ]
# # L.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)


# # reel_url = 'https://www.instagram.com/reel/C8BvfMdRRcI/'


# # # def start_chrome():
# # #     chrome_options = webdriver.ChromeOptions()
# # #     downloads = os.path.join(os.getcwd(), 'downloads')
# # #     prefs = {'download.default_directory': downloads}
# # #     chrome_options.add_experimental_option('prefs', prefs)
# # #     chrome_options.add_experimental_option("detach", True)
# # #     service = Service(ChromeDriverManager().install())
# # #     driver = webdriver.Chrome(service=service, options=chrome_options)
# # #     return driver
# # from selenium import webdriver
# # from selenium.webdriver.chrome.service import Service
# # from webdriver_manager.chrome import ChromeDriverManager
# # import os

# # def start_chrome():
# #     chrome_options = webdriver.ChromeOptions()
    
# #     # Set download directory
# #     downloads = os.path.join(os.getcwd(), 'downloads')
# #     prefs = {'download.default_directory': downloads}
# #     chrome_options.add_experimental_option('prefs', prefs)
    
# #     # Detach browser so it doesn't close when the script ends
# #     chrome_options.add_experimental_option("detach", True)
    
# #     # Set user agent
# #     user_agent = generate_user_agent()
# #     chrome_options.add_argument(f'user-agent={user_agent}')
    
# #     # Set proxy (change IP)
# #     # proxy = "http://your_proxy_ip:your_proxy_port"
# #     # Get list of proxies
# #     # proxies = get_proxies()

# #     # # Select a random proxy from the list
# #     # proxy = random.choice(proxies)
# #     # chrome_options.add_argument(f'--proxy-server={proxy}')
    
# #     # Open in incognito mode
# #     chrome_options.add_argument("--incognito")
    
# #     # Initialize Chrome WebDriver
# #     service = Service(ChromeDriverManager().install())
# #     driver = webdriver.Chrome(service=service, options=chrome_options)
    
# #     return driver


# # def login_instagram(driver):
# #     driver.get("https://www.instagram.com/accounts/login/")
# #     timer() #eep(2)
# #     driver.find_element(By.NAME, "username").send_keys(INSTAGRAM_USERNAME)
# #     timer()
# #     driver.find_element(By.NAME, "password").send_keys(INSTAGRAM_PASSWORD)
# #     timer()
# #     driver.find_element(By.XPATH, "//button[@type='submit']").click()
# #     timer() #eep(5)

# # def get_top_videos(driver, page_url, top_n=5):
# #     driver.get(page_url)
# #     timer() #eep(3)
# #     reels = driver.find_elements(By.XPATH, "//a[contains(@href, '/reel/')]")
# #     reel_links = [reel.get_attribute("href") for reel in reels[:top_n]]
# #     return reel_links

# # def wait_for_download(file_path, timeout=90):
# #     start_time = time.time()
# #     print("file_path >>>>>>>>.",file_path)
# #     while time.time() - start_time < timeout:
# #         if os.path.exists(file_path):
# #             return True
# #         timer() #eep(1)
# #     return False

# # def download_videos(reel_links, total_duration=0):
# #     video_files = []
# #     for link in reel_links:

# #         # Extract the shortcode from the URL
# #         shortcode = link.split('/')[-2]
# #         print("short_code >>>>>>",shortcode)

# #         # Download the reel
# #         post = instaloader.Post.from_shortcode(L.context, shortcode)
# #         L.download_post(post, target='downloads')
# #         print("downloaded >>>>>>>")

# #         for filename in os.listdir(os.path.join(os.getcwd(), 'downloads')):
# #             if filename.startswith(post.date_utc.strftime('%Y-%m-%d')) and filename.endswith('.mp4'):
# #                 # Construct the full path to the downloaded file
# #                 video_file = os.path.join(os.getcwd(), 'downloads', filename)
# #                 break
# #         print("video_file >>>>>>>>>>",video_file)

# #         if wait_for_download(video_file):
# #             video_clip = VideoFileClip(video_file)
# #             video_files.append(video_clip)
# #             total_duration += video_clip.duration
# #             if total_duration >= 600:
# #                 break
# #         else:
# #             print(f"Error: Download for {video_file} timed out.")


# #     return video_files, total_duration


# # def main():
# #     driver = start_chrome()
# #     timer()
# #     # login_instagram(driver)
# #     # timer()

# #     video_files = []
# #     total_duration = 0

# #     while total_duration < 600 or total_duration > 900:
# #         selected_page = random.choice(LIST_OF_PAGES)
# #         timer()
# #         reel_links = get_top_videos(driver, selected_page)
        
# #         selected_videos = random.sample(reel_links, min(len(reel_links), 2))
# #         video_files, total_duration = download_videos(selected_videos, total_duration)
# #         print("total_duration >>>>>>>>.",total_duration)

# #     final_clip = concatenate_videoclips(video_files)
# #     final_clip.write_videofile("videos/final_video.mp4")
# #     final_video_file = os.path.join(os.getcwd(), 'videos', "final_video.mp4")

# #     # Upload to YouTube (YouTube API integration code needed here)
# #     uploadYtvid(VIDEO_FILE_NAME=final_video_file, title='test', description='test')

# #     driver.quit()

# # if __name__ == "__main__":
# #     main()


# import os
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

# def start_chrome():
#     print("inside start crome >>>>>")
#     chrome_options = webdriver.ChromeOptions()
#     print("chrome_options >>>",chrome_options)
#     chromedriver_path = ChromeDriverManager().install()
#     print(f"Using ChromeDriver at: {chromedriver_path}")
#     service = Service(chromedriver_path)
#     driver = webdriver.Chrome(service=service, options=chrome_options)
#     return driver

# def main():
#     print("Starting ChromeDriver...")
#     driver = start_chrome()
#     print("ChromeDriver started successfully.")
#     # Your code here
#     driver.quit()

# if __name__ == "__main__":
#     main()

import os
import re

def collect_tags_from_files(folder_path):
    tags = []
    # Loop through all files in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            # Construct full file path
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                # Find all words starting with #
                tags.extend(re.findall(r'#\w+', content))
    return tags

# Specify the folder containing the .txt files
folder_path = 'downloads'

# Collect tags
tags_list = collect_tags_from_files(folder_path)

# Print the collected tags
print(tags_list)
