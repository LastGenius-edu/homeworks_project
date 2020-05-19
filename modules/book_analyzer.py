#!/usr/bin/env python3
"""
Sultanov Andriy
MIT License 2020
"""
from book_downloader import search, download
from library import Library


def run():
    book_list = ["Macbeth"]
    author_list = []

    with open("book_list.txt", "r") as file:
        for line in file.readlines():
            book_list.append(line.replace("\n", "").capitalize())

    with open("author_list.txt", "r") as file:
        for line in file.readlines():
            author_list.append(line.replace("\n", ""))

    library = Library()
    print("Created library instance")
    # books = [2701, 215, 1400, 1342, 1952] + search(book_list, author_list)
    books = [2701, 215, 1400, 1342, 1952]
    download(books, library)
    print("Finished downloading")
    library.generate_webpage()


if __name__ == '__main__':
    run()
