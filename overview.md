# Secure Access Control System - Overview

## Objective
To implement a secure, role-based access system for corporate environments using password and multifactor authentication.

## Features
- User login with 2FA
- Dashboard access based on roles
- Session handling
- Logout and timeout functionality

Title: Create login functionality with username and password

Description:
Implement a secure login feature where users can enter a username and password to gain access to a protected area of the application. If credentials are valid, users are redirected to a success page. If invalid, an error message is shown.

Steps to Reproduce:

Navigate to the login.html page.

Enter a sample username and password.

Click the "Login" button.

Expected Behavior:
Users with correct credentials are redirected to a success.html page, while users with incorrect credentials see an error message on error.html.

Actual Behavior:
Currently, login functionality does not exist. No input validation or credential matching is implemented yet.

Additional Context:

User credentials will be stored in a users.txt file or a simple data structure.

Basic validation and sanitization will be added to prevent injection attacks.

Future enhancements may include hashing passwords.

Labels:

enhancement

feature

security

Assignees:
@Brrivera08

__________________________________________________________________

Title: Add second authentication factor after password verification

Description:
After the user successfully enters the correct username and password, prompt them for a second authentication factor (e.g., verification code). This adds an extra layer of security to prevent unauthorized access even if credentials are compromised.

Steps to Reproduce:

Login with correct username and password.

Prompt appears asking for second factor (e.g., a 6-digit verification code).

User enters code and submits.

Expected Behavior:
User is only granted access to the success.html page after passing both password and second-factor verification.

Actual Behavior:
Currently, users are redirected to the success page after only entering a correct username and password. There is no second factor involved.

Screenshots:
Not applicable at this stage – pending feature development.

Additional Context:

The second factor could be a hardcoded code, time-based code (like Google Authenticator), or sent via email/text.

Helps align with multi-factor authentication (MFA) best practices.

You can use Python’s smtplib for email, twilio for SMS, or pyotp for app-based codes.

TASKS:

 Choose how to send the code (email, SMS, or app)

 Make system send code after correct password

 Create page to enter the code

 Check if the code is correct

 Let user in if both steps pass

Labels:

enhancement

security

authentication

Assignees:
@slackey369

__________________________________________________________

Title: Integrate HR system to detect employee offboarding events

Description:
Develop functionality that connects to the HR system to monitor and detect when an employee is offboarded (i.e., leaves the organization). This detection should trigger automatic revocation of access to internal systems, enforcing proper access control.

Steps to Reproduce:

HR system flags an employee as offboarded or terminated.

The system polls or receives a trigger about the change.

Access credentials are revoked and sessions terminated.

Expected Behavior:
When offboarding is detected, the user's system access is automatically revoked, and logs are updated for compliance and audit tracking.

Actual Behavior:
Currently, the system has no awareness of HR changes. Access revocation is manual and potentially delayed.

Screenshots:
Not available – integration still under development.

Additional Context:

Use a mock or real HR data source (like a JSON file, database, or API).

Design for future automation or webhook support.

Ensure changes are logged and reversible only by admins.

TASKS:

 Implement integration with HR system to detect when an employee is marked as offboarded or terminated

 Trigger automated access revocation upon detection

 Log each offboarding action for auditing

 Verify access is blocked after revocation

 Create test cases to simulate offboarding scenarios

Labels:

security

automation

integration

enhancement

Assignees:
@SethLackey

__________________________________________________________

Title: Implement Automatic Access Revocation Logic Based on Offboarding Events

Description:
Develop the back-end logic that automatically revokes a user’s access to the system once they are flagged as offboarded by the HR system. This ensures that terminated employees cannot access sensitive resources after departure.

Steps to Reproduce:

HR system flags a user as offboarded or terminated.

Access control module processes the offboarding flag.

The system removes login ability, assigned roles, and credentials.

Expected Behavior:
The user’s access is completely revoked — all roles, credentials, and permissions are stripped, and the user can no longer authenticate or perform any system action.

Actual Behavior:
Currently, access remains active after offboarding unless manually revoked.

Screenshots:
Not applicable – logic still under development.

Additional Context:

This is a continuation of Issue #3 (detecting offboarding events).

The revocation should be immediate and logged for auditing purposes.

Roles and permissions may be stored in a file, database, or session variable — design accordingly.

TASKS:

 Develop logic to automatically revoke system access when an offboarding event is detected

 Remove all assigned roles, permissions, and credentials

 Invalidate all login sessions and prevent future logins

 Log revocation activity with user ID, timestamp, and reason

 Test with simulated offboarding events to ensure full coverage

Labels:

security

automation

access-control

critical

Assignees:

__________________________________________________________

Title: Add Temporary Access Role Functionality

Description:
Create functionality that allows administrators to assign temporary access roles (e.g., for interns or contractors) that automatically expire after a set time. This prevents long-term access for users who only need short-term permissions.

Steps to Reproduce:

Admin selects a user and assigns a temporary role.

Admin sets an expiration duration (e.g., 2 hours, 7 days).

The system grants the role and starts a countdown.

After the configured time, the role is automatically removed.

Expected Behavior:
Temporary roles are applied immediately and expire automatically when their duration ends, revoking access without admin intervention.

Actual Behavior:
The current system does not differentiate between temporary and permanent roles. All roles remain active until manually removed.

Screenshots:
No screenshots – functionality not yet implemented.

Additional Context:

Temporary roles help enforce least privilege principles.

Useful for onboarding short-term users or giving time-boxed elevated access.

Implementing this may require a time-based revocation mechanism or scheduled background job.

TASKS:

 Implement support for assigning temporary access roles to users such as interns and contractors

 Allow admins to configure the role duration upon assignment

 Track and monitor role expiration times

 Revoke roles automatically once the duration expires

 Log when temporary access is granted and revoked

Labels:

access-control

automation

security

enhancement

Assignees:
@aamata1

__________________________________________________________

Title: Create HR Interface for Granting Temporary Access

Description:
Develop a user-friendly interface for HR personnel to grant temporary access roles to users such as interns, contractors, or newly onboarded employees. The interface should allow HR to search for a user, assign a temporary role, set a duration, and validate against organizational policy limits.

Steps to Reproduce:

HR manager logs into the HR dashboard.

Navigates to the "Grant Temporary Access" section.

Searches for a user by name or ID.

Selects access level and sets duration.

Submits the form to grant access.

Expected Behavior:
HR can efficiently assign access with proper controls in place. The system ensures the duration does not exceed preset limits, and logs the event.

Actual Behavior:
There is currently no interface or automated way for HR to assign temporary access roles.

Screenshots:
N/A – feature not yet built.

Additional Context:

Integrates with Issue #5 (temporary access logic)

Should include real-time validation (e.g., max 30 days)

Designed for ease of use by non-technical HR staff

Could use Flask form with dropdowns and date/time fields

TASKS:

 Develop a user-friendly interface in the HR dashboard that allows HR managers to grant temporary access to users

 HR can search for and select a user

 HR can specify access level and duration

 System validates that the duration does not exceed policy limits

 Connect interface to backend access control logic

 Provide confirmation feedback and logging

Labels:

UI

enhancement

access-control

HR-tool

Assignees:

__________________________________________________________


Title: Implement Email Token Generation and Validation

Description:
Develop backend functionality that generates a secure, time-limited token when a user requests a password reset. The system should send this token to the user’s email within a reset link. When the user clicks the link and enters a new password, the system must validate the token before allowing the password update.

Steps to Reproduce:

User clicks “Forgot Password” on the login page.

System generates a unique token and sends it to the user’s email with a reset link.

User clicks the link and is taken to a password reset form.

User enters a new password and submits.

System validates the token and updates the password.

Expected Behavior:
Token is securely generated and emailed. It expires after a set time, is valid only once, and allows the user to securely reset their password.

Actual Behavior:
There is no current functionality for password reset or token generation.

Screenshots:
Not available yet – feature pending development.

Additional Context:

Use libraries such as secrets, itsdangerous, or uuid for token generation.

Email body should include a secure URL like https://example.com/reset?token=abc123...

Token should be hashed/stored securely and expire in ~10–15 minutes.

Reset form should enforce strong password policies and validation.

TASKS:

 Develop backend logic to generate a secure, time-limited token when a user requests a password reset

 Ensure token is single-use and securely stored/validated

 Send token via email inside a password reset link

 Create a secure password reset form for the user to submit a new password

 Invalidate token after it’s used or expired

 Log reset attempts and completions for security auditing

Labels:

security

password-reset

email

backend

enhancement

Assignees:

__________________________________________________________

Title: Implement a Form Accessible Through the Tokenized Link, Allowing Users to Enter and Confirm a New Password

Description:
Create a secure password reset form that is only accessible via a valid tokenized link sent to the user’s email. The form should allow users to enter and confirm a new password, validate both inputs, and update the password only if the token is valid and not expired.

Steps to Reproduce:

User clicks on a password reset link received by email.

System verifies the token and displays the password reset form.

User enters and confirms a new password.

System validates and updates the password if token and inputs are valid.

Expected Behavior:
The form enforces strong password rules, ensures both fields match, and only allows resets using a valid, active token.

Actual Behavior:
There is currently no form for password reset through tokenized links.

Screenshots:
N/A – feature pending.

Additional Context:

Token validation must occur before password reset is allowed.

Password must meet minimum complexity: e.g., length, uppercase, symbol, number.

Limit token usage and form access to prevent brute force or abuse.

Rate-limit or CAPTCHA may be used to protect endpoint.

TASKS:

 Requires both new password and confirmation fields

 Form validates token before allowing password reset

 Strong password requirements are enforced

 Add security measures to prevent abuse of password reset feature

 Redirect users with success or failure messages

 Log reset attempts for audit and security review

Labels:

UI

password-reset

security

validation

Assignees:

__________________________________________________________


Title: Implement Rate Limiting and CAPTCHA to Prevent Brute-Force or Spam Attempts on the Password Reset Feature

Description:
Enhance the password reset feature's security by adding rate limiting and CAPTCHA protection. These measures prevent brute-force attacks, repeated spam submissions, and abuse of the reset functionality by limiting the number of reset attempts and verifying user authenticity.

Steps to Reproduce:

Navigate to the password reset form.

Submit multiple reset requests rapidly using the same or different emails.

Attempt to trigger a CAPTCHA or bypass the form’s limits.

Expected Behavior:
The system should restrict excessive reset requests per IP/email, prompt for CAPTCHA when thresholds are exceeded, and log any suspicious activity.

Actual Behavior:
Currently, the system does not limit reset attempts or use CAPTCHA, leaving it vulnerable to automated abuse.

Screenshots:
N/A – feature pending implementation.

Additional Context:

CAPTCHA can be integrated using Google reCAPTCHA, hCaptcha, or a simple math challenge.

Flask extensions like Flask-Limiter can enforce request thresholds.

Logs can be stored in a local file or security event log for review.

TASKS:

 CAPTCHA added to request form after repeated attempts

 Limit reset requests per IP/email within a time frame

 Log suspicious activities

 Display clear error or warning messages for blocked actions

 Allow legitimate users to retry after cooldown period

 Ensure CAPTCHA is accessible and responsive for all users

Labels:

security

anti-abuse

enhancement

password-reset

Assignees:

__________________________________________________________

Title: Alert System for Suspicious Login Attempts and Unauthorized Access

Description:
Implement an alerting system that detects suspicious login behavior and unauthorized access attempts. When triggered, the system should notify designated administrators via email or another communication method (e.g., Slack). This is essential for timely threat detection and response.

Steps to Reproduce:

Trigger multiple failed login attempts.

Attempt to access restricted areas without authentication.

Log in from a suspicious or unrecognized IP or device.

Expected Behavior:
The system should detect and flag unusual behavior, then alert an admin or log the event in real-time.

Actual Behavior:
No monitoring or alerting currently exists. Login activity is not actively tracked or responded to.

Screenshots:
N/A – feature in planning phase.

Additional Context:

Detection thresholds (e.g., 3 failed logins within 1 minute) can be configurable.

Alerts can be sent via SMTP email, Slack webhook, or a dashboard view.

Should work in tandem with the audit logging and rate limiting already planned.

TASKS:

 Design detection logic for triggering alerts

 Implement monitoring for login activities

 Integrate alert notification system (e.g., email, Slack)

 Document the alert system in the security section of the knowledge base

 Create test scenarios to validate alert triggers

 Ensure alert throttling to avoid spam/flooding

Labels:

security

alerting

monitoring

enhancement

Assignees:

__________________________________________________________

Title: Alert Management Dashboard for Suspicious Login Attempts

Description:
Create a secure administrative dashboard to manage and review alerts triggered by suspicious login attempts and unauthorized access activities. The dashboard should allow authorized personnel to view, filter, and act on alerts in real time, helping the organization respond quickly to potential security threats.

Steps to Reproduce:

System generates an alert after suspicious behavior (e.g., 5 failed login attempts).

Admin accesses the alert management dashboard.

Views list of active alerts and takes action (e.g., mark as reviewed or escalate).

Expected Behavior:
Admins can log in to a protected dashboard, view recent alerts, filter them, and take defined actions like acknowledging or escalating. The system restricts access to authorized users only.

Actual Behavior:
There is currently no interface or tool for managing or tracking security alerts.

Screenshots:
Not available – feature in development.

Additional Context:

UI may use an HTML table layout with Bootstrap or another lightweight framework.

Filtering could be by user, severity, date, or alert type.

Actions taken on alerts should be logged for auditing purposes.

Access to the dashboard must be limited to predefined admin roles.

TASKS:

 Design UI layout for the alert management dashboard

 Implement alert list view with relevant data fields (user, IP, time, alert type)

 Add filtering and search capabilities

 Enable actions: mark as reviewed, acknowledge, escalate

 Ensure access controls restrict dashboard to authorized roles

 Document dashboard usage and permissions

Labels:

security

admin-dashboard

alerting

enhancement

UI

Assignees:

__________________________________________________________