from flaskr import create_app
from unittest.mock import patch
from flaskr.backend import Backend
import pytest
import io

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
#Test #1 for home page, testing the welcome statement
def test_home_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"The Python Wiki Server" in resp.data

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

#Test #1 for pages page, testing title
def test_pages_page_1(client):
    resp = client.get("/pages")
    assert resp.status_code == 200
    assert b'Pages contained in this Wiki' in resp.data

# Test #2 for pages page, testing if the list of pages are displayed fully and correctly
def test_pages_page_2(client):
    resp = client.get("/pages")
    assert resp.status_code == 200
    backend = Backend('wiki-user-uploads')
    pages = backend.get_all_page_names()
    for i in range(len(pages)):
        assert bytes(pages[i], 'utf-8') in resp.data


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

#Test #3 for log in (sign in) page, test the POST method in which a user inputs invalid login info
def test_signin_page_3(client):
    resp = client.post("/signin", data={'username':'testuser', 'password':'wrongpassword'})
    assert resp.status_code == 200
    assert b'ERROR: Your login attempt has failed. Make sure the username and password are correct.' in resp.data

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

# Test #1 for upload page, test a successful upload
def test_upload_page_1(client):
    with client.session_transaction() as session:
        session['username'] = 'testuser'
    resp = client.post("/upload", data={'wikiname':'test-wiki', 'wiki': (io.BytesIO(b'my file contents'), 'testfile.txt')}, content_type='multipart/form-data')
    assert resp.status_code == 200
    assert b'test-wiki has been uploaded successfully!' in resp.data

# Test #2 for upload page, test that whenever a wikiname is missing, the status code will be 400 - which indicates the server won't process the request due to client error
def test_upload_page_2(client):
    with client.session_transaction() as session:
        session['username'] = 'testuser'
    resp = client.post("/upload", data={'wiki': (io.BytesIO(b'my file contents'), 'testfile.txt')}, content_type='multipart/form-data')
    assert resp.status_code == 400
    
# Test #1 for log out page, test that the log out route will lead the user back to main.html
def test_logout_page_1(client):
    resp = client.get("/logout")
    assert resp.status_code == 200
    assert b"The Python Wiki Server" in resp.data