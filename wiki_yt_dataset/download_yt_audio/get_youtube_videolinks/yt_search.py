import os
import random
import subprocess


def read_search_phrases(filename: str) -> list:
    with open(filename, encoding="utf-8") as file:
        phrases = file.readlines()
    random.shuffle(phrases)
    return phrases


def search(phrase: str, tmp_dir: str, videos_per_phrase: int, proxy: str) -> None:
    search_args = [
        "youtube-dl",
        f"ytsearch{videos_per_phrase}:'{phrase}'",
        "-o",
        os.path.join(tmp_dir, "%(id)s.%(ext)s"),
        "--no-playlist",
        "--write-info-json",
        "--skip-download",
        "--quiet",
        "--ignore-errors"
    ]

    if proxy is not None:
        search_args.append('--proxy')
        search_args.append(proxy)

    subprocess.run(search_args)
