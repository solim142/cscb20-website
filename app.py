from flask import Flask, render_template, request, flash, redirect, url_for
from flask import session as app_session
from flask_bcrypt import Bcrypt
from sqlalchemy import *
from sqlalchemy.orm import *
from flask_sqlalchemy import SQLAlchemy
import datetime

# CONSTANTS
IS_LOGGED_IN = 'logged_in'
SESSION_NAME = 'session_name'
ACCOUNT_TYPE = 'account_type'

#  EASY RENDER WITH SESSION
def basic_render(html: str):
    if not app_session.get(IS_LOGGED_IN):
        return redirect(url_for('login_account'))
    else:
        print(f"{app_session.get(SESSION_NAME)} is already logged in, sending to home page...")
        return render_template(html)

# QUERY FUNCTIONS
def ADD_NEW_USER_QUERY(new_username: str, new_password: str, new_acctype: str):
    return insert(Accounts).values(
        username=new_username, 
        password=new_password,
        account_type=new_acctype
    )

def GET_GRADES_BY_USERNAME_QUERY(username: str):
    return select(Grades).where(Grades.username == f'{username}')

def GET_USER_BY_NAME_QUERY(username: str):
    return select(Accounts).where(Accounts.username == f'{username}')

# INITIALIZE APP AND BCRYPT
app = Flask(__name__)
app.config['SECRET_KEY'] = 'cbad71fb55b1579ecd6c34133dcab059692c1a00891e186313251fb9537d2f20'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignment3.db'
bcrypt = Bcrypt(app)

# INITIALIZE DATABASE
db = SQLAlchemy(app=app)

class Accounts(db.Model):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    account_type: Mapped[str]

    def __repr__(self):
        return f"Accounts({self.id}, '{self.username}', '{self.password}', '{self.account_type}')"


class Grades(db.Model):
    __tablename__ = "grades"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(ForeignKey('accounts.username'))
    assignment: Mapped[str]
    grade: Mapped[float]

    def __repr__(self):
        return f"Grades({self.id}, '{self.username}', '{self.assignment}', {self.grade})"

class Feedback(db.Model):
    __tablename__ = "feedback"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    instructor_username: Mapped[str] = mapped_column(ForeignKey('accounts.username'))
    teaching_likes: Mapped[str]
    teaching_improvements: Mapped[str]
    lab_likes: Mapped[str]
    lab_improvements: Mapped[str]
    timestamp: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)


with app.app_context():
    db.create_all()

###########################
#ROUTING ENDPOINT HANDLING#
###########################

@app.route("/")
@app.route("/home")
def home():
    return basic_render("index.html")

@app.route("/syllabus")
def syllabus():
    return basic_render("syllabus.html")

@app.route("/news")
def news():
    return basic_render("news.html")

# Temporary
@app.route("/lecture")
def lecture():
    return basic_render("lecture.html")

@app.route("/tests")
def tests():
    return basic_render("tests.html")

@app.route("/calendar")
def calendar():
    return basic_render("calendar.html")

@app.route("/tutorials")
def tutorials():
    return basic_render("labs.html")

@app.route("/assignments")
def assignments():
    return basic_render("assignments.html")

@app.route("/assignment1")
def assignment1():
    return basic_render("assignment1.html")

@app.route("/assignment2")
def assignment2():
    return basic_render("assignment2.html")

@app.route("/assignment3")
def assignment3():
    return basic_render("assignment3.html")

@app.route("/feedback")
def feedback():
    return basic_render("feedback.html")

@app.route("/resources")
def resources():
    return basic_render("resources.html")

@app.route("/team")
def team():
    return basic_render("team.html")


@app.route("/register", methods=('POST', 'GET'))
def register_account():
    if request.method == 'GET':
        return render_template("create_account.html")
    
    entered_username = request.form['username']
    entered_password = request.form['password']
    entered_verify_password = request.form['confirm_password']
    entered_user_type = request.form['usertype']
    find_user_query_output = db.session.execute(GET_USER_BY_NAME_QUERY(entered_username))
    if(len(find_user_query_output._allrows()) > 0):
        flash("Account already exists!")
        return render_template("create_account.html")

    if(entered_password != entered_verify_password):
        flash("Passwords do not match!")
        return render_template("create_account.html")

    hashed_password = bcrypt.generate_password_hash(entered_password).decode('utf-8')
    db.session.execute(ADD_NEW_USER_QUERY(entered_username, hashed_password, entered_user_type))
    db.session.commit()
    return redirect(url_for('login_account'))


@app.route("/logout")
def logout_account():
    app_session.clear()
    return redirect(url_for('login_account'))


@app.route("/login", methods=('POST', 'GET'))
def login_account():
    if request.method == 'GET':
        return render_template("login_account.html")
    
    entered_username = request.form['username']
    entered_password = request.form['password']
    find_user_query_output = db.session.execute(GET_USER_BY_NAME_QUERY(entered_username))
    query_data = find_user_query_output.first()
    if(query_data == None):
        flash("Account username does not exist.")
        return render_template("login_account.html")
    
    user_data = query_data[0]
    if(not bcrypt.check_password_hash(user_data.password, entered_password)):
        flash("Password entered was incorrect.")
        return render_template("login_account.html")

    app_session[IS_LOGGED_IN] = True
    app_session[SESSION_NAME] = user_data.username
    app_session[ACCOUNT_TYPE] = user_data.account_type
    return redirect(url_for('home'))


@app.route('/grades')
@app.route('/grades/get', methods=('POST', 'GET'))
def grades():
    if request.method == 'GET':
        return render_template('grade_editor.html')
    
    student_to_get = request.form['student_username']
    if not app_session[IS_LOGGED_IN]:
        return redirect(url_for('home'))

    if app_session[ACCOUNT_TYPE] != 'Teacher':
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
    if not app_session[IS_LOGGED_IN]:
        return redirect(url_for('home'))

    if app_session[ACCOUNT_TYPE] != 'Teacher':
        return redirect(url_for('home'))
    
    if request.method == 'GET':
        return render_template('grade_editor.html')
    # Query the student to see if their grade already exists
    # if it exists, update that row with UPDATE_GRADE_QUERY
    # if row does not exist add in row with ADD_GRADE_QUERY

#feedback route
@app.route('/feedback', methods=['GET', 'POST'])
def submit_feedback():
    if not app_session.get(IS_LOGGED_IN) or app_session.get(ACCOUNT_TYPE) != 'student':
        flash('Only logged-in students can submit feedback.')
        return redirect(url_for('login_account'))

    instructors = Accounts.query.filter_by(account_type='instructor').all()

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
        return redirect(url_for('submit_feedback'))

    return render_template('feedback.html', instructors=instructors)

if __name__ == '__main__':
    app.run(debug=True)
