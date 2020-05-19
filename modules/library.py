#!/usr/bin/env python3
"""
Sultanov Andriy
MIT License 2020
"""
import os
import json
import nltk
import pylab
import logging
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import names
import webpage_generation


# Setting up the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HOME = os.path.dirname(os.path.realpath(__file__))


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
        """
        Generates a webpage for the category
        """
        with open(os.path.join(HOME, "templates", "categories", f"{self.name}.html"), "w") as file:
            file.write(webpage_generation.category_page(self))

        logger.info(f" Generated webpage for {self.name}")

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

    def __getitem__(self, item):
        """
        Returns one of the categories from name
        """
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

    def generate_webpage(self, title):
        webpage = webpage_generation.category_list_page(self)

        with open(os.path.join(HOME, "templates", "categories", title), "w") as file:
            file.write(webpage)


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
        self.frequency_dist = dict()

        text = self.get_text()
        self.get_most_popular_words(text)
        self.generate_wordcloud()
        self.generate_colorwords(text)
        self.generate_dispersion_plot(text)
        self.generate_name_dispersion_plot(text)
        self.generate_webpage()

    def get_text(self):
        """
        Reads the file and returns plaintext in a string
        """
        filename = os.path.join(HOME, "static", "output", "books", self.filename)
        with open(filename, "r", errors="ignore", encoding="UTF-8") as file:
            text = file.read()
        return text

    def get_most_popular_words(self, text):
        """
        Gets 100 most popular words and their frequency
        """
        all_stopwords = set(stopwords.words('english'))

        words = nltk.word_tokenize(text)

        # Remove single-character tokens (mostly punctuation)
        words = [word for word in words if len(word) > 1]

        # Remove numbers
        words = [word for word in words if not word.isnumeric()]

        # Lowercase all words (default_stopwords are lowercase too)
        words = [word.lower() for word in words]

        # Remove stopwords
        words = [word for word in words if word not in all_stopwords]

        # Calculate frequency distribution
        frequency_dist = nltk.FreqDist(words)

        for word, frequency in frequency_dist.most_common(500):
            self.frequency_dist[word] = frequency

        logger.info(f" Generated 500 popular words for the {self.title}")

    def generate_wordcloud(self):
        """
        Creates a wordcloud based on frequency of words
        Saves into a jpg image
        """
        # Path for the font for the image
        font_path = os.path.join(HOME, "static", "output", "wordclouds", "Montserrat-Bold.ttf")

        # Generating a WordCloud from the previously  made frequency dict
        wc = WordCloud(font_path=font_path, background_color="#1D1D1D",
                       max_words=1000, max_font_size=135, width=1080, height=1080)
        wc.generate_from_frequencies(self.frequency_dist)

        # Save the image
        image = wc.to_image()
        image.save(os.path.join(HOME, "static", "output", "wordclouds", f"{self.title}.jpg"))

        logger.info(f" Generated word clouds for {self.title}")

    def generate_colorwords(self, text):
        """
        Creates an html file with colored words
        """
        # Load the list of all colors
        with open("colors.json", "r") as file:
            color_list = json.load(file)

        # Find all the colors mentioned in the book and assign a hex value to them
        color_words = [x for x in word_tokenize(text) if x.lower() in color_list]
        color_values = [f'<p style="color:{color_list[color.lower()]}";>{color.upper()} </p>' for color in color_words]

        # Save the paragraphs with words and values for further HTML use
        with open(os.path.join(HOME, "static", "output", "wordcolors", f"{self.title}.html"), "w") as file:
            file.write(f"""{''.join(color_values[:250])}</body>""")

        logger.info(f" Generated colorwords for {self.title}")

    @staticmethod
    def __dispersion_graph(text, words, filepath):
        """
        Generates a dispersion graph from text for words.
        Saves the png in filepath

        Based on source code from nltk.draw modules
        """
        # Set some figure parameters
        fig = plt.figure(figsize=(18, 7), dpi=250)
        plt.rcParams['axes.facecolor'] = "#191919"

        # Reverse the words and generate the points for the graph
        words.reverse()
        points = [(x, y) for x in range(len(text))
                  for y in range(len(words))
                  if text[x] == words[y]]

        # Generate the plot and the titles with needed colors
        x, y = zip(*points)
        pylab.plot(x, y, "b|", scalex=.1, color="#BB86FC")
        pylab.yticks(range(len(words)), words, color="#BB86FC")
        pylab.xticks(color="#BB86FC")
        pylab.ylim(-1, len(words))
        title_obj = pylab.title("", color="#BB86FC")
        plt.setp(title_obj, color="#BB86FC")
        pylab.xlabel("Word Offset", color="#BB86FC")
        pylab.savefig(filepath, facecolor="#1D1D1D", edgecolor="none")

    def generate_dispersion_plot(self, text):
        """
        Generates dispersion plot of top 10 words by frequency
        """
        # Turn the tokenized text into NTLK class for method use
        my_text = nltk.Text(word_tokenize(text))
        my_text = list(my_text)

        # Generate a list of top-10 words by their frequency and save the image
        words = list(self.frequency_dist.keys())[:10]
        filepath = os.path.join(HOME, "static", "output", "dispersion", f"{self.title}.png")
        self.__dispersion_graph(my_text, words, filepath)

        logger.info(f" Finished generating dispersion plots for top 10 words of {self.title}")

    def generate_name_dispersion_plot(self, text):
        """
        Generates dispersion plot of names, supposedly
        """

        # Lookup all the possible male and female names from the lists
        male_names = names.words("male.txt")
        female_names = names.words("female.txt")
        met_male_names, met_female_names = dict(), dict()

        # Search for all the instances of names in the text, save the frequency
        for word in word_tokenize(text):
            if word in male_names:
                value = met_male_names.get(word, 0)
                met_male_names[word] = value + 1
            if word in female_names:
                value = met_female_names.get(word, 0)
                met_female_names[word] = value + 1

        # Save top-10 met names by their frequency
        met_male_names = [k for k, v in sorted(met_male_names.items(), key=lambda item: item[1], reverse=True)[:10]]
        met_female_names = [k for k, v in sorted(met_female_names.items(), key=lambda item: item[1], reverse=True)[:10]]

        my_text = list(nltk.Text(word_tokenize(text)))

        # Save top-10 male met names by frequency in a plot image
        filepath = os.path.join(HOME, "static", "output", "malenames", f"{self.title}.png")
        self.__dispersion_graph(my_text, list(met_male_names), filepath)

        # Save top-10 female met names by frequency in a plot image
        filepath = os.path.join(HOME, "static", "output", "femalenames", f"{self.title}.png")
        self.__dispersion_graph(my_text, list(met_female_names), filepath)

        logger.info(f" Finished generating names dispersion plots for {self.title}")

    def generate_webpage(self):
        """
        Generates a webpage for the book with linked name and graphs
        """
        # Looks up HTML paragraphs of met colors
        with open(os.path.join(HOME, "static", "output", "wordcolors", f"{self.title}.html"), "r") as file:
            wordcolor = file.read()

        # Save the webpage
        with open(os.path.join(HOME, "templates", "books", f"{self.title}.html"), "w") as file:
            file.write(webpage_generation.book_page(self.title, wordcolor))

        logger.info(f" Generated webpage for {self.title}")

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
            logger.info(f" Created author {author}")
        real_author = self.authors_list[author]

        if year not in self.published_years:
            self.published_years.add_category(year)
            logger.info(f" Created year {year}")
        real_year = self.published_years[year]

        # Create a Book instance with pre-processed parameters
        book = Book(title, filename, real_author, real_year)

        # Adding the reference to this book to authors and published years categories
        self.authors_list[author].add_book(book)
        self.published_years[year].add_book(book)

        logger.info(f" Created book {book}")

        # Add the book to the general bookshelf
        self.general_book_list.append(book)

    def generate_freqdist(self):
        """
        Generates frequency word ditribution for all the books on a timeline
        """
        # top_ten_list = dict()
        # for book in self.general_book_list:
        #     for word, value in book.frequency_dist.items():
        #         value = top_ten_list.get(word, 0) + value
        #         top_ten_list[word] = value
        #
        # top_ten_list = {k: v for k, v in sorted(top_ten_list.items(), key=lambda item: item[1], reverse=True)[:10]}

        # cfd = nltk.ConditionalFreqDist()
        # for book in self.general_book_list:
        #     condition = book.year
        #     top_ten = {k: v for k, v in
        #                sorted(book.frequency_dist.items(), key=lambda item: item[1], reverse=True)[:10]}
        #     for word, value in top_ten.items():
        #         cfd[condition][word] = value

        # logger.info(" Generated Frequency Distribution for all books")

        # cfd.plot()

    def generate_webpage(self):
        """
        Generates homepage
        """
        homepage = webpage_generation.home_page(self.general_book_list, self.authors_list.categories, self.published_years.categories, None)
        with open(os.path.join(HOME, "templates", "home.html"), "w") as file:
            file.write(homepage)

        logger.info(" Finished generating the home page")

        self.authors_list.generate_webpage("authors.html")
        self.published_years.generate_webpage("years.html")

        books_page = webpage_generation.book_list_page(self.general_book_list)
        with open(os.path.join(HOME, "templates", "categories", "books.html"), "w") as file:
            file.write(books_page)

        for category in self.authors_list.categories:
            category.generate_webpage()

        for category in self.published_years.categories:
            category.generate_webpage()
