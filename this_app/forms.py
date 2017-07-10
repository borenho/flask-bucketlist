from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import Required, Length, Email
from wtforms import ValidationError

from .models import User


class SignupForm(Form):
    """Render and validate the signup form"""
    email = StringField("Email", validators=[Required(), Email(), Length(1, 32)])
    username = StringField("Username", validators=[Required(), Length(1, 32)])
    password = PasswordField("Password", validators=[Required(), Length(1, 32)])

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data).first()
