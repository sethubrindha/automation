# import os
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

# def start_chrome():
#     print("inside start chrome >>>>>")
#     chrome_options = webdriver.ChromeOptions()
#     print("chrome_options >>>", chrome_options)
#     try:
#         chromedriver_path = ChromeDriverManager().install()
#         chromedriver_executable = os.path.join(os.path.dirname(chromedriver_path), 'chromedriver.exe')
#         print(f"Using ChromeDriver executable at: {chromedriver_executable}")
#         service = Service(chromedriver_executable)
#         driver = webdriver.Chrome(service=service, options=chrome_options)
#         return driver
#     except Exception as e:
#         print(f"Error starting ChromeDriver: {e}")
#         raise

# def main():
#     print("Starting ChromeDriver...")
#     try:
#         driver = start_chrome()
#         print("ChromeDriver started successfully.")
#         # Your code here
#         driver.quit()
#     except Exception as e:
#         print(f"Error in main: {e}")

# if __name__ == "__main__":
#     main()









import instaloader
import os
import random
import requests
import time
from bs4 import BeautifulSoup
from moviepy.editor import VideoFileClip, concatenate_videoclips
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from upload_youtube import uploadYtvid
from utils import timer
from user_agent import generate_user_agent
from constants import *

L = instaloader.Instaloader()
L.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve proxies. Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    proxies_table = soup.find('table')
    
    if proxies_table is None:
        raise Exception("Failed to find the proxy list table on the page.")
    
    proxies = []
    for row in proxies_table.tbody.find_all('tr'):
        ip = row.find_all('td')[0].text
        port = row.find_all('td')[1].text
        proxy = f"{ip}:{port}"
        proxies.append(proxy)
    
    return proxies


def start_chrome():
    chrome_options = webdriver.ChromeOptions()
    
    # Set download directory
    downloads = os.path.join(os.getcwd(), 'downloads')
    prefs = {'download.default_directory': downloads}
    chrome_options.add_experimental_option('prefs', prefs)
    
    # Detach browser so it doesn't close when the script ends
    chrome_options.add_experimental_option("detach", True)
    
    # Set user agent
    user_agent = generate_user_agent()
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    # Set proxy (change IP)
    # proxy = "http://your_proxy_ip:your_proxy_port"
    # Get list of proxies
    # proxies = get_proxies()

    # # Select a random proxy from the list
    # proxy = random.choice(proxies)
    # chrome_options.add_argument(f'--proxy-server={proxy}')
    
    # Open in incognito mode
    chrome_options.add_argument("--incognito")
    
    # Initialize Chrome WebDriver
    try:
        chromedriver_path = ChromeDriverManager().install()
        chromedriver_executable = os.path.join(os.path.dirname(chromedriver_path), 'chromedriver.exe')
        print(f"Using ChromeDriver executable at: {chromedriver_executable}")
        service = Service(chromedriver_executable)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://www.google.com/")
        return driver
    except Exception as e:
        print(f"Error starting ChromeDriver: {e}")
        raise
    # service = Service(ChromeDriverManager().install())
    # driver = webdriver.Chrome(service=service, options=chrome_options)
    # driver.get("https://www.google.com/")
    # return driver

def select_url():
	unique_urls = list(set(LIST_OF_PAGES))
	random.shuffle(unique_urls)
	selected_size = random.randint(10, 15)
	selected_urls = unique_urls[:selected_size]
	return selected_urls



def login_instagram(driver):
    driver.get("https://www.instagram.com/accounts/login/")
    timer()
    driver.find_element(By.NAME, "username").send_keys(INSTAGRAM_USERNAME)
    timer()
    driver.find_element(By.NAME, "password").send_keys(INSTAGRAM_PASSWORD)
    timer()
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    timer()

def get_top_videos(driver, top_n=4):
    # driver.get(page_url)
    timer()
    driver.switch_to.window(driver.window_handles[-1])
    timer()
    try:
        reels = driver.find_elements(By.XPATH, "//a[contains(@href, '/reel/')]")
        reel_links = [reel.get_attribute("href") for reel in reels[:top_n]]
    except:
        get_top_videos(driver, top_n=4)
    return reel_links

def wait_for_download(file_path, timeout=90):
    start_time = time.time()
    print("file_path >>>>>>>>.",file_path)
    while time.time() - start_time < timeout:
        if os.path.exists(file_path):
            return True
        timer()
    return False

def download_videos(total_duration=0):
    video_files = []

    for filename in os.listdir(os.path.join(os.getcwd(), 'downloads')):
        if filename.endswith('.mp4'):
            # Construct the full path to the downloaded file
            video_file = os.path.join(os.getcwd(), 'downloads', filename)
            print("video_file >>>>>>>>>>",video_file)

            if wait_for_download(video_file):
                video_clip = VideoFileClip(video_file)
                video_files.append(video_file)
                total_duration += video_clip.duration
                if total_duration >= 300:
                 break

            else:
                print(f"Error: Download for {video_file} timed out.")


    return video_files, total_duration


def main():

    video_files = []
    total_duration = 0

    while total_duration < 300 or total_duration > 900:
        print("inside while >>>>")
        video_file, total_duration = download_videos(total_duration)
        video_files.extend(video_file)
        print("total_duration :",total_duration)
        # if total_duration > 600 or total_duration < 900: break

    print(video_files)
    # final_clip = concatenate_videoclips(video_files)
    # final_clip.write_videofile("videos/final_video.mp4")
    # final_video_file = os.path.join(os.getcwd(), 'videos', "final_video.mp4")
    # Load all video clips
    # clips = []
    # for video in video_files:
    #     clip = VideoFileClip(video)
    #     clips.append(clip)

    # # Concatenate all clips
    # final_clip = concatenate_videoclips(clips)

    # # Write the result to a file
    # final_clip.write_videofile("videos/output.mp4")

    # # Close all clips
    # for clip in clips:
    #     clip.close()

    # # Close the final clip
    # final_clip.close()
    import ffmpeg
    # Create a text file with the list of videos to concatenate
    list_file_path = 'video_list.txt'
    with open(list_file_path, 'w') as f:
        for video in video_files:
            f.write(f"file '{video}'\n")

    # Verify that the list file was created and contains correct paths
    if os.path.exists(list_file_path):
        print(f"List file '{list_file_path}' created successfully.")
    else:
        print(f"Error: List file '{list_file_path}' not found.")

    # Check the content of the list file
    with open(list_file_path, 'r') as f:
        print("Content of the list file:")
        print(f.read())

    # Use ffmpeg to concatenate the videos
    print("list_file_path >>>>>",list_file_path)
    try:
        ffmpeg.input(list_file_path, format='concat', safe=0).output('output.mp4', c='copy').run()
        print("Concatenation completed successfully.")
    except ffmpeg.Error as e:
        print(f"ffmpeg error: {e}")



if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("error >>>.",e.args)

