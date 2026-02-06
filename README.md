RBAC Authentication System

Overview

This project is a production-style Role-Based Access Control (RBAC) authentication system built with FastAPI, PostgreSQL, SQLAlchemy, and JSON Web Tokens (JWT). It demonstrates how modern backend systems enforce authentication, authorization, and accountability in security-sensitive environments.
The system is intentionally designed to mirror real-world enterprise and government backend architecture, rather than a simplified demo or CRUD-style application.

Purpose of the Project
The goal of this project is to demonstrate:
Secure user authentication using JWTs
Role-based authorization enforced at the API boundary
Controlled administrative privilege escalation
Immutable audit logging for sensitive actions
Clean, maintainable, and scalable backend design

This project is suitable as:
A backend security portfolio project
A demonstration of RBAC best practices
A reference implementation for FastAPI-based security systems

Core Features
Authentication
User registration and login
Secure password hashing using Argon2
JWT-based authentication
Access tokens include:
sub (subject / user identity)
iat (issued at)
exp (expiration)
Expired or invalid tokens are automatically rejected
Authorization (RBAC)
Users can have multiple roles
Roles are stored and managed in the database
Role checks are enforced using FastAPI dependency injection
Unauthorized users are blocked before business logic executes
Authentication and authorization concerns are fully separated
Administrative Privileges
Admin-only routes protected by RBAC
Administrators can promote users to admin
Duplicate promotions are prevented
Privilege escalation is impossible without the admin role
Audit Logging
All privileged administrative actions are logged
Each audit record includes:
Actor (who performed the action)
Action (what occurred)
Target (who or what was affected)
Timestamp
Audit logs are written atomically with admin actions
Logs are read-only and admin-accessible
No delete or update operations exist for audit records
Demo-Friendly Protected Routes
Explicit user-only and admin-only endpoints
RBAC enforcement is visible without reading source code
Designed for live demos and walkthroughs

Technology Stack
Backend
Python 3.13
FastAPI – API framework
SQLAlchemy 2.0 – ORM
PostgreSQL – Relational database
Uvicorn – ASGI server
Security
JWT (JSON Web Tokens) – Authentication
python-jose – JWT encoding and validation
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
User Registration
Password is securely hashed using Argon2
User record is stored in the database
User Login
Credentials are verified
A JWT access token is issued
Token includes iat and exp claims
Accessing Protected Routes
JWT is validated on every request
Expired or invalid tokens are rejected
Role checks are enforced via dependencies
Administrative Actions
Only users with the admin role can perform admin actions
All admin actions generate immutable audit logs

Example API Endpoints
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
Key properties:
Audit logs are written in the same database transaction as the admin action
An administrative action cannot succeed without an audit record
Logs are immutable and read-only
Only administrators can view audit history
This design mirrors patterns used in government, financial, and compliance-focused systems.

RBAC Bootstrap Strategy
RBAC systems require an initial administrator.
This project uses a one-time bootstrap process:
The first admin is assigned directly in the database
After bootstrap, all role changes are performed via secured API endpoints
No further manual role assignment is required
This approach prevents unauthorized privilege escalation and ensures long-term access control integrity.

Security Considerations
Passwords are never stored in plaintext
Tokens are cryptographically signed and time-limited
Authorization is enforced server-side only
Client-supplied role data is never trusted
Secrets are managed via environment variables
Sensitive files are excluded via .gitignore

Disclaimer
This project is intended for educational and demonstration purposes.
It is not a drop-in production security solution without additional hardening, such as:
Token refresh mechanisms
Rate limiting
Account lockout policies
Centralized logging or SIEM integration
Automated test coverage

Summary
This RBAC Authentication System demonstrates how to design and implement:
Secure authentication
Strict role-based authorization
Controlled administrative privilege escalation
Immutable audit logging
Clean, scalable backend architecture
The project focuses on security correctness, auditability, and real-world design patterns, going beyond basic CRUD-style applications.
