import requests

# Replace with your Instagram access token
ACCESS_TOKEN = "IGAAQRUs9awr1BZAFB6UWd2UVdQV0hqSWF6SmQ2NGZAKYVZAJbTVLZAkZA1VFBFeVdERXNTWUdLSnpNdkgydXBaVVE4UHZAJWko0bEVkYzlvX0pqSFVLbXRBb0xfTDBrSlNHLXVVSF9xc3hJSVlaSHhWWmViSWYxX3RwaWhaeklzaWZAlWQZDZD"

# Replace with your Instagram User ID
USER_ID = "43040586087"

# Instagram API endpoint to get user media
MEDIA_URL = f"https://graph.instagram.com/{USER_ID}/media?fields=id,caption,media_type,media_url,thumbnail_url,timestamp&access_token={ACCESS_TOKEN}"

def get_instagram_videos():
    response = requests.get(MEDIA_URL)
    if response.status_code == 200:
        media_data = response.json()
        videos = [
            media for media in media_data.get("data", []) 
            if media.get("media_type") == "VIDEO"
        ]
        
        if videos:
            print("Fetched Instagram Videos:")
            for video in videos:
                print(f"ID: {video['id']}")
                print(f"Caption: {video.get('caption', 'No caption')}")
                print(f"Video URL: {video['media_url']}")
                print(f"Thumbnail URL: {video.get('thumbnail_url', 'No thumbnail')}")
                print(f"Posted on: {video['timestamp']}")
                print("-" * 40)
        else:
            print("No videos found.")
    else:
        print(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    get_instagram_videos()
