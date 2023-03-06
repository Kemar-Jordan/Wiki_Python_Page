from flaskr.backend import Backend
from flask import Flask, render_template, send_file


def make_endpoints(app):
    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page
        return render_template("main.html")

    # TODO(Project 1): Implement additional routes according to the project requirements.
    @app.route("/about")
    def about():
        backend = Backend('wiki-viewer-data')
        author_1 = backend.get_image('https://storage.googleapis.com/wiki-viewer-data/scooby.jpg')
        return render_template("about.html",author_1 = author_1)
