from flask import Flask, render_template, url_for, redirect, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
# db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
boot = Bootstrap(app)
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SECRET_KEY'] = 'secretKey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


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

admin = Admin(app, index_view=MyAdminIndexView())


class User(db.Model, UserMixin):
    id = db.Column('id', db.Integer, primary_key = True)
    username = db.Column('username', db.String(100))
    password = db.Column('password', db.String(100))
    # def get_id(self):
    #     return id

class Teacher(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column('name', db.String(100))
    user_id = db.Column('user_id', db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('Teacher', uselist=False))
    # classes = db.relationship('Classes', backref='owner')
class TeacherView(ModelView):
    column_list = ['user.username','name']
# many to many relationship between student and classes
class Student(db.Model):
    __tablename__ = 'Student'
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column('name', db.String(100))
    user_id = db.Column('user_id', db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('Student', uselist=False))

    # enrollment = db.relationship('Enrollment', backref=db.backref('Student'))
class StudentView(ModelView):
    column_list = ['user.username','name']

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
    id = db.Column('id', db.Integer)
    student_id = db.Column('student_id', db.ForeignKey('Student.id'), primary_key=True)
    course_id = db.Column('course_id', db.ForeignKey('Courses.id'), primary_key=True)
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


admin.add_view(MyModelView(User, db.session))
# admin.add_view(MyModelView(Teacher, db.session))
admin.add_view(TeacherView(Teacher, db.session))

# admin.add_view(MyModelView(Student, db.session))
admin.add_view(StudentView(Student, db.session))

# admin.add_view(ModelView(Courses, db.session))
admin.add_view(CourseView(Courses, db.session))
# admin.add_view(ModelView(Enrollment, db.session))
admin.add_view(EnrollmentView(Enrollment, db.session))

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), nullable=False, unique=True)
#     password = db.Column(db.String(80), nullable=False)


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
            if user.password == form.password.data:
                student = db.session.query(User).join(Student).filter(User.id == user.id).all()
                teacher = db.session.query(User).join(Teacher).filter(User.id == user.id).all()
                # print(student)
                if student:
                    # print('student')
                    login_user(user)

                    return redirect('/student')
                elif teacher:
                    # print('teacher')
                    login_user(user)

                    return redirect('/teacher')

                else:
                    # print('admin')
                    login_user(user)

                    return redirect(url_for('admin.index'))

            # return redirect(url_for('dashboard'))
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


@app.route('/getstudentcourses', methods=['GET'])
def getStudentCourses():
    student = Student.query.filter_by(user_id=current_user.id).first()
    result = db.session.query(Student, Courses, Enrollment)\
        .filter(Student.id == Enrollment.student_id)\
        .filter(Courses.id == Enrollment.course_id)\
        .filter(Student.id == student.id).all()

    studentCourses = {}
    for course in result:
        studentCourses.update({course.Enrollment.id : \
            (course.Courses.courseName,
            course.Courses.teacher.name,
            course.Courses.time,
            str(course.Courses.numEnrolled) + '/' + str(course.Courses.capacity)
            )})

    return studentCourses

@app.route('/getallcourses', methods=['GET'])
def getAllCourses():
    student = Student.query.filter_by(user_id=current_user.id).first()
    subquery = db.session.query(Enrollment).join(Student, student==Enrollment.student).subquery()
    result = db.session.query(Courses, subquery).outerjoin(subquery, Courses.id == subquery.c.course_id)
    # print(result)
    # result = db.session.query(Courses)
    allCourses = {}
    for course in result:
        # print(course)
        allCourses.update({course.Courses.id: \
            (course.Courses.courseName, \
            course.Courses.teacher.name, \
            course.Courses.time, \
            str(course.Courses.numEnrolled) + '/' + str(course.Courses.capacity),
            'enrolled' if course[1] else 'not enrolled'
            )})
    # print(allCourses)
    return allCourses



@app.route('/getteachercourses', methods=['GET'])
def getTeacherCourses():
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()

    result = db.session.query(Courses) \
            .join(Teacher, teacher.id==Courses.teacher_id).all()

    teacherCourses = {}

    for course in result:
        teacherCourses.update({course.id:
            {'cName' : course.courseName,
            'tName' : course.teacher.name,
            'time' : course.time,
            'enrolled' : course.numEnrolled,
            'capacity' : course.capacity,
            'id' : course.id
             }

        })
    print(teacherCourses)
    return teacherCourses

@app.route('/getstudentgrades/<courseid>', methods=['GET'])
def getStudentGrades(courseid):
    result = db.session.query(Enrollment, Student, Courses) \
            .join(Student, Enrollment.student_id == Student.id)\
            .join(Courses, Enrollment.course_id == courseid) \
            .all()

    studentGrades = {}
    for student in result:
        studentGrades.update({student.Enrollment.id:
            {
                'name' : student.Student.name,
                'grade' : student.Enrollment.grade

            }})
    # print(studentGrades)
    return studentGrades



# @app.route('/grades/<name>', methods=['PUT'])
# def update_grade(name):
#     student = Grade.query.get(name)
#     student.name = request.json['name']
#     student.grade = request.json['grade']
#     db.session.commit()
#     return {student.name: student.grade}
# @app.route('/grades', methods=['POST'])
# def create_student():
#     student = Grade(name=request.json['name'], grade=request.json['grade'])
#     db.session.add(student)
#     db.session.commit()

#     return {student.name: student.grade}
# add student to course
@app.route('/addstudent', methods=['POST'])
def addStudentToClass():
    course = Courses.query.get(request.json['course_id'])
    if course.numEnrolled + 1 > course.capacity:
        return abort(406)

    course.numEnrolled += 1
    # print(Student.query.filter_by(user_id=current_user.id).first().id, request.json['course_id'])

    enrollment = Enrollment(student_id=Student.query.filter_by(user_id=current_user.id).first().id, course_id=request.json['course_id'])
    db.session.add(enrollment)
    db.session.commit()

    return {enrollment.id : [enrollment.student_id, enrollment.course_id]}

@app.route('/dropcourse', methods=['DELETE'])
def delete_student():
    student_id = current_user.id
    course_id = request.json['course_id']

    course = Courses.query.get(course_id)
    course.numEnrolled -= 1

    enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()

    print(enrollment)

    db.session.delete(enrollment)
    db.session.commit() 
    return {}, 204
    
@app.route('/updategrade', methods=['PUT'])
def updateGrade():
    student = request.json['student_id']
    course = request.json['course_id']
    grade = request.json['grade']

    enrollment = Enrollment.query.get(student_id=student, course_id=course)
    enrollment.grade = grade

    db.session.commit()

    return 200




# @app.route('/courses', methods=['GET', 'POST'])
# # @login_required
# def courses():
#     return render_template('courses.html')

# @app.route('/teacher', methods=['GET', 'POST'])
# # @login_required
# def teacher():
#     return render_template('teacher.html')

# @app.route('/student', methods=['GET', 'POST'])
# # @login_required
# def student():
#     return render_template('student.html')

# @app.route('/admin', methods=['GET', 'POST'])
# def admin():
#     return redirect(url_for('admin.index'))

@app.route('/courses/<courseid>', methods=['GET', 'POST'])
@login_required
def courses(courseid):
    course = Courses.query.get(courseid)
    
    result = db.session.query(Enrollment, Student, Courses) \
            .join(Student, Enrollment.student_id == Student.id)\
            .join(Courses, Enrollment.course_id == courseid) \
            .all()

    studentGrades = {}
    for student in result:
        studentGrades.update({student.Enrollment.id:
            {
                'id' : student.Student.id,
                'name' : student.Student.name,
                'grade' : student.Enrollment.grade

            }})
    return render_template('courses.html', course=course, studentGrades=studentGrades)

@app.route('/teacher', methods=['GET', 'POST'])
@login_required
def teacher():
    user = current_user.id
    teach = Teacher.query.filter_by(user_id=user).first()
    courses = getTeacherCourses()
    return render_template('teacher.html', courses=courses, teacher=teach)


@app.route('/student', methods=['GET', 'POST'])
# @login_required
def student():
    user = current_user.id
    stdnt = Student.query.filter_by(user_id=user).first()
    return render_template('student.html', student=stdnt)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return redirect(url_for('admin.index'))

if __name__ == "__main__":
    app.run(debug=True)