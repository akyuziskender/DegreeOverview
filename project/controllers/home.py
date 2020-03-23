from project import app
from flask import render_template, redirect, url_for
from flask_login import current_user
from project.models.dbOperations import getCourseConnections, getInstructorsCourses


@app.route('/')
@app.route('/home', methods= ['GET'])
def home():
    userType = ""
    courses = []
    nodes = []
    connections = []
    if not current_user.is_authenticated:
        userType = 'guest'
    elif current_user.isInstructor():
        userType = 'instructor'
        courses = getInstructorsCourses(current_user.user_id)
    elif current_user.isStudent():
        userType = 'student'
        nodes, connections = getCourseConnections(current_user.user_id)

    keys, cons = ConnectionModifier(nodes, connections)
    return render_template('rootHOME.html', keys=keys, cons=cons, title='Home', courses=courses, userType=userType)


def ConnectionModifier(nodes, connections):
    nodes_length = len(nodes)
    connections_length = len(connections)
    keys = ""
    cons = ""
    i = 0
    for node in nodes:
        keys += '{"key": '
        keys += str(node['course_id'])
        keys += ', "text": "'
        keys += node['code']
        keys += '"}'
        if i != nodes_length - 1:
            keys += ','
        i += 1
    i = 0
    for connection in connections:
       cons += '{"from": '
       cons += str(connection['first'])
       cons += ', "to": '
       cons += str(connection['second'])
       cons += ' }'
       if i != connections_length - 1:
           cons +=','
       i += 1
    return keys, cons

