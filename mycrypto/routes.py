import os
from queue import Empty
import secrets
from urllib.request import Request,urlopen
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from mycrypto import app, db, bcrypt, mail
from mycrypto.forms import *
from mycrypto.models import User, WatchList
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from flask_mail import Message
import json

def ran(x):
    return range(x)


app.jinja_env.filters["ran"] = ran


@app.route("/")
def home():
    if current_user.is_authenticated:
        return render_template("/pages/home.html")
    else:
        return render_template("/pages/home.html")


@app.route("/about")
def about():
    return render_template("/pages/about.html")
    

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                next_page = request.args.get("next")
                # if current_user.user_type == "teacher":
                #     return redirect(next_page) if next_page else redirect(url_for("home"))
                # else:
                #     return redirect(next_page) if next_page else redirect(url_for("home2"))
                return redirect(url_for("home"))
            else:
                flash("Login Unsuccessful. Please check email and password", 'alert alert-danger')
    return render_template("/pages/sign-in.html", title="Login", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            first_name=form.first_name.data, last_name=form.last_name.data,  password=hashed_password, 
            email=form.email.data
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("home"))
    return render_template("/pages/sign-up.html", title="Register", form=form)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)



@app.route("/password-reset", methods=["GET", "POST"])
def password_reset():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'alert alert-primary')
        return redirect(url_for('login'))
    return render_template("/pages/password-reset.html", form=form, title="password-reset")



@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = NewPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'alert alert-success')
        return redirect(url_for('login'))
    print('ssssssss',form.password.errors)
    return render_template('/pages/new-password.html', title='Reset Password', form=form)



@app.route("/coin_search", methods=["GET", "POST"])
def coin_search():
    if request.method == "POST":
        coin_id = request.form["coin_id"]
        print(coin_id)
        return redirect(url_for("home"))    
    



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        db.session.commit()
        flash("Your account has been updated!", "alert alert-success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template(
        "/pages/account-setting.html", title="Account", image_file=image_file, form=form
    )

@app.route("/change-password", methods=['GET', 'POST'])
def change_password():
    if current_user.is_authenticated:
        form = NewPasswordForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated!', 'alert alert-success')
            logout_user()
            return redirect(url_for('login'))
        return render_template('/pages/new-password.html', title='Reset Password', form=form)
    return redirect(url_for('login'))

@app.route("/add-watchlist/", methods=['GET', 'POST'])
def add_watchlist():
    if current_user.is_authenticated:
        data = json.loads(request.data)
        coin = data["coin"]
        get_coin = WatchList.query.filter_by(user_id=current_user.id, coin_id=coin).first()
        if not get_coin:
            try:
                add_watch = WatchList(
                    author=current_user, coin_id=coin
                )
                db.session.add(add_watch)
                db.session.commit()
                return jsonify({"success": True})
            except:
                return jsonify({"success": False})

    return jsonify({"login": False})


@app.route("/get-watchlist/", methods=['GET', 'POST'])
def get_watchlist():
    if current_user.is_authenticated:
        coin_list = []
        get_coin = WatchList.query.filter_by(user_id=current_user.id)
        for i in get_coin:
            coin_list.append(i.coin_id)
        return jsonify({"watchlist": coin_list})
    return jsonify({"login": False})


@app.route("/remove-coin/", methods=['GET', 'POST'])
def remove_coin():
    if current_user.is_authenticated:
        data = json.loads(request.data)
        coin = data["coin"]
        get_coin = WatchList.query.filter_by(user_id=current_user.id, coin_id=coin).first()
        if get_coin:
            try:
                db.session.delete(get_coin)
                db.session.commit()
                return jsonify({"success": True})
            except:
                return jsonify({"success": False})
    return jsonify({"login": False})

@app.route("/check-coin/", methods=['GET', 'POST'])
def check_coin():
    if current_user.is_authenticated:
        data = json.loads(request.data)
        coin = data["coin"]
        get_coin = WatchList.query.filter_by(user_id=current_user.id, coin_id=coin).first()
        if get_coin:
            return jsonify({"find": True})
        return jsonify({"find": False})
    return jsonify({"login": False})