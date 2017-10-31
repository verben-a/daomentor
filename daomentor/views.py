from flask import Flask, render_template, Response, request, flash, redirect, url_for
from flask_login import login_user, login_required, current_user, logout_user
from getpass import getpass
from werkzeug.security import generate_password_hash, check_password_hash

# import cloudinary
# from cloudinary.uploader import upload
# from cloudinary.utils import cloudinary_url

import json
import os

from . import app
from .database import session  # not known yet.
from .models import User, Profile


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/tou_privacy")
def tou_privacy():
    return render_template("tou_privacy.html")

@app.route("/contacts")
def contacts():
    return render_template("contacts.html")

@app.route("/team")
def team():
    return render_template("team.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    # GET

    email = request.form.get('email') # or request.form['email']
    password = request.form.get('password')

    # POST

    user = session.query(User).filter(User.email==email).first()
    
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger") 
        return redirect(url_for("login"))

    login_user(user)
    return redirect(request.args.get('next') or url_for("profile"))


@app.route("/signup")
def signup():
    return render_template("sign_up.html")


@app.route("/signup", methods=['POST'])
def signup_post():

    name_surname = request.form.get('name_surname')  
    email = request.form.get('email')
    password = request.form.get('password')
    position_at_company = request.form.get('position_at_company')
    experience = request.form.get('experience')
    education = request.form.get('education')
    location = request.form.get('location')
    language = request.form.get('language')
    skills = request.form.get('skill')
    service = request.form.get('service')
    linkedin = request.form.get('linkedin')
    facebook = request.form.get('facebook')
    # photo
    
    password = generate_password_hash(password)

    user = User(email=email, password=password)

    profile = Profile(name_surname=name_surname,
                      position_at_company=position_at_company,
                      experience = experience,
                      location=location,
                      education = education,
                      language = language,
                      skills = skills,
                      service = service,
                      linkedin = linkedin,
                      facebook=facebook)
    user.profile = profile

    session.add(user)
    session.commit()
    return redirect(url_for("profile"))


@app.route("/view/<profile_id>", methods=["GET"])
def profile_view():
    return render_template("profile.html")

@app.route("/profile/<profile_id>", methods=["GET", "PUT", "DELETE"])
# @login_required
def profile():
    # import pdb; pdb.set_trace()
    return render_template("profile.html")


@app.route("/dashboard/mentors/<page>", methods=["GET"])
# @login_required
def mentors_profiles():
    profiles = session.query(Profile)
    profiles = profiles.order_by(Profile.name.desc())
    profiles = profiles.all()
    return render_template("profiles.html", profiles=profiles
                           )

@app.route("/dashboard/mentees/<page>", methods=["GET"])
def mentees_profiles():
    profiles = session.query(Profile)
    profiles = profiles.order_by(Profile.name.desc())
    profiles = profiles.all()
    return render_template("profiles.html", profiles=profiles
                           )


# @app.route("/logout/")
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for("home"))

# @app.route("/profile/edit/", methods=["GET"])
# @login_required
# def profile_edit_get():
#     # fetch the user

#     return render_template("edit_profile.html", name = current_user.profile.name, 
#         surname = current_user.profile.surname, 
#         email = current_user.email,
#         # password = current_user.password,
#         faculty = current_user.profile.faculty,
#         location = current_user.profile.location,
#         industry = current_user.profile.industry,
#         year = current_user.profile.year,
#         company = current_user.profile.company,
#         position = current_user.profile.position,
#         expertise = current_user.profile.expertise)

# @app.route("/profile/edit/", methods=["PUT", "POST"])
# @login_required
# def profile_edit_post():
#     # import pdb; pdb.set_trace() # debugging -- stops it for investigations    
#     user = session.query(User).get(current_user.id)
#     user.profile.name = request.form.get('name') 
#     user.profile.surname = request.form.get('surname')
#     user.email = request.form.get('email')
#     if request.form.get("password") != "":
#         user.password = generate_password_hash(request.form.get('password'))
#     user.profile.faculty = request.form.get('faculty')
#     user.profile.location = request.form.get('location')
#     user.profile.industry = request.form.get('industry')
#     user.profile.year = request.form.get('year')
#     user.profile.company = request.form.get('company')
#     user.profile.position = request.form.get('position')
#     user.profile.expertise = request.form.get('expertise')

#     if request.files:
#         # your code goes here
#         file_to_upload = request.files['file']

#         if file_to_upload:
#             upload_result = upload(file_to_upload)
#             thumbnail_url, options = cloudinary_url(upload_result['public_id'], format="jpg", crop="fill", width=150, height=150)
#             user.profile.photo = thumbnail_url
            

#     session.commit()

#     return redirect(url_for("profile"))