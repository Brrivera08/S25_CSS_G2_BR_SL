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