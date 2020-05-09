#!/usr/bin/env python3
"""
Sultanov Andriy
MIT License 2020
"""


class Author:
    """
    Author class
    """
    def __init__(self, name):
        """
        Creates an author object to contain author's books
        :name: str
        """
        self.name = name
        self.books = []

    def add_books(self, book):
        """
        Adds books to the author's instance
        """
        assert isinstance(book, Book), "Instance of Book class should be provided"
        self.books.append(book)


class AuthorList:
    """
    AuthorList class - a container for authors
    """
    def __init__(self):
        """
        Creates the AuthorList instance
        """
        self.author_list = []

    def add_author(self, name):
        """
        Adds the author to the list
        """
        self.author_list.append(Author(name))

    def __getitem__(self, item):
        assert item in self, "Can only get existing authors"

        for author in self.author_list:
            if author.name == item:
                return author

    def __contains__(self, item):
        """
        Checks if the author with the name already exists
        """
        for author in self.author_list:
            if author.name == item:
                return True
        return False


class Book:
    """
    Book class
    """
    def __init__(self, title, filename, authors, year):
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
        self.general_book_list = []
        self.authors_list = AuthorList()

    def add_book(self, title, filename, authors, year):
        real_authors = []

        for author_name in authors:

            if author_name not in self.authors_list:
                self.authors_list.add_author(author_name)

            real_authors.append(self.authors_list[author_name])

        book = Book(title, filename, real_authors, year)
        self.general_book_list.append(book)
