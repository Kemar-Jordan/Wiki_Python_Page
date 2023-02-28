from flask import render_template


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
        return 'The about page'
        #return render_template('about.html')

    # Sign up route
    @app.route("/signup")
    def signup():
        return 'The sign up page'
        #return render_template('signup.html')

    # Login route
    @app.route("/login")
    def login():
        return 'The login page'
        #return render_template('login.html')

    # Pages route
    @app.route("/pages")
    def pages():
        return 'The pages page'
        #return render_template('pages.html')