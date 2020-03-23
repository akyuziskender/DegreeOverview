from project import login_manager
from project.models.models import *
from project.config.crypto import Crypto
from project.config.Database import db


def registerUser(form):
    secret_password = Crypto.convertPassword(form.password.data)
    user = RegUser.query.filter_by(email=form.email.data+"@itu.edu.tr").first()
    if not user:    # if the email is not taken, create the user
        type = 2 if len(form.title.data) == 0 else 1
        user = RegUser(name=form.name.data, surname=form.surname.data, 
                email=form.email.data+"@itu.edu.tr", password=secret_password, 
                user_type=type, department_id=form.department.data)
        db.session.add(user)
        db.session.commit()
        if type == 1:   # if new user is a instructor
            instructor = Instructor(instructor_id=user.user_id, title=form.title.data)
            db.session.add(instructor)
            db.session.commit()
        else:           # otherwise, the user is a student
            student = Student(student_id=user.user_id, id_number=form.student_no.data)
            db.session.add(student)
            db.session.commit()
        return True
    else:
        print("The email is already taken.")
        return False

def registerCourse(form, user_id):
    course = Course.query.filter_by(crn=form.crn.data).first()
    if not course:
        course = Course(crn=form.crn.data, name=form.name.data, course_code=form.course_code.data,
                        credit=form.credit.data, department_id=form.department.data, instructor_id=user_id)
        db.session.add(course)
        db.session.commit()
        for id in form.prerequisites.data:      # adding all the prerequisites
            prerequisite = Prerequisite(course_id=course.course_id, requisite_id=id)
            db.session.add(prerequisite)
            db.session.commit()
        for outcome_id in form.outcomes.data:   # adding all the outcomes
            course_outcome = Course_Outcome(course_id=course.course_id, outcome_id=outcome_id)
            db.session.add(course_outcome)
            db.session.commit()
        return True
    else:
        return False



def updateCourseData(course_id, form):
    course = Course.query.filter_by(crn=form.crn.data).first()
    updated_course = Course.query.get_or_404(course_id)
    if course and updated_course.crn != form.crn.data:
        return False
    updated_course.crn = form.crn.data
    updated_course.name = form.name.data
    updated_course.course_code = form.course_code.data
    updated_course.credit = form.credit.data
    updated_course.department_id = form.department.data


    Course_Outcome.query.filter_by(course_id=course_id).delete()
    Prerequisite.query.filter_by(course_id=course_id).delete()

    for id in form.prerequisites.data:  # adding all the prerequisites
        prerequisite = Prerequisite(course_id=updated_course.course_id, requisite_id=id)
        db.session.add(prerequisite)
    for outcome_id in form.outcomes.data:  # adding all the outcomes
        course_outcome = Course_Outcome(course_id=updated_course.course_id, outcome_id=outcome_id)
        db.session.add(course_outcome)

    db.session.commit()
    return True



def deleteCourse(course_id):
    course = Course.query.get_or_404(course_id)
    if not course:
        return False
    else:
        db.session.delete(course)
        db.session.commit()
    return True


def registerOutcome(form):
    outcome = Outcome.query.filter_by(name=form.name.data).first()
    if not outcome:
        outcome = Outcome(name=form.name.data)
        db.session.add(outcome)
        db.session.commit()
        return True
    else:
        return False


def getUserData(user_id):
    userData = {}
    user = RegUser.query.filter_by(user_id=user_id).first()
    userData['user_id'] = user_id
    userData['type'] = 'Instructor' if user.user_type == 1 else 'Student'
    userData['name'] = user.name
    userData['surname'] = user.surname
    userData['department'] = Department.query.filter_by(department_id=user.department_id).first().department_name

    if user.user_type == 1 :
        userData['private_info'] = user.instructor.title
        userData['user_type'] = 1
    else:
        userData['private_info'] = user.student.id_number
        userData['user_type'] = 2

    userData['email'] = user.email
    
    return userData


def updateUserData(user_id, form):
    user = RegUser.query.get_or_404(user_id)
    user.name = form.name.data
    user.surname = form.surname.data
    user.department_id = form.department.data
    if user.user_type == 1:
        user.instructor.title = form.private_info.data
    else:
        user.student.id_number = form.private_info.data
    db.session.commit()
    return


def updateUserPassword(user_id, form):
    secret_password = Crypto.convertPassword(form.password.data)        # encrypting the password
    user = RegUser.query.get_or_404(user_id)                            # getting the user
    user.password = secret_password                                     # change the password in database
    db.session.commit()                                                 # commit
    return

def getPrerequisites(course_id):
    prerequisite = []
    requisite_ids = Prerequisite.query.filter_by(course_id=course_id)
    for _id in requisite_ids:
        requisite = {}
        requisite['course_id'] = _id.requisite_id
        requisite['name'] = Course.query.get_or_404(_id.requisite_id).course_code
        prerequisite.append(requisite.copy())
    return prerequisite

def getPrerequisitesAsString(course_id):
    prerequisite = ""
    requisite_ids = Prerequisite.query.filter_by(course_id=course_id)
    for _id in requisite_ids:
        prerequisite += Course.query.get_or_404(_id.requisite_id).course_code
        prerequisite += ", "
    prerequisite = prerequisite[:-2]
    return prerequisite


def getOutcomes(course_id):
    outcome = ""
    outcome_ids = Course_Outcome.query.filter_by(course_id=course_id)
    for _id in outcome_ids:
        outcome += Outcome.query.get_or_404(_id.outcome_id).name
        outcome += ", "
    outcome = outcome[:-2]
    return outcome


def getAllCourses():
    result_courses = []
    courseData = {}
    courses = Course.query.all()

    for course in courses:
        courseData['course_id'] = course.course_id
        courseData['code'] = course.course_code

        prerequisites = getPrerequisitesAsString(course.course_id)
        courseData['prerequisites'] = prerequisites
        
        outcomes = getOutcomes(course.course_id)
        courseData['outcomes'] = outcomes

        result_courses.append(courseData.copy())
    return result_courses, len(courses)

def getInstructorFullName(instructor_id):
    return '%s %s' % (RegUser.query.filter_by(user_id=instructor_id).first().name, 
                                        RegUser.query.filter_by(user_id=instructor_id).first().surname)

   
def getCourseData(course_id):
    courseData = {}
    course = Course.query.get_or_404(course_id)
    courseData['course_code'] = course.course_code
    courseData['course_name'] = course.name
    courseData['department'] = Department.query.filter_by(department_id=course.department_id).first().department_name
    courseData['instructor'] = getInstructorFullName(course.instructor_id)
    courseData['insturctorId'] = course.instructor_id
    courseData['crn'] = course.crn
    courseData['credit'] = course.credit
    courseData['prerequisites'] = getPrerequisitesAsString(course_id)
    courseData['outcomes'] = getOutcomes(course_id)

    return courseData

def getCourse(course_id):
    return Course.query.get_or_404(course_id)


def getPrerequisitesIds(course_id):
    prerequisites = Prerequisite.query.filter_by(course_id=course_id)
    prerequisite_ids = []
    for _id in prerequisites:
        prerequisite_ids.append((_id.requisite_id))

    return prerequisite_ids


def getOutcomeIds(course_id):
    outcomes = Course_Outcome.query.filter_by(course_id=course_id)
    outcome_ids = []
    for _id in outcomes:
        outcome_ids.append((_id.outcome_id))

    return outcome_ids


def getInstructorIdForACourse(course_id):
    return Course.query.get_or_404(course_id).instructor_id


def getAllInstructors():
    result_instructors = []
    instructorData = {}
    instructors = Instructor.query.all()
    for instructor in instructors:
        instructorData['instructor_id'] = instructor.instructor_id
        instructorData['name'] = getInstructorFullName(instructor.instructor_id)
        department_id = RegUser.query.filter_by(user_id=instructor.instructor_id).first().department_id
        instructorData['faculty'] = Department.query.filter_by(department_id=department_id).first().faculty_name

        result_instructors.append(instructorData.copy())

    return result_instructors, len(instructors)

def getInstructorData(instructor_id):
    instructorData = {}
    instructor = Instructor.query.get_or_404(instructor_id)
    instructorData['name'] = getInstructorFullName(instructor_id)
    instructorData['title'] = instructor.title
    userData = RegUser.query.get_or_404(instructor_id)
    instructorData['email'] = userData.email
    instructorData['department'] = Department.query.filter_by(department_id=userData.department_id).first().department_name
    instructorData['courses'] = getInstructorsCourses(instructor_id)
    instructorData['course_count'] = len(instructor.courses)

    return instructorData

def getInstructorsCourses(instructor_id):
    instructor = Instructor.query.get_or_404(instructor_id)
    courseData = {}
    final_courses = []
    for course in instructor.courses:
        courseData['course_id'] = course.course_id
        courseData['code'] = course.course_code
        courseData['prerequisites'] = getPrerequisitesAsString(course.course_id)
        courseData['outcomes'] = getOutcomes(course.course_id)

        final_courses.append(courseData.copy())
    return final_courses

def getStudentGrade(user_id, course_id):
    studentGrade = Student_Grade.query.filter_by(student_id=user_id, course_id=course_id).first()
    if studentGrade is None:
        return None
    else:
        return studentGrade.grade


def addStudentGrade(user_id, course_id, grade):
    studentGrade = Student_Grade.query.filter_by(student_id=user_id, course_id=course_id).first()
    if not studentGrade:
        studentGrade = Student_Grade(student_id=user_id, course_id=course_id, grade=grade)
        db.session.add(studentGrade)
    else:
        studentGrade.grade = grade
    db.session.commit()
    return

def deleteGradeDB(user_id, course_id):
    studentGrade = Student_Grade.query.filter_by(student_id=user_id, course_id=course_id).first()
    if not studentGrade:
        return False
    else:
        db.session.delete(studentGrade)
        db.session.commit()
        return True


def deleteUserDB(user_id):
    user = RegUser.query.get_or_404(user_id)
    if not user:
        flash('User could not found on the system.')
        return False
    db.session.delete(user)
    db.session.commit()
    return True


def getCourseConnections(user_id):
    final_nodes = []
    final_connections = []
    course_ids = []
    nodes = {}
    connection = {}
    courses = Student_Grade.query.filter_by(student_id=user_id).all()

    for course in courses:
        requisites = []
        course_ids.append(course.course_id)
        nodes['course_id'] = course.course_id
        nodes['code'] = Course.query.get_or_404(course.course_id).course_code
        prerequisites = Prerequisite.query.filter_by(course_id=course.course_id).all()
        for prerequisite in prerequisites:
            requisites.append(prerequisite.requisite_id)
        nodes['requisites'] = requisites
        final_nodes.append(nodes.copy())
        #requisites.clear()
    for course in final_nodes:
        for requisite in course['requisites']:
            if requisite in course_ids and requisite != course['course_id']:
                connection['first'] = requisite
                connection['second'] = course['course_id']
                final_connections.append(connection.copy())
    
    return final_nodes, final_connections
