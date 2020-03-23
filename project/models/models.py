from project.config.Database import db
from flask_login import UserMixin
from project import login_manager

@login_manager.user_loader
def load_user(user_id):
    return RegUser.query.get(int(user_id))

class Department(db.Model):
    __tablename__ = 'department'
    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(50))
    faculty_name = db.Column(db.String(50))
    users = db.relationship('RegUser', backref='department', lazy=True)
    courses = db.relationship('Course', backref='department', lazy=True)

    def __repr__(self):
        return f"department('{self.department_name}', '{self.faculty_name}')"

class RegUser(db.Model,UserMixin):
    __tablename__ = 'reguser'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    surname = db.Column(db.String(30))
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.Integer, default=0)
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'),nullable=False)
    instructor = db.relationship('Instructor', backref='reguser', single_parent=True, cascade="all, delete-orphan", uselist=False)
    student = db.relationship('Student', backref='reguser', single_parent=True, cascade="all, delete-orphan", uselist=False)

    def get_id(self):
        return (self.user_id)

    def isAdmin(self):
        if(self.user_type == 0):
            return True
        else:
            return False

    def isInstructor(self):
        if(self.user_type == 1):
            return True
        else:
            return False

    def isStudent(self):
        if(self.user_type == 2):
            return True
        else:
            return False

    def __repr__(self):
        return f"reguser('{self.name}', '{self.surname}', '{self.email}', '{self.password}', '{self.user_type}'), '{self.department_id}"

class Instructor(db.Model):
    __tablename__ = 'instructor'
    title = db.Column(db.String(50))
    instructor_id = db.Column(db.Integer, db.ForeignKey('reguser.user_id'), nullable=False, primary_key=True)
    courses = db.relationship('Course', backref='instructor', cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f"instructor('{self.title}')"

class Student(db.Model):
    __tablename__ = 'student'
    id_number = db.Column(db.String(9))
    student_id = db.Column(db.Integer, db.ForeignKey('reguser.user_id'), nullable=False, primary_key=True)
    grades = db.relationship('Student_Grade', backref='student', cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f"student('{self.id_number}')"

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True)
    crn = db.Column(db.String(5))
    name = db.Column(db.String(50))
    course_code = db.Column(db.String(10))
    credit = db.Column(db.String(3))
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.instructor_id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'))
    
    courseOutcomes = db.relationship('Course_Outcome', backref='course', cascade="all, delete-orphan", lazy=True)
    grades = db.relationship('Student_Grade', backref='course', cascade="all, delete-orphan", lazy=True)

    requisites = db.relationship(
        'Prerequisite', primaryjoin="or_(Course.course_id==Prerequisite.course_id, Course.course_id==Prerequisite.requisite_id)", cascade="all, delete-orphan", lazy='dynamic')

    def __repr__(self):
        return f"course('{self.crn}', '{self.name}', '{self.course_code}', '{self.instructor_id}')"

class Outcome(db.Model):
    __tablename__ = 'outcome'
    outcome_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    courseOutcomes = db.relationship('Course_Outcome', backref='outcome', cascade="all, delete-orphan", lazy=True)
    def __repr__(self):
        return f"outcome('{self.name}')"

class Course_Outcome(db.Model):
    __tablename__ = 'course_outcome'
    course_outcome_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'))
    outcome_id = db.Column(db.Integer, db.ForeignKey('outcome.outcome_id'))

    def __repr__(self):
        return f"course_outcome('{self.course_id}', '{self.outcome_id}')"

class Prerequisite(db.Model):
    __tablename__ = 'prerequisite'
    prerequisite_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)
    requisite_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)

    def __repr__(self):
        return f"prerequisite('{self.course_id}', '{self.requisite_id}')"

class Student_Grade(db.Model):
    __tablename__ = 'student_grade'
    student_grade_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'))
    grade = db.Column(db.String(2))

    def __repr__(self):
        return f"student_grade('{self.student_id}', '{self.course_id}','{self.grade}')"
