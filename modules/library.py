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


class Book:
    """
    Book class
    """
    def __init__(self, title, filename, tags, similar_books, authors, year):
        pass


class Library:
    pass
