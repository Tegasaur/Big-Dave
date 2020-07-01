from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, BooleanField, DecimalField, FileField, HiddenField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from connector.models import User
from wtforms.fields.html5 import DateField


class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password =  StringField('Password', validators=[DataRequired(), Length(min=6)])
    submit =  SubmitField("Login")

class MenuForm(FlaskForm):
    meal_name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    meal_price = DecimalField('Price', validators=[DataRequired()])
    meal_description = TextAreaField('Description')
    meal_special = BooleanField('Special')
    submit =  SubmitField("Submit")

class PartsForm(FlaskForm):
    part_name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    part_price = DecimalField('Price', validators=[DataRequired()])
    image = FileField('Image')
    submit =  SubmitField("Submit")

class RemovePartsForm(FlaskForm):
    p_id = HiddenField("p_id")
    remove = SubmitField("Remove")
    reduce_ = SubmitField("Reduce")
    add = SubmitField("Add")

class RemoveMenuForm(FlaskForm):
    m_id = HiddenField("m_id")
    remove2 = SubmitField("Remove")

class RemoveCartForm(FlaskForm):
    c_id = HiddenField("c_id")
    remove = SubmitField("Remove")

class CartForm(FlaskForm):
    p_id = HiddenField("p_id")
    add = SubmitField("Add to Cart")

class PaymentForm(FlaskForm):
    card_name =  StringField('Card Holder', validators=[DataRequired()])
    card_number = IntegerField('Card Number', validators=[DataRequired()])
    cvv = IntegerField('CVV',  validators=[DataRequired()])
    expiry = DateField('Expiry date',  validators=[DataRequired()])
    zipcode = IntegerField('Zipcode', validators=[DataRequired()])
    purchase = SubmitField('Checkout')

class FeedbackForm(FlaskForm):
    name =  StringField('Your Name', validators = [DataRequired()])
    email = StringField('Your Email', validators = [DataRequired(), Email()])
    subject = StringField('Subject')
    message = TextAreaField('Message',validators = [DataRequired()])
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password =  StringField('Password', validators=[DataRequired(), Length(min=6)])
    password_confirm =  StringField('Password Confirm', validators=[DataRequired(), Length(min=6), EqualTo('password')])
    first_name = StringField('First Name',validators=[DataRequired(), Length(min=2,max=55)])
    last_name = StringField('Last Name',validators=[DataRequired(), Length(min=2,max=55)])
    submit =  SubmitField("Register Now")

    def validate_email(self, email):
        user = User.objects(email = email.data).first()
        if user:
            raise ValidationError("Email is already in use. Pick another one.")