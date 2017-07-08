from flask import Flask

# Initialize the app
app = Flask(__name__, instance_relative_config=True)

# The import views should be down here so as to avoid circular references since we are gonna import the app instance declared above in the views module
from this_app import views

# Load the config file
app.config.from_object('config')
