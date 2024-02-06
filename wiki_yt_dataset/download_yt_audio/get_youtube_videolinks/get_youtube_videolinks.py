import argparse
import json
import logging
import os
import shutil
import sys
import tempfile

from polyglot.detect import Detector
from tqdm import tqdm


def create_default_search_params(args: dict) -> dict:
    return {
        'max_videos': args.max_videos,
        'output': args.output,
        'proxy': args.proxy,
        'videos_per_phrase': args.videos_per_phrase
    }


def start_downloads(args: dict) -> None:
    search_params = create_default_search_params(args)

    if os.path.isfile(args.input):
        lang_code = os.path.basename(args.input).split('_')[0]

        search_params['lang_code'] = lang_code
        search_params['phrase_file_path'] = args.input

        find_videos(search_params)

    elif os.path.isdir(args.input):
        if not os.listdir(args.input):
            print('Provided input directory does not contain any files')
            exit(0)

        for phrase_file in os.listdir(args.input):
            phrase_file_path = os.path.join(args.input, phrase_file)
            lang_code = os.path.basename(phrase_file_path).split('_')[0]

            search_params['lang_code'] = lang_code
            search_params['phrase_file_path'] = phrase_file_path

            find_videos(search_params)

    else:
        print('Invalid input file or directory')
        exit(0)


def find_videos(params: dict) -> None:
    search_phrases = read_search_phrases(params['phrase_file_path'])
    valid_videos = set()

    tmp_dl_dir = '/tmp/tmp_videos'
    os.makedirs(tmp_dl_dir, exist_ok=True)

    with tqdm(total=params['max_videos']) as pbar:
        pbar.set_description('Searching for videos')
        for phrase in search_phrases:
            search(phrase, tmp_dl_dir,
                   params['videos_per_phrase'], params['proxy'])

            new_valid_videos = get_valid_videos(tmp_dl_dir, params['lang_code'])

            valid_videos.update(new_valid_videos)

            save_videos(new_valid_videos, params['output'], params['lang_code'])

            pbar.update(len(new_valid_videos))
            pbar.set_postfix(
                {
                    'video_count': len(valid_videos),
                    'lang_code': params['lang_code']
                }
            )

            if len(valid_videos) >= params['max_videos']:
                return


def save_videos(videos: list, output_path: str, lang_code: str) -> None:
    os.makedirs(output_path, exist_ok=True)
    output_file_path = os.path.join(output_path, lang_code + '_video_ids.txt')
    with open(output_file_path, 'a+') as fout:
        for video in videos:
            fout.write(f'{video}\n')


def get_valid_videos(tmp_dir: str, lang_code: str) -> list:
    valid_videos = []
    for tmp_file in os.listdir(tmp_dir):
        tmp_file_path = os.path.join(tmp_dir, tmp_file)

        if not os.path.isfile(tmp_file_path):
            logging.error('File {tmp_file} does not exist')
            continue

        with open(tmp_file_path) as tmp_json_file:
            try:
                metadata = json.load(tmp_json_file)
            except ValueError:
                logging.error('Failed to decode json from file {tmp_file}')

                delete_file(tmp_file_path)

                continue

        text = metadata['title'].strip() + ' ' + \
               metadata['description'].strip()

        # Remove non printable characters/symbols, which sometimes cause errors in Polyglot Detecor
        printable_str = ''.join(x for x in text if x.isprintable())

        detector = Detector(printable_str, quiet=True)

        if detector.language.code == lang_code:
            valid_videos.append(metadata['id'])

        delete_file(tmp_file_path)

    return valid_videos


def delete_file(file_path: str) -> None:
    try:
        os.remove(file_path)
    except OSError:
        logging.error(f'Error deleting file {file_path}')






