# local file with API keys
import keys

# overall imports
# goodreads API for book lists and details
# Gutenberg API for plaintext books downloads
import os
from goodreads import client, request
from gutenberg.acquire import load_etext, get_metadata_cache
# from gutenberg.acquire.metadata import SleepycatMetadataCache
from gutenberg.cleanup import strip_headers
from gutenberg.query import get_etexts, get_metadata


def main():
    """
    Main function of the test module
    """
    
    # setting up the API keys from local keys.py file
    goodreads_key = os.environ['GOODREADS_KEY']
    goodreads_secret = os.environ['GOODREADS_SECRET']

    # creating a client for book search and information retrieval
    gc = client.GoodreadsClient(goodreads_key, goodreads_secret)

    # Starting and populating Gutenberg cache for fast metadata queries.
    # WARNING - TAKES A LOT OF TIME!!!!!!!!!!!!!!!!!!!! (For me was around an hour)
    # NEEDS TO BE DONE ONLY ONCE!!!!!!!!
    # print("\n\nStarted populating")
    # cache = get_metadata_cache()
    # cache.populate()
    # print("\n\nFinished populating")

    current_path = os.getcwd()

    file = open(os.path.join(current_path, "output", "log.txt"), "a")

    # Getting the title of the first 3000 books on Project Gutenberg (EXTREMELY FAST)
    for i in range(1, 10):
        title = list(get_metadata('title', i))
        if title:
            # prepare the string for the file name
            filename = ''.join(e for e in title[0] if e.isalnum()) + ".txt"
            text = strip_headers(load_etext(i)).strip()
            with open(os.path.join(current_path, "output", filename), "w") as output_file:
                output_file.write(text)
            file.write(f"{title[0]} plaintext saved to '{title[0]}.txt'\n")

    # Getting the titles and publishing years for the first 3000 books on Goodreads
    # Pretty slow because Goodreads allows 1 request per second
    for i in range(1, 20):
        try:
            book = gc.book(i)
            file.write(f"{book.title} - published in {dict(dict(book.work)['original_publication_year'])['#text']}\n")
        except (request.GoodreadsRequestException, KeyError):
            continue


if __name__ == "__main__":
    main()
