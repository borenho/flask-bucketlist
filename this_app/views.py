from flask import Flask, flash, redirect, render_template, url_for, request, session, Markup
from this_app import app , login_manager
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from .forms import SignupForm, LoginForm

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/signup', methods=['GET', 'POST'])

def signup():
    form = SignupForm(request.form)

    if form.validate_on_submit():  # This avoids you the trouble of checking if method==post
        
        # Throw an error if email is already registered
        if form.email.data in User.users:
            email_exists = Markup("<div class='alert alert-info' role='alert'>\
                            The email entered is registered, please login instead\
                            </div>")
            flash(email_exists)

            return redirect(url_for("login.html", form=LoginForm()))
        
        # If email is not registered, register the user
        new_user = User(form.email.data, form.username.data, form.password.data)
        new_user.create_user()

        successful_signup = Markup("<div class='alert alert-success' role='alert'>\
                            Account created successfully. Now login\
                            </div>")
        flash(successful_signup)

        print(User.users)

        return redirect(url_for("login", form=LoginForm()))

    if form.errors:
        form_error = Markup("<div class='alert alert-danger' role='alert'>\
                            Form error. Either email, username or password is invalid\
                            </div>")
        flash(form_error)

    # If GET
    return render_template("signup.html", form=SignupForm())

@login_manager.user_loader
def user_loader(user_id):
    """ Takes the unicode id of the user and returns the user object
        Given the unicode id, the method returns the user with the given id
        This is loaded after every request
    """
    users_dict = User.users.items()
    user = {key:value for key, value in users_dict if key == int(user_id)}

    return user
    # for counter in User.users.keys():
    #     id = counter

    #     return User.users.get(int(id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        # Iterate over each user's stored data
        users_dict = User.users.items()
        this_user = {key:value for key, value in users_dict if form.email.data in value['email']}
        if this_user:
            # Check if the stored password and form password match
            valid_user = [v for v in this_user.values() if v['password']==form.password.data]
            if valid_user:
                successful_login = Markup("<div class='alert alert-success' role='alert'>\
                                            Login successful\
                                            </div>")
                flash(successful_login)
                
                # Now log the user in
                login_user(valid_user, remember=form.remember.data)
                return redirect(url_for('show_bucketlists'))

            # If wrong password
            incorrect_password = Markup("<div class='alert alert-danger' role='alert'>\
                                        Incorrect password. Please use the correct password\
                                        </div>")
            flash(incorrect_password)

            return redirect(url_for("login", form=LoginForm()))

        # If email is not registered yet
        not_registered = Markup("<div class='alert alert-info' role='alert'>\
                            Email not yet registered. Please create account to continue\
                            </div>")
        flash(not_registered)

        alt_form = SignupForm()
        # return render_template("signup.html", form=form)
        return redirect(url_for('signup', form=alt_form ))

    if form.errors:
        form_error = Markup("<div class='alert alert-danger' role='alert'>\
                            Form error. Either email or password is invalid\
                            </div>")
        flash(form_error)

    # If GET
    return render_template("login.html", form=form)

@app.route('/show_bucketlists')
@login_required
def show_bucketlists():
    return render_template("show_bucketlists.html")

@app.route('/show_items')
def show_items():
    return render_template("show_items.html")                                                        
