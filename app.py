from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_bcrypt import Bcrypt
from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped
from flask_sqlalchemy import SQLAlchemy
import datetime


# QUERY FUNCTIONS
def ADD_NEW_USER_QUERY(new_username: str, new_password: str, new_acctype: str):
    return Accounts(
        username=new_username, 
        password=new_password,
        account_type=new_acctype
    )

def GET_GRADES_BY_USERNAME_QUERY(username: str):
    print(Grades.query.filter_by(username=username))
    return Grades.query.filter_by(username=username)

def GET_USER_BY_NAME_QUERY(username: str):
    print(Accounts.query.filter_by(username=username).first())
    return Accounts.query.filter_by(username=username).first()

# INITIALIZE APP AND BCRYPT
app = Flask(__name__)
app.config['SECRET_KEY'] = 'cbad71fb55b1579ecd6c34133dcab059692c1a00891e186313251fb9537d2f20'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignment3.db'
bcrypt = Bcrypt(app)

# INITIALIZE DATABASE
db = SQLAlchemy(app=app)

"""
Using mapped_columns instead of columns as it provides additional configs: https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html
"""
class Accounts(db.Model):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    account_type: Mapped[str] # During the creation, it doesn't allow any other type

    # Establishing the relationships
    grades = db.relationship('Grades', backref='author', lazy=True)

    def __repr__(self):
        return f"Accounts({self.id}, '{self.username}', '{self.password}', '{self.account_type}')"


class Grades(db.Model):
    __tablename__ = "grades"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(ForeignKey('accounts.username'), nullable=False)
    assignment: Mapped[str] = mapped_column(nullable=False)
    grade: Mapped[float] = mapped_column(default=0, nullable=False)

    # https://docs.sqlalchemy.org/en/14/orm/declarative_tables.html
    #https://docs.sqlalchemy.org/en/20/core/constraints.html#check-constraint
    __table_args__ = (
        CheckConstraint('grade >= 0'),  
    )

    def __repr__(self):
        return f"Grades('{self.username}', '{self.assignment}', {self.grade})"

class Feedback(db.Model):
    __tablename__ = "feedback"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    instructor_username: Mapped[str] = mapped_column(ForeignKey('accounts.username'))
    teaching_likes: Mapped[str] = mapped_column(default="None")
    teaching_improvements: Mapped[str] = mapped_column(default="None")
    lab_likes: Mapped[str] = mapped_column(default="None")
    lab_improvements: Mapped[str] = mapped_column(default="None")
    timestamp: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    reviewed: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f"Feedback('{self.instructor_username}', '{self.teaching_likes}', '{self.teaching_improvements}', '{self.lab_likes}', '{self.lab_improvements}', '{self.timestamp}')"


###########################
#ROUTING ENDPOINT HANDLING#
###########################

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/syllabus")
def syllabus():
    return render_template("syllabus.html")

@app.route("/news")
def news():
    return render_template("news.html")

# Temporary
@app.route("/lecture")
def lecture():
    return render_template("lecture.html")

@app.route("/tests")
def tests():
    return render_template("tests.html")

@app.route("/calendar")
def calendar():
    return render_template("calendar.html")

@app.route("/tutorials")
def tutorials():
    return render_template("labs.html")

@app.route("/assignments")
def assignments():
    return render_template("assignments.html")

@app.route("/assignment1")
def assignment1():
    return render_template("assignment1.html")

@app.route("/assignment2")
def assignment2():
    return render_template("assignment2.html")

@app.route("/assignment3")
def assignment3():
    return render_template("assignment3.html")

@app.route("/resources")
def resources():
    return render_template("resources.html")

@app.route("/team")
def team():
    return render_template("team.html")


@app.route("/register", methods=('POST', 'GET'))
def register_account():
    if request.method == 'GET':
        return render_template("create_account.html")
    else:
        entered_username = request.form['username']
        entered_password = request.form['password']
        entered_verify_password = request.form['confirm_password']
        entered_user_type = request.form['usertype']
        find_user_query_output = GET_USER_BY_NAME_QUERY(entered_username)
        if find_user_query_output:
            flash("Account already exists!")
            return render_template("create_account.html")

        if(entered_password != entered_verify_password):
            flash("Passwords do not match!")
            return render_template("create_account.html")

        hashed_password = bcrypt.generate_password_hash(entered_password).decode('utf-8')
        db.session.add(Accounts(username = entered_username, password = hashed_password, account_type = entered_user_type))
        
        db.session.commit()
        return redirect(url_for('login_account'))


@app.route("/logout")
def logout():
    session.pop('session_name', default=None)
    session.pop('account_type', default=None)
    return redirect(url_for('login_account'))


@app.route("/login", methods=('POST', 'GET'))
def login_account():
    if request.method == 'GET':
        return render_template("login_account.html")
    
    entered_username = request.form['username']
    entered_password = request.form['password']
    find_user_query_output = GET_USER_BY_NAME_QUERY(entered_username)
    if (find_user_query_output == None):
        flash("Account username does not exist.")
        return render_template("login_account.html")
    
    if (not bcrypt.check_password_hash(find_user_query_output.password, entered_password)):
        flash("Password entered was incorrect.")
        return render_template("login_account.html")

    session['session_name'] = entered_username
    session['account_type'] = find_user_query_output.account_type
    return redirect(url_for('home'))


@app.route('/grades')
@app.route('/grades/get', methods=('POST', 'GET'))
def grades():
    if request.method == 'GET':
        return render_template('grade_editor.html')
    
    student_to_get = request.form['student_username']

    if session['account_type'] != 'Teacher':
        return redirect(url_for('home'))
    
    grades_query = db.session.execute(GET_GRADES_BY_USERNAME_QUERY(student_to_get))
    if len(grades_query._allrows()) == 0:
       return render_template('grade_editor.html')
    
    return render_template('grade_editor.html', student_data=grades_query._allrows())

#######################
#GRADE HANDLING SYSTEM#
#######################

@app.route('/grades/set', methods=('POST', 'GET'))
def set_grade():
    student_to_update = request.form['student_username']
    assignment_to_set_grade = request.form['assignment']
    grade_to_set = request.form['grade']

    if session['account_type'] != 'Teacher':
        return redirect(url_for('home'))
    
    if request.method == 'GET':
        return render_template('grade_editor.html')
    # Query the student to see if their grade already exists
    # if it exists, update that row with UPDATE_GRADE_QUERY
    # if row does not exist add in row with ADD_GRADE_QUERY

#feedback route
#feedback route
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if session['account_type'] != 'Student':
        flash('Only logged-in students can submit feedback.')
        return redirect(url_for('login_account'))

    instructors = Accounts.query.filter_by(account_type='Instructor').all()
    print("Number of instructors available: ", len(instructors))

    if request.method == 'POST':
        instructor_username = request.form['instructor_username']
        teaching_likes = request.form['teaching_likes']
        teaching_improvements = request.form['teaching_improvements']
        lab_likes = request.form['lab_likes']
        lab_improvements = request.form['lab_improvements']

        feedback = Feedback(
            instructor_username=instructor_username,
            teaching_likes=teaching_likes,
            teaching_improvements=teaching_improvements,
            lab_likes=lab_likes,
            lab_improvements=lab_improvements
        )
        
        db.session.add(feedback)
        db.session.commit()
        flash("Your feedback has been submitted successfully!")
        return redirect(url_for('feedback'))

    return render_template('feedback.html', instructors=instructors)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        accounts = [
            Accounts(username = 'student1', password = bcrypt.generate_password_hash('student1').decode('utf-8'), account_type = 'Student'), 
            Accounts(username = 'student2', password = bcrypt.generate_password_hash('student2').decode('utf-8'), account_type = 'Student'),
            Accounts(username = 'instructor1', password = bcrypt.generate_password_hash('instructor1').decode('utf-8'), account_type = 'Instructor'), 
            Accounts(username = 'instructor2', password = bcrypt.generate_password_hash('instructor2').decode('utf-8'), account_type = 'Instructor')
        ]

        for account in accounts:
            query = GET_USER_BY_NAME_QUERY(account.username)
            if not query:
                db.session.add(account)
                db.session.commit()

    app.run(debug=True)
