import os
import datetime
import re
import struct

from PIL import Image, ExifTags

class DateReader:

    def __init__(self) -> list:

        self.regex_date_pattern = re.compile(
            # yyyy-mm-dd date in the 21st c.
            r"(?<!\d)(20\d{2})[-_\s]?(0[1-9]|1[0-2])[-_\s]?(0[1-9]|[12]\d|3[01])(?!\d)")

        self.readers = {
            # pictures
            '.jpeg':    self._read_jpeg_exif,
            '.jpg':     self._read_jpeg_exif,
            '.png':     self._read_png_exif,
            '.webp':    self._read_jpeg_exif,
            # videos
            '.mov':     self._read_mov_metadata,
            '.mp4':     self._read_mov_metadata,
        }

    def read_from_filename(self, file_path:str) -> datetime.datetime:

        match = self.regex_date_pattern.search(os.path.basename(file_path))
        if not match:
            return None
        year, month, day = (int(group) for group in match.groups())
        try:
            return datetime.datetime(year, month, day)
        except:
            return None
    
    def read_from_metadata(self, file_path:str):

        date = None

        ext = os.path.splitext(file_path)[1].lower()
        if ext in self.readers:
            try:
                date = self.readers[ext](file_path)
            except:
                date = None

        return date

    def _parse_exif_datetime(self, value) -> datetime.datetime:

        value = value.strip()
        # exif standard format : 'YYYY:MM:DD HH:MM:SS'
        try:
            return datetime.datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
        except:
            pass
        try:
            return datetime.datetime.strptime(value[:10], '%Y:%m:%d')
        except:
            pass
        return None

    def _read_jpeg_exif(self, file_path:str):

        with Image.open(file_path) as img:

            exif = img.getexif()
            if not exif:
                return None
            try:
                exif_ifd = exif.get_ifd(ExifTags.IFD.Exif)
            except:
                exif_ifd = {}

            for source, tag_id in [ # DateTimeOriginal, DateTimeDigitized, DateTime
                (exif_ifd, 36867), (exif_ifd, 36868), (exif, 306)
            ]:
                value = source.get(tag_id)
                if not value:
                    continue
                date = self._parse_exif_datetime(value)
                if date:
                    return date

            return None

    def _read_png_exif(self, file_path:str):

        date = self._read_jpeg_exif(file_path)
        if date:
            return date

        with Image.open(file_path) as img:
            text = img.info.get('Creation Time') or img.info.get('creation_time')
            if text:
                try: # FRFC 2822 format
                    return datetime.datetime.strptime(text.strip(), '%a, %d %b %Y %H:%M:%S %Z')
                except:
                    pass

        return None

    def _find_moov(self, data:bytes):

        pos, end = 0, len(data)
        while pos + 8 <= end:
            size = struct.unpack('>I', data[pos:pos + 4])[0]
            box_type = data[pos + 4:pos + 8]
            header_size = 8
            if size == 1:
                if pos + 16 > end:
                    break
                size = struct.unpack('>Q', data[pos + 8:pos + 16])[0]
                header_size = 16
            elif size == 0:
                size = end - pos
            if size < header_size:
                break
            if box_type == b'moov':
                return pos + header_size, pos + size
            pos += size
        return None, None

    def _read_mov_metadata(self, file_path:str):

        with open(file_path, 'rb') as f:
            data = f.read()

        moov_start, moov_end = self._find_moov(data)
        if moov_start is None:
             return None

        # search for movie creation date from moov/mvhd atom
        pos = moov_start
        while pos + 8 <= moov_end:
            size = struct.unpack('>I', data[pos:pos + 4])[0]
            box_type = data[pos + 4:pos + 8]
            header_size = 8
            if size == 1:
                if pos + 16 > moov_end:
                    break
                size = struct.unpack('>Q', data[pos + 8:pos + 16])[0]
                header_size = 16
            elif size == 0:
                size = moov_end - pos
            if size < header_size:
                break

            if box_type == b'mvhd':
                content_start = pos + header_size
                version = data[content_start]
                try:
                    if version == 1:
                        creation_time = struct.unpack(
                            '>Q', data[content_start + 4:content_start + 12])[0]
                    else:
                        creation_time = struct.unpack(
                            '>I', data[content_start + 4:content_start + 8])[0]
                except struct.error:
                    return None
                if not creation_time:
                    return None
                try:
                    return datetime.datetime.fromtimestamp(
                        creation_time - 2082844800, tz=datetime.timezone.utc
                    ).replace(tzinfo=None)
                except (OSError, OverflowError, ValueError):
                    return None

            pos += size

        return None