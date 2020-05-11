#!/usr/bin/env python3
"""
Sultanov Andriy
MIT License 2020
"""
from book_downloader import search, download
from library import Library


def run():
    book_list = []
    author_list = []

    with open("book_list.txt", "r") as file:
        for line in file.readlines():
            book_list.append(line.replace("\n", "").capitalize())

    with open("author_list.txt", "r") as file:
        for line in file.readlines():
            author_list.append(line.replace("\n", ""))

    library = Library()
    books = search(book_list, author_list) + [2701]
    print(books)
    download(books, library)


if __name__ == '__main__':
    run()
