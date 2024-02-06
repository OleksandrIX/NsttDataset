import click
from loguru import logger
from .config.logger import init_logger

init_logger(app_name="wiki-yt-dataset",
            std_level="TRACE",
            file_level="INFO",
            log_rotation="1 day",
            log_compression="gz")


@click.group()
def cli():
    pass


@cli.command(name="wiki")
@click.option("--download", "-d", is_flag=True, help="Download wiki dumps")
@click.option("--extract", "-e", is_flag=True, help="Extract wiki dumps")
@click.option("--languages", "-l", required=True, default="en", help="Languages to download and extract")
@click.option("--date-dump", "-D", required=True, help="Date of wiki dumps to download and extract")
@click.option("--output-path", "-o", required=True, help="Output directory to save wiki dumps")
def download_wiki_dumps(download: bool, extract: bool, languages: str, date_dump: str, output_path: str):
    """
    Download and extract wiki dumps\n
    For the download and extract options, you can do not specify any of them, or specify both of them.\n
    If you do not specify any of them, both of them will be executed.\n
    """
    from .download_extract_wiki import download_wiki_dumps, extract_wiki_dumps

    languages = languages.strip().split()
    logger.info(f"Languages: {languages}")

    if (download and extract) or (not download and not extract):
        logger.info("Downloading and extracting wiki dumps...")
        download_wiki_dumps(languages, date_dump, output_path)
        extract_wiki_dumps(languages, date_dump, output_path)
    elif download:
        logger.info("Downloading wiki dumps...")
        download_wiki_dumps(languages, date_dump, output_path)
    elif extract:
        logger.info("Extracting wiki dumps...")
        extract_wiki_dumps(languages, date_dump, output_path)


@cli.command(name="generate-phrases")
@click.option("--input-path", "-i", required=True, help="Path to an input file or a directory")
@click.option("--output-path", "-o", required=True, help="Path to a directory where to write the output file(s)")
@click.option("--phrase-length", type=int, default=3, help="Length of search phrase (amount of words)")
@click.option("--document-limit", type=int, default=10000, help="Maximum amount how many random documents to use")
@click.option("--document-top-phrases", type=int, default=5, help="How many top phrases to take from one document")
def generate_phrases(input_path: str,
                     output_path: str,
                     phrase_length: int,
                     document_limit: int,
                     document_top_phrases: int):
    """
    Generate search phrases from Wikipedia documents by applying TF-IDF
    on the data and finding top n ngrams for each document.
    """
    import os
    from .generate_search_phrase import generate_phrases

    if input_path:
        if os.path.isfile(input_path):
            logger.info(f"Generating search phrases for file {os.path.basename(input_path)}")
            generate_phrases(filename=input_path,
                             output_path=output_path,
                             document_limit=document_limit,
                             document_top_phrases=document_top_phrases,
                             phrase_length=phrase_length)

        elif os.path.isdir(input_path):
            if not os.listdir(input_path):
                logger.error("Provided input directory does not contain any files")
                return

            logger.info(f"Generating search phrases for files in directory {input_path}")
            for file in os.listdir(input_path):
                current_file = os.path.join(input_path, file)
                if os.path.isfile(current_file):
                    generate_phrases(filename=current_file,
                                     output_path=output_path,
                                     document_limit=document_limit,
                                     document_top_phrases=document_top_phrases,
                                     phrase_length=phrase_length)

        else:
            logger.error("Invalid input file or directory")
            return


@cli.command(name="yt-links")
@click.option("--input-path", "-i",
              required=True,
              type=str,
              help="File containing search phrases or a directory that contains multiple files with search phrases")
@click.option("--output-path", "-o",
              required=True,
              type=str,
              default="./",
              help="Output path where file(s) with valid video links will be saved")
@click.option("--max-videos",
              type=int,
              default=1000,
              help="Maximum amount how many video id-s to collect")
@click.option("--videos-per-phrase",
              type=int,
              default=1,
              help="How many videos to take from search results for each search phrase")
@click.option("--proxy",
              type=str,
              default=None,
              help="Proxy to use for youtube-dl downloads")
def search_yt_links(input_path: str,
                    output_path: str,
                    max_videos: int,
                    videos_per_phrase: int,
                    proxy: str):
    """
    Use text phrases to search for videos on Youtube, filter found videos and save suitable video id-s.
    """
    logger.debug(f"{input_path=}")
    logger.debug(f"{output_path=}")
    logger.debug(f"{max_videos=}")
    logger.debug(f"{videos_per_phrase=}")
    logger.debug(f"{proxy=}")
    pass


if __name__ == "__main__":
    cli()
