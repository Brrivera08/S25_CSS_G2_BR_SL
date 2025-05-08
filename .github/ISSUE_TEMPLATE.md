---
name: 🐞 Bug Report
about: Report unexpected behavior, errors, or system flaws
title: "[Bug] 2FA code not required after successful login"
labels: bug, security
assignees: @slackey369
---

## 🐛 Description

After entering the correct username and password, the system redirects users directly to `success.html` without prompting for a second authentication factor (2FA code), bypassing the intended MFA process.

## ✅ Expected Behavior

After verifying username and password, the system should present a second screen requesting the 6-digit verification code. Only upon successful code entry should the user be granted access.

## ❌ Actual Behavior

Users are redirected to the success page after entering valid credentials without ever seeing the 2FA prompt. This creates a significant security vulnerability by bypassing the second factor entirely.

## 🧪 Steps to Reproduce

1. Run `app.py` and navigate to `/login`
2. Enter valid credentials for a test user (e.g., `seth@uiw.edu` / `testpass`)
3. Click "Login"
4. Observe that no 2FA prompt is shown, and user is redirected to `success.html`

## 💻 Environment Details

- OS: macOS Ventura 13.5
- Browser: Chrome 124.0
- Python: 3.11.4
- Flask: 2.3.3
- Route: `/login` and `/verify-code` (not triggered)

## 📂 Impacted Files or Modules

- `app.py`
- `verify_code.html`
- Possibly `session` or `redirect` logic

## 🔐 Security Impact

- [ ] None
- [ ] Low (e.g., cosmetic issue)
- [ ] Medium (e.g., bypassed minor validation)
- [x] High (e.g., critical MFA bypass or privilege escalation)

## 📝 Additional Context

This may be due to conditional logic skipping the `verify_code` page. We should check whether `session["authenticated"]` is being set too early in the flow.

