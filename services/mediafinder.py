import os

class MediaFinder:

    def __init__(self, media_dir_path:str, media_extensions):

        self.media_dir_path = os.path.abspath(media_dir_path)
        self.media_extensions = {ext.lower() for ext in media_extensions}

    def iter_media(self) -> object:

        if not os.path.exists(self.media_dir_path):
            return
        for root, _, filenames in os.walk(self.media_dir_path):
            for filename in filenames:
                media_path = os.path.join(root, filename)
                if self.is_media(media_path):
                    yield media_path

    def is_media(self, media_path:str) -> bool:

        ext = os.path.splitext(media_path)[1].lower()
        return ext in self.media_extensions and os.path.isfile(media_path)

