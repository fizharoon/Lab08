from flask import Flask, render_template, url_for, redirect, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
db = SQLAlchemy(app)
#admin = Admin(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secretKey'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class MyModelView(ModelView):
    def is_accessible(self):
        if(current_user.is_authenticated):
            isStudent = Student.query.filter_by(user_id=current_user.id).first()
            isTeacher = Teacher.query.filter_by(user_id=current_user.id).first()
            if(not(isStudent or isTeacher)):
                return current_user.is_authenticated
        
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if(current_user.is_authenticated):
            isStudent = Student.query.filter_by(user_id=current_user.id).first()
            isTeacher = Teacher.query.filter_by(user_id=current_user.id).first()
            if(not(isStudent or isTeacher)):
                return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class User(db.Model, UserMixin):
    id = db.Column('id', db.Integer, primary_key = True)
    username = db.Column('username', db.String(100), nullable=False, unique = True)
    password = db.Column('password', db.String(100), nullable=False)

class Teacher(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column('name', db.String(100))
    user_id = db.Column('user_id', db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('Teacher', uselist=False))

# many to many relationship between student and classes
class Student(db.Model):
    __tablename__ = 'Student'
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column('name', db.String(100))
    user_id = db.Column('user_id', db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('Student', uselist=False))

class Courses(db.Model):
    __tablename__ = 'Courses'
    id = db.Column('id', db.Integer, primary_key = True)
    courseName =  db.Column('c_name', db.String(100))
    teacher_id = db.Column('teacher_id', db.ForeignKey('teacher.id'), nullable=False)
    numEnrolled = db.Column('numEnrolled', db.Integer)
    capacity = db.Column('capacity', db.Integer)
    time = db.Column('time', db.String(100))
    teacher = db.relationship('Teacher', backref=db.backref('Courses'))

class Enrollment(db.Model):
    __tablename__='Enrollment'
    id = db.Column('id', db.Integer, primary_key = True)
    student_id = db.Column('student_id', db.ForeignKey('Student.id'), nullable=False)
    course_id = db.Column('course_id', db.ForeignKey('Courses.id'), nullable=False)
    grade = db.Column('grade', db.Integer)
    student = db.relationship('Student', backref=db.backref('Enrollment'))
    courses = db.relationship('Courses', backref=db.backref('Enrollment'))

class CourseView(ModelView):
    def is_accessible(self):
        if(current_user.is_authenticated):
            isStudent = Student.query.filter_by(user_id=current_user.id).first()
            isTeacher = Teacher.query.filter_by(user_id=current_user.id).first()
            if(not(isStudent or isTeacher)):
                return current_user.is_authenticated
        
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
    column_labels = {'Teacher.Name': 'Teacher'}
    column_list = ['courseName','teacher.name','numEnrolled','capacity','time']

class EnrollmentView(ModelView):
    def is_accessible(self):
        if(current_user.is_authenticated):
            isStudent = Student.query.filter_by(user_id=current_user.id).first()
            isTeacher = Teacher.query.filter_by(user_id=current_user.id).first()
            if(not(isStudent or isTeacher)):
                return current_user.is_authenticated
        
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
    column_list = ['student.name', 'courses.courseName', 'grade']

admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Teacher, db.session))
admin.add_view(MyModelView(Student, db.session))
admin.add_view(CourseView(Courses, db.session))
admin.add_view(EnrollmentView(Enrollment, db.session))


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Register')
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
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
            if (user.password == form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')
    #return redirect(url_for('admin.index'))


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)