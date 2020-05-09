#!/usr/bin/env python3
"""
Sultanov Andriy
MIT License 2020
"""


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

    # def __str__(self):
    #     return f"Category {self.name} contains these books: {str(self.books)}"

    def __repr__(self):
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

    def add_book(self, title, filename, authors, year):
        """
        Adds a book to the library, converting needed parameters
        to class instances for easier manipulation and search.
        """

        if title in self.general_book_list:
            return

        # If the Author category doesn't yet exist, create and remember him
        real_authors = []
        for author_name in authors:

            if author_name not in self.authors_list:
                self.authors_list.add_category(author_name)
                print(f"Created author {author_name}")

            real_authors.append(self.authors_list[author_name])

        # If the Year category doesn't yet exist, create and remember him
        if year not in self.published_years:
            self.published_years.add_category(year)
            print(f"Created year {year}")
        real_year = self.published_years[year]

        # Create a Book instance with pre-processed parameters
        book = Book(title, filename, real_authors, real_year)
        print(f"Created book {book}")

        # Adding the reference to this book to authors and published years categories
        for real_author in real_authors:
            real_author.add_book(book)
        self.published_years[year].add_book(book)

        # Add the book to the general bookshelf
        self.general_book_list.append(book)
