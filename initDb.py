import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    """
    CREATE TABLE DEPARTMENT ( 
                    Department_ID SERIAL PRIMARY KEY, 
                    Department_Name VARCHAR(50), 
                    Faculty_Name VARCHAR(50)
                    );
    CREATE TABLE REGUSER ( 
                    User_ID SERIAL PRIMARY KEY, 
                    Name VARCHAR(30), 
                    Surname VARCHAR(30),
                    Email VARCHAR(50) UNIQUE NOT NULL,
                    Password VARCHAR(100) NOT NULL,
                    Department_ID INTEGER REFERENCES DEPARTMENT (Department_ID),
                    User_type INTEGER DEFAULT 0
                    );
    CREATE TABLE INSTRUCTOR ( 
                    Instructor_ID INTEGER REFERENCES REGUSER (User_ID) UNIQUE, 
                    Title VARCHAR(50)
                    );
    CREATE TABLE STUDENT ( 
                    Student_ID INTEGER REFERENCES REGUSER (User_ID) UNIQUE,
                    Id_Number VARCHAR(9) 
                    );
    CREATE TABLE COURSE ( 
                    Course_ID SERIAL PRIMARY KEY, 
                    Crn VARCHAR(5),
                    Course_Code VARCHAR(10),
                    Instructor_ID INTEGER REFERENCES INSTRUCTOR (Instructor_ID),
                    Credit INTEGER,
                    Department_ID INTEGER REFERENCES DEPARTMENT (Department_ID)
                    );
    CREATE TABLE OUTCOME (
                    Outcome_ID SERIAL PRIMARY KEY,
                    Name VARCHAR(30)
                    );
    CREATE TABLE COURSE_OUTCOME (
                    Course_ID INTEGER REFERENCES COURSE (Course_ID),
                    Outcome_ID INTEGER REFERENCES OUTCOME (Outcome_ID)
                    );
    CREATE TABLE PREREQUISITE (
                    Course_ID INTEGER REFERENCES COURSE (Course_ID),
                    Outcome_ID INTEGER REFERENCES OUTCOME (Outcome_ID)
                    );
    CREATE TABLE STUDENT_GRADE (
                    Student_ID INTEGER REFERENCES STUDENT (Student_ID),
                    Course_ID INTEGER REFERENCES COURSE (Course_ID),
                    Grade VARCHAR(2)
                    );

    INSERT INTO REGUSER (Name, Surname, Email, Password, user_type) 
    VALUES ('admin','admin','admin@gmail.com', 'gAAAAABd9BaEELg95qbxr7i1H-bnoUGyjGnEBYjAnVOpXEZFvwCdUoDzPuIgny3W1ou9JwwiR-WeIv0YgPU21OKI7T2Tg5wgCA==', 0);

    INSERT INTO REGUSER (Name, Surname, Email, Password, user_type) 
    VALUES ('Iskender','Akyuz','akyuzi15@itu.edu.tr', 'gAAAAABd9BaEELg95qbxr7i1H-bnoUGyjGnEBYjAnVOpXEZFvwCdUoDzPuIgny3W1ou9JwwiR-WeIv0YgPU21OKI7T2Tg5wgCA==', 2);

    INSERT INTO STUDENT (Student_ID, Id_Number) 
    VALUES ((select User_ID from REGUSER where REGUSER.Email='akyuzi15@itu.edu.tr'),'15016000');
    """
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
