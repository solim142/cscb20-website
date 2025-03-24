from flask import Flask, render_template, request
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine, text

def GET_USER_BY_NAME_QUERY(user_name: str) -> str:
    return f"SELECT username, password, usertype FROM accounts WHERE username = {user_name}"


def ADD_USER_QUERY(user_name: str, hashed_password: str, user_type: int) -> str:
    return f"INSERT INTO accounts VALUES('{user_name}', '{hashed_password}', {user_type})"


db_instance = create_engine("sqlite:///assignment3.db")
db_connection = db_instance.connect()

db_connection.execute(text("""
CREATE TABLE IF NOT EXISTS accounts(
    username varchar(256) PRIMARY KEY,
    password varchar(256),
    usertype int
);
"""))

app = Flask(__name__)
bcrypt = Bcrypt(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/register", methods=['POST', 'GET'])
def register_account():
    entered_username = request.form['username']
    entered_password = request.form['password']
    entered_user_type = request.form['usertype']

    find_user_query_output = db_connection.execute(text(GET_USER_BY_NAME_QUERY(entered_username)))
    if(find_user_query_output.rowcount != 0):
        # flash that user already exists
        return "failed_account_creation"

    hashed_password = bcrypt.generate_password_hash(entered_password).decode('utf-8')
    db_connection.execute(text(ADD_USER_QUERY(entered_username, hashed_password, int(entered_user_type))))
    return "create_account_test"


@app.route("/login", methods=['POST', 'GET'])
def login_account():
    entered_username = request.form['username']
    entered_password = request.form['password']

    find_user_query_output = db_connection.execute(text(GET_USER_BY_NAME_QUERY(entered_username)))
    if(find_user_query_output.rowcount == 0):
        # flash that username does not exist
        return "failed_login"

    user_data = find_user_query_output.all()[0]
    if(not bcrypt.check_password_hash(user_data[1], entered_password)):
        # flash that password is incorrect
        return "failed_login"
    
    return "login_account_test"


if __name__ == '__main__':
    app.run(debug=True)