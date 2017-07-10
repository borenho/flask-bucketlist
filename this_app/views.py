from flask import Flask, flash, redirect, render_template, url_for, request, session, Markup
from .models import User
from .forms import SignupForm
from this_app import app

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/signup', methods=['GET', 'POST'])

def signup():
    form = SignupForm(request.form)

    if request.method == 'POST':
        
        # Throw an error if email is already registered
        if form.email.data in User.users:
            email_exists = Markup("<div class='alert alert-danger' role='alert'>\
                            The email enetred is registered, please login instead\
                            </div>")
            flash(email_exists)

            return redirect(url_for('login'))
        
        # If no error, register the user
        new_user = User(form.email.data, form.username.data, form.password.data)
        new_user.create_user()

        successful_signup = Markup("<div class='alert alert-success' role='alert'>\
                            Account created successfully\
                            </div>")
        flash(successful_signup)

        print(User.users)

        return render_template('login.html')

    # If GET
    return render_template("signup.html", form=SignupForm())

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/show_bucketlists')
def show_bucketlists():
    return render_template("show_bucketlists.html")

@app.route('/show_items')
def show_items():
    return render_template("show_items.html")                                                        
