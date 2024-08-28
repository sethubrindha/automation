from flask import Flask, render_template, request, redirect, url_for
import os
import time
import instaloader
from constants import *
from database_handler import Post

app = Flask(__name__)

L = instaloader.Instaloader()
# Configuring the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        url = request.form['url']
        print("url >>>>>>", url)
        file = request.files['file']
        print("file >>>>>>.",file)

        if file and url:
            filename = file.filename
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print("image_path >>>>>>>",image_path)
            file.save(image_path)

            shortcode = url.split('/')[-2]
            print("short_code >>>>>>",shortcode)

            # Download the reel
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            video_file_name = f"{post.date_utc.strftime('%Y-%m-%d')}.mp4"
            L.download_post(post, target='downloads')
            video_path = os.path.join('downloads', video_file_name)
            print("video_path >>>>>>",video_path)
            Post.create(video_path=video_path, image_path=image_path)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
