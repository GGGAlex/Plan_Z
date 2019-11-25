
## stucture of project directory

app/:
.
└── app
    ├── __init__.py
    ├── admin
    ├── data_analysis
    ├── home
    ├── models.py
    ├── static
    └── templates

- models.py: to store some customer object type

app/admin/:
	app/admin/
	├── classifier.py
	├── cosine
	├── indices
	├── smd
	└── views.py

- views.py: store the flask api
- classifier.py, cosine, indices, smd: machining learning

app/home/:
	app/home
	├── __init__.py
	├── forms.py
	├── utils.py
	└── views.py

- views.py: the view of flask project
- utils.py: tool file
- forms.py: store some object of the flask form

## Migrate project:
1. open Pycharm -> File -> New Project (such as: sample)
2. Right click the new Project -> New -> Python Package (named: app), paste the content of the original ass2/app/__init__.py to the new sample/app/__init__.py
3. Right click the new app/ -> New -> Python Package (named: home), past the content of the original ass2/app/home/__init__.py to the new sample/app/home/__init__.py
4. paste other files and folders to the new Project directory (sample/app/)

## Modify the mysql connection:
in app/__init__.py:

``
	homeApp.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Unsw1995@localhost:3306/movie"
``
modify the 'root:Unsw1995' to your own mysql 'username:password'

## Migrate of Mysql:
open the terminal, change directory to the project directory

``
	(base) xxx:sample xxx$ python
``

input:

``
	>>> from app import db
``
``	
	>>> db.create_all()
``

## Launch the project
first, you should run the __main__ in app/admin/views.py, and then run the __main__ in app/home/__init__.py
Finally, open the browser input http://127.0.0.1:5000 and http://0.0.0.0:8080
