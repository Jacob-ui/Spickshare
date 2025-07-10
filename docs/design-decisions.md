# Design Decisions We Made


## Using Flask-Login For User Authentication and Session Management

- Needed to manage login state, restrict access to certain routes, and identify the current user in a secure and scalable way
- Considered Flask’s Session for storing user_id, but it required writing custom logic for user loading and route protection
- Chose Flask-Login for its built-in login management tools like `@login_required`, `login_user()`, and `current_user`
- Reduced the risk of security mistakes and long and repetitive code

## Replacing Raw SQL With SQLAlchemy For Database Interaction

- Initially used raw SQL for all database operations
- Needed class-based user models to work with flask_login, which led us to SQLAlchemy
- Chose SQLAlchemy for cleaner models, easier relationship handling, and maintainability
- Gained compatibility with Flask ecosystem and removed repetitive and boring SQL code
