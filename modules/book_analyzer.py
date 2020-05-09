#!/usr/bin/env python3
"""
Sultanov Andriy
MIT License 2020
"""
from book_downloader import search, download
from library import Library


def main():
    library = Library()
    books = ["Moby Dick", "Macbeth"]
    book_list = search(books)
    print(book_list)
    download(book_list, library)


if __name__ == '__main__':
    main()
