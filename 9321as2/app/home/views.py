# coding: utf-8

import requests
import json
from . import home
from flask import make_response, render_template, redirect, url_for, flash, session, request
from werkzeug.security import generate_password_hash
from .forms import LoginForm, RegisterForm, PostMovieForm, RecommandForm
from app.models import User, Userlog, Movie, BestMovie, CountryNum, TypeNum, Log
from app.models import db
from .utils import Pagination
from time import time


@home.route("/")
@home.route("/page/<int:page>")
def index(page=1):
    r = requests.get('http://127.0.0.1:5000/movies')
    movie = json.loads(r.text, object_hook=Movie.dict2movie)
    page_list = Pagination(page, 9, movie)
    headers = {'Content-Type': 'application/json'}
    log = Log(request.remote_addr, time(), 'Get Movie')
    r = requests.post('http://127.0.0.1:5000/movies/logging', headers=headers,
                      data=json.dumps(log, default=Log.log2json))
    return render_template("home/index.html", pagination=page_list)


@home.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(username=data["username"]).first()
        if not user or not user.check_pwd(data["password"]):
            flash("Error password!", "err")
            return redirect(url_for("home.login"))
        session["user"] = user.username
        session["user_id"] = user.id
        userlog = Userlog(
            user_id=user.id,
            ip=request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()
        headers = {'Content-Type': 'application/json'}
        log = Log(request.remote_addr, time(), 'Login')
        r = requests.post('http://127.0.0.1:5000/movies/logging', headers=headers,
                          data=json.dumps(log, default=Log.log2json))
        return redirect(url_for("home.index"))
    return render_template("home/login.html", form=form)


@home.context_processor
def my_context_processor():
    user = session.get('user')
    if user:
        return {'login_user': user}
    return {}


@home.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home.index"))


@home.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            username=data["username"],
            email=data["email"],
            pwd=generate_password_hash(data["password"])
        )
        db.session.add(user)
        db.session.commit()
        flash("success sign up!", "ok")
        session["user"] = user.username
        session["user_id"] = user.id
        headers = {'Content-Type': 'application/json'}
        log = Log(request.remote_addr, time(), 'Register')
        r = requests.post('http://127.0.0.1:5000/movies/logging', headers=headers,
                          data=json.dumps(log, default=Log.log2json))
        return redirect(url_for("home.index"))
    return render_template("home/register.html", form=form)


@home.route("/postamovie", methods=['GET', 'POST'])
def post_movie():
    if not session.get("user"):
        return redirect(url_for("home.index"))
    form = PostMovieForm()
    if form.validate_on_submit():
        data = form.data
        if not data['vote_count']:
            data['vote_count'] = 0
        if not data['vote_average']:
            data['vote_average'] = 0.0
        if not data['runtime']:
            data['runtime'] = 0.0
        movie = Movie(
            title=data['title'],
            language=data['language'],
            genre=data['genre'],
            overview=data['overview'],
            release_date=data['release_date'],
            runtime=data['runtime'],
            vote_count=data['vote_count'],
            director=data['director'],
            star=data['star'],
            writer=data['writer'],
            country=data['country'],
            vote_average=data['vote_average']
        )
        posts = json.dumps(movie, default=Movie.movie2json)
        headers = {'Content-Type': 'application/json'}
        r = requests.post('http://127.0.0.1:5000/movies', headers=headers, data=posts)
        if r.status_code == 201:
            log = Log(request.remote_addr, time(), 'Post Movie')
            r = requests.post('http://127.0.0.1:5000/movies/logging', headers=headers,
                              data=json.dumps(log, default=Log.log2json))
            return redirect(url_for("home.index"))
        else:
            flash("Something Error!", "err")
            return redirect(url_for("home.post_movie"))
    return render_template("home/post.html", form=form)


@home.route('/movieanalyse')
def dataAnalyse():
    r = requests.get("http://127.0.0.1:5000/movies/analysis/best_movie_year")
    movie = json.loads(r.text, object_hook=BestMovie.dict2movie)
    r = requests.get("http://127.0.0.1:5000/movies/analysis/country")
    country = json.loads(r.text, object_hook=CountryNum.dict2counNum)
    r = requests.get("http://127.0.0.1:5000/movies/analysis/general")
    genre = json.loads(r.text, object_hook=TypeNum.dict2typeNum)
    headers = {'Content-Type': 'application/json'}
    log = Log(request.remote_addr, time(), 'Get /movies/analysis/best_movie_year/')
    r = requests.post('http://127.0.0.1:5000/movies/logging', headers=headers,
                      data=json.dumps(log, default=Log.log2json))
    log = Log(request.remote_addr, time(), 'Get /movies/analysis/movies/analysis/country/')
    r = requests.post('http://127.0.0.1:5000/movies/logging', headers=headers,
                      data=json.dumps(log, default=Log.log2json))
    log = Log(request.remote_addr, time(), 'Get /movies/analysis/movies/analysis/general')
    r = requests.post('http://127.0.0.1:5000/movies/logging', headers=headers,
                      data=json.dumps(log, default=Log.log2json))
    return render_template('home/analyse.html', movies=movie, countries=country, genres=genre, genreNum=len(genre))

@home.route("/recommand", methods=['POST', 'GET'])
def recommand():
    form = RecommandForm()
    if form.validate_on_submit():
        r = requests.get("http://127.0.0.1:5000/recommand/"+form.data['recommand'])
        if r.status_code ==200:
            movie = json.loads(r.text, object_hook=Movie.dict2movie)
            return render_template('home/recommand.html', form=form, recommands=movie[1:])
    return render_template('home/recommand.html', form=form)
