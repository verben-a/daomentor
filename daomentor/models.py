from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, Float, Sequence
from sqlalchemy.orm import relationship
from .database import Base
from flask_login import UserMixin


class User(Base, UserMixin):
	"""ONE ----> to """
	"""docstring for User"""
	__tablename__ = "users"
	id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
	email = Column(String(128), unique=True)
	password = Column(String(128))
	is_mentor = Column(Boolean, default=False)

	profile = relationship("Profile")

class Profile(Base):
	"""docstring for Profile

	ONE -_ > relationship"""
	__tablename__ = "profiles"

	id = Column(Integer, Sequence('profile_id_seq'), primary_key=True)
	name_surname = Column(String(100))
	summary = Column(String(300))
	position_at_company = Column(String(300))
	educations = relationship("Education")
	location = Column(String(100))
	languages = relationship("Language")
	skills = relationship("Skill", backref="skills")
	photo = Column(String(300))
	service = relationship("Service", backref="services")
	linkedin = Column(String(300))
	facebook = Column(String(300))
	experiences = relationship("Experience")

	user_id = Column(Integer, ForeignKey('users.id'), nullable = False)
	user = relationship("User", backref="profiles")
		

class Experience(Base):
	"""docstring for Position"""
	__tablename__= "experiences"

	id = Column(Integer, Sequence('experience_id_seq'), primary_key=True)
	company_name = Column(String(100))
	position_name = Column(String(100))
	position_summary = Column(String(300))

	profile_id = Column(Integer, ForeignKey("profiles.id"))
	profile = relationship("Profile", back_populates="experiences")

class Education(Base):
	"""docstring for education"""
	__tablename__= "educations"

	id = Column(Integer, Sequence('edu_id_seq'), primary_key=True)
	university_name = Column(String(300))
	major_name = Column(String(300))
	education_summary = Column(String(400))

	profile_id = Column(Integer, ForeignKey("profiles.id"))

class Language(Base):
	"""docstring for Language"""
	__tablename__="languages"

	id = Column(Integer, Sequence('language_id_seq'), primary_key=True)
	language_name = Column(String(50))

	profile_id = Column(Integer, ForeignKey("profiles.id"))

class Skill(Base):
	"""docstring for Skill"""
	__tablename__="skills"

	id = Column(Integer, Sequence('skill_id_seq'), primary_key=True)
	skill_name = Column(String(70))

	profile_id = Column(Integer, ForeignKey("profiles.id"))

class Service(Base):
	"""docstring for Service"""
	__tablename__="services"

	id = Column(Integer, Sequence('service_id_seq'), primary_key=True)
	service_name = Column(String(50))
	cost = Column(Float)

	profile_id = Column(Integer, ForeignKey("profiles.id"))
