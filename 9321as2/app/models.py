# coding:utf-8
import datetime
from app import db
import json
import time


# 会员
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    username = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱

    # is_authenticated 方法有一个具有迷惑性的名称。
    # 一般而言，这个方法应该只返回 True，
    # 除非表示用户的对象因为某些原因不允许被认证
    @property
    def is_authenticated(self):
        return True

    # is_active 方法应该返回 True，除非是用户是无效的，
    # 比如因为他们的账号是被禁止
    @property
    def is_active(self):
        return True

    # is_anonymous 方法应该返回 True，
    # 如果是匿名的用户不允许登录系统。
    @property
    def is_anonymous(self):
        return False

    # get_id 方法应该返回一个用户唯一的标识符，以 unicode 格式。
    # 我们使用数据库生成的唯一的 id。
    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return "<User %r>" % self.username

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 会员登录日志
class Userlog(db.Model):
    __tablename__ = "userlogs"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 所属会员
    ip = db.Column(db.String(100))  # ip地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow())  # 登陆时间

    def __repr__(self):
        return "<Userlog %r>" % self.id


class Movie:
    def __init__(self, title, language="", genre="", overview="", release_date="", \
                 runtime=0.0, vote_count=0, director="", star="", writer="", country="", vote_average=0.0):
        self.title = title
        self.language = language
        self.overview = overview
        self.release_date = release_date
        self.runtime = runtime
        self.genre = genre
        self.vote_count = vote_count
        self.director = director
        self.star = star
        self.writer = writer
        self.country = country
        self.vote_average = vote_average

    def dict2movie(dic):
        return Movie(dic['title'], dic['language'], dic['genre'], dic['overview'], \
                     dic['release_date'], dic['runtime'], dic['vote_count'], \
                     dic['director'], dic['star'], dic['writer'], dic['country'], \
                     dic['vote_average'])

    def movie2json(obj):
        return {
            "title": obj.title,
            "language": obj.language,
            "overview": obj.overview,
            "release_date": obj.release_date,
            "runtime": obj.runtime,
            "genre": obj.genre,
            "vote_count": obj.vote_count,
            "director": obj.director,
            "star": obj.star,
            "writer": obj.writer,
            "country": obj.country,
            "vote_average": obj.vote_average,
        }


class BestMovie:
    def __init__(self, title, language, release_date, country, vote_average, director):
        self.title = title
        self.language = language
        self.release_date = release_date
        self.country = country
        self.vote_average = vote_average
        self.director = director

    def dict2movie(self):
        return BestMovie(
            self['title'], self['language'], self['release_date'], self['country'], \
            self['vote_average'], self['director']
        )


class CountryNum:
    def __init__(self, country, count):
        self.country = country
        self.count = count

    def dict2counNum(self):
        return CountryNum(
            self['country'], self['country_count']
        )


class TypeNum:
    def __init__(self, genre, count):
        self.genre = genre
        self.count = count

    def __str__(self):
        classDic = self.__dict__
        return json.dumps(classDic)

    def dict2typeNum(self):
        return TypeNum(
            self['genre'], self['count']
        )


class Log:
    def __init__(self, IP_address, Time, Function):
        self.IP_address = IP_address
        self.Time = str(time.strftime('%Y-%m-%d',time.localtime(Time)))
        self.Function = Function

    def log2json(self):
        return {
            "IP_address": self.IP_address,
            "Time": self.Time,
            "Function": self.Function
        }