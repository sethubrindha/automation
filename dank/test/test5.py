import re
import instaloader
import os
import random
import requests
import time
from bs4 import BeautifulSoup
from moviepy.editor import VideoFileClip,concatenate_videoclips
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from upload_youtube import uploadYtvid
from utils import timer
from user_agent import generate_user_agent
from constants import *

L = instaloader.Instaloader()
# L.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)


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
    downloads = os.path.join(os.getcwd(), 'videos')
    prefs = {'download.default_directory': downloads}
    chrome_options.add_experimental_option('prefs', prefs)
    # chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (recommended)
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model (Linux specific)
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    
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
    # chrome_options.add_argument("--incognito")
    
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

def download_videos(reel_links, total_duration=0):
    video_files = []
    for post in reel_links:

        # # Extract the shortcode from the URL
        # shortcode = link.split('/')[-2]
        print("post >>>>>>",post)

        # Download the reel
        # post = instaloader.Post.from_shortcode(L.context, link)
        L.download_post(post, target='downloads')
        print("downloaded >>>>>>>")

        for filename in os.listdir(os.path.join(os.getcwd(), 'downloads')):
            if filename.startswith(post.date_utc.strftime('%Y-%m-%d')) and filename.endswith('.mp4'):
                # Construct the full path to the downloaded file
                video_file = os.path.join(os.getcwd(), 'downloads', filename)
                break
        print("video_file >>>>>>>>>>",video_file)
 
        if wait_for_download(video_file):
            video_clip = VideoFileClip(video_file)
            video_files.append(video_clip)
            if video_clip.duration <= 60:
                total_duration += video_clip.duration
            if total_duration >= 600:
                break
        else:
            print(f"Error: Download for {video_file} timed out.")

    return video_files, total_duration


# def concatenate_videoclips(driver, video_files=[]):
#     driver.get("https://videobolt.net/simple-video-tools/merge")
#     timer(20)
#     try:
#         cookies_button = '/html/body/div[3]/div[2]/div'
#         ignore_button = '/html/body/div[1]/div[3]/button'
#         driver.find_element(By.XPATH, cookies_button).click()
#         driver.find_element(By.XPATH, ignore_button).click()
#     except: ...
#     timer()
#     print("ignore button clicked >>>>>.")
    
#     driver.find_element(By.XPATH, '//input[@type="file"]').send_keys(video_files[0])
#     print("first file uploaded >>>>>")
#     timer()
#     timer(30)
#     for i in range(1,len(video_files)):
#         driver.find_element(By.XPATH, '//input[@type="file"]').send_keys(video_files[i])
#         timer(20)
#     timer(20)
#     upload_done = False
#     while not upload_done:
#         try:
#             blur_button = "//div[contains(text(), 'Blurred')]"
#             driver.find_element(By.XPATH, blur_button).click() #bg blur button
#             timer()
#             download_button = "//div[contains(text(), 'Merge & Download')]"
#             driver.find_element(By.XPATH, download_button).click() #download button
#             upload_done = True
#         except Exception as e:
#             print("eror >>>>>",e.args)


def get_download_videos(total_duration=0):
    video_files = []

    for filename in os.listdir(os.path.join(os.getcwd(), 'downloads')):
        if filename.endswith('.mp4'):
            # Construct the full path to the downloaded file
            video_file = os.path.join(os.getcwd(), 'downloads', filename)
            print("video_file >>>>>>>>>>",video_file)

            if wait_for_download(video_file):
                video_clip = VideoFileClip(video_file)
                video_files.append(video_clip)
                total_duration += video_clip.duration
                if total_duration >= 300:
                 break

            else:
                print(f"Error: Download for {video_file} timed out.")


    return video_files, total_duration

def clear_folder(folder_path):
    for filename in os.listdir(folder_path): 
        print('filename >>>>', filename)
        file_path = os.path.join(folder_path, filename)

    # Check if it's a file or directory
        if os.path.isfile(file_path):
            print('file_path >>>>', file_path)
            os.remove(file_path)
            print(f'Removed file: {file_path}')
        elif os.path.isdir(file_path):
            print(f'{file_path} is a directory, skipping...')


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

def main():
    pages = '''
            '''
    timer()

    video_files = []
    reel_list = []
    total_duration = 0
    selected_pages = select_url()
    print("selected_pages >>>>>\n", selected_pages)
    final_description = DESCRIPTION_1+pages+DESCRIPTION_2
    timer()


    # for page_url in selected_pages:
    #     try:
    #         profile_name = page_url[26:-7]
    #         print('profile_name >>>>>>',profile_name)
    #         profile = instaloader.Profile.from_username(L.context, profile_name)
    #         # Get all reels (posts of type 'igtv' or 'video')
    #         reel_list += [post for post in profile.get_posts() if post.typename in ['GraphVideo', 'GraphSidecar']]
    #         pages += f'\n@{profile_name} '
    #         timer(random.randint(30, 60))
    #     except: ...
    # print('reel_list >>>>>',reel_list)

    # final_description = DESCRIPTION_1+pages+DESCRIPTION_2

    # while total_duration < 600 or total_duration > 900:
    #     print("inside while >>>>")
    #     selected_videos = random.sample(reel_list, min(len(reel_list), 2))
    #     print("selected_videos >>>>>>>>",selected_videos)
    #     video_file, total_duration = download_videos(selected_videos, total_duration)
    #     video_files.extend(video_file)
    #     print("total_duration :",total_duration)
    #     # if total_duration > 600 or total_duration < 900: break


    video_files_path, duration = get_download_videos()
    print("video_files_path >>>>>",video_files_path)
    print('video_files')
    clip_0 = video_files_path.pop(0)
    print('clip_0 >>>',clip_0)
    clip_1 = video_files_path.pop(1)
    print('clip_1 >>>',clip_1)
    final_clip = concatenate_videoclips([clip_0, clip_1])
    print("Final video generated successfully!")
    # Save the final video
    final_clip.write_videofile("videos/final_video.mp4", codec="libx264", fps=24)


    # driver = start_chrome()
    # concatenate_videoclips(driver, video_files_path)
    print("video downloaded >>>>>")
    final_video_file = None
    while not final_video_file:
        for filename in os.listdir(os.path.join(os.getcwd(), 'videos')):
            if filename.endswith('.mp4'):
                final_video_file = os.path.join(os.getcwd(), 'videos', filename)
                break

    print("final_video_file >>>>>>",final_video_file)
    # Upload to YouTube (YouTube API integration code needed here)

    # # Collect tags
    # tags_list = collect_tags_from_files('downloads')

    # # Print the collected tags
    # print(tags_list)
    # uploadYtvid(
    #     VIDEO_FILE_NAME=final_video_file, 
    #     title="Tamil Dank Memes: Prepare for Uncontrollable Laughter!", 
    #     description=final_description,
    #     tags=tags_list
    #     )
    # print("uplod done")


    # driver.quit()
    # timer(60)
    # # remove all the files
    # downloads_path = os.path.join(os.getcwd(), 'downloads')
    # videos_path = os.path.join(os.getcwd(), 'videos')

    # done = False
    # while not done:
    #     try:
    #         clear_folder(downloads_path)
    #         print("downloads cleared ")
    #         clear_folder(videos_path)
    #         print("videos cleared ")
    #         done = True
    #     except: ...

    print("Done!")


if __name__ == "__main__":
    main()
