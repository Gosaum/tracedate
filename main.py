import argparse
import datetime
import os
import time

from services.datereader import DateReader
from services.filenamer import FileNamer
from services.mediafinder import MediaFinder

from services.filenamer import GenerationMode

def create_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('media_dir_path')

    return parser

def run(target:str, settings:dict):

    mediafinder_service = MediaFinder(
        media_dir_path=target,
        media_extensions={ '.jpeg', '.jpg', '.png', '.webp', '.mov', '.mp4'}
    )
    datereader_service = DateReader()
    filenamer_service = FileNamer(media_dir_path=target)

    media_by_date = {}
    media_times = {}

    for media_path in mediafinder_service.iter_media():

        filename_date = datereader_service.read_from_filename(file_path=media_path)
        metadata_datetime = datereader_service.read_from_metadata(file_path=media_path)

        file_datetime = metadata_datetime or filename_date or None

        if filename_date and metadata_datetime and filename_date != metadata_datetime:
            file_datetime = min(metadata_datetime, filename_date)

        file_date = file_datetime.date() if file_datetime else None
        file_time = metadata_datetime.time() if metadata_datetime else None

        media_by_date.setdefault(file_date, []).append(media_path)
        media_times[media_path] = file_time

    for date, media in media_by_date.items():

        media.sort(key=lambda path: (media_times[path] is None, media_times[path] or datetime.time.min))

        quantity = len(media)
        names = filenamer_service.generate(
            qty=quantity,
            date=date,
            sep=settings.get('separator', '-'),
            generation=settings.get('identifier', GenerationMode.Paddedint)
        )
        
        for media_path, name in zip(media, names):
            filenamer_service.rename(file_path=media_path, new_name=name)

if __name__ == "__main__":

    parser = create_parser()

    args = parser.parse_args()

    media_dir_path = args.media_dir_path

    if not os.path.isdir(media_dir_path):
        parser.error(f"'{media_dir_path}' is not a valid directory")

    separators = { '1': '-', '2': ' ', '3': '_', }
    current_separator = separators['1']

    identifiers = {
        '1': GenerationMode.Paddedint,
        '2': GenerationMode.Parensint,
        '3': GenerationMode.Hexstring, }
    current_identifier =identifiers['1']

    while True:
        print(
r"""
  __                      __     __     
 / /________ ________ ___/ /__ _/ /____ 
/ __/ __/ _ `/ __/ -_) _  / _ `/ __/ -_)
\__/_/  \_,_/\__/\__/\_,_/\_,_/\__/\__/                
""")
        print("Welcome to `tracedate`! Choose an option:")
        print("[1] Run script")
        print("[2] Settings")
        print("[3] Bye (quit)")
        choice = input("\n> ").strip()
        match choice:

            case '1':
                print(f"Let's go! Running the script...")
                start = time.time()
                run(target=media_dir_path, settings={
                    'separator': current_separator, 'identifier': current_identifier
                })
                end = time.time()
                print(f"Done! Time: {(end - start):.3f} s")
                break

            case '2':

                print(f"\nChoose the separator: [1] '-' [2] ' ' [3] '_'")
                settings_choice = separators.get(input("\n> ").strip(), None)
                if settings_choice:
                    current_separator = settings_choice
                else:
                    print(f"Choice not saved - unrecognized input")

                print(f"\nChoose the identifier type: [1] '0001' [2] '(1)' [3] '0xFF'")
                settings_choice = identifiers.get(input("\n> ").strip(), None)
                if settings_choice:
                    current_identifier = settings_choice
                else:
                    print(f"Choice not saved - unrecognized input")

            case '3':
                print(f"Bye !")
                break

            case _:
                print(f"Unrecognised choice: {choice!s}")