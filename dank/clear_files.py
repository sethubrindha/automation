import os
from utils import *

def main():
    # remove all the files
    downloads_path = os.path.join(os.getcwd(), 'downloads')
    videos_path = os.path.join(os.getcwd(), 'videos')

    done = False
    while not done:
        try:
            clear_folder(downloads_path)
            print("downloads cleared ")
            clear_folder(videos_path)
            print("videos cleared ")
            done = True
        except Exception as e: 
            print("Error clearing folder: ", e.args)
            timer(30)


if __name__ == "__main__":
    main()
