import os
from database_handler import Post
from video_generator import edit_video
from upload_insta import upload_reel
from upload_youtube import uploadYtShort
import instaloader
from constants import *

L = instaloader.Instaloader()


def main(): 
    post_list = Post.objects.filter(is_posted=False)

    if post_list:
        video_url = post_list[0].video_path
        image_path = post_list[0].image_path
        print(video_path, image_path)

        image_path = os.path.abspath(image_path)
        # Download the reel
        post = instaloader.Post.from_shortcode(L.context, video_url)
        video_file_name = f"{post.date_utc.strftime('%Y-%m-%d')}.mp4"
        L.download_post(post, target='downloads')
        video_path = os.path.join('downloads', video_file_name)
        print("video_path >>>>>>",video_path)

        print(f"Image Path: {image_path} \n")

        # Ensure the paths are correct before passing them to the video editor
        if not os.path.exists(video_path):
            print("video path does not exist >>>")
        if not os.path.exists(image_path):
            print("image path does not exist >>>")
        edit_video(video_path, image_path)
        final_video_file = None
        while not final_video_file:
            for filename in os.listdir(os.path.join(os.getcwd(), 'videos')):
                if filename.endswith('.mp4'):
                    final_video_file = os.path.join(os.getcwd(), 'videos', filename)
                    break

        print("final_video_file >>>>>>",final_video_file)


        uploadYtShort(
            VIDEO_FILE_NAME=final_video_file, 
            title="Tamil Dank Memes: Prepare for Uncontrollable Laughter!", 
            description='',
            tags=['#shorts']
            )
        print("uploaded >>>>.")

if __name__ == "__main__":
    main()
