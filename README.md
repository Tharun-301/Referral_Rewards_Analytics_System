# 🚀 Referral & Rewards Analytics System

A secure backend system for referral tracking, analytics, and reward management built with **FastAPI**, **SQLAlchemy**, and **JWT Authentication**.

## ✨ Features

✅ User Registration & Login (JWT Auth)
✅ Unique Referral Code Generation
✅ Referral Tracking & Analytics
✅ Reward Points Management
✅ Admin Dashboard APIs
✅ Configurable Reward System
✅ SQLite / PostgreSQL Support
✅ Environment Variable Security

---

## 🛠️ Tech Stack

* Python 3.11
* FastAPI
* SQLAlchemy
* SQLite
* JWT Authentication
* Passlib (Password Hashing)

---

## ⚙️ Setup (Windows PowerShell)

### Clone Repository

```powershell
git clone https://github.com/Tharun-301/Referral_Rewards_Analytics_System.git
cd referral-system
```

### Create Virtual Environment

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

### Install Dependencies

```powershell
pip install -r requirements.txt
```

### Configure Environment

Create `.env`

```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///./referral.db
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Run Application

```powershell
uvicorn app.main:app --reload
```

### Open API Docs

```text
http://127.0.0.1:8000/docs
```

---

## 📌 API Endpoints

### Authentication

| Method | Endpoint           |
| ------ | ------------------ |
| POST   | /api/auth/register |
| POST   | /api/auth/login    |

### Referral

| Method | Endpoint                         |
| ------ | -------------------------------- |
| POST   | /api/referral/generate           |
| POST   | /api/referral/apply              |
| GET    | /api/referral/analytics/summary  |
| GET    | /api/referral/analytics/list     |
| GET    | /api/referral/analytics/timeline |

### Rewards

| Method | Endpoint             |
| ------ | -------------------- |
| GET    | /api/rewards/summary |
| GET    | /api/rewards/history |

### Admin

| Method | Endpoint                              |
| ------ | ------------------------------------- |
| GET    | /api/admin/referral/top               |
| POST   | /api/admin/rewards/{reward_id}/credit |

---

## 🔒 Security

* Password Hashing using Passlib
* JWT Authentication
* Environment Variable Configuration
* Admin Authorization Checks
* Reward Idempotency Protection

---

## 🎯 Highlights

* Referral Conversion Analytics
* Configurable Reward Engine
* Admin Reward Approval Flow
* Clean Service-Based Architecture
* Easily Switchable to PostgreSQL

---

## 🏗️ Project Architecture

- Router Layer → Handles API requests
- Service Layer → Business logic
- Database Layer → SQLAlchemy ORM
- Authentication Layer → JWT-based security
- Analytics Layer → Referral & reward insights

---
## 📋 Assumptions

1. **Referral codes can be reused by multiple users**

   * A single referral code may be used by many different users.
   * Self-referral and duplicate referral usage are restricted.

2. **One user can apply only one referral code**

   * Once a user successfully applies a referral code, they cannot apply another code.

3. **Rewards are configuration-driven**

   * Reward amounts are fetched from the `reward_config` table instead of being hardcoded in the application.

4. **Admin privileges are managed directly in the database**

   * No public API is provided to grant admin access for security reasons.

5. **Reward creation is idempotent**

   * Duplicate rewards for the same referral are prevented through validation checks.

6. **Authentication uses JWT access tokens**

   * Users must authenticate and include a valid JWT token to access protected endpoints.

7. **SQLite is used as the default database**

   * The system is designed to support PostgreSQL by simply updating the database connection string.

8. **Analytics are generated from referral records**

   * Summary, timeline, and referral list reports are calculated dynamically from stored referral data.

9. **Referral rewards require successful referral completion**

   * Rewards are created only after a referral is successfully applied and validated.


-----



⭐ Built with FastAPI for scalable referral and rewards management.
