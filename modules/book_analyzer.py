#!/usr/bin/env python3
"""
Sultanov Andriy
MIT License 2020
"""
import json
from book_downloader import search, download
from library import Library
from nltk.tokenize import word_tokenize


def html_body(background='#000000'):
    """
    Creates an html file with colored words
    """
    with open("colors.json", "r") as file:
        color_list = json.load(file)

    color_names = [color["name"] for color in color_list]

    color_words = [x for x in word_tokenize("I love red and white croissants") if x.lower() in color_names]
    color_values = [f'<p style="color:{color_list[color]}";>{color.upper()}</p>' for color in color_words]

    with open("test.html", "w") as file:
        file.write(f"""<body style="background-color:{background};">{''.join(color_values)}</body>""")


def main():
    library = Library()
    books = ["Moby Dick", "Macbeth"]
    book_list = search(books)
    print(book_list)
    download(book_list, library)


if __name__ == '__main__':
    # main()
    # painter()
    cleanup_colors()
