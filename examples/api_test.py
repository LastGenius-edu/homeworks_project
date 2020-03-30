# local file with API keys
import keys

# overall imports
# goodreads API for book lists and details
# Gutenberg API for plaintext books downloads
import os
from goodreads import client, request


# setting up the API keys from local file
goodreads_key = os.environ['GOODREADS_KEY']
goodreads_secret = os.environ['GOODREADS_SECRET']

gc = client.GoodreadsClient(goodreads_key, goodreads_secret)

for i in range(1, 3000):
    try:
        book = gc.book(i)
        print(f"{book.title} - published in {dict(dict(book.work)['original_publication_year'])['#text']}")
    except (request.GoodreadsRequestException, KeyError):
        continue
