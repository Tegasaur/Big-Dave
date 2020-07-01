from app import db,app
from flask import render_template, redirect, Response, Blueprint, send_file, current_app, session, url_for, flash, request
from connector.models import Parts, Cart, Feedback
from connector.forms import CartForm, FeedbackForm

bike = Blueprint('bike_shop', __name__ , template_folder='templates_2')
@bike.route("/bike_home", methods =['GET', 'POST'])
def bike_home():
    fform =  FeedbackForm()
    if request.method == "POST":
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

    return render_template("bike_home.html", fform = fform)

@bike.route("/parts_shop", methods =['GET', 'POST'])
def parts_shop():
    form = CartForm()
    fform =  FeedbackForm()
    if session['email'] == None:
        session['return_url'] = url_for('bike_shop.parts_shop')
        return redirect(url_for('connector.login'))
    
    else:
        parts =  Parts.objects.all()
        for part in parts:
            if part.image.read() != None:
                with open("static" + "/" + part.part_name+".jpg", 'wb') as f:
                    l = part.image.fs.get(part.image.grid_id).read()
                    f.write(l)
        if request.method == 'POST':
            if form.validate_on_submit():

                p_id = form.p_id.data
                if Cart.objects(item_id = p_id).first():
                    flash('You already have this in the cart', 'danger')
                    redirect(url_for('bike_shop.parts_shop'))
                else:
                    cart = Cart(user_email = session['email'], item_id = p_id)
                    cart.save()
                    flash('Item added successfully', 'success')
                    return redirect(url_for('bike_shop.parts_shop'))
            else:
                flash('Something went wrong', 'danger')
                return redirect(url_for('bike_shop.parts_shop'))

    return render_template("shop_home.html", parts = parts, form = form)