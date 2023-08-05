import os

from yt_concate.settings import DOWNLOADS_DIR
from yt_concate.settings import VIDEOS_DIR
from yt_concate.settings import CAPTIONS_DIR


class Utils:
    def __int__(self):
        pass

    def create_dirs(self):
        os.makedirs(DOWNLOADS_DIR, exist_ok=True)
        os.makedirs(VIDEOS_DIR, exist_ok=True)
        os.makedirs(CAPTIONS_DIR, exist_ok=True)

    @staticmethod
    def get_video_id_from_url(url):
        return url.split('watch?v=')[-1]  # split分開的左右兩邊是0和1，-1是指從後面數來第一個，這邊要寫1也可以

    def get_caption_filepath(self, url):
        return os.path.join(CAPTIONS_DIR, self.get_video_id_from_url(url) + 'txt')

    def caption_file_exists(self, url):
        path = self.get_caption_filepath(url)
        return os.path.exists(path) and os.path.getsize(path) > 0

    def get_video_list_filepath(self, channel_id):
        return os.path.join(DOWNLOADS_DIR, channel_id + 'txt')

    def video_file_exists(self, channel_id):
        path = self.get_caption_filepath(channel_id)
        return os.path.exists(path) and os.path.getsize(path) > 0
