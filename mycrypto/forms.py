from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    TextAreaField,
    IntegerField,
    SelectField,
    EmailField,
)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from mycrypto.models import User


class RegistrationForm(FlaskForm):
    email = EmailField(
    "Email", validators=[DataRequired(), Length(min=2, max=20)]
    )
    first_name = StringField(
        "First Name", validators=[DataRequired(), Length(min=2, max=20)]
    )
    last_name = StringField(
    "Last Name", validators=[DataRequired(), Length(min=2, max=20)]
    )

    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)],)
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )

    submit = SubmitField("Sign Up")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "Thais email is already taken. Please choose a different one."
            )

    def validate_password(self, password):

        if len(str(password)) < 8:
            raise ValidationError(
                "Use 8 or more characters with a mix of letters, numbers & symbols."
            )

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class PasswordResetForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    submit = SubmitField("Login")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class NewPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)],)
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Submit")

class UpdateAccountForm(FlaskForm):
    first_name = StringField(
        "First Name", validators=[DataRequired(), Length(min=2, max=20)]
    )
    last_name = StringField(
    "Last Name", validators=[DataRequired(), Length(min=2, max=20)]
    )
    picture = FileField(
        "Update Profile Picture", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Update")