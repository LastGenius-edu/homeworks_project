#!/usr/bin/env python3
"""
Sultanov Andriy
MIT License 2020
"""
import json
import logging
import os.path
from flask import Flask, redirect, render_template, request, url_for


# Setting up Flask
app = Flask(__name__)
app.config["DEBUG"] = True

# Setting up the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HOME = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(HOME, "static", "output", "log.json"), "r") as file:
    TITLES = json.load(file)


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Function for the main page, handling all the user input
    """
    logger.info("INDEX")
    if request.method == "GET":
        logger.info("GET")
        print(url_for('static', filename='css/style.css'))
        return render_template("home.html")

    if request.method == "POST":
        logger.info("POST")


@app.route("/title")
def title():
    """
    (None) -> None

    Function that loads the error page
    """
    title = request.args.get('title')
    if title in TITLES:
        return render_template(f"books/{title}.html")
    else:
        return redirect(url_for(error))


@app.route("/category")
def category():
    """
    (None) -> None

    Function that loads the error page
    """
    title = request.args.get('title')
    try:
        return render_template(f"categories/{title}.html")
    except FileNotFoundError:
        return redirect(url_for(error))


@app.route("/error")
def error():
    """
    (None) -> None

    Function that loads the error page
    """
    return render_template("error.html")


if __name__ == '__main__':
    app.run(debug=True)
