import instaloader
import random

# Initialize Instaloader
L = instaloader.Instaloader()

# Load the profile
profile_name = 'abdul_la_s'
def scrape_reels(L, profile_name):
    profile = instaloader.Profile.from_username(L.context, profile_name)

# Get all reels (posts of type 'igtv' or 'video')
    reels = [post for post in profile.get_posts() if post.typename in ['GraphVideo', 'GraphSidecar']]

# Select 2 random reels
    random_reels = random.sample(reels, 2)

# Download the selected reels
    for reel in random_reels:
        print('reel >>',reel)
        L.download_post(reel, target='downloads')

scrape_reels(L, profile_name)

print("Downloaded 2 random reels.")
