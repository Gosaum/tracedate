import datetime
import enum
import os
import secrets

class GenerationMode(enum.Enum):
    Paddedint = enum.auto()
    Parensint = enum.auto()
    Hexstring = enum.auto()
    
class FileNamer:

    def __init__(self, media_dir_path:str):

        self.media_dir_path = os.path.abspath(media_dir_path)

    def generate(self, qty:int, date:datetime, sep:str, generation:GenerationMode):

        date_prefix = date.strftime(f"%Y{sep}%m{sep}%d") if date else 'undated'

        suffixes = []
        match generation if date else GenerationMode.Hexstring:
            case GenerationMode.Paddedint:

                suffixes = [f"{i:05d}" for i in range(1, qty + 1)]

            case GenerationMode.Parensint:

                suffixes = [f"({i})" for i in range(1, qty + 1)]

            case GenerationMode.Hexstring:

                raw_hashes = sorted(secrets.token_hex(6) for _ in range(qty))
                suffixes = [f"{h[:4]}{sep}{h[4:8]}{sep}{h[8:]}" for h in raw_hashes]

        return [f"{date_prefix}{sep}{suffix}" for suffix in suffixes]

    def rename(self, file_path:str, new_name:str):

        file_path = os.path.abspath(file_path)
        dir_path = os.path.dirname(file_path)

        new_filename = f"{new_name}{os.path.splitext(file_path)[1]}"
        new_file_path = os.path.join(dir_path, new_filename)

        if new_filename != file_path:
            os.rename(file_path, new_file_path)