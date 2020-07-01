from app import db,app
from flask import render_template, redirect, Response, Blueprint, url_for, session, request, flash, current_app
from connector.models import *
from connector.forms import *
import os
from werkzeug.utils import secure_filename

conn = Blueprint('connector', __name__ , template_folder='templates_1')
@conn.route("/")
@conn.route("/index")
def index():
    try:
        session['email']
        session['user_id']
        session['return_url']
        session['master']
    except:
        session['email'] = None
        session['user_id'] = None
        session['return_url'] = None
        session['master'] = False
    return render_template("index.html", index = True)

@conn.route("/login", methods=['POST','GET'])
def login():

    if session.get('email'):
        return redirect(url_for('connector.index'))

    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email =  form.email.data
            password =  form.password.data

            user = User.objects(email = email).first()
            if user and user.get_password(password):
                session['email'] = user.email
                session['user_id'] = str(user.pk)
                flash('Login was successfull', "success")
                if session['return_url'] != None:
                    url = session['return_url']
                    current_app.logger.warning(url)
                    session['return_url'] = None
                    return redirect(url)
                elif form.password.data == current_app.config['MASTER_PASSWORD']:
                    session['master'] = True
                    return redirect(url_for('connector.admin'))
                else:
                    return redirect(url_for('connector.index'))
            else:
                flash('Sorry stuff happened')
                return redirect(url_for('connector.login'))
    return render_template('login.html', form = form, login = True)

@conn.route("/register", methods = ['GET','POST'])
def register():
    if session.get('email'):
        return redirect(url_for('connector.index'))

    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            first_name = form.first_name.data
            last_name =  form.last_name.data
            email = form.email.data
            password = form.password.data
            user = User(first_name = first_name, 
                        last_name = last_name, email = email, 
                        password = password)
            user.set_password(password)
            user.save()
            session['email'] = user.email
            session['user_id'] = str(user.pk)
            if form.password.data == current_app.config['MASTER_PASSWORD']:
                    session['master'] = True
            flash('Registration was successfull', 'success')
            return redirect(url_for('connector.index'))
        else:
            flash('Sorry stuff happened', 'danger')
            return redirect(url_for('connector.register'))

    return render_template("register.html", form = form, register = True)


@conn.route("/logout")
def logout():
    session['email'] = None
    session['user_id'] = None
    session['master'] = False
    return redirect(url_for('connector.index'))

@conn.route("/checkout", methods = ['GET','POST'])
def checkout():
    cart = Cart.objects(user_email = session['email'])
    parts = []
    for part in cart:
        parts.append(Parts.objects(pk = part.item_id).first())
    form = PaymentForm()
    form2 = RemoveCartForm()
    if request.method == "POST":

        if form.validate_on_submit():
            card_name = form.card_name.data
            card_number =  form.card_number.data
            cvv = form.cvv.data
            expiry = form.expiry.data
            zipcode = form.zipcode.data
            for payment in Payment.objects(user_id = session['user_id']):
                payment.delete()
            check = Payment(user_id = session['user_id'],
                            card_name = card_name,
                            card_number = card_number,
                            expiry = expiry,
                            zipcode = zipcode,
                            cvv = cvv)
            if len(cart) != 0:
                for part in cart:
                    p = Parts.objects(pk = part.item_id).first()
                    if p.stock > 0:
                        p.stock -= 1
                        p.save()
                    else:
                        flash('Item is out of stock.', "danger")
                check.save()
                cart.delete()
                flash('Purchase is being processed. We will email you with the status.', "success")
                return redirect(url_for('bike_shop.parts_shop'))
            else:
                flash('There is nothing in your cart.',"danger")
                return redirect(url_for('connector.checkout'))

            

        elif form2.validate_on_submit():

            c_id = form2.c_id.data
            Cart.objects(user_email = session['email'], item_id = c_id).first().delete()
            flash('Item deleted.', 'success')
            return redirect(url_for('connector.checkout'))

        else:

            flash('Purchase failed, try again later.', 'danger')
            return redirect(url_for('connector.checkout'))

    return render_template('checkout.html', form2 = form2, form = form, parts = parts, cart = cart)


@conn.route('/admin', methods = ['GET','POST'])
def admin():
    menu_form =  MenuForm()
    parts_form =  PartsForm()
    remove_p = RemovePartsForm()
    remove_m = RemoveMenuForm()
    menudb =  Menu.objects.all()
    partsdb =  Parts.objects.all()

    if not session['master']:
        return redirect(url_for('connector.index'))

    if request.method == 'POST':

        if menu_form.validate_on_submit():
            meal_name = menu_form.meal_name.data
            meal_price = menu_form.meal_price.data
            meal_description = menu_form.meal_description.data
            meal_special = menu_form.meal_special.data
            menu = Menu(meal_name = meal_name, meal_price = meal_price,
                        meal_description = meal_description,
                        meal_special = meal_special)
            menu.save()
            flash('Meal saved successfully', ['success','meal'])
            return redirect(url_for('connector.admin', _anchor = "contact1"))

        elif parts_form.validate_on_submit():
            assets_dir = os.path.join(os.path.dirname(app.instance_path), 'media')
            image = None
            try:
                image = parts_form.image.data
            except:
                pass


            stock = 1
            part_name = parts_form.part_name.data
            part_price = parts_form.part_price.data
            if image:
                part = Parts(part_name = part_name, part_price = part_price,
                            stock = stock, image = image)
            else:
                part = Parts(part_name = part_name, part_price = part_price,
                            stock = stock)
            part.save()
            flash('Part saved successfully', ['success','part'])
            return redirect(url_for('connector.admin',_anchor = "contact2"))

        elif remove_p.validate_on_submit():
            if remove_p.p_id.data:
                p_id = remove_p.p_id.data
                if remove_p.remove.data:
                    Parts.objects(pk = p_id).delete()
                    flash('Part deleted', ['success','part'])

                elif remove_p.reduce_.data:
                    part = Parts.objects(pk = p_id).first()
                    part.stock -= 1
                    current_app.logger.warning(part.stock)
                    part.save()

                elif remove_p.add.data:
                    part = Parts.objects(pk = p_id).first()
                    part.stock += 1
                    part.save()


                return redirect(url_for('connector.admin',_anchor = "contact2"))

            elif remove_m.m_id.data:
                m_id = remove_m.m_id.data
                current_app.logger.warning(m_id)
                if remove_m.remove2.data:
                    Menu.objects(pk = m_id).delete()
                flash('Meal deleted', ['success','meal'])
                return redirect(url_for('connector.admin',_anchor = "contact1"))

        else:
            flash('Sorry stuff happened', ['danger','none'])
            return redirect(url_for('connector.admin'))

    return render_template("admin.html", menu_form = menu_form, parts_form = parts_form, remove_m = remove_m,
                            admin = True, menu = menudb, parts = partsdb, remove_p = remove_p)
