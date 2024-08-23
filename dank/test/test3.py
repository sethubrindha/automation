# import av
# import os
# import instaloader
# import os
# import random
# import requests
# import time
# from bs4 import BeautifulSoup
# from moviepy.editor import VideoFileClip, concatenate_videoclips
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from upload_youtube import uploadYtvid
# from utils import timer
# from user_agent import generate_user_agent
# from constants import *
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC


# # List of video file paths
# video_files = [
#     r'D:\sethu\automation\dank\downloads\2024-03-22_16-58-28_UTC.mp4',
#     r'D:\sethu\automation\dank\downloads\2024-04-04_16-25-38_UTC.mp4',
#     r'D:\sethu\automation\dank\downloads\2024-04-07_08-42-41_UTC.mp4',
#     r'D:\sethu\automation\dank\downloads\2024-04-23_10-32-20_UTC.mp4',
#     r'D:\sethu\automation\dank\downloads\2024-04-24_11-52-18_UTC.mp4',
#     r'D:\sethu\automation\dank\downloads\2024-05-06_10-33-09_UTC.mp4',
#     r'D:\sethu\automation\dank\downloads\2024-05-07_11-40-38_UTC.mp4',
#     r'D:\sethu\automation\dank\downloads\2024-05-08_02-05-49_UTC.mp4',
#     r'D:\sethu\automation\dank\downloads\2024-05-24_03-31-34_UTC.mp4',
#     r'D:\sethu\automation\dank\downloads\2024-05-31_16-26-16_UTC.mp4',
#     r'D:\sethu\automation\dank\downloads\2024-06-10_07-44-11_UTC.mp4',
#     r'D:\sethu\automation\dank\downloads\2024-06-23_02-58-52_UTC.mp4',
#     r'D:\sethu\automation\dank\downloads\2024-06-27_04-30-09_UTC.mp4'
# ]


# chrome_options = webdriver.ChromeOptions()

# # Set download directory
# downloads = os.path.join(os.getcwd(), 'downloads')
# prefs = {'download.default_directory': downloads}
# chrome_options.add_experimental_option('prefs', prefs)

# # Detach browser so it doesn't close when the script ends
# chrome_options.add_experimental_option("detach", True)

# # Set user agent
# user_agent = generate_user_agent()
# chrome_options.add_argument(f'user-agent={user_agent}')

# # Set proxy (change IP)
# # proxy = "http://your_proxy_ip:your_proxy_port"
# # Get list of proxies
# # proxies = get_proxies()

# # # Select a random proxy from the list
# # proxy = random.choice(proxies)
# # chrome_options.add_argument(f'--proxy-server={proxy}')

# # Open in incognito mode
# # chrome_options.add_argument("--incognito")

# # Initialize Chrome WebDriver
# try:
#     chromedriver_path = ChromeDriverManager().install()
#     chromedriver_executable = os.path.join(os.path.dirname(chromedriver_path), 'chromedriver.exe')
#     print(f"Using ChromeDriver executable at: {chromedriver_executable}")
#     service = Service(chromedriver_executable)
#     driver = webdriver.Chrome(service=service, options=chrome_options)


#     driver.get("https://videobolt.net/simple-video-tools/merge")
#     print("got url >>>>>>>")
#     timer(20)
#     driver.find_element(By.XPATH, '//input[@type="file"]').send_keys(video_files[0])
#     timer()
#     print("got element >>>>>>.")
#     timer(30)
#     for i in range(1,6):
#         driver.find_element(By.XPATH, '//input[@type="file"]').send_keys(video_files[i])
#         timer(20)
#     print("keys sent >>>>>>>>.")
#     timer(20)
#     blur_button = "//div[contains(text(), 'Blurred')]"
#     driver.find_element(By.XPATH, blur_button).click() #bg blur button
#     timer()
#     print("blurred >>>>>.")
#     download_button = "//div[contains(text(), 'Merge & Download')]"
#     driver.find_element(By.XPATH, download_button).click() #download button
#     print("downloaded >>>>>>>>")

# except Exception as e:
#     print(f"Error starting ChromeDriver: {e}")
#     raise


import os
# remove all the files
downloads_path = os.path.join(os.getcwd(), 'downloads')
videos_path = os.path.join(os.getcwd(), 'videos')

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

clear_folder(downloads_path)
print("downloads cleared ")
clear_folder(videos_path)
print("videos cleared ")
