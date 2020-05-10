#!/usr/bin/env python3
"""
Sultanov Andriy
MIT License 2020
"""


def main():
    # Creating a new library instance
    library = Library()

    # Adding a new book
    library.add_book("Macbeth", "Macbeth.txt", "Shakespeare, William", 1606)
    # Created a new Category Author Shakespeare, William
    # Created a new Category Year 1606

    print(library.authors_list)
    # "CategoryList Authors: Category Shakespeare, William, contains these books <Macbeth, 1606>

    # Getting the list of all published years categories
    print(library.published_years)
    # "CategoryList Publication Years: Category 1606, contains these books <Macbeth, 1606>

    # Reading the text of the book
    for book in library.published_years[1606]:
        with open(book.filename, "r") as file:
            text = file.read

    # Reading the text of the book
    for book in library.authors_list["Shakespeare, William"]:
        with open(book.filename, "r") as file:
            text = file.read


if __name__ == '__main__':
    main()