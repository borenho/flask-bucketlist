from flask import Flask, Markup

# Initialize the app
app = Flask(__name__, instance_relative_config=True)

# Load the config file
app.config.from_object('config')

# The import views should be down here so as to avoid circular references since we are gonna import the app instance declared above in the views module
from this_app import views
