# 🛡️ S25_CSS_G2_BR_SL – Computer Systems Security Project

This project simulates a secure access control environment built to demonstrate core concepts in computer systems security. It integrates multiple layers of authentication, role-based access, HR integration, and automated monitoring to reflect real-world enterprise security operations.

---

## 🔍 Project Objective

The main goal of this project is to:

- Implement secure **user authentication** with multi-factor support
- Integrate **HR-driven access control** for onboarding/offboarding
- Enable **temporary access roles** with automated expiration
- Provide **alerting and monitoring** of suspicious login activity
- Offer **admin dashboards** for access and alert management

---

## 🚀 Key Features

### 🔐 Authentication System
- Username + password login
- Second-factor verification (2FA) via email tokens
- Password reset with secure token validation

### 🧑‍💼 HR System Integration
- Detect employee offboarding events
- Automatically revoke access upon termination
- HR dashboard to assign temporary access roles (interns, contractors)

### ⏳ Temporary Access Roles
- Admins and HR can assign roles with time-limited access
- System automatically removes expired roles

### 📨 Password Reset & Token Logic
- Tokenized email-based reset links
- Token validation, expiration, and form-based password change
- CAPTCHA and rate-limiting to prevent abuse

### 📊 Security Monitoring & Alerts
- Alert generation for suspicious login attempts
- Admin alert management dashboard with search and filtering
- Alerts logged and actionable (e.g., escalate or acknowledge)

---


## 🛠️ Technologies Used

- **Python 3.11**
- **Flask** (Micro web framework)
- **HTML/CSS/JS** (for UI)
- **smtplib**, **secrets**, **itsdangerous**, **Flask-Limiter**
- Optional: **CAPTCHA API**, **Slack webhook**

---

## 📖 Use Cases

- Demonstrating secure login and 2FA flows  
- Automating HR-driven access removal  
- Managing short-term user access roles  
- Monitoring user behavior and generating alerts  
- Reviewing and escalating alerts via a dashboard

---

## 📚 Documentation

See the [Wiki](https://github.com/Brrivera08/S25_CSS_G2_BR_SL/wiki) for:

- ✅ [User Stories](https://github.com/Brrivera08/S25_CSS_G2_BR_SL/wiki/User-Stories)  
- 🔐 [Access Control & Authentication](https://github.com/Brrivera08/S25_CSS_G2_BR_SL/wiki/Access-Control)  
- 🚨 [Security Monitoring & Alerts](https://github.com/Brrivera08/S25_CSS_G2_BR_SL/wiki/Alert-System)

---

## 🤝 Contributing

1. Fork the repository  
2. Create a new branch: `git checkout -b feature-name`  
3. Commit your changes  
4. Push to your fork  
5. Open a pull request with details

All code should follow best practices for security and be well-documented.

---

## 👥 Authors

- @Brrivera08  
- @SethLackey  
- @aamata1  
- Group 2 – S25 CSS Class

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.


