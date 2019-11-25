# coding: utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import pymysql

SECRET_KEY = os.urandom(32)

homeApp = Flask(__name__)

homeApp.debug = True
homeApp.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Unsw1995@localhost:3306/movie"
homeApp.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
homeApp.config["SECRET_KEY"] = SECRET_KEY

db = SQLAlchemy(homeApp)

from app.home import home as home_blueprint

homeApp.register_blueprint(home_blueprint)


