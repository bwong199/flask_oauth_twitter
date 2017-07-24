from flask import Flask, render_template, session, redirect, request, url_for, g
from twitter_utils import get_request_token, get_oauth_verifier_url, get_access_token
from user import User
from database import Database

app = Flask(__name__)
app.secret_key = '1234ABC'

Database.initialise(host='localhost', database='learning', user='postgres', password='password')


@app.before_request
def load_user():
    if 'screen_name' in session:
        g.user = User.load_from_db_by_screen_name(session['screen_name'])
        print(g.user)

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/login/twitter')
def twitter_login():
    request_token = get_request_token()
    print(request_token)
    session['request_token'] = request_token
    session['ABC'] = "ABC"
    print("session request token 1 " + str(session['request_token']))
    print(session['ABC'])
    print(session)
    return redirect(get_oauth_verifier_url(request_token))

    # redirecting the user to Twitter so they can confirm authorization

@app.route('/auth/twitter')  # http://127.0.0.1:3333/auth/twitter?oauth_verifier=1234567
def twitter_auth():
    oauth_verifier = request.args.get('oauth_verifier')
    print("oauth verifier " + str(oauth_verifier))
    print("All session " + str(session))
    print("request token token 2 " + str(session['request_token']))
    access_token = get_access_token(session['request_token'], oauth_verifier)
    print(access_token['screen_name'])

    user = User.load_from_db_by_screen_name(access_token['screen_name'])
    if not user:
        user = User(access_token['screen_name'], access_token['oauth_token'], access_token['oauth_token_secret'], None)
        user.save_to_db()


    session['screen_name'] = user.screen_name
    print("User " + str(user.screen_name))

    return redirect(url_for('profile'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('homepage'))

@app.route("/profile")
def profile():
    print(g.user)
    return render_template("profile.html", user=g.user)

app.run(port=3333)