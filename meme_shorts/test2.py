from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
from PIL import Image

# Load the main video
video = VideoFileClip("downloads/WhatsApp Video 2024-08-06 at 11.02.35 AM.mp4")
print("video >>>>>", video)

# Mute the audio
video = video.without_audio()

# Load and resize the image using the correct method
image_path = "uploads/WhatsApp Image 2024-08-06 at 11.02.36 AM.jpeg"
img = Image.open(image_path)

# Resize the image using LANCZOS instead of the deprecated ANTIALIAS
img_resized = img.resize((video.w, int(img.height * video.w / img.width)), Image.LANCZOS)

# Save the resized image temporarily
resized_image_path = "uploads/resized_image.png"
img_resized.save(resized_image_path)

# Load the resized image into MoviePy
image = ImageClip(resized_image_path)
print("image >>>>>>", image)

# Set the image position at the bottom and match the duration with the video
image = image.set_position(("center", "center")).set_duration(video.duration)

# Create the first composite video with the image overlaid
final_video_1 = CompositeVideoClip([video, image])
print("video 1 generated >>>>>>>>")

# Load the reaction video
reaction_video = VideoFileClip('templates/resized_video.mp4')

# Load the original and reaction videos
original_video = final_video_1
reaction_video = reaction_video

# Resize the reaction video (optional, adjust as needed)
# reaction_video = reaction_video.resize(height=150)  # Resize by height
reaction_video = reaction_video.set_position(("center", "bottom"))  # Position it in the bottom-right corner

# Overlay the reaction video onto the original video
final_video = CompositeVideoClip([original_video, reaction_video.set_start(0)])

# Set the duration of the final video to match the original video (optional)
final_video = final_video.set_duration(reaction_video.duration)

# Save the final video
final_video.write_videofile("videos/final_video.mp4", codec="libx264", fps=24)

print("Final video generated successfully!")
