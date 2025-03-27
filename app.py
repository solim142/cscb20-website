from flask import Flask, render_template, request, flash, redirect, url_for
from flask import session as app_session
from flask_bcrypt import Bcrypt
from sqlalchemy import *
from sqlalchemy.orm import *
from flask_sqlalchemy import SQLAlchemy

# CONSTANTS
IS_LOGGED_IN = 'logged_in'
SESSION_NAME = 'session_name'
ACCOUNT_TYPE = 'account_type'

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
app.config['SECRET_KEY'] = '12438324'
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


with app.app_context():
    db.create_all()

###########################
#ROUTING ENDPOINT HANDLING#
###########################
@app.route("/")
@app.route("/home")
def home():
    if not app_session.get(IS_LOGGED_IN):
        return redirect(url_for('login_account'))
    
    print(f"{app_session.get(SESSION_NAME)} is already logged in, sending to home page...")
    return render_template("index.html")


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
def get_grades():
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


@app.route('/grades/set', methods=('POST', 'GET'))
def set_grade():
    student_to_update = request.form['student_username']
    assignment_to_set_grade = request.form['assignment']
    grade_to_set = request.form['grade']
    if not app_session[IS_LOGGED_IN]:
        return redirect(url_for('home'))

    if app_session[USER_TYPE] != 'Teacher':
        return redirect(url_for('home'))
    
    # Query the student to see if their grade already exists
    # if it exists, update that row with UPDATE_GRADE_QUERY
    # if row does not exist add in row with ADD_GRADE_QUERY


if __name__ == '__main__':
    app.run(debug=True)