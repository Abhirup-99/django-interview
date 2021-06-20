### Welcome to the repo.

## Demo
Deployed at: https://young-spire-82698.herokuapp.com/

## Linting

The formatting is done with isort(for import sorting), and black(for overall formatting).

The types are added through the mypy library.

## Features

- Schedule interviews.
- View all interviews.
- Edit an interview.
- Send emails to candidates on interview scheduling.
- Upload resumes.

## Tech Stack

The backend is created with Django with sqlite3 as the database. The Django ORM powers the SQL
interactions.

The format is created with HTML5, CSS3 and JS.

The emails are sent through Sendgrid API, and the file uploads are powered by Firebase storage.

## How to use it?

- Clone the repo.
- Run `python3 -m venv venv`.
- Run `source venv/bin/activate`.
- Run `pip install -r requirements.txt`.
- Finally serve the application using `python manage.py runserver` :).
