## Design Decisions we made



## Design Decision 1: Choosing Flask_login over Flask Session for User Authentification and Session Management

## Context
We need to authenticate users in our web application so that only registered users can upload, download, or vote on cheatsheets. The authentication system must persist the login state across requests and allow route-level protection (e.g., only logged-in users can vote).

Initially, we considered using Flask's built-in `session` to store a `user_id` and manually manage authentication and access control.

## Decision
We decided to use the `flask_login` extension to handle authentication and session management.

## Status
Accepted – 2025-06-29

## Consequences
+ Simplifies login/logout/session handling using standard decorators like `@login_required`
+ Provides built-in support for current user management via `current_user`
+ Forces a clean user model with required methods (`is_authenticated`, `get_id`, etc.)
+ Cleaner route protection and user state checks
- Requires a dedicated `User` class and integration with a persistent storage system, until now we have     only used raw sql for the database, the mandatory use of classes would make this more complicated
- Adds a third-party dependency to the project

## Alternatives Considered
**Manual session handling using Flask's `session`:**
- Pros: Lightweight, no dependencies
- Cons: easy to make security mistakes, no built-in route protection, must create all functions excluding storing user data manually



# Design Decision 2: Adopting SQLAlchemy instead of Raw SQL for Database Interaction

## Context
We initially used raw SQL queries to interact with our SQLite database since we were already familiar with SQL. This allowed precise control over queries but required a lot of boring and repetitive code and manual connection handling.

When integrating `flask_login`, we needed a `User` class with specific attributes and methods. This naturally pointed toward using SQLAlchemy's ORM (Object Relational Mapping) with class-based models.

## Decision
We decided to use SQLAlchemy's features to define and access our database models.

## Status
Accepted – 2025-06-29

## Consequences
+ Cleaner, reusable code with declarative class-based models
+ Full integration with Flask and `flask_login`
+ Easier relationship management between users, cheatsheets, and votes
+ Easier to refactor and migrate in the future
- Requires us to completely rewrite our existing code
- Requires learning the SQLAlchemy ORM API
- Slight abstraction overhead over raw SQL

## Alternatives Considered
**Raw SQL queries:**
- Pros: Direct, transparent, and highly performant
- Cons: Boring, repetitive, error-prone, hard to maintain and scale, more complicated to combine with flask_login



# Design Decision 3: Combining Votes and UserCheatsheetAccess into a single table

## Context
Initially, we had planned to use two separate tables:
UserCheatsheetAccess(user_id, cheatsheet_id) to track which users have purchased which cheatsheets
Votes(user_id, cheatsheet_id, vote) to record user votes (upvotes/downvotes)

However, this approach introduced redundant data (duplicate foreign keys) and required additional logic to enforce that users could only vote if they had access. It also complicated queries, requiring joins and cross-table validations to check access and voting eligibility.

## Decision
We decided to merge both concerns into a single table:
UserCheatsheetAccess(user_id, cheatsheet_id, vote)
This table tracks both access and the user's single allowed vote on a cheatsheet.

## Status
Accepted - 2025-07-5

## Consequences
+ Simplified database schema with no duplicated foreign key combinations
+ Enforces "one vote per user per cheatsheet" by design
+ Easy to check both access and vote status in one query
+ Reduces logic complexity in both backend routes and templates
+ The UserCheatsheetAccess table now has dual responsibility (access + voting)
- May require refactoring if voting logic expands in the future (e.g., vote history, reaction types)

## Alternatives Considered
**Separate Votes table**
- Pros: Clear separation of responsibilities, more flexible if voting expands
- Cons: Requires additional joins and logic to enforce voting eligibility, Redundant storage of user_id and cheatsheet_id, higher complexity



## Design Decision 4: Using Email Verification with itsdangerous and flask_mail Instead of Phone Verification with Firebase

## Context
We needed a user verification system for our Flask web application. Our initial idea was to verify users via phone number using Firebase Authentication, as it is commonly used in production applications for its higher trust level and better resistance to fake accounts.
However, our project had specific restrictions: we were not allowed to use JavaScript or external programs. Phone verification with Firebase requires frontend JavaScript or additional setup that violated these constraints.
Email verification using itsdangerous (for secure tokens) and flask_mail (to send verification links) emerged as a viable alternative. It integrates easily with Flask while not breaking any rules of our project.

## Decision
We decided to implement user verification via email using itsdangerous and flask_mail.

## Status
Accepted - 2025-07-18

## Consequences
+ Compatible with our project’s technology and restriction requirements
+ Fully Python-based, no need for external frontend tools or JavaScript
+ Easily integrates with Flask's ecosystem and our existing user model
+ Free to use (no cost for sending emails in low volume via SMTP)
- Slightly less secure than phone verification (email spoofing and disposable addresses are possible)
- Easier for users to exploit if they use fake or temporary email services
- Requires managing email sending and token expiration manually

## Alternatives Considered
**Phone Verification with Firebase**
- Pros: More secure, harder to spoof, industry-standard in many production applications
- Cons: Requires JavaScript and external dependencies, violates project restrictions, higher setup complexity and potential costs