from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine, text

# CONSTANTS
IS_LOGGED_IN = 'logged_in'
SESSION_NAME = 'session_name'
USER_TYPE = 'user_type'

#QUERY STRINGS
def ADD_GRADE_QUERY(student_name: str, assignment: str, grade: float):
    return f"INSERT INTO grades VALUES('{student_name}', '{assignment}', {grade})"

def UPDATE_GRADE_QUERY(student_name: str, assignment: str, grade: float):
    return f"UPDATE grades SET grade={grade} WHERE username='{student_name}' AND assignment='{assignment}"

def GET_GRADES_BY_NAME_QUERY(user_name: str) -> str:
    return f"SELECT * FROM grades WHERE user_name = {user_name}"

def GET_USER_BY_NAME_QUERY(user_name: str) -> str:
    return f"SELECT * FROM accounts WHERE username = '{user_name}'"

def ADD_USER_QUERY(user_name: str, hashed_password: str, user_type: int) -> str:
    return f"INSERT INTO accounts VALUES('{user_name}', '{hashed_password}', '{user_type}')"

# INITIALIZE DATABASE
db_instance = create_engine("sqlite:///assignment3.db")
db_connection = db_instance.connect()

# CREATE ALL TABLES THAT WILL BE USED IF NOT EXISTING
db_connection.execute(text("""
CREATE TABLE IF NOT EXISTS accounts(
    username varchar(256) PRIMARY KEY,
    password varchar(256),
    usertype varchar(7)
);
"""))

db_connection.execute(text("""
CREATE TABLE IF NOT EXISTS grades(
    username varchar(256),
    assignment varchar(128)
    grade numeric(2, 2),
    FOREIGN KEY (username) REFERENCES accounts(username)
);
"""))

db_connection.execute(text("""
CREATE TABLE IF NOT EXISTS feedback(
    feedbackString varchar(512)
);
"""))

# INITIALIZE APP AND BCRYPT
app = Flask(__name__)
app.config['SECRET_KEY'] = '12438324'
bcrypt = Bcrypt(app)

@app.route("/")
@app.route("/home")
def home():
    if not session.get(IS_LOGGED_IN):
        return redirect(url_for('login_account'))
    
    print(f"{session.get(SESSION_NAME)} is already logged in, sending to home page...")
    return render_template("index.html")


@app.route("/register", methods=('POST', 'GET'))
def register_account():
    if request.method == 'GET':
        return render_template("create_account.html")
    
    entered_username = request.form['username']
    entered_password = request.form['password']
    entered_user_type = request.form['usertype']

    find_user_query_output = db_connection.execute(text(GET_USER_BY_NAME_QUERY(entered_username)))
    if(find_user_query_output._allrows().__len__() > 0):
        print("User already exists...")
        return render_template("create_account.html")

    hashed_password = bcrypt.generate_password_hash(entered_password).decode('utf-8')
    db_connection.execute(text(ADD_USER_QUERY(entered_username, hashed_password, entered_user_type)))
    db_connection.commit()

    return redirect(url_for('login_account'))


@app.route("/logout")
def logout_account():
    session.clear()
    return redirect(url_for('login_account'))


@app.route("/login", methods=('POST', 'GET'))
def login_account():
    if request.method == 'GET':
        return render_template("login_account.html")
    
    entered_username = request.form['username']
    entered_password = request.form['password']
    find_user_query_output = db_connection.execute(text(GET_USER_BY_NAME_QUERY(entered_username)))
    query_data = find_user_query_output.all()
    print(query_data)
    if(len(query_data) == 0):
        print("Account username does not exist.")
        flash("Account username does not exist.")
        return render_template("login_account.html")

    user_data = query_data[0]
    if(not bcrypt.check_password_hash(user_data[1], entered_password)):
        print("Password entered was incorrect.")
        flash("Password entered was incorrect.")
        return render_template("login_account.html")

    session[IS_LOGGED_IN] = True
    session[SESSION_NAME] = user_data[0]
    session[USER_TYPE] = user_data[2]
    return redirect(url_for('home'))


@app.route('grades')
@app.route('grades/get', methods=('POST', 'GET'))
def get_grades():
    if request.method == 'GET':
        return render_template('grade_editor.html')
    
    student_to_get = request.form['student_username']
    if not session[IS_LOGGED_IN]:
        return redirect(url_for('home'))

    if session[USER_TYPE] != 'Teacher':
        return redirect(url_for('home'))
    
    grades_query = db_connection.execute(text(GET_GRADES_BY_NAME_QUERY(student_to_get)))
    if len(grades_query._allrows()) == 0:
       return render_template('grade_editor.html')
    
    return render_template('grade_editor.html', student_data=grades_query._allrows())


@app.route('grades/set', methods=('POST'))
def set_grade():
    student_to_update = request.form['student_username']
    assignment_to_set_grade = request.form['assignment']
    grade_to_set = request.form['grade']
    if not session[IS_LOGGED_IN]:
        return redirect(url_for('home'))

    if session[USER_TYPE] != 'Teacher':
        return redirect(url_for('home'))
    
    # Query the student to see if their grade already exists
    # if it exists, update that row with UPDATE_GRADE_QUERY
    # if row does not exist add in row with ADD_GRADE_QUERY


if __name__ == '__main__':
    app.run(debug=True)