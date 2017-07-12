from flask import Flask, Markup
# from flask_login import LoginManager

# Initialize the app
app = Flask(__name__, instance_relative_config=True)

# Load the config file
app.config.from_object('config')

# Use flask-login's LoginManager to log in users
# login_manager = LoginManager()
# login_manager.login_view = 'login'
# login_manager.init_app(app)
# login_manager.login_message = Markup("<div class='alert alert-success' role='alert'>\
#                                         Please login to access this page\
#                                         </div>")


# The import views should be down here so as to avoid circular references since we are gonna import the app instance declared above in the views module
from this_app import views
