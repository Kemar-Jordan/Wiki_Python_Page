from flaskr.backend import Backend
from flask import Flask, render_template, send_file


def make_endpoints(app):
    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page
        return render_template("home.html")

    # TODO(Project 1): Implement additional routes according to the project requirements.
    @app.route("/about")
    def about():
        backend = Backend('wiki-viewer-data')
        author_1 = 'https://storage.googleapis.com/wiki-viewer-data/kemar.jpg'
        author_2 = 'https://storage.googleapis.com/wiki-viewer-data/danielle.jpg'
        return render_template('about.html',author_1 = author_1,author_2 = author_2,get_image=backend.get_image)

    # Sign up route
    @app.route("/signup")
    def sign_up():
        return render_template('signup.html')

    # Login route
    @app.route("/login")
    def login():
        return render_template('login.html')

    # Pages route
    @app.route("/pages")
    def pages():
        return render_template('pages.html')
