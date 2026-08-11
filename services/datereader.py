import os
import datetime
import re

class DateReader:

    def __init__(self) -> list:

        self.regex_date_pattern = re.compile(
            # yyyy-mm-dd date in the 21st c.
            r"(?<!\d)(20\d{2})[-_\s]?(0[1-9]|1[0-2])[-_\s]?(0[1-9]|[12]\d|3[01])(?!\d)")

    def read_from_filename(self, file_path:str):

        match = self.regex_date_pattern.search(os.path.basename(file_path))
        if not match:
            return None
        year, month, day = (int(group) for group in match.groups())
        try:
            return datetime.datetime(year, month, day).date()
        except:
            return None

    def read_from_metadata(self, file_path:str):

        return None