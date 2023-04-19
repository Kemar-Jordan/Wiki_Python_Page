from flaskr.backend import Backend
from flask import Flask, render_template, send_file, request, redirect, url_for, session, make_response
from werkzeug.utils import secure_filename
from firebase import firebase
from datetime import datetime
import pandas as pd
import json
import plotly
import plotly.express as px

firebase_url = "https://wikigroup10-default-rtdb.firebaseio.com/"
firebase = firebase.FirebaseApplication(firebase_url, None)


def make_endpoints(app):
    """ Defines all the routes in the application

    Args:

    app: instance of a flask applciation.

    Returns: Flask route selected.
    """

    @app.route("/")
    def home():
        value = request.cookies.get('value')
        username = request.cookies.get('username')
        welcome = request.cookies.get('welcome')
        return render_template("home.html",
                               value=value,
                               username=username,
                               welcome=welcome)

    """ Defines the route URL or home page of the applciation.

    Args:  None.

    Returns: a render template of the home html page.
    It retrieves values from cookies: value, username and welcome using "request.cookies.get()
    and renders "home.html"

    """

    @app.route("/about")
    def about():
        backend = Backend('wiki-viewer-data')
        author_1 = backend.get_image('kemar_j.jpg')
        author_2 = backend.get_image('danielle.jpg')
        author_3 = backend.get_image('kris.jpg')
        value = request.cookies.get('value')
        username = request.cookies.get('username')
        welcome = True
        resp = make_response(
            render_template("about.html",
                            author_1=author_1,
                            author_2=author_2,
                            author_3=author_3,
                            value=value,
                            username=username,
                            welcome=welcome))
        resp.set_cookie('welcome', '', expires=0)
        return resp

    """ Defines the "/about" URL of the application.

    Args:

    None

    Returns: a render template of the about html page. It retrieves 
    an image for three authors using backend.get_image() and values from
    cookies and 'value' and 'username'.
    """

    # Sign up route
    @app.route("/signup", methods=['GET', 'POST'])
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

    """ Defines the "/signup" URL of the application.

    Args:

    None

    Returns: Checks to see whether user has signed in correctly. If HTTP request method is POST, 
    it retrieves the username and password from the form data and then calls the backend.sign_up()
    to sign the user up and then redirects  them to the "login" route, if sign up is successful. Otherwise,
    renders "signup.html.
    """

    @app.route("/signin", methods=['GET', 'POST'])
    def login():
        backend = Backend('wiki-credentials')
        message = ''
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            session['username'] = username
            value = backend.sign_in(username, password)
            if value:
                welcome = 'True'
                resp = make_response(
                    render_template('home.html',
                                    value=value,
                                    username=username,
                                    welcome=welcome))
                resp.set_cookie('value', 'True')
                resp.set_cookie('username', username)
                resp.set_cookie('welcome', 'True')
                return resp
            else:
                message = 'ERROR: Your login attempt has failed. Make sure the username and password are correct.'
                return render_template('signin.html', message=message)
        else:
            return render_template('signin.html', message=message)

    """ Defines the "/signin" URL of the application.

    Args:

    None

    Returns: If user logs in correctly, it renders the signin.html.
    Otherwise, it renders the signup.html.
    """

    # Pages route
    @app.route("/pages", methods=['GET', 'POST'])
    def pages():
        if request.method == 'POST':
            username = session['username']
            author = request.form['author']
            backend = Backend('wiki-user-uploads')
            pages = backend.get_all_page_names(author)
            if pages == []:
                pages = backend.get_authors()
                message = 'Error: Author does not exist.'
                return render_template('pages.html',
                                       message=message,
                                       pages=pages,
                                       username=username)
            return render_template('authors.html',
                                   author=author,
                                   pages=pages,
                                   username=username)
        else:
            backend = Backend('wiki-user-uploads')
            pages = backend.get_authors()
            value = request.cookies.get('value')
            username = request.cookies.get('username')
            resp = make_response(
                render_template('pages.html', value=value, username=username))
            resp.set_cookie('welcome', '', expires=0)
            return render_template('pages.html',
                                   pages=pages,
                                   value=value,
                                   username=username)

    @app.route("/author_page/<page>", methods=['GET', 'POST'])
    def show_author_uploads(page):
        username = session['username']
        author = page[1:-1]
        session['author'] = author
        backend = Backend('wiki-user-uploads')
        pages = backend.get_all_page_names(author)
        return render_template('authors.html',
                            author=author,
                            pages=pages,
                            username=username)
        

    """ Defines the "/author_page/<page>" URL of the application.

    Args:

    None

    Returns: It renders page which shows the author's name and their uploaded pages..
    """

    @app.route("/upload", methods=['GET', 'POST'])
    def upload():
        backend = Backend('wiki-user-uploads')
        username = session['username']
        if request.method == 'POST':
            wikiname = request.form['wikiname']
            wiki = request.files['wiki']
            filepath = '/tmp/' + wiki.filename
            wiki.save(filepath)
            backend.upload(filepath, wikiname, username)
            message = wikiname + ' has been uploaded successfully!'
            return render_template('upload.html',
                                   username=username,
                                   message=message)
        return render_template('upload.html', username=username)

    """ Defines the "/upload" URL of the application.

    Args:

    None

    Returns: It renders page which enables a user to uplaod a page to the website.
    """

    @app.route("/logout")
    def logout():
        resp = make_response(render_template("home.html"))
        resp.set_cookie('value', '', expires=0)
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('welcome', '', expires=0)
        return resp

    """ Defines the "/author_page/<page>" URL of the application.

    Args:

    None

    Returns: It renders home.html when user logs out with cookies updated to expired.
    """

    @app.route('/submit_comment', methods=['POST'])
    def submit_comment():
        backend = Backend('wiki-user-uploads')
        username = session['username']
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        author = session.get('author')
        # Get the comment data from the request
        comment = request.form['comment']
        comment_id = backend.get_comment_ID(current_time, comment)
        user_id = backend.get_userID(username, current_time)
        data = {
            'Username': username,
            'Comment': comment,
            'Comment_ID': comment_id,
            'User_ID': user_id,
            'Time': current_time
        }
        firebase.post(author, data)

        return render_template('authors.html')

    """ Defines the "/author_page/<page>" URL of the application.

    Args:

    None

    Returns: It renders page which shows author.html page after user has made a comment.Handles 
    how the data is tranferred to the database after the website receives it from the form.
    """

    @app.route('/metadata')
    def visualize_metadata():
        username = session['username']
        df = pd.DataFrame({
            'Username': username,
            'status': ['Login', 'Logout'],
            'values': [100, 65]
        })
        fig1 = px.bar(df, x='status', y='values', color='Username')
        graphJSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('chart.html',
                               graphJSON=graphJSON,
                               username=username)