#!/usr/bin/env python3
"""
Sultanov Andriy
MIT License 2020
"""
# local file with API keys
import keys

# General imports
import json
import logging
import os
import sys
import gutenberg_cleaner as cleaner
from goodreads import client, request # Goodreads API for book lists and details
from gutenberg.acquire import load_etext, get_metadata_cache # Gutenberg API for plaintext books downloads
from gutenberg.cleanup import strip_headers
from gutenberg.query import get_etexts, get_metadata, list_supported_metadatas
from gutenberg._domain_model.exceptions import UnknownDownloadUriException
from json.decoder import JSONDecodeError


# Setting up the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def populate_cache():
    """
    Starting and populating Gutenberg cache for fast metadata queries.
    WARNING - TAKES A LOT OF TIME!!!!!
    (For me was around an hour)
    NEEDS TO BE DONE ONLY ONCE!!!!!!!!
    """
    print("\n\nStarted populating")
    cache = get_metadata_cache()
    cache.populate()
    print("\n\nFinished populating")


def searcher(title_list, authors_list):
    """
    Receives two lists of books to download.
    Searches for their availability on Gutenberg and returns list of gutenberg IDs.
    """
    book_list = set()

    print(list_supported_metadatas())

    for title in title_list:
        found_texts = get_etexts("title", title)
        if found_texts:
            book_list.add(found_texts[0])

    for author in authors_list:
        found_texts = get_etexts("author", author)
        if found_texts:
            book_list.add(found_texts[0])

    return book_list


def download(book_list):
    """
    Downloads and cleans up books from the List of Gutenberg IDs.
    """

    # setting up the API keys from local keys.py file
    goodreads_key = os.environ['GOODREADS_KEY']
    goodreads_secret = os.environ['GOODREADS_SECRET']

    # creating a client for book search and information retrieval
    gc = client.GoodreadsClient(goodreads_key, goodreads_secret)

    current_path = os.getcwd()

    try:
        with open(os.path.join(current_path, "output", "read_list.json"), "r") as file:
            read_list = json.load(file)
    except (FileNotFoundError, JSONDecodeError):
        read_list = []

    gutenberg_titles = []
    # Getting the title of the first 3000 books on Project Gutenberg (EXTREMELY FAST)
    for book_number in book_list:
        title = list(get_metadata('title', book_number))

        if title:
            # prepare the string for the file name
            filename = ''.join(e for e in title[0] if e.isalnum() or e == ' ') + ".txt"

            if filename[:-4] in read_list:
                logger.info(f" File <{filename[:35]}...> already processed and downloaded")
                continue
            try:
                text = strip_headers(load_etext(book_number)).strip()
                text = cleaner.simple_cleaner(text)
            except UnknownDownloadUriException:
                continue

            read_list.append(filename[:-4])
            gutenberg_titles.append(filename[:-4])
            with open(os.path.join(current_path, "output", "books", filename), "w") as output_file:
                output_file.write(text)
            logger.info(f" File <{filename[:35]}...> download finished")

    with open(os.path.join(current_path, "output", "read_list.json"), "w") as file:
        json.dump(read_list, file, indent=4)

    logger.info(" Plaintext files download is finished")

    try:
        with open(os.path.join(current_path, "output", "log.json"), "r") as file:
            titles = json.load(file)
    except FileNotFoundError:
        titles = dict()

    # Searching for the books on Goodreads, reading their metadata
    for book_title in gutenberg_titles:
        try:
            lst = gc.search_books(book_title, search_field='title')

            if not lst:
                continue
            else:
                book = lst[0]

            logger.info(f" Found Goodreads metadata for <{book_title[:35]}...>")
            titles[book.title] = (book_title + ".txt", str(book.popular_shelves),
                                  str(book.similar_books), str(book.authors),
                                  dict(dict(book.work)['original_publication_year'])['#text'])

        except (request.GoodreadsRequestException, KeyError, TypeError):
            continue

    with open(os.path.join(current_path, "output", "log.json"), "w") as file:
        json.dump(titles, file, indent=4)

    logger.info("Metadata files download is finished")


if __name__ == "__main__":
    download("Moby Dick")
