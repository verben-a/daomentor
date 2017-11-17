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
from .models import User, Profile, Experience, Education, Language, Skill, Service


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


@app.route("/login", methods=["GET"])
def login_get():

    return render_template('login.html')    

    # POST
@app.route("/login", methods=["POST"])
def login_post():

    email = request.form.get('email') # or request.form['email']
    password = request.form.get('password')

    user = session.query(User).filter(User.email==email).first()

    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger") 
        print("user: ", user)
        # return render_template('login_successful.html')
        return redirect(url_for("login"))

    login_user(user)
    return redirect(request.args.get('next') or url_for("profiles"))


@app.route("/signup")
def signup():
    return render_template("sign_up.html")


@app.route("/signup", methods=['POST'])
def signup_post():

    name_surname = request.form.get('name_surname')  
    email = request.form.get('email')
    password = request.form.get('password')
    summary = request.form.get('summary')
    position_at_company = request.form.get('position_at_company')
    location = request.form.get('location')
    
    password = generate_password_hash(password)

    user = User(email=email, password=password)

    profile = Profile(name_surname=name_surname,
                      position_at_company=position_at_company,
                      summary=summary,
                      location=location
                      )
    print (type(user))

    user.profile = [profile]

    session.add(user)
    session.commit()
    login_user(user)
    return redirect(url_for("add_info"))

@app.route("/add_info", methods=["GET","POST"])
def add_info():

    if request.method == "GET":
        return render_template("signup_successful.html")

    elif request.method == "POST":
        
        print(str(current_user))
        # experience = request.form.get('experience')
        company_name = request.form.get('company_name')
        position_name = request.form.get('position_name')
        position_summary = request.form.get('position_summary')
        # education = request.form.get('education')
        university_name = request.form.get('university_name')
        major_name = request.form.get('major_name')
        education_summary = request.form.get('education_summary')
        # language = request.form.get('language')
        language_name = request.form.get('language_name')
        # skills = request.form.get('skill')
        skill_name = request.form.get('skill_name')
        # service = request.form.get('service')
        service_name = request.form.get('service_name')
        cost = request.form.get('cost')

    # linkedin = request.form.get('linkedin')
    # facebook = request.form.get('facebook')
    # photo

        experience = Experience(company_name = company_name, 
                            position_name = position_name,
                            position_summary = position_summary)

        education = Education(university_name = university_name,
                          major_name = major_name,
                          education_summary = education_summary)

        language = Language(language_name = language_name)

        skill = Skill(skill_name = skill_name)

        service = Service(service_name = service_name,
                      cost = cost)

    # linkedin = Linkedin()

    # facebook = Facebook()

        # profile.experience = [experience]

        # profile.education = [education]

        # profile.language = [language]

        # profile.skill = [skill]

        # profile.service = [service]

        # experience.profile = current_user.profile.experience
        # education.profile = current_user.profile.education
        # language.profile = current_user.profile.language
        # skill.profile = current_user.profile.skill
        # service.profile = current_user.profile.service

        # session.add(profile)
        session.add(experience)
        session.add(education)
        session.add(language)
        session.add(skill)
        session.add(service)
        session.commit()

        return redirect(url_for("profile"))


@app.route("/view/<profile_id>", methods=["GET"])
def profile_view():
    return render_template("profile.html")

@app.route("/profile/", methods=["GET", "PUT", "DELETE"])
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