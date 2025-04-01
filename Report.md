# Features added/changed:
- (Added) Accounts (Log in, Log out, Register).
- (Changed) Feedback (Anonymous for students, only instructors can view).
- (Added) Assignment & Remark Request system.
- (Changed) Changed drop-down menu to sub-navigation bar for better looks.
- (Changed) Implemented a proper dark mode toggle button that doesn't load a new .html and .css.
- (Added) Only logged in accounts can view site content. Attempts to access routes without a session re-routes to the log in screen.

# Lucas's Side
For the assignment, I implemented the account management (account creation, logging in, logging out), and session handling systems (data onif the user is logged in, and what kind of account the user is under (student or instructor)).

# Daniel's Side
For the assignment, I refactored the old .html to the new Jinja template, with .template.html as the parent template, as well as implemented the Grades & Remark system (Different view for instructor and student, displaying query as a table, adding the buttons to hide or show grade update/student remark request)

# Tahir's Side


# Struggles
In general, there weren't many struggles for building the site. We already had most pages complete, with global colour variables and pre-set colours and options from Assignment 2 that allowed for modularity, so re-factoring was not a lot of trouble.

When implementing the Grades and the Remark request, it was a bit difficult to decide if it would be best to have two relations, one for grades and one for remark requests, or one that has grades and their remark requests. Although the two relation was tested at first, it caused problems in terms of assignments having multiple requests, as well as how to join them, so it was instead changed to one relation, where the initial remark requests are set to "None" by default. A student that submits a request would overwrite the value, and this would ensure only 1 remark request per entry.