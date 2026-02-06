RBAC Authentication System
Overview
This project is a production-style Role-Based Access Control (RBAC) authentication system built using FastAPI, PostgreSQL, SQLAlchemy, and JSON Web Tokens (JWT). It demonstrates how modern backend systems enforce authentication, authorization, and accountability in security-sensitive environments.
The system is designed to reflect real-world enterprise and government security architecture, not a simplified demo. Core goals include secure credential handling, strict role enforcement, auditability of privileged actions, and clean separation of concerns.
Purpose of the Project
The purpose of this project is to demonstrate:
Secure user authentication using JWTs
Role-based authorization enforced at the API boundary
Admin-only privilege escalation with accountability
Immutable audit logging for sensitive actions
Clean, scalable backend architecture
This project is suitable as:
A backend security portfolio project
A demonstration of RBAC principles
A reference implementation for secure FastAPI services
Key Features
Authentication
User registration and login
Secure password hashing using Argon2
JWT-based authentication
Time-limited access tokens with expiration (exp) and issued-at (iat) claims
Automatic rejection of expired or invalid tokens
Authorization (RBAC)
Users may have multiple roles
Roles are stored in the database (not hardcoded)
Role enforcement is implemented using FastAPI dependencies
Unauthorized access is blocked before business logic executes
Clear separation between authentication and authorization logic
Admin Privileges
Admin-only routes protected by RBAC
Admins can promote users to admin role
Privilege escalation is strictly controlled
Duplicate promotions are prevented
Audit Logging
All privileged admin actions are logged
Each audit log entry records:
Who performed the action
What action occurred
The target of the action
Timestamp
Admin-only audit log viewer endpoint
Logs are immutable (no update or delete operations)
Demo-Friendly Protected Routes
Explicit user-only and admin-only endpoints
RBAC enforcement is visible without reading source code
Designed for live demos and security walkthroughs
Technology Stack
Backend
Python 3.13
FastAPI – API framework
SQLAlchemy 2.0 – ORM
PostgreSQL – Relational database
Uvicorn – ASGI server
Security
JWT (JSON Web Tokens) – Authentication
python-jose – JWT encoding/decoding
Passlib + Argon2 – Password hashing
Tooling
Postman – API testing
dotenv – Environment variable management

app/
├── core/
│   ├── auth.py          # JWT validation & RBAC enforcement
│   ├── deps.py          # Database session dependency
│   ├── security.py      # Password hashing & JWT creation
│   └── seed_roles.py    # Initial role seeding
│
├── models/
│   ├── user.py          # User model
│   ├── role.py          # Role model
│   └── audit_log.py     # Audit log model
│
├── routes/
│   ├── auth.py          # Registration & login
│   ├── admin.py         # Admin-only actions & audit viewer
│   └── protected.py    # RBAC demo routes
│
├── schemas/
│   ├── user.py          # Request/response schemas
│   └── auth.py
│
├── database.py          # Database engine & session setup
├── main.py              # Application entry point

Authentication & Authorization Flow
User registers
Password is securely hashed (Argon2)
User record is stored in the database
User logs in
Credentials are verified
A JWT access token is issued
Token includes sub, iat, and exp claims
User accesses protected routes
JWT is validated on every request
Expired or invalid tokens are rejected
Role checks are enforced via dependencies
Admin actions
Only users with the admin role may perform admin actions
All admin actions generate immutable audit logs

Example Endpoints

Authentication
POST /auth/register
POST /auth/login

RBAC Demo
GET /protected/user     # Any authenticated user
GET /protected/admin    # Admin-only

Admin Actions
POST /admin/promote/{user_id}
GET  /admin/audit-logs

Audit Logging Design
Audit logging is implemented to ensure accountability and non-repudiation.
Key characteristics:
Logs are written inside the same database transaction as the admin action
An action cannot succeed without a corresponding audit record
Logs are read-only and admin-visible
No deletion or modification endpoints exist
This mirrors patterns used in government, financial, and compliance-focused systems.
Security Considerations
Passwords are never stored in plaintext
Tokens are cryptographically signed and time-limited
Authorization is enforced server-side only
Role data is not trusted from client input
Secrets are externalized via environment variables
.gitignore prevents sensitive files from being committed
Disclaimer
This project is intended for educational and demonstration purposes.
It is not a drop-in replacement for a production security system without further hardening, such as:
Token refresh mechanisms
Rate limiting
Account lockout policies
Comprehensive test coverage
Centralized logging / SIEM integration
Summary
This RBAC Authentication System demonstrates how to design and implement:
Secure authentication
Strict role-based authorization
Privileged action accountability
Clean, maintainable backend architecture
It goes beyond basic CRUD applications by focusing on security correctness, auditability, and real-world design patterns.