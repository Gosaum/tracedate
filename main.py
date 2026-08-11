import argparse
import os

from services.datereader import DateReader
from services.filenamer import FileNamer
from services.mediafinder import MediaFinder

from services.filenamer import GenerationMode

def create_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('media_dir_path')

    return parser

def run(target:str):

    mediafinder_service = MediaFinder(
        media_dir_path=target,
        media_extensions={ '.png', '.jpg', '.jpeg', '.webp', '.mov', '.mp4'}
    )
    datereader_service = DateReader()
    filenamer_service = FileNamer(media_dir_path=target)

    media_by_date = {None: []}

    for media_path in mediafinder_service.iter_media():

        filename_date = datereader_service.read_from_filename(file_path=media_path)
        metadata_date = datereader_service.read_from_metadata(file_path=media_path)

        file_date = metadata_date or filename_date or None

        if filename_date and metadata_date and filename_date != metadata_date:
            file_date = min(metadata_date, filename_date)

        media_by_date.setdefault(file_date, []).append(media_path)

    for date, media in media_by_date.items():

        quantity = len(media)
        names = filenamer_service.generate(
            qty=quantity, date=date,sep='-', generation=GenerationMode.Paddedint)
        
        for media_path, name in zip(media, names):
            filenamer_service.rename(file_path=media_path, new_name=name)

if __name__ == "__main__":

    parser = create_parser()

    args = parser.parse_args()

    media_dir_path = args.media_dir_path

    if not os.path.isdir(media_dir_path):
        parser.error(f"'{media_dir_path}' is not a valid directory")

    run(target=media_dir_path)