# Python standard libraries
import json
import os
import sqlite3

import requests

# Third-party libraries
from flask import Flask, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient

import BS4Azn
import BS4fpkrt
import featureGrab

# Internal imports
from db import init_db_command
from user import User

form_val="nill"
# def triall():
#     test_var='works'
#     return test_var

# Configuration
GOOGLE_CLIENT_ID = "755960925170-ittebt844scr9v19617vqmf64b1a403c.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
flag = 1

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.context_processor
def example():
    return dict(myexample="This is an example")


@app.route("/")
def index():
    if current_user.is_authenticated or flag == 0:
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))


@app.route("/home", methods=["POST", "GET"])  # this sets the route to this page
def home():
    if current_user.is_authenticated or flag == 0:
        if request.method == "POST":
            search_string = request.form["search_string"]
            print(search_string)
            # return render_template('results.html',search_string=search_string)
            return redirect(url_for("resultsPage", search_stringss=search_string))
        else:
            return render_template("index.html")
    else:
        return redirect(url_for("login"))


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route("/loginG")
def loginG():
    global flag
    flag = 1
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/about")
def about():
    if current_user.is_authenticated or flag == 0:
        return render_template("about.html")
    else:
        return redirect(url_for("login"))


@app.route("/contact")
def contact():
    if current_user.is_authenticated or flag == 0:
        return render_template("contact.html")
    else:
        return redirect(url_for("login"))


@app.route("/howtouse")
def howtouse():
    if current_user.is_authenticated or flag == 0:
        return render_template("howtouse.html")
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        userID = request.form["Uname"]
        pw = request.form["Pass"]
        if userID == "admin" and pw == "1234":
            global flag
            flag = 0
            user = User(
                id_="12345", name="admin", email="admin@gmail.com", profile_pic="placeholder"
            )
            if not User.get("12345"):
                User.create("12345", "admin", "admin@gmail.com", "placeholder")

            # Begin user session by logging the user in
            login_user(user)
            return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/loginG/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint, authorization_response=request.url, redirect_url=request.base_url, code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]

    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided
    # by Google
    user = User(id_=unique_id, name=users_name, email=users_email, profile_pic=picture)

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))


@app.route("/logout")
# @login_required
def logout():
    logout_user()
    global flag
    if flag == 0:
        flag = 1
    return redirect(url_for("index"))

@app.route("/userpage")
def userpage():
    if current_user.is_authenticated and flag == 1:
        return render_template("userpage.html")
    elif flag == 0:
        return redirect(url_for("adminpage"))
    else:
        return redirect(url_for("login"))

@app.route("/adminpage")
def adminpage():
    if flag == 0:
        return render_template("adminpage.html")
    else:
        return redirect(url_for("login"))

@app.route("/resultsPage/<search_stringss>", methods=["POST", "GET"])
def resultsPage(search_stringss):
    if request.method == "POST":
        global form_val
        form_val = request.form["myradio1"]
        search_string = request.form["search_string"]
        print(form_val, 'inside the post method')
        #print(search_string)
        #print(data.get("myradio1"))

        #radio = data.get("myradio1")

        # return render_template('results.html',search_string=search_string)
        return redirect(url_for("resultsPage", search_stringss=search_string))

    def remove_char(x):
        import locale
        import re

        decimal_point_char = locale.localeconv()["decimal_point"]
        clean = re.sub(r"[^0-9" + decimal_point_char + r"]+", "", str(x))
        return float(clean)

    def add_char(x):
        return "{:,}".format(x)

    for i in range(10, 1, -1):
        try:
            for l in range(5):
                try:
                    print(form_val, 'outside the post method')
                    FeaturelistA=[]
                    FeaturelistF=[]
                    FlipkartList = BS4fpkrt.getNewlists(search_stringss, i)
                    AmazonList = BS4Azn.amzLists(search_stringss, i)
                    
                    AmazonList[1] = [remove_char(j) for j in AmazonList[1]]
                    FlipkartList[1] = [remove_char(j) for j in FlipkartList[1]]
                    
                    AmazonList[1] = [add_char(j) for j in AmazonList[1]]
                    FlipkartList[1] = [add_char(j) for j in FlipkartList[1]]

                    for k in range(10):
                        try:
                            for j in range(i):
                                FeaturelistA.append(featureGrab.getAmzFeatures(AmazonList[2][j]))
                                FeaturelistF.append(featureGrab.getAmzFeatures(FlipkartList[2][j]))
                        except:
                            pass
                    return render_template("results.html",search_stringss=search_stringss,listF=FlipkartList,listA=AmazonList,featuresA=FeaturelistA,featuresF=FeaturelistF)

                except IndexError as Iderr:
                    print(Iderr)
                    continue

                except Exception as diffex:
                    print("different ex thrown" + str(diffex))
                    continue        
        except:
            pass

@app.errorhandler(404)
def error404(error):
    return render_template("error.html")

if __name__ == "__main__":
    app.run(ssl_context="adhoc", debug=True)