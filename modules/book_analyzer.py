#!/usr/bin/env python3
"""
Sultanov Andriy
MIT License 2020
"""
import json
import os.path
from book_downloader import search, download
from library import Library
from nltk.tokenize import word_tokenize


def html_body(text, filename, background='#191919'):
    """
    Creates an html file with colored words
    """
    current_path = os.getcwd()

    with open("colors.json", "r") as file:
        color_list = json.load(file)

    color_words = [x for x in word_tokenize(text) if x.lower() in color_list]
    color_values = [f'<p style="color:{color_list[color.lower()]}";>{color.upper()} </p>' for color in color_words]

    with open(os.path.join(current_path, "output", filename), "w") as file:
        file.write(f"""<head><meta charset="utf-8">
                   <link rel="stylesheet" type="text/css" href="style.css">
                   </head>
                   <body style="background-color:{background};">
                   {''.join(color_values)}</body>""")


def main():
    current_path = os.getcwd()
    library = Library()
    books = ["Macbeth"]
    book_list = search(books) + [2701]
    print(book_list)
    download(book_list, library)

    for book in library.general_book_list:
        filename = os.path.join(current_path, "output", "books", book.filename)
        with open(filename, "r", encoding="UTF-8", errors="ignore") as file:
            text = file.read()
            html_body(text, book.title + ".html")


if __name__ == '__main__':
    main()
