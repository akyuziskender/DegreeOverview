from project import app
from flask import render_template, redirect, url_for, flash, request
from project.models.dbOperations import *
from flask_login import login_required, current_user
from project.controllers.forms import CourseRegistrationForm, OutcomeRegistrationForm, StudentGradeForm,CourseUpdateForm

@app.route('/courses', methods = ['GET', 'POST'])
def courses():
    courses, courses_count = getAllCourses()
    form = StudentGradeForm()

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            return redirect(url_for('Login'))
        if current_user.isStudent():
            GradeFormManager(form, current_user.user_id, int(request.form['course']))
            return redirect(url_for('courses'))
        else:
            flash("You must be student.")
    return render_template('courses.html', courses=courses, form=form, courses_count=courses_count, title='Courses')

@app.route("/course/<int:course_id>", methods = ['GET', 'POST'])
def course(course_id):
    user_type = ""
    course = getCourseData(course_id)
    studentGrade = GradeSetup(course_id)

    if current_user.is_authenticated:
        if course['insturctorId'] == current_user.user_id:
            user_type = "instructor"
        elif current_user.isStudent():
            user_type = "student"    
    form = StudentGradeForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            return redirect(url_for('Login'))
        if current_user.isStudent():
            GradeFormManager(form, current_user.user_id, course_id)
            return redirect(url_for('course', course_id=course_id))
        else:
            flash("You need to be student to add a grade.")
    return render_template('course.html', user_type=user_type, form=form, course=course, course_id=course_id, student_grade=studentGrade, title='Courses')

@app.route('/addCourse', methods = ['GET', 'POST'])
@login_required
def courseAdd():
    if (current_user.isInstructor() == False):
        flash("You don't have permission to add a course.")
        return redirect('home')
    form = CourseRegistrationForm()
    if form.validate_on_submit():
        if registerCourse(form, current_user.user_id):
            flash('New course has been created!', 'success')
            return redirect(url_for('home'))
        else:
            flash('The crn already exist.')
    return render_template('courseAdd.html', form=form, title='Courses')


@app.route('/editCourse/<int:course_id>', methods = ['GET', 'POST'])
@login_required
def courseEdit(course_id):
    if (current_user.isInstructor() == False):
        return redirect(url_for('home'))
    course = getCourse(course_id)
    form = CourseUpdateForm()
    if form.validate_on_submit():
        if updateCourseData(course_id, form):
            flash('Course edited!', 'success')
            return redirect(url_for('course',course_id= course_id))
        else:
            flash('Course could not be edited.')
    elif request.method == 'GET':
        form.name.data = course.name
        form.crn.data = course.crn
        form.course_code.data = course.course_code
        form.credit.data = course.credit
        form.department.data = course.department_id
        form.prerequisites.data = getPrerequisitesIds(course_id)
        form.outcomes.data = getOutcomeIds(course_id)

    return render_template('courseAdd.html', form=form, course=course, title='Courses')

@app.route('/deleteCourse/<int:course_id>')
@login_required
def courseDelete(course_id):
    instructor_id = getInstructorIdForACourse(course_id)
    if current_user.isInstructor() and current_user.user_id == instructor_id:       # checking if the user is instructor and opened this course
        if deleteCourse(course_id):
            flash("The course has been deleted.")
    else:
        flash("You don't have authorization to delete this course.")
    return redirect(url_for('home'))


@app.route('/addOutcome', methods = ['GET', 'POST'])
@login_required
def outcomeAdd():
    if (current_user.isInstructor() == False):
        flash("You don't have permission to add an outcome.")
        return redirect('home')
    form = OutcomeRegistrationForm()
    if form.validate_on_submit():
        if registerOutcome(form):
            flash('New outcome has been created!', 'success')
            return redirect(url_for('home'))
        else:
            flash('The outcome already exists.')
    return render_template('outcomeAdd.html', form=form, title='Add a new outcome')

def GradeSetup(course_id):
    studentGrade = '-'
    if current_user.is_authenticated:
        studentGrade = getStudentGrade(current_user.user_id, course_id)
        if studentGrade is None:
            studentGrade = '-'
    print(studentGrade)
    return studentGrade

def GradeFormManager(form, user_id, course_id):
    if form.aa.data:
        addStudentGrade(user_id, course_id, 'AA')
    elif form.ba.data:
        addStudentGrade(user_id, course_id, 'BA')
    elif form.bb.data:
        addStudentGrade(user_id, course_id, 'BB')
    elif form.cb.data:
        addStudentGrade(user_id, course_id, 'CB')
    elif form.cc.data:
        addStudentGrade(user_id, course_id, 'CC')
    elif form.dc.data:
        addStudentGrade(user_id, course_id, 'DC')
    elif form.dd.data:
        addStudentGrade(user_id, course_id, 'DD')
    elif form.vf.data:
        addStudentGrade(user_id, course_id, 'VF')
    elif form.ff.data:
        addStudentGrade(user_id, course_id, 'FF')
    return redirect(url_for('course', course_id=course_id))
