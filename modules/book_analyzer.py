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

import os
import re
import multidict as multidict
from wordcloud import WordCloud
from PIL import Image


# Home folder for further use
HOME = os.getcwd()


def wordcloud_analyzer(text, filename):
    """
    Creates a wordcloud based on frequency of words
    Saves into a jpg image
    """

    # Making dict for counting frequencies
    fullTermsDict = multidict.MultiDict()
    tmpDict = {}

    for word in text.split(" "):
        if re.match(r"a|the|an|the|to|in|for|of|or|by|with|is|on|that|be", word) or len(word) < 3:
            continue
        val = tmpDict.get(word, 0)
        tmpDict[word.lower()] = val + 1
    for key in tmpDict:
        fullTermsDict.add(key, tmpDict[key])

    # Path for the font for the image
    font_path = os.path.join(HOME, "output", "wordclouds", "Montserrat-Bold.ttf")

    # Generating a WordCloud from the previously  made frequency dict
    wc = WordCloud(font_path=font_path, background_color="#1D1D1D",
                   max_words=1000, max_font_size=135, width=1080, height=1080)
    wc.generate_from_frequencies(fullTermsDict)

    # Save the image
    image = wc.to_image()
    # image.show()
    image.save(os.path.join(HOME, "output", "wordclouds", filename))


def color_analyzer(text, filename, background='#191919'):
    """
    Creates an html file with colored words
    """

    with open("colors.json", "r") as file:
        color_list = json.load(file)

    color_words = [x for x in word_tokenize(text) if x.lower() in color_list]
    color_values = [f'<p style="color:{color_list[color.lower()]}";>{color.upper()} </p>' for color in color_words]

    with open(os.path.join(HOME, "output", "wordcolors", filename), "w") as file:
        file.write(f"""<head><meta charset="utf-8">
                   <link rel="stylesheet" type="text/css" href="style.css">
                   </head>
                   <body style="background-color:{background};">
                   {''.join(color_values)}</body>""")


def main():
    library = Library()
    books = ["Macbeth"]
    book_list = search(books) + [2701]
    print(book_list)
    download(book_list, library)

    for book in library.general_book_list:
        filename = os.path.join(HOME, "output", "books", book.filename)
        with open(filename, "r", encoding="UTF-8", errors="ignore") as file:
            text = file.read()
            color_analyzer(text, book.title + ".html")
            wordcloud_analyzer(text, book.title + ".jpg")


if __name__ == '__main__':
    main()
