from app import db
from flask import render_template, redirect, Response, Blueprint, flash, url_for, request
from connector.models import Menu, Feedback
from connector.forms import FeedbackForm

food = Blueprint('restaurant', __name__ , template_folder='templates_3')
@food.route("/food_home", methods = ['GET','POST'])
def food_home():
    fform  = FeedbackForm()
    menu = Menu.objects.all()
    if request.method == 'POST':
        if fform.validate_on_submit():
            name = fform.name.data
            email = fform.email.data
            subject =  fform.subject.data
            message =  fform.message.data
            feedback =  Feedback(name = name, email = email, subject = subject, message = message)
            feedback.save()
            flash('Your feedback was submitted successfully', 'success')
            return redirect(url_for('bike_shop.bike_home', _anchor = "contact"))
        else:
            flash('Something went wrong sorry', 'danger')
            return redirect(url_for('bike_shop.bike_home', _anchor = "contact"))

    return render_template("food_home.html", menu = menu, fform =  fform )
