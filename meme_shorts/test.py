# import instaloader


# L = instaloader.Instaloader()
# # L.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)

# link = 'https://www.instagram.com/reel/C9sPlDUPIuO/?igsh=MTk1bjZwMTdmZW5uNA%3D%3D'
# print("link")
# shortcode = link.split('/')[-2]
# print("short_code >>>>>>",shortcode)

# # Download the reel
# post = instaloader.Post.from_shortcode(L.context, shortcode)
# L.download_post(post, target='downloads')
# print("downloaded >>>>>>>")




from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip,concatenate_videoclips
from PIL import Image

video_files = []
# Load the video
video = VideoFileClip("downloads/WhatsApp Video 2024-08-06 at 11.02.35 AM.mp4")
print("video >>>>>", video)

# Load and resize the image using Pillow
image_path = "templates/reaction_image.webp"
img = Image.open(image_path)
img_resized = img.resize((video.w, int(img.height * video.w / img.width)), Image.LANCZOS)

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
image_path = "uploads/WhatsApp Image 2024-08-06 at 11.02.36 AM.jpeg"
img = Image.open(image_path)

# # Resize the image using LANCZOS instead of the deprecated ANTIALIAS
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
clip_2 = CompositeVideoClip([video, image])
print("clip 2 generated successfully")

# Load the reaction video
reaction_video = VideoFileClip('templates/resized_video.mp4')

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