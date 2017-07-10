from this_app import app
# Enable Flask's debugging features. Should be False in production
app.DEBUG = True

WTF_CSRF_ENABLED = True
SECRET_KEY = 'guess-it'
