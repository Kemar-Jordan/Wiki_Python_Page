from flaskr import create_app
from unittest.mock import patch
from flaskr.backend import Backend
import pytest

# See https://flask.palletsprojects.com/en/2.2.x/testing/ 
# for more info on testing
@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# TODO(Checkpoint (groups of 4 only) Requirement 4): Change test to
# match the changes made in the other Checkpoint Requirements.
#Test #1 for home page
def test_home_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Welcome to the Python Wiki!" in resp.data

#Test #2 for home page
def test_home_page_2(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"A Hub for Python Projects" in resp.data

#Test #1 for about page, testing author names
def test_about_page_1(client):
    resp = client.get("/about")
    assert resp.status_code == 200
    assert b"Founding Authors" in resp.data
    assert b"Kemar Jordan" in resp.data
    assert b"Danielle McIntosh" in resp.data
    assert b"Kristofer Valerio" in resp.data

#Test #2 for about page, testing author images
def test_about_page_2(client):
    resp = client.get("/about")
    assert resp.status_code == 200
    assert b'kemar_j.jpg' in resp.data
    assert b'danielle.jpg' in resp.data
    assert b'kris.jpg' in resp.data

#Test #1 for pages page, testing titles
def test_pages_page_1(client):
    resp = client.get("/pages")
    assert resp.status_code == 200
    assert b'Pages contained in this Wiki' in resp.data

#TODO, test new implentations for pages

#Test #1 for log in (sign in) page, test that the page loads
def test_signin_page_1(client):
    resp = client.get("/signin")
    assert resp.status_code == 200
    assert b'Login' in resp.data

#Test #2 for log in (sign in) page, test the POST method where a user successfully logs in
def test_signin_page_2(client):
    resp = client.post("/signin", data={'username':'testuser', 'password':'testpassword'})
    assert resp.status_code == 200
    assert b'testuser' in resp.data
    #assert b'logged_in.html' in resp.data

#Test #3 for log in (sign in) page, test the POST method in which a user inputs invalid login info
def test_signin_page_3(client):
    resp = client.post("/signin", data={'username':'testuser', 'password':'wrongpassword'})
    assert resp.status_code == 200
    assert b'Password is incorrect' in resp.data

#Test #1 for sign up page, test when a user attempts to sign up with an existing username
def test_signup_page_1(client):
    resp = client.post("/signup", data={'username':'testuser', 'password':'testpassword'})
    assert resp.status_code == 200
    assert b'Username already exists' in resp.data

# Test #2 for sign up page, test when a user successfully signs up with a valid username and password
def test_signup_page_2(client):
    resp = client.post("/signup", data={'username':'mockuser', 'password':'mockpassword'})
    assert resp.status_code == 302
    # Delete the mock user after testing, test that the user is successfully deleted
    backend = Backend('wiki-credentials')
    assert backend.delete_user('mockuser') == True

