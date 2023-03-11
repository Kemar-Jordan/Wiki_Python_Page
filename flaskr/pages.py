from flaskr.backend import Backend
from flask import Flask, render_template, send_file, request, redirect, url_for, session,make_response
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def make_endpoints(app):
    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page
        username = request.cookies.get('username')
        return render_template("home.html",username = username)

    # TODO(Project 1): Implement additional routes according to the project requirements.
    @app.route("/about")
    def about():
        backend = Backend('wiki-viewer-data')
        author_1 = backend.get_image('kemar_j.jpg')
        author_2 = backend.get_image('danielle.jpg')
        author_3 = backend.get_image('kris.jpg')
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
            session['username'] = username
            if backend.sign_in(username, password) == True:
                resp = make_response(render_template('home.html',username = username))
                resp.set_cookie('username',username)
                return resp
            else:
                return "Password is incorrect"
        else:
            return render_template('signin.html')

    # Pages route
    @app.route("/pages")
    def pages():
        backend = Backend('wiki-user-uploads')
        pages = backend.get_all_page_names()
        return render_template('pages.html', pages = pages)


    # Upload Route
    @app.route("/upload",methods=['GET','POST'])
    def upload():
        backend = Backend('wiki-user-uploads')
        username = session['username']
        if request.method == 'POST':
            wikiname = request.form['wikiname']
            wiki = request.files['wiki']
            filepath = '/tmp/' + wiki.filename 
            wiki.save(filepath)
            backend.upload(filepath, wikiname)
            message = wikiname + ' has been uploaded successfully!'
            return render_template('upload.html', username = username, message = message)
        return render_template('upload.html', username = username)

    # Logout route
    @app.route("/logout")
    def logout():
        return render_template('main.html')
