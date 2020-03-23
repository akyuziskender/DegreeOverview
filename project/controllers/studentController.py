from project import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_required,current_user
from project.models.dbOperations import *


@app.route('/deleteGrade/<int:course_id>')
@login_required
def deleteGrade(course_id):
    if (current_user.isStudent() == False):
        return redirect('home')
    else:
        if deleteGradeDB(current_user.user_id, course_id):
            flash("Your grade has been deleted succesfully.")
            return(redirect(url_for('courses')))
        else:
            flash("Your grade could not been deleted.")
            return(redirect(url_for('courses')))