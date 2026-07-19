# Secure Login System

## Description
A Flask-based web application that implements a secure login system with
password hashing, protection against SQL injection, session-based
authentication, and an optional Two-Factor Authentication (2FA) step.

## Key Features
- **User registration and login** with securely hashed passwords
  (using Werkzeug's `generate_password_hash` / `check_password_hash`,
  which uses a salted scrypt/PBKDF2-based hash — no plain-text passwords
  are ever stored)
- **SQL injection protection** — all database queries use parameterized
  statements (`?` placeholders) instead of string concatenation
- **Session management** — logged-in state is tracked securely using
  Flask sessions, with a working logout feature that clears the session
- **Optional 2FA** — after a correct username/password, the user must
  enter a One-Time Passcode (OTP) before reaching the dashboard
  (for demo purposes, the OTP is shown on screen instead of being sent by
  email/SMS)

## Requirements
- Python 3
- Flask

Install dependencies:
```
pip install -r requirements.txt
```

## How to Run
1. Install dependencies (see above)
2. Run the app:
   ```
   python app.py
   ```
3. Open your browser to `http://127.0.0.1:5000`
4. Register a new account, then log in
5. Enter the OTP shown on screen (demo only) to reach the dashboard
6. Use the Logout button to end your session

## Project Structure
```
secure_login/
├── app.py                  # Main Flask application
├── requirements.txt
├── README.md
└── templates/
    ├── login.html
    ├── register.html
    ├── verify_otp.html
    └── dashboard.html
```

## Security Notes
- Passwords are never stored in plain text — only their hashes.
- All SQL queries use parameterized statements to prevent SQL injection.
- The `app.secret_key` in `app.py` should be replaced with a long, random
  string before any real/production use.
- The OTP is shown directly on screen in this demo for simplicity. In a
  real system, it would be sent securely via email or SMS instead.

## What I Learned
This project covered core web application security practices: securely
hashing and verifying passwords, using parameterized queries to prevent
SQL injection, safely managing user sessions, and adding an extra layer
of protection with two-factor authentication.

## Possible Future Improvements
- Send the OTP via a real email service instead of displaying it
- Add rate-limiting to prevent brute-force login attempts
- Add password strength requirements during registration
- Use HTTPS and secure, HttpOnly cookies in production
- Add "forgot password" functionality with secure reset tokens
