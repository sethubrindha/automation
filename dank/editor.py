import os
import random
from utils import start_chrome, get_download_videos, concatenate_videoclips, timer

class VideoEditor:
    def __init__(self, download_path, video_download_path):
        self.driver = start_chrome(video_download_path)
        self.duration = 0
        self.video_files = []
        self.download_path = download_path
        self.final_video_file = []
        self.filler_videos = []

    def align_videos(self):
        random.shuffle(self.video_files_path)
        final_list = [os.path.join(os.getcwd(),'dank' , 'templates', 'disclimer.mp4')]
        for num in self.video_files_path:
            final_list.append(num)
            # final_list.append(random.choice(self.list_2)) #break list
        return final_list

    def edit(self):
        self.video_files_path, self.duration = get_download_videos(self.duration, self.download_path)
        concatenate_videoclips(self.driver, self.align_videos())
        while not self.final_video_file:
            for filename in os.listdir(os.path.join(os.getcwd(), 'dank', 'videos')):
                if filename.endswith('.mp4'):
                    self.final_video_file = os.path.join(os.getcwd(), 'dank', 'videos', filename)
                    break
            print('waiting for download ...')
            timer(30)
        print("final video downloaded ...")
        print("final video file :",self.final_video_file)
        self.driver.close()
        return self.final_video_file

    def clear_folder(self):
        for file_path in os.listdir(self.final_video_file): 
            print('file path :', file_path)

            # Check if it's a file or directory
            if os.path.isfile(file_path):
                print('file_path :', file_path)
                os.remove(file_path)
                print(f'Removed file : {file_path}')

if __name__ == "__main__":
    video_editor = VideoEditor('D:\\sethu\\automation\\dank\\downloads')
    video_editor.edit()