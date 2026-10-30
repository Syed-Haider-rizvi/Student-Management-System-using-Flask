# Student Management System (Flask + MySQL)

A basic CRUD web application to add, view, search, update, and delete student records.

## Requirements
- Python 3.10 or newer
- MySQL Server
- MySQL database user with permission to create/use tables

## 1. Create the database

Run this in MySQL Workbench or phpMyAdmin:

```sql
CREATE DATABASE student_management
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

## 2. Configure the database connection

Open `config.py` and replace `YOUR_PASSWORD` with your MySQL password.

Alternatively, set the `DATABASE_URL` environment variable. Example PowerShell:

```powershell
$env:DATABASE_URL = "mysql+pymysql://root:YourPassword@localhost/student_management"
$env:SECRET_KEY = "replace-with-a-long-random-secret"
```

For passwords containing special URL characters, URL-encode the password.

## 3. Install and run (Windows PowerShell)

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

If PowerShell blocks activation, run this for the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

Open: http://127.0.0.1:5000

The `students` table is created automatically when the app starts.

## Routes
- `GET /` — list and search students
- `GET, POST /add` — add a student
- `GET, POST /edit/<id>` — update a student
- `POST /delete/<id>` — delete a student

## Notes
- Bootstrap is loaded from a CDN, so the UI needs internet access for Bootstrap styling.
- This is a learning/development project. Before production deployment, add authentication, CSRF protection, stronger validation, secure secret management, migrations, and a production WSGI server. Do not run with Flask debug mode enabled in production.
