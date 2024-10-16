from flask import Flask, render_template, request, redirect, url_for
import os
import time
import instaloader
from constants import *
from database_handler import Post

app = Flask(__name__)

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

            Post.create(video_path=shortcode, image_path=image_path)
            return render_template('thankyou.html')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
