from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_bcrypt import Bcrypt
from sqlalchemy import ForeignKey, CheckConstraint, UniqueConstraint, text
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

def GET_USER_BY_NAME_QUERY(username: str):
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

    remark_status: Mapped[str] = mapped_column(default='None')
    remark_reason: Mapped[str] = mapped_column(default='None')

    # https://docs.sqlalchemy.org/en/14/orm/declarative_tables.html
    # https://docs.sqlalchemy.org/en/20/core/constraints.html#check-constraint
    __table_args__ = (
        CheckConstraint('grade >= 0'),
        UniqueConstraint('username', 'assignment'), # There should only be 1 grade for each assignment of each student, https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint
        CheckConstraint(remark_status.in_(["None", "Pending", "Approved", "Rejected"]))
    )

    def __repr__(self):
        return f"Grades('{self.username}', '{self.assignment}', '{self.grade}', '{self.remark_status}', '{self.remark_reason}')"
    

class Feedback(db.Model):
    __tablename__ = "feedback"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    instructor_username: Mapped[str] = mapped_column(ForeignKey('accounts.username'))
    teaching_likes: Mapped[str] = mapped_column(default="None")
    teaching_improvements: Mapped[str] = mapped_column(default="None")
    lab_likes: Mapped[str] = mapped_column(default="None")
    lab_improvements: Mapped[str] = mapped_column(default="None")
    timestamp: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    reviewed = db.Column(db.Boolean, default=False) # True if reviewed

    def __repr__(self):
        return f"Feedback('{self.instructor_username}', '{self.teaching_likes}', '{self.teaching_improvements}', '{self.lab_likes}', '{self.lab_improvements}', '{self.timestamp}')"


#####################################
# GENERAL ROUTING ENDPOINT HANDLING #
#####################################

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

##########################
# ACCOUNT ROUTE HANDLING #
##########################

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

######################
# GRADES AND REMARKS #
######################

@app.route("/grades", methods = ('POST', 'GET'))
def grades():

    if request.method == 'GET':
        if session['account_type'] == 'Student':
            all_grades = Grades.query.filter_by(username = session['session_name']).all()
            return render_template('grades.html', all_grades = all_grades, view_type = 'Student')
        else:
            all_grades = Grades.query.all()
            all_students = Accounts.query.filter_by(account_type = 'Student').all() # Because some students may not have any assignments graded
            return render_template('grades.html', all_grades = all_grades, all_students = all_students, view_type = 'Instructor')

    # The POST only exists for instructors. 
    else: 
        student_to_update = request.form['students']
        assignment_to_set_grade = request.form['assignment']
        grade_to_set = request.form['grade']

        # If it exists, edit it, else create it
        query = Grades.query.filter_by(username = student_to_update, assignment = assignment_to_set_grade).first()

        if not query: 
            grade = Grades(username = student_to_update, assignment = assignment_to_set_grade, grade = grade_to_set)
            db.session.add(grade)
            db.session.commit()
            flash("Grade submitted successfully!")
        else:
            flash("This grade already exists, edit the student grades directly!")

        all_grades = Grades.query.all()
        all_students = Accounts.query.filter_by(account_type = 'Student').all()
        return render_template('grades.html', all_grades = all_grades, all_students = all_students, view_type = 'Instructor')


@app.route("/remark", methods = ['POST'])
def remark():
    reason = request.form['remark-reason']
    username = request.form['username']
    assignment = request.form['assignment']

    query = Grades.query.filter_by(username = username, assignment = assignment).first()
    
    if query.remark_status == 'Pending': # If a remark request already exists
        flash(message="Remark request updated!")
    else:
        flash(message="Remark request submitted!")

    Grades.query.filter_by(username = username, assignment = assignment).update(dict(remark_status='Pending', remark_reason=reason))
    db.session.commit()

    return redirect(url_for('grades'))


@app.route("/editGrade", methods=['POST'])
def editGrade():
    username = request.form['username']
    assignment = request.form['assignment']
    grade = request.form['grade']
    reason = request.form['reason']
    status = request.form['status']
    
    Grades.query.filter_by(username = username, assignment = assignment).update(dict(grade = grade, remark_status = status, remark_reason = reason))

    db.session.commit()
    flash(message="Grade updated successfully.")

    return redirect(url_for('grades'))

############################
# FEEDBACK HANDLING SYSTEM #
############################
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if session['account_type'] != 'Student':
        return redirect(url_for('view_feedback')) # redirecting instructors to view their feedback

    instructors = Accounts.query.filter_by(account_type='Instructor').all()

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

@app.route('/view_feedback', methods=['GET', 'POST'])
def view_feedback():
    if session['account_type'] != 'Instructor':
        return redirect(url_for('feedback'))

    instructor_username = session['session_name']

    if request.method == 'POST':
        feedback_id = request.form.get('feedback_id')
        feedback = Feedback.query.get(feedback_id)
        if feedback and feedback.instructor_username == instructor_username:
            feedback.reviewed = True
            db.session.commit()
            flash('Feedback marked as reviewed.')

    feedbacks = Feedback.query.filter_by(instructor_username=instructor_username).all()
    return render_template('view_feedback.html', feedbacks=feedbacks)


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
        
        grade_submissions = [
            Grades(username = 'student1', assignment = 'Assignment 1', grade = 0),
            Grades(username = 'student1', assignment = 'Assignment 2', grade = 20),
            Grades(username = 'student2', assignment = 'Assignment 1', grade = 30),
            Grades(username = 'student2', assignment = 'Assignment 3', grade = 40, remark_status = "Pending", remark_reason = "I forgot."),
        ]

        for submission in grade_submissions:
            query = Grades.query.filter_by(username = submission.username, assignment = submission.assignment).first()
            if not query:
                db.session.add(submission)
                db.session.commit()

        if len(Feedback.query.all()) == 0:
            db.session.add(Feedback(instructor_username='instructor1', 
                                    teaching_likes='Test', 
                                    teaching_improvements='test', 
                                    lab_likes='test', 
                                    lab_improvements='test',
                                    reviewed=False))
            db.session.commit()

    app.run(debug=True)
