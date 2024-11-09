import random
from time import sleep
from selenium.webdriver.common.by import By
import re
import instaloader
import os
import random
import requests
import time
from bs4 import BeautifulSoup
from moviepy.editor import VideoFileClip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from constants import *
from user_agent import generate_user_agent
from yt_constants import * 
import platform

L = instaloader.Instaloader()
# L.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)

LANGUAGES = ['tamil', 'english', 'spanish', 'hindi', 'portuguese', 'arabic', 'japanese']

def msg(
        _message_,
        _option_=None
        ):
    if _option_ == 1:
        print('\x1b[0;32;40m> %s\x1b[0m' % _message_)
    elif _option_ == 2:
        print('\x1b[0;32;40m>\x1b[0m %s' % _message_)
    elif _option_ == 3:
        print('\n\x1b[0;32;40m[\x1b[0m%s\x1b[0;32;40m]\x1b[0m' % _message_)
    else:
        print('\n\x1b[0;31;40m[ERROR]\x1b[0m')

def timer(sec=None):
    if sec:
        sleep(sec)
    else:
        sleep(random.randint(1,4))


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
    chrome_options.add_argument("--headless")  # Enable headless mode
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
        print("chromedriver_path >>>>>>.",chromedriver_path)
        print('platform >>>>',platform.system())
        if platform.system() == "Windows":
            chromedriver_executable = os.path.join(os.path.dirname(chromedriver_path), 'chromedriver.exe')
        else:
            chromedriver_executable = os.path.join(os.path.dirname(chromedriver_path), 'chromedriver')
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

def extract_instagram_challenge_url(text):
    # Define a regular expression pattern to capture Instagram URLs with "challenge" in the path
    pattern = r'https:\/\/www\.instagram\.com\/challenge\/[^\s,\'"]+'
    
    # Search for the pattern in the provided text
    match = re.search(pattern, text)
    
    # Return the matched URL or None if not found
    return match.group(0) if match else None

def select_url(page_list:list):
	unique_urls = list(set(page_list))
	random.shuffle(unique_urls)
	selected_size = random.randint(10, 15)
	selected_urls = unique_urls[:selected_size]
	return selected_urls

def login_instagram(driver):
    driver.get("https://www.instagram.com/accounts/login/")
    timer()
    driver.find_element(By.NAME, "username").send_keys(INSTAGRAM_USERNAME)
    print("username addded >>>.")
    timer()
    driver.find_element(By.NAME, "password").send_keys(INSTAGRAM_PASSWORD)
    print("password added >>>>")
    timer()
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    print("logged in >>>>.")
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
        video_file = None
        for filename in os.listdir(os.path.join(os.getcwd(), 'downloads')):
            if filename.startswith(post.date_utc.strftime('%Y-%m-%d')) and filename.endswith('.mp4'):
                print("filename >>>>>>",filename)
                # Construct the full path to the downloaded file
                video_file = os.path.join(os.getcwd(), 'downloads', filename)
                break
 
        if video_file:
            if wait_for_download(video_file):
                video_clip = VideoFileClip(video_file)
                video_files.append(video_clip)
                if video_clip.duration <= 60:
                    total_duration += video_clip.duration
                if total_duration >= 300:
                    break
        else:
            print(f"Error: Download for {video_file} timed out.")

    return video_files, total_duration

def concatenate_videoclips(driver, video_files_list=[]):
    video_files = random.sample(video_files_list, len(video_files_list))
    driver.get("https://videobolt.net/simple-video-tools/merge")
    timer(20)
    try:
        cookies_button = '/html/body/div[3]/div[2]/div'
        ignore_button = '/html/body/div[1]/div[3]/button'
        driver.find_element(By.XPATH, cookies_button).click()
        driver.find_element(By.XPATH, ignore_button).click()
    except: ...
    timer()
    print("ignore button clicked >>>>>.")
    
    disclimer = video_file = os.path.join(os.getcwd(), 'templates', 'disclimer.mp4')
    driver.find_element(By.XPATH, '//input[@type="file"]').send_keys(disclimer)
    print("first file uploaded >>>>>")
    timer()
    timer(30)
    for i in range(0,len(video_files)):
        driver.find_element(By.XPATH, '//input[@type="file"]').send_keys(video_files[i])
        timer(20)
    timer(20)
    upload_done = False
    while not upload_done:
        try:
            blur_button = "//div[contains(text(), 'Blurred')]"
            driver.find_element(By.XPATH, blur_button).click() #bg blur button
            timer()
            download_button = "//div[contains(text(), 'Merge & Download')]"
            driver.find_element(By.XPATH, download_button).click() #download button
            upload_done = True
        except Exception as e:
            print("eror >>>>>",e.args)
    timer(150)

def get_download_videos(total_duration=0):
    video_files = []

    for filename in os.listdir(os.path.join(os.getcwd(), 'downloads')):
        if filename.endswith('.mp4'):
            # Construct the full path to the downloaded file
            video_file = os.path.join(os.getcwd(), 'downloads', filename)
            print("video_file >>>>>>>>>>",video_file)

            if wait_for_download(video_file):
                video_clip = VideoFileClip(video_file)
                video_files.append(video_file)
                if video_clip.duration <= 60:
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
                found_tags = [tag[1:] for tag in re.findall(r'#\w+', content)]
                print(" >>>>>>>>>>>>>", found_tags)
                tags.extend(found_tags)
    return tags


def get_video_details(language:str | None=LANGUAGES[0]) -> dict:
        """Returns a dictionary with title and description and tag for the video"""
        if language == LANGUAGES[0]:
            return DESCRIPTION_1, DESCRIPTION_2, TAMIL_TITLE, TAMIL_TAG_LIST, TAMIL_LIST_OF_PAGES
