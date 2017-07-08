from flask import render_template

from this_app import app

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/show_bucketlists')
def show_bucketlists():
    return render_template("show_bucketlists.html")

@app.route('/show_items')
def show_items():
    return render_template("show_items.html")                                                        
