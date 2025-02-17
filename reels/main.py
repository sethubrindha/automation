from ytscrapper import YTScrapper
from upload_insta import InstaUploder
from constants import CREDENTIALS, INSTAGRAM_PASSWORD
import os, random, sys
from time import sleep


def main():
    page_index = int(sys.argv[1])
    user_name = CREDENTIALS[page_index]['user_name']
    apikey = CREDENTIALS[page_index]['apikey']
    file_name = f"shorts_{random.randint(1000, 9999)}"
    download_path = os.path.join(os.path.dirname(__file__), 'downloads', f"{file_name}.mp4")

    scrapper = YTScrapper(download_path, apikey)
    video_title = scrapper.scrape()

    insta_uploader = InstaUploder(download_path, f"🔥 {video_title} | #Shorts #Reels", 
                                  user_name, INSTAGRAM_PASSWORD)
    insta_uploader.upload_reels()

    # Get the directory where the file is located
    directory = os.path.join(os.path.dirname(__file__), 'downloads')

    sleep(300)
    # Loop through the files in the directory and check for a matching base name
    for file in os.listdir(directory):
        if file.startswith(file_name):  # Check if the file starts with the base name
            file_path = os.path.join(directory, file)
            os.remove(file_path)  # Delete the file
            print(f"File '{file_path}' has been deleted.")


if __name__ == "__main__":
    main()
