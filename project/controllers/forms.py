from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from project.models.models import Course, Outcome, Department, RegUser
from project.config.Database import db


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')

  
class RegistrationForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired(), Length(min=2, max=30)], render_kw={"placeholder": "First Name"})
    surname = StringField('Surname:', validators=[DataRequired(), Length(min=2, max=30)], render_kw={"placeholder": "Last Name"})
    email = StringField('Email', validators=[DataRequired(), Length(min=2, max=30)], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', 
                             validators=[DataRequired(),Length(min=5, max=10)], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "re-Password"})
    department = SelectField('Department:', validators=[DataRequired()], choices=[(dept.department_id, dept.department_name) for dept in db.session.query(Department).all()], coerce= int, render_kw={"placeholder": "Department"})
    title = StringField('Title', validators=[Length(max=30)], render_kw={"placeholder": "Title"})
    student_no = StringField('Student No', validators=[Length(max=9)], render_kw={"placeholder": "Student Number"})
    submit = SubmitField('Sign Up')


class InstructorProfileUpdateForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired(), Length(min=2, max=30)], render_kw={"placeholder": "First Name"})
    surname = StringField('Surname:', validators=[DataRequired(), Length(min=2, max=30)], render_kw={"placeholder": "Last Name"})
    department = SelectField('Department:', validators=[DataRequired()], choices=[(
        dept.department_id, dept.department_name) for dept in db.session.query(Department).all()], coerce=int, render_kw={"placeholder": "Department"})
    private_info = StringField('Title', validators=[Length(max=30)], render_kw={"placeholder": "Title"})
    submit = SubmitField('Update')

class StudentProfileUpdateForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired(), Length(min=2, max=30)], render_kw={"placeholder": "First Name"})
    surname = StringField('Surname:', validators=[DataRequired(), Length(min=2, max=30)], render_kw={"placeholder": "Last Name"})
    department = SelectField('Department:', validators=[DataRequired()], choices=[(
        dept.department_id, dept.department_name) for dept in db.session.query(Department).all()], coerce=int, render_kw={"placeholder": "Department"})
    private_info = StringField('Student Number', validators=[Length(max=9)], render_kw={"placeholder": "Student Number"})
    submit = SubmitField('Update')

class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(),Length(min=5, max=10)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Change Password')
    

class CourseRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=5, max=50)])
    crn = StringField('CRN', validators=[DataRequired(), Length(min=5, max=5)], render_kw={"placeholder": "12560"})
    course_code = StringField('Code',validators=[DataRequired(), Length(min=6, max=8)], render_kw={"placeholder": "MAT103E"})
    credit = StringField('Credit', validators=[DataRequired(), Length(min=1, max=3)], render_kw={"placeholder": "3.0"})
    department = SelectField('Department:', validators=[DataRequired()], choices=[(
        dept.department_id, dept.department_name) for dept in db.session.query(Department).all()], coerce=int)
    prerequisites = SelectMultipleField('Prerequisite/s:', coerce=int)
    outcomes = SelectMultipleField('Outcome/s:', coerce=int)
    submit = SubmitField('Add')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.outcomes.choices = [(out.outcome_id, out.name)
                                 for out in db.session.query(Outcome).all()]
        self.prerequisites.choices = [(
            course.course_id, course.course_code) for course in db.session.query(Course).all()]


class CourseUpdateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=5, max=50)])
    crn = StringField('CRN', validators=[DataRequired(), Length(min=5, max=5)], render_kw={"placeholder": "12560"})
    course_code = StringField('Code', validators=[DataRequired(), Length(min=6, max=8)], render_kw={"placeholder": "MAT103E"})
    credit = StringField('Credit', validators=[DataRequired(), Length(min=1, max=3)], render_kw={"placeholder": "3.0"})
    department = SelectField('Department:', validators=[DataRequired()], choices=[(
        dept.department_id, dept.department_name) for dept in db.session.query(Department).all()], coerce=int)
    prerequisites = SelectMultipleField('Prerequisite/s:', coerce=int)
    outcomes = SelectMultipleField('Outcome/s:', coerce=int)
    submit = SubmitField('Update')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.outcomes.choices = [(out.outcome_id, out.name)
                                 for out in db.session.query(Outcome).all()]
        self.prerequisites.choices = [(
            course.course_id, course.course_code) for course in db.session.query(Course).all()]

class OutcomeRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=30)])
    submit = SubmitField('Add')

class StudentGradeForm(FlaskForm):
    aa = SubmitField('AA')
    ba = SubmitField('BA')
    bb = SubmitField('BB')
    cb = SubmitField('CB')
    cc = SubmitField('CC')
    dc = SubmitField('DC')
    dd = SubmitField('DD')
    vf = SubmitField('VF')
    ff = SubmitField('FF')

class DeleteUserForm(FlaskForm):
    delete = SubmitField('DELETE')

class InstructorUpdateProfileForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired(), Length(min=2, max=30)])
    surname = StringField('Surname:', validators=[DataRequired(), Length(min=2, max=30)])
    title = StringField('Title:', validators=[DataRequired(), Length(min=3, max=50)])
    department = SelectField('Department:', validators=[DataRequired()], choices=[(
        dept.department_id, dept.department_name) for dept in db.session.query(Department).all()], coerce=int)
    submit = SubmitField('Update profile')

class StudentUpdateProfileForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired(), Length(min=2, max=30)])
    surname = StringField('Surname:', validators=[DataRequired(), Length(min=2, max=30)])
    id_num = StringField('Student No:', validators=[DataRequired(), Length(min=8, max=9)])
    department = SelectField('Department:', validators=[DataRequired()], choices=[(
        dept.department_id, dept.department_name) for dept in db.session.query(Department).all()], coerce=int)
    submit = SubmitField('Update profile')

class ChangePasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(),Length(min=6,max=10)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Change password')
