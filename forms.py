from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, FileField, EmailField, ValidationError, TextAreaField
from wtforms.validators import Length, EqualTo, DataRequired, Email, Regexp
from flask_sqlalchemy import SQLAlchemy
from models import User

class AddProduct(FlaskForm):
    name = StringField(label="Name")
    url = StringField(label="URL")
    price = IntegerField(label="Price")
    password_hash = PasswordField(label="Password")
    repeat_password = PasswordField(label="Repeat Password", validators=[EqualTo("password_hash")])
    submit = SubmitField(label="Submit")
    file = FileField(label="file")
    folder = StringField(label="Folder", validators=[DataRequired()])
    description = StringField(label="Product Description", validators=[DataRequired()])

    def __str__(self):
        return f"{self.name}"

class RegisterForm(FlaskForm):
    username = StringField(label="UserName")
    password = PasswordField(label="Password")
    repeat_password = PasswordField(label="Repeat Password", validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.')
    ])
    mail = StringField(label="Email", validators=[DataRequired(), Email(message='Invalid email address.')])
    register = SubmitField(label="Register")

class LoginForm(FlaskForm):
    username = StringField(label="UserName")
    password = PasswordField(label="Password")
    login = SubmitField(label="Login")

class ContactForm(FlaskForm):
    name = StringField(label="Name")
    number = IntegerField(label="Phone Number")
    mail = EmailField(label="Mail")
    country = StringField(label="Country")
    city = StringField(label="City/Region")
    subject = StringField(label="Subject")
    text = TextAreaField(label="Your Message")
    submit = SubmitField(label="Submit")

class PurchaseForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    zip_code = StringField('ZIP/Postal Code', validators=[DataRequired()])
    card_cvc = StringField('CVC', validators=[DataRequired(), Length(min=3, max=4)])
    submit = SubmitField('Purchase Item')

