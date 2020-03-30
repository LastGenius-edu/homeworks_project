# local file with API keys
import keys

# overall imports
# goodreads API for book lists and details
# Gutenberg API for plaintext books downloads
import os
from goodreads import client, request
from gutenberg.acquire import load_etext, get_metadata_cache, set_metadata_cache
from gutenberg.acquire.metadata import SleepycatMetadataCache
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

    print("\n\nStarted populating")
    # Starting and populating Gutenberg cache for fast metadata queries.
    # WARNING - TAKES A LOT OF TIME!!!!!!!!!!!!!!!!!!!!
    cache = SleepycatMetadataCache('/../cache/gutenberg/metadata/cache.db')
    cache.populate()
    set_metadata_cache(cache)
    print("\n\nFinished populating")

    print(get_metadata('title', 2701))

    for i in range(1, 3000):
        try:
            book = gc.book(i)
            print(f"{book.title} - published in {dict(dict(book.work)['original_publication_year'])['#text']}")
        except (request.GoodreadsRequestException, KeyError):
            continue


if __name__ == "__main__":
    main()
