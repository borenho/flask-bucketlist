from flask import flash, redirect, render_template, url_for, request, session, Markup, abort
from this_app import app
from this_app.models import User, Bucketlist, Activity
from werkzeug.security import check_password_hash
from .forms import SignupForm, LoginForm, BucketlistForm, ActivityForm

# Set var to check if user is logged in
global logged_in
logged_in = False

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global logged_in
    if logged_in:
        return logout_required()
    else:
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

            successful_signup = Markup("<div class='alert alert-success' role='alert'>\
                                            Account created successfully\
                                        </div>")
            flash(successful_signup)

            print('All users - ', User.users)

            return redirect(url_for("login", form=LoginForm()))

        if form.errors:
            if len(form.password.data) < 4:
                form_error = Markup("<div class='alert alert-danger' role='alert'>\
                                        Password should be more than 4 chars\
                                    </div>")
                flash(form_error)
            if len(form.username.data) < 4:
                form_error = Markup("<div class='alert alert-danger' role='alert'>\
                                        Username should be more than 4 chars\
                                    </div>")
                flash(form_error)
            else:
                form_error = Markup("<div class='alert alert-danger' role='alert'>\
                                        Enter valid email, like j.deere@mail.com\
                                    </div>")
                flash(form_error)

        # If GET
        logged_in = False
        return render_template("signup.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    global logged_in
    if logged_in:
        return logout_required()
    
    # If user is not logged in
    form = LoginForm(request.form)

    if form.validate_on_submit():
        users_dict = User.users.items()
        existing_user = {k:v for k, v in users_dict if form.email.data in v['email']}
        if existing_user:
            valid_user = [v for v in existing_user.values() if check_password_hash(v['password'], form.password.data)]
            if valid_user:  
                logged_in = True

                successful_login = Markup("<div class='alert alert-success' role='alert'>\
                                                Login successful\
                                            </div>")
                flash(successful_login)

                for key, value in users_dict:
                    if form.email.data in value['email']:
                        session['user_id'] = key

                        bucketlist_dict = Bucketlist.bucketlists.items()
                        has_bucks = {k:v for k, v in bucketlist_dict if session['user_id'] in v.values()}
    
                        # If this user has bucketlists
                        if has_bucks:
                            return render_template('show_bucketlists.html', form=BucketlistForm(), data=has_bucks)

                        # If user has no bucketlists
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
        return redirect(url_for('signup', form=alt_form ))

    if form.errors:
        form_error = Markup("<div class='alert alert-danger' role='alert'>\
                                Enter valid email, like j.deere@mail.com\
                            </div>")
        flash(form_error)

    # If GET
    return render_template("login.html", form=form)

@app.route('/show_bucketlists', methods=['GET', 'POST'])
def show_bucketlists():
    if logged_in:
        form = BucketlistForm(request.form)
        if form.validate_on_submit():
            new_bucketlist = Bucketlist(form.name.data, form.description.data)
            new_bucketlist.create_bucketlist()

            bucketlist_created = Markup("<div class='alert alert-success' role='alert'>\
                                            Bucketlist created successfully\
                                        </div>")
            flash(bucketlist_created)

            bucketlist_dict = Bucketlist.bucketlists.items()
            user_bucketlists = {k:v for k, v in bucketlist_dict if session['user_id']==v['user_id']}

            print ('Existing bucks in lst - ', Bucketlist.bucketlists)
            print ('Users bucks - ', user_bucketlists)

            return render_template("show_bucketlists.html", form=form, data=user_bucketlists)

        if form.errors:
            form_error = Markup("<div class='alert alert-danger' role='alert'>\
                                    Form error. Could not create bucketlist *#*#*??\
                                </div>")
            flash(form_error)

        bucketlist_dict = Bucketlist.bucketlists.items()
        # Check if user has bucketlists
        has_bucks = {k:v for k, v in bucketlist_dict if session['user_id'] in v.values()}

        if has_bucks:

            return render_template('show_bucketlists.html', form=form, data=has_bucks)

        # If GET
        return render_template("show_bucketlists.html", form=form)
    
    # If user is not logged in:
    return login_required()

@app.route('/show_activities/<int:bucketlist_id>', methods=['GET', 'POST'])
def show_activities(bucketlist_id):
    """
    Show a bucketlists's activities
    """
    form = ActivityForm(request.form)
    if logged_in:

        # Check if buck has activities
        all_activities = Activity.activities
        buck_activities = {k:v for k, v in all_activities.items() if bucketlist_id==v['bucketlist_id']}
        if buck_activities:
            return render_template("show_activities.html", form=form, bucketlist_id=bucketlist_id, data=buck_activities)

        # If buck ids do not match
        return render_template('show_activities.html', form=form, bucketlist_id=bucketlist_id)

    # If user is not logged in:
    return login_required()

@app.route('/show_activities/create_activity/<int:bucketlist_id>', methods=['GET', 'POST'])
def create_activity(bucketlist_id):
    """
    Creates and adds activities to a bucketlist
    """
    form = ActivityForm(request.form) 
    if form.validate_on_submit():
        new_activity = Activity(form.title.data, form.description.data, form.status.data)
        new_activity.create_activity(bucketlist_id)

        activity_created = Markup("<div class='alert alert-success' role='alert'>\
                                        Bucketlist activity created successfully\
                                    </div>")
        flash(activity_created)
        
        # Select the activity belonging to the current bucket and pass it to show_activities
        all_activities = Activity.activities.items()
        created_activities = {k:v for k, v in all_activities if bucketlist_id==v['bucketlist_id']}
        
        if created_activities:

            return redirect(url_for("show_activities", form=form, data=all_activities, bucketlist_id=bucketlist_id))
        
        # Else if the activity was not created
        return redirect(url_for('show_activities', form=form, bucketlist_id=bucketlist_id))

    if form.errors:
        form_error = Markup("<div class='alert alert-danger' role='alert'>\
                                Form error. Could not create bucketlist activity *#*#*??\
                            </div>")
        flash(form_error)

    # If GET
    return render_template('show_activities.html', form=form, bucketlist_id=bucketlist_id)

@app.route('/delete_bucketlist', methods=['GET', 'POST'])
def delete_bucketlist():
    if logged_in: 
        bucketlists_dict = Bucketlist.bucketlists.items()
        user_bucketlists = {k:v for k, v in bucketlists_dict if session['user_id']==v['user_id']}
        Bucketlist.delete_bucketlist()

        return redirect(url_for("show_bucketlists", data=user_bucketlists))

@app.route('/show_activities/delete_activity/<int:bucketlist_id>/<int:key>', methods=['GET', 'POST'])
def delete_activity(bucketlist_id, key):
    if logged_in:
        all_activities = Activity.activities
        print ('All activities - ', all_activities)
        print('Bbuck id', bucketlist_id)
        print('key', key)
        buck_activities = {k:v for k, v in all_activities.items() if bucketlist_id==v['bucketlist_id']}
        if buck_activities:
            Activity.delete_activity(bucketlist_id, key)

            return redirect(url_for("show_activities", form=ActivityForm(), bucketlist_id=bucketlist_id, data=buck_activities))
        # If buck not found
        return render_template("show_activities.html", form=ActivityForm(), bucketlist_id=bucketlist_id, data=buck_activities)
                

@app.route('/edit_bucketlist', methods=['GET', 'POST'])
def edit_bucketlist():
    if logged_in:
        form = BucketlistForm(request.form)

        bucketlists_dict = Bucketlist.bucketlists.items()
        user_bucketlists = {k:v for k, v in bucketlists_dict if session['user_id']==v['user_id']}
        bucketlist = {k:v for k, v in user_bucketlists.items() if k==int(request.form['key'])}

        if form.validate_on_submit():
            bucketlist = Bucketlist(form.name.data, form.description.data)

            bucketlist.edit_bucketlist()

            return redirect(url_for("show_bucketlists", data=user_bucketlists))

        if form.errors:
            form_error = Markup("<div class='alert alert-danger' role='alert'>\
                                    Form error. Could not edit bucketlist *#*#*??\
                                </div>")
            flash(form_error)

        # If GET
        return redirect(url_for("show_bucketlists", form=form))

@app.route('/show_activities/edit_activity/<int:bucketlist_id>/<int:key>', methods=['GET', 'POST'])
def edit_activity(bucketlist_id, key):
    if logged_in:
        form = ActivityForm(request.form)

        all_activities = Activity.activities.items()
        buck_activites = {k:v for k, v in all_activities if k == key}

        if form.validate_on_submit():
            new_activity = Activity(form.title.data, form.description.data, form.status.data)

            new_activity.edit_activity(bucketlist_id, key)

            return redirect(url_for("show_activities", form=form, bucketlist_id=bucketlist_id, data=all_activities))

        if form.errors:
            form_error = Markup("<div class='alert alert-danger' role='alert'>\
                                    Form error. Could not edit activity *#*#*??\
                                </div>")
            flash(form_error)

        # If GET
        return redirect(url_for("show_activities", form=form, bucketlist_id=bucketlist_id, data=all_activities))

@app.route('/logout')
def logout():
    global logged_in
    logged_in = False
    session.pop('user_id', None)
    session.pop('bucketlist_id', None)

    return redirect(url_for('index')) 

def login_required():
    # If user is not logged in:
    sign_in_first = Markup("<div class='alert alert-danger' role='alert'>\
                                Please sign in first to see your bucketlists\
                            </div>")
    flash(sign_in_first)

    return render_template("login.html", form=LoginForm())

def logout_required():
    logout_instead = Markup("<div class='alert alert-info' role='alert'>\
                                    You are logged in. You might want to logout first\
                                </div>")
    flash(logout_instead)

    return redirect(url_for("show_bucketlists", form=BucketlistForm()))
