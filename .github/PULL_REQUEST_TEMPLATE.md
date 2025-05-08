# 🚀 Pull Request Summary

Implemented email-based token validation for password reset functionality. This enables users to securely reset their password using a time-limited token sent via email, improving account recovery and aligning with our security goals.

## 🔧 Type of Change

Check the relevant option(s):

- [x] New feature ✨
- [x] Security enhancement 🔐
- [ ] Documentation update 📝

## 📂 Areas Affected

- [ ] Login / Authentication
- [ ] 2FA / MFA
- [ ] HR Integration
- [ ] Role-Based Access Control (RBAC)
- [ ] Temporary Access
- [x] Password Reset Flow
- [ ] Audit Logging
- [ ] Alert System
- [ ] Admin Dashboards

## 🧪 How to Test

```bash
1. Run `python app.py`
2. Click "Forgot Password" on the login page
3. Enter a valid user email
4. Check email (uses console for now) and click token link
5. Enter and confirm a new password
6. Log in with the updated credentials
