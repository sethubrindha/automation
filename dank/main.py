import os
from upload_youtube import uploadYtvid
from utils import *
from constants import *
from instascrapper import InstaScrapper
from editor import VideoEditor
from time import sleep

def main():
    description_1, description_2, title, tags_list, page_list = get_video_details()
    selected_pages = select_url(page_list)

    print("selected_pages :\n", selected_pages)
    download_path = os.path.join(os.path.dirname(__file__), 'downloads')
    timer()

    scrapper = InstaScrapper(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, download_path)
    for page_url in selected_pages:
        profile_name = page_url[26:-7]
        print('profile_name :',profile_name)
        description_1 = description_1+f'{profile_name}\n'
        scrapper.scrape(profile_name)
        sleep(30)
        
    scrapper.logout()

    editor = VideoEditor(download_path)
    final_video_file = editor.edit()

    uploadYtvid(VIDEO_FILE_NAME=final_video_file, title=title, description=description_1+description_2, tags=tags_list)
    editor.clear_folder()
    print("Done!")


if __name__ == "__main__":
    main()
