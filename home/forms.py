from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, Regexp, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    username = StringField(
        label="Username",
        validators=[DataRequired("Please input username")],
        description="username",
        render_kw={
            "class": "input100",
            "placeholder": "Enter username",
        },
    )
    password = PasswordField(
        label='Password',
        validators=[DataRequired("Please input password")],
        description="password",
        render_kw={
            "class": "input100",
            "placeholder": "Enter password",
        },
    )
    remember_me = BooleanField(
        label='Remember me',
        description="Remember Me",
        render_kw={
            "class": "input-checkbox100",
        },
    )

    submit = SubmitField(
        label='login',
        description='submit',
        render_kw={
            "class": "login100-form-btn",
        }
    )


class RegisterForm(FlaskForm):
    username = StringField(
        label="Username",
        validators=[DataRequired("Please input username")],
        description="username",
        render_kw={
            "class": "input100",
            "placeholder": "Enter username",
        },
    )

    password = PasswordField(
        label='Password',
        validators=[DataRequired("Please input password")],
        description="password",
        render_kw={
            "class": "input100",
            "placeholder": "Enter password",
        },
    )

    email = StringField(
        label='Email',
        validators=[
            DataRequired("Please input email"),
        ],
        description="email",
        render_kw={
            "class": "input100",
            "placeholder": "Enter email",
        },
    )

    submit = SubmitField(
        label='sign_up',
        description='submit',
        render_kw={
            "class": "login100-form-btn",
        }
    )

    def validate_name(self, field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user == 1:
            raise ValidationError("Username exist")


class PostMovieForm(FlaskForm):
    title = StringField(
        label='movie title',
        description='title',
        validators=[DataRequired("Please input a movie title")],
        render_kw={
            "class": "form-control",
        }
    )

    overview = TextAreaField(
        label='overview',
        description='overview',
        render_kw={
            "class": "form-control",
            "row": 3,
        }
    )

    language = StringField(
        label='Language',
        description='languge',
        render_kw={
            "class": "form-control",
        }
    )

    country = StringField(
        label='Country',
        description='country',
        render_kw={
            "class": "form-control",
        }
    )

    director = StringField(
        label='Director',
        description='director',
        render_kw={
            "class": "form-control",
        }
    )

    writer = StringField(
        label='Writer',
        description='writer',
        render_kw={
            "class": "form-control",
        }
    )

    company = StringField(
        label='Company',
        description='company',
        render_kw={
            "class": "form-control",
        }
    )

    runtime = StringField(
        label='Runtime',
        description='runtime',
        render_kw={
            "class": "form-control",
        }
    )

    release_date = StringField(
        label='Release Date',
        description='release_date',
        render_kw={
            "class": "form-control",
        }
    )

    genre = StringField(
        label='Genre',
        description='genre',
        render_kw={
            "class": "form-control",
        }
    )

    star = StringField(
        label='Star',
        description='star',
        render_kw={
            "class": "form-control",
        }
    )

    vote_average = StringField(
        label='Vote average',
        description='vote_average',
        render_kw={
            "class": "form-control",
        }
    )

    vote_count = StringField(
        label='Vote count',
        description='vote_count',
        render_kw={
            "class": "form-control",
        }
    )

    submit = SubmitField(
        label='Submit',
        description='submit',
        render_kw={
            "class": "btn btn-light",
        }
    )


class RecommandForm(FlaskForm):
    recommand = StringField(
        label='Search movie',
        validators=[DataRequired("Please input a movie title")],
        description="recommand",
        render_kw={
            "class": "form-control",
        }
    )

    submit = SubmitField(
        label='Submit',

        description='submit',
        render_kw={
            "class": "btn btn-light",
        }
    )
