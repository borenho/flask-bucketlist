from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Required, Length, Email


class SignupForm(FlaskForm):
    """Render and validate the signup form"""
    email = StringField("Email", validators=[Required(), Email(), Length(1, 32)])
    username = StringField("Username", validators=[Required(), Length(1, 32)])
    password = PasswordField("Password", validators=[Required(), Length(1, 32)])
