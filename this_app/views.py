from flask import flash, redirect, render_template, url_for, request, session, Markup
from this_app import app
from .models import User, Bucketlist
from .forms import SignupForm, LoginForm, BucketlistForm

# session['logged_in'] is False

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # If user is not signed in
    form = SignupForm(request.form)

    if form.validate_on_submit():  # This avoids you the trouble of checking if method==post
        
        # Throw an error if email is already registered
        if form.email.data in User.users:
            email_exists = Markup("<div class='alert alert-info' role='alert'>\
                            The email entered is registered, please login instead\
                            </div>")
            flash(email_exists)

            return redirect(url_for("login", form=LoginForm()))
        
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
                

                return redirect(url_for('show_bucketlists', form=BucketlistForm()))

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

@app.route('/show_bucketlists', methods=['GET', 'POST'])
def show_bucketlists():
    form = BucketlistForm(request.form)

    if form.validate_on_submit():
        # Create the bucketlist
        new_bucketlist = Bucketlist(form.name.data, form.description.data)
        new_bucketlist.create_bucketlist()

        bucketlist_created = Markup("<div class='alert alert-success' role='alert'>\
                            Bucketlist created successfully\
                            </div>")
        flash(bucketlist_created)

        print(Bucketlist.bucketlists)

        return redirect(url_for('show_bucketlists', form=form))

    if form.errors:
        form_error = Markup("<div class='alert alert-danger' role='alert'>\
                            Form error. Could not create bucketlist *#*#*??\
                            </div>")
        flash(form_error)

    # If GET
    return render_template("show_bucketlists.html", form=BucketlistForm())

@app.route('/show_items')
def show_items():
    return render_template("show_items.html")

@app.route('/logout')
def logout():
    pass

    return redirect(url_for('/'))                                                      
