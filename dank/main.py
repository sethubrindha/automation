import re
import instaloader
import os
import random
from upload_youtube import uploadYtvid
from utils import *
from constants import *

L = instaloader.Instaloader()

try:
    # Load session if exists
    L.load_session_from_file(INSTAGRAM_USERNAME)
except:
    # Log in and save session if not already saved
    L.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
    L.save_session_to_file()

print("Is authenticated:", L.context.is_logged_in)

print('logged in >>>>>')

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


    for page_url in selected_pages:
        try:
            profile_name = page_url[26:-7]
            print('profile_name >>>>>>',profile_name)
            profile = instaloader.Profile.from_username(L.context, profile_name)
            print("profile >>>>>",profile)

            # Get all reels (posts of type 'igtv' or 'video')
            reel_list += [post for post in profile.get_posts() if post.typename in ['GraphVideo', 'GraphSidecar']]
            # Limit the number of posts retrieved to 100, for example
            # post_list = list(profile.get_posts())
            # print('post_list length >>>>>>>', len(post_list))
            # if post_list:
            #     for post in post_list:
            #         print(post, post.typename)
            #         if post.is_video:
            #             reel_list.append(post)
            #             if len(reel_list) >= 100:
            #                 break
            # else:
            #     print("No posts found.")

            print("reel_list >>>>>>",reel_list)
            pages += f'\n@{profile_name} '
            timer(random.randint(30, 60))

        except instaloader.exceptions.AbortDownloadException:
            try:
                print("Session expired. Logging in again...")
                print('INSTAGRAM_USERNAME >>>>>>>',INSTAGRAM_USERNAME)
                print('INSTAGRAM_PASSWORD >>>>>>>',INSTAGRAM_PASSWORD)
                L.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
                L.save_session_to_file()
                print("relogged in >>>>")
            except instaloader.exceptions.LoginException as e:
                print('check point required : ',e)

        except Exception as e: 
            print(f"Error: {e}")
        

    print('reel_list >>>>>',reel_list)

    final_description = DESCRIPTION_1+pages+DESCRIPTION_2

    while total_duration < 600 or total_duration > 900:
        print("inside while >>>>")
        selected_videos = random.sample(reel_list, min(len(reel_list), 2))
        print("selected_videos >>>>>>>>",selected_videos)
        if not selected_videos:
            breakpoint()
        video_file, total_duration = download_videos(selected_videos, total_duration)
        video_files.extend(video_file)
        print("total_duration :",total_duration)


    video_files_path, duration = get_download_videos()
    print('video_files')

    driver = start_chrome()
    concatenate_videoclips(driver, video_files_path)
    final_video_file = None
    while not final_video_file:
        for filename in os.listdir(os.path.join(os.getcwd(), 'videos')):
            print('filename >>>>>>>>',filename)
            if filename.endswith('.mp4'):
                final_video_file = os.path.join(os.getcwd(), 'videos', filename)
                break
        print('waiting for download ...')
        timer(30)
    print("video downloaded >>>>>")

    print("final_video_file >>>>>>",final_video_file)
    # # Upload to YouTube (YouTube API integration code needed here)

    tags_list = [
        'tamildank', 'tamildankmemes', 'tamilmemes', 'kollywoodmemes', 'tamiltroll',
        'trolltamil', 'tamiljokes', 'tamilcomedy', 'vadivelumemes', 'trendingtamilmemes',
        'tamilfunny', 'chennaimemes', 'vetrimaranmemes', 'tamilviral', 'tamiltrending',
        'tamildankcommunity', 'danktamil'
    ]

    uploadYtvid(
        VIDEO_FILE_NAME=final_video_file, 
        title="Tamil Dank Memes: Prepare for Uncontrollable Laughter!", 
        description=final_description,
        tags=tags_list
        )
    print("uplod done")

    driver.quit()
    timer(300)
    print("Done!")


if __name__ == "__main__":
    main()
