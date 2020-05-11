#!/usr/bin/env python3
"""
Sultanov Andriy
MIT License 2020
"""
import os
import re
import json
import multidict as multidict
from wordcloud import WordCloud
from PIL import Image
from nltk.tokenize import word_tokenize


class Category:
    """
    Category class
    Acts as an Author, Year
    """
    def __init__(self, name):
        """
        Creates a Category object to contain category's books
        :name: str
        """
        self.name = name
        self.books = []

    def add_book(self, book):
        """
        Adds books to the author's instance
        """
        assert isinstance(book, Book), "Instance of Book class should be provided"
        self.books.append(book)

    def generate_webpage(self):
        pass

    def __str__(self):
        """
        Returns a string representation of Category object
        """
        return f"Category {self.name} contains these books: {str(self.books)}"

    def __repr__(self):
        """
        Returns a shorter string representation of Category object
        """
        return f"<Category {self.name}, size={len(self.books)}>"


class CategoryList:
    """
    CategoryList class - a container for categories
    """
    def __init__(self, name):
        """
        Creates the CategoryList instance
        """
        self.name = name
        self.categories = []

    def add_category(self, name):
        """
        Adds the author to the list
        """
        self.categories.append(Category(name))

    def generate_webpage(self):
        pass

    def __getitem__(self, item):
        assert self.__contains__(item), "Can only get existing categories"

        for category in self.categories:
            if category.name == item:
                return category

    def __contains__(self, item):
        """
        Checks if the category with the name already exists
        """
        for category in self.categories:
            if category.name == item:
                return True
        return False

    def __str__(self):
        """
        Returns a string representation of CategoryList container
        """
        return f"CategoryList {self.name}: {', '.join(category.__repr__() for category in self.categories)}"


class Book:
    """
    Book class
    """
    def __init__(self, title, filename, authors, year):
        """
        Initializes a Book instance

        :title: str
        :filename: str
        :authors: List[Author]
        :year: Year
        """
        self.title = title
        self.filename = filename
        self.authors = authors
        self.year = year

        text = self.get_text()
        self.generate_wordcloud(text)
        self.generate_colorwords(text)
        self.generate_webpage()

    def get_text(self):
        """
        Reads the file and returns plaintext in a string
        """
        cur_path = os.getcwd()
        filename = os.path.join(cur_path, "output", "books", self.filename)
        with open(filename, "r", errors="ignore", encoding="UTF-8") as file:
            text = file.read()
        return text

    def generate_wordcloud(self, text):
        """
        Creates a wordcloud based on frequency of words
        Saves into a jpg image
        """
        home = os.getcwd()
        # Making dict for counting frequencies
        full_terms_dict = multidict.MultiDict()
        tmp_dict = {}

        for word in text.split(" "):
            if re.match(r"a|the|an|the|to|in|for|of|or|by|with|is|on|that|be", word) or len(word) < 4:
                continue
            val = tmp_dict.get(word, 0)
            tmp_dict[word.lower()] = val + 1
        for key in tmp_dict:
            full_terms_dict.add(key, tmp_dict[key])

        # Path for the font for the image
        font_path = os.path.join(home, "output", "wordclouds", "Montserrat-Bold.ttf")

        # Generating a WordCloud from the previously  made frequency dict
        wc = WordCloud(font_path=font_path, background_color="#1D1D1D",
                       max_words=1000, max_font_size=135, width=1080, height=1080)
        wc.generate_from_frequencies(full_terms_dict)

        # Save the image
        image = wc.to_image()
        image.save(os.path.join(home, "output", "wordclouds", f"{self.title}.jpg"))

        print(f"Generated word clouds for {self.title}")

    def generate_colorwords(self, text):
        """
        Creates an html file with colored words
        """
        home = os.getcwd()

        with open("colors.json", "r") as file:
            color_list = json.load(file)

        color_words = [x for x in word_tokenize(text) if x.lower() in color_list]
        color_values = [f'<p style="color:{color_list[color.lower()]}";>{color.upper()} </p>' for color in color_words]

        with open(os.path.join(home, "output", "wordcolors", f"{self.title}.html"), "w") as file:
            file.write(f"""<head><meta charset="utf-8">
                           <link rel="stylesheet" type="text/css" href="style.css">
                           </head><body">{''.join(color_values)}</body>""")

        print(f"Generated colorwords for {self.title}")

    def generate_webpage(self):
        pass

    def __str__(self):
        """
        Returns a string representation of a book object
        """
        return f"<{self.title}> - written by {self.authors}, published in {self.year}"

    def __repr__(self):
        """
        Returns a string representation of a book object for a list
        """
        return f"<{self.title}>"


class Library:
    def __init__(self):
        """
        Initializes Library class instance with empty book shelf and no authors.
        """
        self.general_book_list = []
        self.authors_list = CategoryList("Authors")
        self.published_years = CategoryList("Years")

    def add_book(self, title, filename, author, year):
        """
        Adds a book to the library, converting needed parameters
        to class instances for easier manipulation and search.
        """

        # If the book has already been added, don't do anything
        if title in self.general_book_list:
            return

        # If author or year category don't exist, create them
        # And remember for further easier linking
        if author not in self.authors_list:
            self.authors_list.add_category(author)
            print(f"Created author {author}")
        real_author = self.authors_list[author]

        if year not in self.published_years:
            self.published_years.add_category(year)
            print(f"Created year {year}")
        real_year = self.published_years[year]

        # Create a Book instance with pre-processed parameters
        book = Book(title, filename, real_author, real_year)

        # Adding the reference to this book to authors and published years categories
        self.authors_list[author].add_book(book)
        self.published_years[year].add_book(book)

        print(f"Created book {book}")

        # Add the book to the general bookshelf
        self.general_book_list.append(book)

    def generate_webpage(self):
        pass