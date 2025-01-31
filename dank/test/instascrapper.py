from utils import start_chrome, timer, INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD
import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
from selenium.webdriver.support.ui import WebDriverWait


class InstagramScraper:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = start_chrome()

    def human_type(self, element, text):
        """Types like a human with random delays."""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.4))  # Random typing speed

    def login(self):
        """Logs into Instagram with human-like behavior."""
        self.driver.get("https://www.instagram.com/")
        time.sleep(random.uniform(3, 6))  # Wait for the page to load


        # Find input fields
        username_input = self.driver.find_element(By.NAME, "username")
        password_input = self.driver.find_element(By.NAME, "password")

        # Type username & password like a human
        self.human_type(username_input, self.username)
        time.sleep(random.uniform(1, 3))
        self.human_type(password_input, self.password)

        # Press Enter to login
        password_input.send_keys(Keys.RETURN)
        time.sleep(random.uniform(5, 10))  # Wait for login to complete

        # Locate button by XPath
        save_info_button = self.driver.find_element(By.XPATH, "//button[text()='Save info']")
        
        # Move cursor to the button (mimics human behavior)
        ActionChains(self.driver).move_to_element(save_info_button).perform()
        time.sleep(1)  # Small delay before clicking
        
        # Click the button
        save_info_button.click()

    def search_profile(self, profile_name):
        """Searches for an Instagram profile and clicks on it."""
        timer(random.uniform(3, 5))
        self.driver.get(f"https://www.instagram.com/{profile_name}/")
        time.sleep(random.uniform(5, 7))


    def click_reels(self):
        """Clicks on the 'Reels' button on a profile."""
        time.sleep(3)  # Allow time for elements to load

        try:
            # Locate the "Reels" tab using text-based XPath
            reels_button = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Reels')]")
            
            # Move cursor to the button (human-like behavior)
            ActionChains(self.driver).move_to_element(reels_button).perform()
            time.sleep(1)  # Small delay before clicking
            
            # Click the "Reels" button
            reels_button.click()
            print("Clicked 'Reels' button successfully!")
        except Exception as e:
            print("Could not find 'Reels' button:", e)

    def get_reels(self):
        """Extracts reel links, views, and likes."""
        time.sleep(random.uniform(3, 5))
        reels_data = []
        
        try:
            reel_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@role='button']//a"))
            )
        except Exception as e:
            print("Error finding reels:", e)
            return []

        for i, reel in enumerate(reel_elements[:15]):  # Get first 15 reels
            try:
                link = reel.get_attribute("href")
                self.driver.execute_script("arguments[0].click();", reel)
                time.sleep(random.uniform(3, 5))

                # Retry mechanism for stale elements
                for _ in range(3):
                    try:
                        views_text = self.wait.until(
                            EC.presence_of_element_located(
                                (By.XPATH, "//section//span[contains(text(), 'views')]")
                            )
                        ).text
                        likes_text = self.wait.until(
                            EC.presence_of_element_located(
                                (By.XPATH, "//section//span[contains(text(), 'likes')]")
                            )
                        ).text
                        views_count = int(views_text.split()[0].replace(",", ""))
                        likes_count = int(likes_text.split()[0].replace(",", ""))
                        break  # Exit loop if no error
                    except Exception as e:
                        print(f"Retry fetching views/likes for reel {i + 1}")

                reels_data.append({"link": link, "views": views_count, "likes": likes_count})
                
                # Close reel
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                time.sleep(random.uniform(2, 4))
            
            except Exception as e:
                print(f"Error processing reel {i + 1}: {e}")

        return reels_data


    def download_reels(self, reels):
        """Downloads the top 10 reels by views."""
        for i, reel in enumerate(reels[:10]):
            video_url = reel["link"]
            response = requests.get(video_url, stream=True)

            if response.status_code == 200:
                with open(f"reel_{i + 1}.mp4", "wb") as file:
                    for chunk in tqdm(response.iter_content(1024), desc=f"Downloading Reel {i+1}"):
                        file.write(chunk)
                print(f"Downloaded reel_{i + 1}.mp4 successfully!")
            else:
                print(f"Failed to download {video_url}")

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    profile_list = ['https://www.instagram.com/karupu.exe/reels/', 'https://www.instagram.com/cringe__seivom/reels/', 'https://www.instagram.com/memesettai/reels/', 'https://www.instagram.com/kunji_da.baalam/reels/', 'https://www.instagram.com/adv_stranger_mbbs/reels/', 'https://www.instagram.com/duraianna.kannni/reels/', 'https://www.instagram.com/psy_fador/reels/', 'https://www.instagram.com/purushoth__tp/reels/', 'https://www.instagram.com/saw_me_nah_done.exe/reels/', 'https://www.instagram.com/boredommemezz/reels/', 'https://www.instagram.com/body__soda_memes/reels/', 'https://www.instagram.com/vaama_thunder_/reels/']
    scraper = InstagramScraper(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
    scraper.login()
    for page_url in profile_list:
        profile_name = page_url[26:-7]
        scraper.search_profile(profile_name)
        scraper.click_reels()
        reels = scraper.get_reels()
        reels_sorted = sorted(reels, key=lambda x: x["views"], reverse=True)
        scraper.download_reels(reels_sorted)
        scraper.close()
