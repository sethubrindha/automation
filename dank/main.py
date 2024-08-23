import re
import instaloader
import os
import random
from upload_youtube import uploadYtvid
from utils import *
from constants import *

L = instaloader.Instaloader()
# L.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)

def main():
    pages = '''
            '''
    timer()

    video_files = []
    reel_list = []
    total_duration = 0
    selected_pages = select_url()
    msg("selected_pages >>>>>\n", selected_pages)
    final_description = DESCRIPTION_1+pages+DESCRIPTION_2
    timer()


    for page_url in selected_pages:
        try:
            profile_name = page_url[26:-7]
            msg('profile_name >>>>>>',profile_name)
            profile = instaloader.Profile.from_username(L.context, profile_name)
            # Get all reels (posts of type 'igtv' or 'video')
            reel_list += [post for post in profile.get_posts() if post.typename in ['GraphVideo', 'GraphSidecar']]
            pages += f'\n@{profile_name} '
            timer(random.randint(30, 60))
        except: ...
    msg('reel_list >>>>>',reel_list)

    final_description = DESCRIPTION_1+pages+DESCRIPTION_2

    while total_duration < 600 or total_duration > 900:
        msg("inside while >>>>")
        selected_videos = random.sample(reel_list, min(len(reel_list), 2))
        msg("selected_videos >>>>>>>>",selected_videos)
        video_file, total_duration = download_videos(selected_videos, total_duration)
        video_files.extend(video_file)
        msg("total_duration :",total_duration)


    video_files_path, duration = get_download_videos()
    msg('video_files')

    driver = start_chrome()
    # concatenate_videoclips(driver, video_files_path)
    final_video_file = None
    while not final_video_file:
        for filename in os.listdir(os.path.join(os.getcwd(), 'videos')):
            msg('filename >>>>>>>>',filename)
            if filename.endswith('.mp4'):
                final_video_file = os.path.join(os.getcwd(), 'videos', filename)
                break
        msg('waiting for download ...')
        # timer(30)
    msg("video downloaded >>>>>")

    msg("final_video_file >>>>>>",final_video_file)
    # # Upload to YouTube (YouTube API integration code needed here)

    # # Collect tags
    tags_list = collect_tags_from_files('downloads')

    # msg the collected tags
    msg(tags_list)
    uploadYtvid(
        VIDEO_FILE_NAME=final_video_file, 
        title="Tamil Dank Memes: Prepare for Uncontrollable Laughter!", 
        description=final_description,
        tags=tags_list
        )
    msg("uplod done")


    driver.quit()
    timer(60)
    # remove all the files
    downloads_path = os.path.join(os.getcwd(), 'downloads')
    videos_path = os.path.join(os.getcwd(), 'videos')

    done = False
    while not done:
        try:
            clear_folder(downloads_path)
            msg("downloads cleared ")
            clear_folder(videos_path)
            msg("videos cleared ")
            done = True
        except: 
            timer(30)

    msg("Done!")


if __name__ == "__main__":
    main()
