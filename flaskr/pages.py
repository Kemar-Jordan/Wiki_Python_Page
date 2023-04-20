from flaskr.backend import Backend
from flask import Flask, render_template, send_file, request, redirect, url_for, session, make_response
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def make_endpoints(app, db_client, bucket_client):
    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page
        value = request.cookies.get('value')
        username = request.cookies.get('username')
        welcome = request.cookies.get('welcome')
        return render_template("home.html",
                               value=value,
                               username=username,
                               welcome=welcome)

    # def home():
    #     # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
    #     # to render main.html on the home page
    #     value = request.cookies.get('value')
    #     username = request.cookies.get('username')
    #     welcome = request.cookies.get('welcome')
    #     return render_template("home.html",value = value,username = username,welcome=welcome)

    # TODO(Project 1): Implement additional routes according to the project requirements.
    @app.route("/about")
    def about():
        backend = Backend('wiki-viewer-data', bucket_client)
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

    # Sign up route
    @app.route("/signup", methods=['GET', 'POST'])
    def sign_up():
        backend = Backend('wiki-credentials', bucket_client)
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if backend.sign_up(username, password):
                return redirect(url_for('login'))
            else:
                return "Username already exists"
        else:
            return render_template('signup.html')

    # # Login route
    @app.route("/signin", methods=['GET', 'POST'])
    def login():
        backend = Backend('wiki-credentials', bucket_client)
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

    # # Pages route
    @app.route("/pages", methods=['GET', 'POST'])
    def pages():
        if request.method == 'POST':
            username = session['username']
            author = request.form['author']
            backend = Backend('wiki-user-uploads', bucket_client)
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
            backend = Backend('wiki-user-uploads', bucket_client)
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
        backend = Backend('wiki-user-uploads', bucket_client)
        pages = backend.get_all_page_names(author)
        return render_template('authors.html',
                               author=author,
                               pages=pages,
                               username=username)

    # # Upload Route
    @app.route("/upload", methods=['GET', 'POST'])
    def upload():
        backend = Backend('wiki-user-uploads', bucket_client)
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

    # # Logout route
    @app.route("/logout")
    def logout():
        resp = make_response(render_template("home.html"))
        resp.set_cookie('value', '', expires=0)
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('welcome', '', expires=0)
        return resp
