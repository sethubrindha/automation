import os
from meme_shorts.database_handler import Post
from meme_shorts.video_generator import edit_video
from meme_shorts.upload_insta import upload_reel
from upload_youtube import uploadYtvid



def main(): 
    post_list = Post.objects.filter(is_posted=False)

    if post_list:
        video_path = post_list[0].video_path
        image_path = post_list[0].image_path
        print(video_path, image_path)

        # Convert to absolute path
        for filename in os.listdir(os.path.join(os.getcwd(), 'downloads')):
            if filename.endswith('.mp4'):
                video_path = os.path.join(os.getcwd(), 'downloads', filename)
                break
        image_path = os.path.abspath(image_path)

        print(f"Video Path: {video_path}, \n Image Path: {image_path} \n")

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


        uploadYtvid(
            VIDEO_FILE_NAME=final_video_file, 
            title="Tamil Dank Memes: Prepare for Uncontrollable Laughter! #shorts", 
            description='',
            tags=['#shorts']
            )
        print("uploaded >>>>.")
        post_list[0].is_posted = True
        post_list[0].save()

if __name__ == "__main__":
    main()
