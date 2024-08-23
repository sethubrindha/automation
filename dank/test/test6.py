from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
import time

def wait_for_download(file_path, timeout=90):
    start_time = time.time()
    print("file_path >>>>>>>>.", file_path)
    while time.time() - start_time < timeout:
        if os.path.exists(file_path):
            return True
    return False

def get_download_videos(total_duration=0):
    video_clips = []

    for filename in os.listdir(os.path.join(os.getcwd(), 'downloads')):
        if filename.endswith('.mp4'):
            # Construct the full path to the downloaded file
            video_file = os.path.join(os.getcwd(), 'downloads', filename)
            print("video_file >>>>>>>>>>", video_file)

            if wait_for_download(video_file):
                try:
                    video_clip = VideoFileClip(video_file)
                    video_clips.append(video_clip)  # Store the VideoFileClip object
                    total_duration += video_clip.duration
                    if total_duration >= 300:
                        break
                except Exception as e:
                    print(f"Error loading {video_file}: {e}")

            else:
                print(f"Error: Download for {video_file} timed out.")

    return video_clips, total_duration

# Get the list of video clips
video_clips, duration = get_download_videos()

# Concatenate all the video clips
if video_clips:
    try:
        final_clip = concatenate_videoclips(video_clips)
        
        # Write the output video file
        output_filename = 'output.mp4'
        final_clip.write_videofile(output_filename, codec="libx264", fps=24)
        
        print(f'Videos joined successfully into {output_filename}')
    except Exception as e:
        print(f"Error concatenating videos: {e}")
else:
    print("No videos found to concatenate.")
