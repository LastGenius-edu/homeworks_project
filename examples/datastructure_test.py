# local file with API keys
import keys
import json

# goodreads API for book lists and details
# Gutenberg API for plaintext books downloads
import os
from goodreads import client, request
from gutenberg.acquire import load_etext, get_metadata_cache
# from gutenberg.acquire.metadata import SleepycatMetadataCache
from gutenberg.cleanup import strip_headers
from gutenberg.query import get_etexts, get_metadata


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


def main():
    """
    Main function of the test module
    """
    
    # setting up the API keys from local keys.py file
    goodreads_key = os.environ['GOODREADS_KEY']
    goodreads_secret = os.environ['GOODREADS_SECRET']

    # creating a client for book search and information retrieval
    gc = client.GoodreadsClient(goodreads_key, goodreads_secret)

    current_path = os.getcwd()

    file = open(os.path.join(current_path, "output", "log.json"), "w")

    gutenberg_titles = []

    # Getting the title of the first 3000 books on Project Gutenberg (EXTREMELY FAST)
    for i in range(1, 10):
        title = list(get_metadata('title', i))
        if title:
            # prepare the string for the file name
            filename = ''.join(e for e in title[0] if e.isalnum() or e == ' ') + ".txt"
            gutenberg_titles.append(filename[:-4])
            text = strip_headers(load_etext(i)).strip()
            with open(os.path.join(current_path, "output", filename), "w") as output_file:
                output_file.write(text)
    
    titles = dict()
    # Searching for the books on Goodreads, reading their metadata
    for book_title in gutenberg_titles:
        try:
            lst = gc.search_books(book_title, search_field='title')
            
            if not lst:
                continue
            else:
                book = lst[0]

            titles[book.title] = (book_title+".txt", str(book.popular_shelves), str(book.similar_books), str(book.authors), dict(dict(book.work)['original_publication_year'])['#text'])
        except (request.GoodreadsRequestException, KeyError, TypeError):
            continue
    
    json.dump(titles, file, indent=4)
    file.close()


if __name__ == "__main__":
    main()
