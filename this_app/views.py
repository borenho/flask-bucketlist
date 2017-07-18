from flask import flash, redirect, render_template, url_for, request, session, Markup
from this_app import app
from .models import User, Bucketlist, BucketlistItem
from werkzeug.security import check_password_hash
from .forms import SignupForm, LoginForm, BucketlistForm, BucketlistItemForm

# Set var to check if user is logged in
global logged_in
logged_in = False

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if logged_in:
        login_instead = Markup("<div class='alert alert-info' role='alert'>\
                                    You are logged in. You might want to logout first\
                                </div>")
        flash(login_instead)

        return redirect(url_for("show_bucketlists", form=BucketlistForm()))

    # If user is not signed in
    form = SignupForm(request.form)

    if form.validate_on_submit(): 
        # Throw an error if email is already registered
        users_dict = User.users.items()    
        existing_user = {k:v for k, v in users_dict if form.email.data in v['email']}
        if existing_user:
            email_exists = Markup("<div class='alert alert-info' role='alert'>\
                                        The email entered is registered, please login instead\
                                    </div>")
            flash(email_exists)

            return render_template("login.html", form=LoginForm())
        
        # If email is not registered, register the user
        new_user = User(form.email.data, form.username.data, form.password.data)
        new_user.create_user()

        for key, value in users_dict:     # gets id, eg 2
            if form.email.data in value['email']:
                session['user_id'] = key
                print ('User signup session ID - ', session['user_id'])

        global logged_in
        logged_in = True

        successful_signup = Markup("<div class='alert alert-success' role='alert'>\
                                        Account created successfully\
                                    </div>")
        flash(successful_signup)

        print('All users - ', User.users)

        return redirect(url_for("show_bucketlists", form=BucketlistForm()))

    if form.errors:
        form_error = Markup("<div class='alert alert-danger' role='alert'>\
                                Form error. Either email, username or password is invalid\
                            </div>")
        flash(form_error)

    # If GET
    return render_template("signup.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        # Iterate over each user's stored data
        users_dict = User.users.items()    # Eg {{1: {'password': 'kaka', 'username': 'kaka', 'email': 'kaka@email.com'}}}
        existing_user = {k:v for k, v in users_dict if form.email.data in v['email']}
        # Check password if user exists
        if existing_user:
            # Check if the stored password and form password match
            # valid_user = [v for v in existing_user.values() if v['password']==form.password.data]
            valid_user = [v for v in existing_user.values() if check_password_hash(v['password'], form.password.data)]
            if valid_user:  
                # Log the user in as credentials are valid
                global logged_in
                logged_in = True

                print (existing_user)
                print ("---------------")
                print (valid_user)

                successful_login = Markup("<div class='alert alert-success' role='alert'>\
                                                Login successful\
                                            </div>")
                flash(successful_login)

                for key, value in users_dict:
                    if form.email.data in value['email']:
                        session['user_id'] = key
                        print ('Login session - ', session['user_id'])

                        bucketlist_dict = Bucketlist.bucketlists.items()
                        has_bucks = {k:v for k, v in bucketlist_dict if session['user_id'] in v.values()}
                        print ('Login bucks - ', has_bucks)
    
                        # If this user has bucketlists
                        if has_bucks:
                            return render_template('show_bucketlists.html', form=BucketlistForm(), data=has_bucks)

                        # If user has no bucketlists
                        print ('has no bucks')
                        return redirect(url_for('show_bucketlists', form=BucketlistForm()))
            # If wrong password
            incorrect_password = Markup("<div class='alert alert-danger' role='alert'>\
                                            Incorrect password. Please use the correct password\
                                        </div>")
            flash(incorrect_password)

            return render_template("login.html", form=form)

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
    if logged_in:
        form = BucketlistForm(request.form)

        print ('Show bucks - ', session['user_id'])

        bucketlist_dict = Bucketlist.bucketlists.items()
        has_bucks = {k:v for k, v in bucketlist_dict if session['user_id'] in v.values()}
        print ('Login bucks - ', has_bucks)

        # If this user has bucketlists
        if has_bucks:
            return render_template('show_bucketlists.html', form=BucketlistForm(), data=has_bucks)

        # If user has no bucketlists
        if form.validate_on_submit():
            # Create the bucketlist
            new_bucketlist = Bucketlist(form.name.data, form.description.data)
            new_bucketlist.create_bucketlist()
            # new_bucketlist.insert_into_user()

            bucketlist_created = Markup("<div class='alert alert-success' role='alert'>\
                                            Bucketlist created successfully\
                                        </div>")
            flash(bucketlist_created)

            bucketlist_dict = Bucketlist.bucketlists.items()    # Eg {user_id: {buck_id: {'buck_name': 'Hiking', ...}}}
            created_buck = {k:v for k, v in bucketlist_dict if session['user_id']==v['user_id']}

            print ('Existing bucks in lst - ', Bucketlist.bucketlists)
            print ('Created bucks - ', created_buck)

            return render_template("show_bucketlists.html", form=form, data=created_buck)

        if form.errors:
            form_error = Markup("<div class='alert alert-danger' role='alert'>\
                                    Form error. Could not create bucketlist *#*#*??\
                                </div>")
            flash(form_error)

        # If GET
        return render_template("show_bucketlists.html", form=form)
    # If user is not logged in:
    sign_in_first = Markup("<div class='alert alert-danger' role='alert'>\
                                Please sign in first to see your bucketlists\
                            </div>")
    flash(sign_in_first)

    return render_template("login.html", form=LoginForm())

@app.route('/show_items', methods=['GET', 'POST'])
def show_items():
    if logged_in:
        form = BucketlistItemForm(request.form)

        if form.validate_on_submit():
            # Create the bucketlist
            new_bucketlist_item = BucketlistItem(form.title.data, form.description.data, form.status.data)
            new_bucketlist_item.create_bucketlist_item()
            new_bucketlist_item.insert_into_bucketlist()

            bucketlist_created = Markup("<div class='alert alert-success' role='alert'>\
                                            Bucketlist Item created successfully\
                                        </div>")
            flash(bucketlist_created)
            
            data = Bucketlist.bucketlist_items
            
            print (data)

            return render_template('show_items.html', form=form, data=data)

        if form.errors:
            form_error = Markup("<div class='alert alert-danger' role='alert'>\
                                    Form error. Could not create bucketlist *#*#*??\
                                </div>")
            flash(form_error)

        # If GET
        return render_template("show_items.html", form=form)

    # If user is not logged in:
    sign_in_first = Markup("<div class='alert alert-danger' role='alert'>\
                                Please sign in first to see your bucketlists\
                            </div>")
    flash(sign_in_first)

    return render_template("login.html", form=LoginForm())

@app.route('/logout')
def logout():
    global logged_in
    logged_in = False
    session.pop('user_id', None)

    return redirect(url_for('index'))
