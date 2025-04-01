# Features added/changed:
- (Added) Accounts (Log in, Log out, Register).
- (Changed) Feedback (Anonymous for students, only instructors can view).
- (Added) Assignment & Remark Request system.
- (Changed) Changed drop-down menu to sub-navigation bar for better looks.
- (Changed) Implemented a proper dark mode toggle button that doesn't load a new .html and .css.
- (Added) Only logged in accounts can view site content. Attempts to access routes without a session re-routes to the log in screen.

# Lucas's Side
For the assignment, I implemented the account management (account creation, logging in, logging out), and session handling systems (data onif the user is logged in, and what kind of account the user is under (student or instructor)).

One challenge I faced was learning how to initially structure the database in python. I initially started with executing sqlite queries from text in the connection class that was created when executing the db_engine.connect() function. Doing it this way was easy as the only learning curve was figuring out how to connect the app to the database. A complication that arose from doing this method is that the output from the connection.execute() functions were in types that were hard to work with. To fix this, I had to switch to using the Object Relational Mapper which was a steep learning curve as I had to learn how to structure classes to be used as tables, and the functions needed to establish relationships between tables. Furthermore, the functions to use to make queries were also a learning curve. It was hard getting it at first, but it just took some time in reading the documentation for flask_sqlalchemy and doing some practice in other isolated projects. Once I was used to using the ORM, I was able to complete the account creation, logging in and out systems fo

# Daniel's Side
For the assignment, I refactored the old .html to the new Jinja template, with .template.html as the parent template, as well as implemented the Grades & Remark system (Different view for instructor and student, displaying query as a table, adding the buttons to hide or show grade update/student remark request).

When implementing the Grades and the Remark request, it was a bit difficult to decide if it would be best to have two relations, one for grades and one for remark requests, or one that has grades and their remark requests. Although the two relation was tested at first, it caused problems in terms of assignments having multiple requests, as well as how to join them, so it was instead changed to one relation, where the initial remark requests are set to "None" by default. A student that submits a request would overwrite the value, and this would ensure only 1 remark request per entry.

# Tahira's Side
I successfully implemented the anonymous feedback system by creating a form that allows students to select an instructor (filtered from the accounts table where account_type is 'Teacher') and submit structured feedback fields (teaching_likes, teaching_improvements, lab_likes, lab_improvements). Upon submission, the feedback is stored in the feedback table using SQLAlchemy, without storing the student's username to ensure anonymity.

I made sure instructors can view only the feedback submitted for them by querying the feedback table using the logged-in instructor’s session['session_name'], ensuring they only access entries linked to their account. Each feedback entry is displayed in a styled "feedback" card layout, and instructors can mark entries as "Reviewed" by submitting a form that updates the reviewed boolean column in the database. I initially struggled with making the reviewed status persist across sessions, but resolved it by ensuring the reviewed value was updated with SQLAlchemy and committed properly using db.session.commit().

As an extra feature, I added interactive filtering options for instructors to view feedback based on status: All, Open, or Reviewed. This was implemented using JavaScript by assigning data-status attributes to each feedback card and toggling their visibility based on the selected filter button