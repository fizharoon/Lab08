from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify
from flask import abort, render_template
# from flask_cors import CORS
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user

app = Flask(__name__)
# CORS(app)
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.sqlite" 
app.config["SECRET_KEY"] = 'urmom'
db = SQLAlchemy(app)

admin = Admin(app)

class User(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    username = db.Column('username', db.String(100))
    password = db.Column('password', db.String(100))

class Teacher(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column('name', db.String(100))
    user_id = db.Column('user_id', db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('Teacher', uselist=False))

class Student(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column('name', db.String(100))
    user_id = db.Column('user_id', db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('Student', uselist=False))

# class UserView(ModelView): 
#     column_searchable_list = ['username'] # make columns searchable
#     form_choices = { # restrict the possible values for a text-field
#     'title': [ 
#         ('MR', 'Mr'), 
#         ('MRS', 'Mrs'), 
#         ('MS', 'Ms'), 
#         ('DR', 'Dr')
#         ] 
#     } 
#     can_export = True # enable csv export of the model view

# class Classes(db.Model):
#     id = db.Column('id', db.Integer, primary_key = True)
#     name = db.Column('name', db.String(100))
#     user_id = db.Column('user_id', db.ForeignKey('user.id'), nullable=False)
#     user = db.relationship('User', backref=db.backref('Student', uselist=False))


# admin.add_view(UserView(User, db.session)) 

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Teacher, db.session))
admin.add_view(ModelView(Student, db.session))

if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)