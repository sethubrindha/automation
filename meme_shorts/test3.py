from moviepy.editor import VideoFileClip
from moviepy.video.fx import crop
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

# Load the original video
video_path = "templates/Zias Laughing Meme Template.mp4"  # Ensure this path is correct
video = VideoFileClip(video_path)

# Specify the desired height
desired_height = 300  # Set this to your desired height

# Apply custom resize function to each frame
resized_video = video.fl_image(lambda frame: resize_image(frame, desired_height))

# Save the resized video
resized_video.write_videofile("resized_video.mp4")
