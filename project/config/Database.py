from flask_sqlalchemy import SQLAlchemy
from project import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zgolxdxdhgqrwk:3f2f58e0d6baa234f1569a4a92bf9043c48a534edb6027902e488c8999fe8e33@ec2-174-129-33-30.compute-1.amazonaws.com:5432/df6qc7mlpccpkh'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


