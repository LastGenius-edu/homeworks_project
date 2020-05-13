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

HOME = os.getcwd()
with open(os.path.join(HOME, "..", "output", "log.json"), "r") as file:
    TITLES = json.load(file)


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Function for the main page, handling all the user input
    """
    logger.info("INDEX")
    if request.method == "GET":
        logger.info("GET")
        return render_template("main_page.html")

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
        return render_template(os.path.join("books", f"{title}.html"))
    else:
        return redirect(url_for(error))


@app.route("/error")
def error():
    """
    (None) -> None

    Function that loads the error page
    """
    return render_template("error.html")
