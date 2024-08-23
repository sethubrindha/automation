from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from email_generator import generate_email_address, get_otp
from query_generator import query_generator
from utils import *
from flow import *
from faker import Faker
from datetime import datetime
import pyautogui
import os
from moviepy.editor import VideoFileClip
from selenium.webdriver.chrome.service import Service
from upload_youtube import uploadYtvid
import pyperclip


'''
generate shorts video about monkey pox awareness. use images without watermark and do not use istock images. use high quality images. generate title, description and hashtags for this video. the video should be ends with please subscribe our channel
'''
QUERY = query_generator()
fake = Faker()

def run_function(key):
	if key == 'generate_email_address':
		return generate_email_address()
	elif key == 'get_otp':
		return get_otp()
	elif key == 'fake_name':
		return fake.name()
	elif key == 'query_generator':
		query =  QUERY+QUERY_SETTINGS
		return query

# Setup Google 
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
client_secrets_file = "googleAPI.json"


class Generate_video():
	def __init__(self, driver=None):
		self.driver = driver
		self.url = 'https://google.com/'
		# self.url = 'https://ai.invideo.io/login'
		self.upload_url = 'https://studio.youtube.com/channel/'
		self.file_name = None
		self.video_title = None
		self.description = None
		self.hash_tags = None


	def start_crome(self):
		chrome_options = webdriver.ChromeOptions()
		# chrome_options.add_argument("--incognito")
		chrome_options.add_experimental_option("detach", True)
		service=Service(ChromeDriverManager().install())
		# chrome_options.binary_location = 'C:\Program Files\Google\Chrome Beta\Application\chrome.exe'
		# prefs = {'download.default_directory' : 'E:\\selenium_automation\\facts\\downloads'}
		# chrome_options.add_experimental_option('prefs', prefs)
		self.driver = webdriver.Chrome(service=service, options=chrome_options)


	# def sample_download(self):
	# 	sample_image = 'https://images.pexels.com/photos/2280549/pexels-photo-2280549.jpeg?cs=srgb&dl=pexels-chokniti-khongchum-2280549.jpg&fm=jpg&_gl=1*jcnacm*_ga*MzEwNzMwMTc1LjE3MDE2NjU1MzQ.*_ga_8JE65Q40S6*MTcwMTY2NTk5Mi4xLjAuMTcwMTY2NTk5Mi4wLjAuMA..'
	# 	self.driver.get(sample_image)
	# 	timer(2)
	# 	pyautogui.press('enter') 
	# 	timer(1)
	# 	print('download path setup done')
	# 	print('self.url >>>>',self.url)
	# 	self.driver.get(self.url)
	# 	print('got url >>>>')

	# 	# self.driver.minimize_window()
	# 	# print("window minimazed >>>>>")


	def invideo_ai_login(self):
		self.driver.get(self.url)
		# self.driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[2]/div[2]/div[2]/div[3]/form/div/input')
		for element in LOGIN_ELEMENTS:
			element['keys'] = run_function(element['keys']) if element['keys'] else None
			element_action(self.driver, element)


	def generate_video(self):
		driver = self.driver
		driver.execute_script(f"window.open('{self.url}');")
		timer()
		driver.switch_to.window(driver.window_handles[1])
		print('new window switched')
		timer(10)

		for element in VIDEO_GENERATOR_ELEMENTS:
			element['keys'] = run_function(element['keys']) if element['keys'] else None
			element_action(self.driver, element)

		self.file_name = f'short-video{datetime.now()}'
		driver.find_element(By.XPATH, DESCRIPTION)
		self.description = pyperclip.paste()
		self.video_title = driver.find_element(By.XPATH, TITLE).get_attribute()


	def export_video(self):
		pass
		# driver = self.driver
		# waiting_message = driver.find_element(By.XPATH, WAITING).get_attribute()
		# print("waiting_message >>>>>",waiting_message)
		# if waiting_message != 'Rendering video...':
		# 	return False


		# timings = driver.execute_script("return window.performance.getEntries();")
		# print ('timings >>>>>>>>',timings)
		# return True


	def edit_video(self):
		height = 1500
		width = 1000
		filename = 'test_video.mp4'
		file_path =f'C:\\Users\\emedhub\\Downloads\\{filename}'
		print("file_path >>>>",file_path)
		video = VideoFileClip(f'C:\\Users\\emedhub\\Downloads\\{filename}')
		# Calculate the center coordinates of the video
		center_x = video.w / 2
		center_y = video.h / 2

		# Calculate the top-left coordinates of the crop box
		crop_x = center_x - width / 2
		crop_y = center_y - height / 2
		# Crop to 1080x1350 size
		video = video.crop(x1=crop_x, y1=crop_y, width=width , height=height)
		# Replace 'cropped_video.mp4' with the name of your output file
		video.write_videofile('videos/cropped_video.mp4')
		os.remove(file_path)


	def upload_video(self):
		print("Uploading to Youtube...")
		uploadYtvid(VIDEO_FILE_NAME=self.file_name,
					title=self.video_title,
					description=self.description)

	def delete_invideo_ai_login(self):
		pass


	def close_crome(self):
		self.driver.close()

