from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip,concatenate_videoclips
from PIL import Image
import numpy as np



def resize_image(image, height):
    # Convert numpy array to PIL image
    pil_image = Image.fromarray(image)
    
    # Calculate new width while maintaining aspect ratio
    aspect_ratio = pil_image.width / pil_image.height
    new_width = int(aspect_ratio * height)
    
    # Resize image
    resized_pil_image = pil_image.resize((new_width, height), Image.LANCZOS)
    
    # Convert PIL image back to numpy array
    return np.array(resized_pil_image)


def edit_video(reel_video, screen_shot):
    video_files = []
    # Load the video
    video = VideoFileClip(reel_video)
    reaction_video = VideoFileClip("templates/Zias Laughing Meme Template.mp4")


    # Load and resize the image using Pillow
    image_path = "templates/reaction_image.webp"
    img = Image.open(image_path)
    img_resized = img.resize((video.w, int(reaction_video.h)), Image.LANCZOS)

    # Save the resized image temporarily
    resized_image_path = "templates/reaction_image.webp"
    img_resized.save(resized_image_path)

    # Load the resized image into moviepy
    image = ImageClip(resized_image_path)
    print("image >>>>>>", image)

    # Set the image position at the bottom and match the duration with the video
    image = image.set_position(("center", "bottom")).set_duration(video.duration)

    # Create a composite video with the image overlaid at the bottom
    clip_1 = CompositeVideoClip([video, image])

    print("clip 1 generated successfully")
    # # Save the final video
    # clip1.write_videofile(r"videos/output_video.mp4", codec="libx264", fps=video.fps)
    video_files.append(clip_1)


    # Mute the audio
    video = video.without_audio()

    # Load and resize the image using the correct method
    img = Image.open(screen_shot)

    # # Resize the image using LANCZOS instead of the deprecated ANTIALIAS
    img_resized = img.resize((video.w, int(img.height * video.w / img.width)), Image.LANCZOS)

    # Save the resized image temporarily
    resized_image_path = "uploads/resized_image.png"
    img_resized.save(resized_image_path)
    print("resize")

    # Load the resized image into MoviePy
    image = ImageClip(resized_image_path)
    print("image >>>>>>", image)

    # Set the image position at the bottom and match the duration with the video
    image = image.set_position(("center", "center")).set_duration(video.duration)

    # Create the first composite video with the image overlaid
    clip_2 = CompositeVideoClip([video, image])
    print("clip 2 generated successfully")

    # Load the reaction video
    # video_path = "templates/Zias Laughing Meme Template.mp4"  # Ensure this path is correct
    # video_path = "templates/resized_video.mp4"  # Ensure this path is correct

    # Load the original and reaction videos

    # Resize the reaction video (optional, adjust as needed)
    # reaction_video = reaction_video.resize(height=150)  # Resize by height
    reaction_video = reaction_video.set_position(("center", "bottom"))  # Position it in the bottom-right corner

    # Overlay the reaction video onto the original video
    clip_3 = CompositeVideoClip([clip_2, reaction_video.set_start(0)])
    print("clip 3 generated successfully")
    # Set the duration of the final video to match the original video (optional)
    clip_3 = clip_3.set_duration(reaction_video.duration)

    video_files.append(clip_3)

    final_clip = concatenate_videoclips(video_files)
    print("Final video generated successfully!")
    # Save the final video
    final_clip.write_videofile("videos/final_video.mp4", codec="libx264", fps=24)

    print('done >>>>>')
