from project import app
from flask import render_template, redirect, url_for
from flask_login import login_required,current_user
from project.models.dbOperations import *


@app.route('/instructors', methods = ['GET'])
def instructors():
    instructors, instructor_count = getAllInstructors()
    return render_template('instructors.html', instructors=instructors, instructor_count=instructor_count, title='Instructors')

@app.route("/instructor/<int:instructor_id>")
def instructor(instructor_id):
    instructor = getInstructorData(instructor_id)
    return render_template('instructor.html', instructor=instructor, title='Instructors')
