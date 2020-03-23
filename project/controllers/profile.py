from project import app
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from project.models.models import RegUser, Department
from project.models.dbOperations import *
from project.controllers.forms import InstructorProfileUpdateForm, StudentProfileUpdateForm, ChangePasswordForm,DeleteUserForm


@app.route('/profile', methods = ['GET','POST'])
@login_required
def profile():
    userData = getUserData(current_user.user_id)
    form = DeleteUserForm()
    if form.validate_on_submit():
        if(deleteUserDB(current_user.user_id)):
            flash("account deleted.")
            return redirect(url_for('logout'))
    return render_template('profile.html', user=userData, title='Profile',form=form)


@app.route('/updateProfile', methods = ['GET', 'POST'])
@login_required
def profileUpdate():
    passwordForm = ChangePasswordForm()

    if current_user.user_type == 1:
        form = InstructorProfileUpdateForm()
    else:
        form = StudentProfileUpdateForm()

    if form.validate_on_submit() and form.submit.data:
        updateUserData(current_user.user_id, form)
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile'))

    if passwordForm.validate_on_submit() and passwordForm.submit.data:
        updateUserPassword(current_user.user_id, passwordForm)
        flash('Your password has been updated!', 'success')
        return redirect(url_for('profile'))

    if request.method == 'GET':
        form.name.data = current_user.name
        form.surname.data = current_user.surname
        form.department.data = current_user.department_id
        if current_user.user_type == 1:
            form.private_info.data = current_user.instructor.title
        else:
            form.private_info.data = current_user.student.id_number

    return render_template('profileEdit.html', form=form, passForm=passwordForm, user_id=current_user.user_type, title='Update Profile')