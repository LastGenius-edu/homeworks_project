#!/usr/bin/env python3
"""
Sultanov Andriy
MIT License 2020
"""
import json
import re
from book_downloader import search, download
from library import Library
from nltk.tokenize import word_tokenize


def cleanup_colors():
    """
    Just a temporary function to cleanup and combine
    a few files with colors from excess colors
    """
    existing_colors = {'amaranth': '#E52B50', 'amber': '#FFBF00', 'amethyst': '#9966CC', 'apricot': '#FBCEB1',
          'aquamarine': '#7FFFD4', 'azure': '#007FFF', 'baby blue': '#89CFF0', 'beige': '#F5F5DC', 'black': '#000000',
          'blue': '#0000FF', 'blue-green': '#0095B6', 'blue-violet': '#8A2BE2', 'blush': '#DE5D83', 'bronze': '#CD7F32',
          'brown': '#964B00', 'burgundy': '#800020', 'byzantium': '#702963', 'carmine': '#960018', 'cerise': '#DE3163',
          'cerulean': '#007BA7', 'champagne': '#F7E7CE', 'chartreuse green': '#7FFF00', 'chocolate': '#7B3F00',
          'cobalt blue': '#0047AB', 'coffee': '#6F4E37', 'copper': '#B87333', 'coral': '#FF7F50', 'crimson': '#DC143C',
          'cyan': '#00FFFF', 'desert sand': '#EDC9Af', 'electric blue': '#7DF9FF', 'emerald': '#50C878',
          'erin': '#00FF3F', 'gold': '#FFD700', 'gray': '#808080', 'green': '#00FF00', 'harlequin': '#3FFF00',
          'indigo': '#4B0082', 'ivory': '#FFFFF0', 'jade': '#00A86B', 'jungle green': '#29AB87', 'lavender': '#B57EDC',
          'lemon': '#FFF700', 'lilac': '#C8A2C8', 'lime': '#BFFF00', 'magenta': '#FF00FF', 'magenta rose': '#FF00AF',
          'maroon': '#800000', 'mauve': '#E0B0FF', 'navy blue': '#000080', 'ochre': '#CC7722', 'olive': '#808000',
          'orange': '#FF6600', 'orange-red': '#FF4500', 'orchid': '#DA70D6', 'peach': '#FFE5B4', 'pear': '#D1E231',
          'periwinkle': '#CCCCFF', 'persian blue': '#1C39BB', 'pink': '#FD6C9E', 'plum': '#8E4585',
          'prussian blue': '#003153', 'puce': '#CC8899', 'purple': '#800080', 'raspberry': '#E30B5C', 'red': '#FF0000',
          'red-violet': '#C71585', 'rose': '#FF007F', 'ruby': '#E0115F', 'salmon': '#FA8072', 'sangria': '#92000A',
          'sapphire': '#0F52BA', 'scarlet': '#FF2400', 'silver': '#C0C0C0', 'slate gray': '#708090',
          'spring bud': '#A7FC00', 'spring green': '#00FF7F', 'tan': '#D2B48C', 'taupe': '#483C32', 'teal': '#008080',
          'turquoise': '#40E0D0', 'ultramarine': '#3F00FF', 'violet': '#7F00FF', 'viridian': '#40826D',
          'white': '#FFFFFF', 'yellow': '#FFFF00'}

    real_colors = []
    color_names = []

    for name, value in existing_colors.items():
        real_colors.append({"value": value, "name": name})

    with open("colors.json", "r") as file:
        colors = json.load(file)

        for color in colors:
            if re.match(r".* \d", color['name']) is None and color["name"] not in color_names:
                real_colors.append({"value": color["value"], "name": color["name"]})
                color_names.append(color["name"])

    with open("colors.json", "w") as file:
        json.dump(real_colors, file, indent=4)


def color_book():
    return [x for x in word_tokenize("I love red and white croissants") if x.lower() in COLORS]


def html_color(color):
    return f'<p style="color:{COLORS[color]}";>{color.upper()}</p>'


def html_body(colors, background='#000000'):
    with open("test.html", "w") as file:
        file.write(f"""<body style="background-color:{background};">
                   {''.join([html_color(color) for color in colors])}
                   </body>""")


def painter():
    color_words = color_book()
    print(html_body(color_words))


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
