from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify
from flask import abort, render_template
# from flask_cors import CORS
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user
from flask_bootstrap import Bootstrap

app = Flask(__name__)
# CORS(app)
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.sqlite"
app.config["SECRET_KEY"] = 'secretkey'
db = SQLAlchemy(app)
boot = Bootstrap(app)
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
    # classes = db.relationship('Classes', backref='owner')

# many to many relationship between student and classes
class Student(db.Model):
    __tablename__ = 'Student'
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column('name', db.String(100))
    user_id = db.Column('user_id', db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('Student', uselist=False))

    # enrollment = db.relationship('Enrollment', backref=db.backref('Student'))

class Courses(db.Model):
    __tablename__ = 'Courses'
    id = db.Column('id', db.Integer, primary_key = True)
    courseName =  db.Column('c_name', db.String(100))
    teacher_id = db.Column('teacher_id', db.ForeignKey('teacher.id'), nullable=False)
    numEnrolled = db.Column('numEnrolled', db.Integer)
    capacity = db.Column('capacity', db.Integer)
    time = db.Column('time', db.String(100))
    teacher = db.relationship('Teacher', backref=db.backref('Courses'))
    # students = db.relationship('Student', secondary=enrollment_course, backref=db.backref('Courses'))

class Enrollment(db.Model):
    __tablename__='Enrollment'
    id = db.Column('id', db.Integer, primary_key = True)
    student_id = db.Column('student_id', db.ForeignKey('Student.id'), nullable=False)
    course_id = db.Column('course_id', db.ForeignKey('Courses.id'), nullable=False)
    grade = db.Column('grade', db.Integer)
    student = db.relationship('Student', backref=db.backref('Enrollment'))
    courses = db.relationship('Courses', backref=db.backref('Enrollment'))

class CourseView(ModelView):
    # course_name = Courses.courseName
    column_labels = {'Teacher.Name': 'Teacher'}
    column_list = ['courseName','teacher.name','numEnrolled','capacity','time']

class EnrollmentView(ModelView):
    # column_labels =
    # column_labels = dict(name='Name', last_name='Last Name')
    column_list = ['student.name', 'courses.courseName', 'grade']

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Teacher, db.session))
admin.add_view(ModelView(Student, db.session))
# admin.add_view(ModelView(Courses, db.session))
admin.add_view(CourseView(Courses, db.session))
# admin.add_view(ModelView(Enrollment, db.session))
admin.add_view(EnrollmentView(Enrollment, db.session))

@app.route('/courses', methods=['GET', 'POST'])
# @login_required
def courses():
    return render_template('courses.html')

@app.route('/teacher', methods=['GET', 'POST'])
# @login_required
def teacher():
    return render_template('teacher.html')

if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)