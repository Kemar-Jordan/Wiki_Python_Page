from flaskr.backend import Backend
from flask import Flask, render_template, send_file, request, redirect, url_for


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
        author_1 = backend.get_image('kemar.jpg')
        author_2 = backend.get_image('danielle.jpg')
        author_3 = backend.get_image('kris.JPG')
        return render_template('about.html',author_1 = author_1, author_2 = author_2, author_3 = author_3)

    # Sign up route
    @app.route("/signup",methods=['GET','POST'])
    def sign_up():
        backend = Backend('wiki-credentials')
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if backend.sign_up(username, password):
                return redirect(url_for('login'))
            else:
                return "Username already exists"
        else:
            return render_template('signup.html')


    # Login route
    @app.route("/signin",methods=['GET','POST'])
    def login():
        backend = Backend('wiki-credentials')
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if backend.sign_in(username, password) == True:
                return render_template('logged_in.html', username = username)
            else:
                return "Password is incorrect"
        else:
            return render_template('signin.html')


    # Pages route
    @app.route("/pages")
    def pages():
        return render_template('pages.html')

     # Pages route
    @app.route("/loggedin")
    def logged_in():
        backend = Backend('wiki-credentials')
        return render_template('logged_in.html')

