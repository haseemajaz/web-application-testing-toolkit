# Testing Workflow — Web Application Testing Toolkit

A controlled workflow for testing a web application you own or have written permission to test. Follow it in order; do not skip the scope step.

## 1. Scope (before any testing)

- Get written authorisation: what URLs, what accounts, what dates, what is out of scope.
- Agree what is forbidden: no production data, no denial-of-service testing, no social engineering unless explicitly in scope.
- Record the scope in `report.md` before you start.

## 2. Inventory

- Run `web_toolkit.py` against the target. It lists forms, methods, and fields, and checks headers and cookies.
- Map the application by hand: login, registration, search, upload, admin pages, API endpoints.
- Note which pages need authentication and which roles can reach them.

## 3. Automated checks

- Headers, cookies, TLS, and the form inventory from the toolkit.
- Record each finding with severity and remediation in `report.md`.

## 4. Manual testing (the part a tool cannot do)

- Input validation: one field at a time, with safe test values, on your own app or an authorised test.
- Authentication: lockout, session expiry, logout, password reset flow.
- Authorisation: try to reach admin / other-user pages as a low-privilege user.
- File upload, if any: type, size, and where files are stored and served from.
- Record every test, pass or fail, in the report. A failed test with no record is wasted work.

## 5. Report

- Findings prioritised, each with evidence (URL, request, response) and remediation.
- A manual checklist with results, and a sign-off section.
- Send the report, then re-test after fixes and record the re-test date.

## What not to do

- Never test a site you do not own or have written permission to test.
- Never use real user data in a test.
- Never run automated exploitation tools against a target outside the agreed scope.
