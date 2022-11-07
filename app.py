from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
# db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
boot = Bootstrap(app)
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SECRET_KEY'] = 'secretKey'
db = SQLAlchemy(app)
admin = Admin(app)

class User(db.Model, UserMixin):
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

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), nullable=False, unique=True)
#     password = db.Column(db.String(80), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                student = db.session.query(User).join(Student).filter(User.id == user.id).all()
                teacher = db.session.query(User).join(Teacher).filter(User.id == user.id).all()
                # print(student)
                if student:
                    # print('student')
                    return render_template('student.html')
                elif teacher:
                    # print('teacher')
                    return render_template('teacher.html')

                else:
                    print('admin')
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('courses.html', form=form)

@app.route('/getstudentcourses/<student>', methods=['GET'])
def getStudentCourses(student):
    result = db.session.query(Student, Courses, Enrollment)\
        .filter(Student.id == Enrollment.student_id)\
        .filter(Courses.id == Enrollment.course_id)\
        .filter(Student.id == student).all()

    courses = {}
    for course in result:
        courses.update({course.Enrollment.id : \
            (course.Courses.courseName, \
            course.Courses.teacher.name, \
            course.Courses.time, \
            course.Courses.numEnrolled, \
            course.Courses.capacity)})

    return courses

@app.route('/getallcourses', methods=['GET'])
def getAllCourses():
    result = db.session.query(Courses).all()

    courses = {}
    for course in result:
        courses.update({course.id: \
            (course.courseName, \
            course.teacher.name, \
            course.time, \
            course.numEnrolled, \
            course.capacity)})

    return courses

# @app.route('/getteachercourses', methods=['GET'])




# @app.route('/getstudentgrades', methods=['GET'])




if __name__ == "__main__":
    app.run(debug=True)