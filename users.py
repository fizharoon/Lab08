from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify
from flask import abort, render_template
# from flask_cors import CORS
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
# CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.sqlite" 
app.config["SECRET_KEY"] = 'urmom'
db = SQLAlchemy(app) 
admin = Admin(app)
class User(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    username = db.Column('username', db.String(100))
    password = db.Column('password', db.String(100))

admin.add_view(ModelView(User, db.session))

if __name__=='__main__':
    # db.create_all()
    app.run(debug=True)