from instagrapi import Client

class InstaUploder:
        def __init__(self, video_path, caption, username, password):
            self.cl = Client()
            self.media_id = None
            self.video_path = video_path
            self.caption = caption
            self.cl.login(username, password)
            print("logged in successfully")

        def upload_reels(self):
            self.cl.clip_upload(
                self.video_path, caption=self.caption
            )

