# ElectroFix — System Design Document

## Software Requirements Specification (SRS) & UML Diagrams

---

## 1. Introduction

### 1.1 Purpose
This document defines the complete system design for the ElectroFix Electronic Appliance Repair Service Management System. It covers the Software Requirements Specification (SRS), system architecture, and UML diagrams used during the development process.

### 1.2 Scope
ElectroFix is a web-based platform for a local repair shop in Shangla, KPK. It digitizes customer repair requests, repair status tracking, and admin management operations.

### 1.3 Definitions

| Term | Meaning |
|------|---------|
| SRS | Software Requirements Specification |
| UML | Unified Modeling Language |
| Actor | A user or system that interacts with the application |
| Use Case | A specific action an actor can perform |
| API | Application Programming Interface |
| CRUD | Create, Read, Update, Delete |

---

## 2. Software Requirements Specification (SRS)

### 2.1 Functional Requirements

#### Customer Requirements
- **FR-C1:** The system shall allow customers to submit repair requests online.
- **FR-C2:** The system shall generate a unique Tracking ID for each submitted request.
- **FR-C3:** The system shall allow customers to choose between Home Service and Shop Repair.
- **FR-C4:** The system shall require an address when Home Service is selected.
- **FR-C5:** The system shall allow customers to track repair status using a Tracking ID.
- **FR-C6:** The system shall allow customers to search for their requests using name or phone number.
- **FR-C7:** The system shall display a step-by-step status timeline for each repair.

#### Admin Requirements
- **FR-A1:** The system shall require admin login with **phone number** and password.
- **FR-A2:** The system shall display a dashboard with repair statistics.
- **FR-A3:** The system shall allow admins to view all repair requests.
- **FR-A4:** The system shall allow admins to update repair status.
- **FR-A5:** The system shall allow admins to add technician notes to requests.
- **FR-A6:** The system shall store and display all customer records.
- **FR-A7:** The system shall display a customer's complete repair history.
- **FR-A8:** The system shall provide a filtered view of Home Service requests.
- **FR-A9:** The system shall allow the logged-in admin to change their account password, verified by a One-Time Password (OTP) sent via SMS to the admin's registered phone.
- **FR-A10:** The system shall allow the logged-in admin to change their registered phone number, verified by a One-Time Password (OTP) sent via SMS to the current phone.

### 2.2 Non-Functional Requirements

| ID | Requirement | Description |
|----|-------------|-------------|
| NFR-1 | Security | Passwords stored as secure hashes (Werkzeug). Admin panel is session-protected. Sensitive account changes (password, phone) require OTP 2FA via SMS. OTPs are single-use and expire in 5 minutes. |
| NFR-2 | Usability | Interface must be usable on both desktop and mobile devices. |
| NFR-3 | Performance | Pages must load within 2 seconds on a local network or Railway cloud instance. |
| NFR-4 | Reliability | Database must use foreign keys to maintain data integrity. |
| NFR-5 | Maintainability | Code must be organized in separate modules (models, routes, frontend files). |
| NFR-6 | Portability | All credentials must be read from environment variables so the app runs unchanged on Railway cloud and locally. |

### 2.3 System Constraints
- Built using HTML, CSS, JavaScript, Python (Flask), and MySQL only.
- Runs locally via XAMPP (MySQL) and Python Flask dev server.
- Admin panel accessible only via direct URL — not linked from customer pages.

---

## 3. System Architecture

### 3.1 Three-Tier Architecture

ElectroFix follows a classic three-tier architecture:

```
┌─────────────────────────────────────────────────────────┐
│                  PRESENTATION TIER                       │
│         (Browser — HTML, CSS, JavaScript)               │
│                                                          │
│   index.html  request.html  tracking.html  admin/*.html │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTP Requests / JSON Responses
                        │
┌───────────────────────▼─────────────────────────────────┐
│                  APPLICATION TIER                         │
│              (Python Flask Backend)                       │
│                                                          │
│   app.py → customer_routes.py → admin_routes.py         │
│   models: customer.py, repair_request.py, admin.py, otp.py │
│   utils: sms.py (Twilio OTP sender)                     │
└───────────────────────┬─────────────────────────────────┘
                        │ SQL Queries
                        │
┌───────────────────────▼─────────────────────────────────┐
│                    DATA TIER                              │
│               (MySQL Database)                            │
│                                                          │
│   admins  |  customers  |  repair_requests  |  otp_codes │
└─────────────────────────────────────────────────────────┘
```

---

## 4. UML Diagrams

### 4.1 Use Case Diagram

```
                    ┌─────────────────────────────────────┐
                    │           ElectroFix System          │
                    │                                      │
  ┌──────────┐      │  ┌─────────────────────────────┐   │
  │          │      │  │  Submit Repair Request       │   │
  │ Customer │─────────►                              │   │
  │          │      │  └─────────────────────────────┘   │
  │  (Actor) │      │                                      │
  │          │      │  ┌─────────────────────────────┐   │
  │          │─────────►  Track Repair by ID          │   │
  │          │      │  └─────────────────────────────┘   │
  │          │      │                                      │
  │          │      │  ┌─────────────────────────────┐   │
  │          │─────────►  Search by Name / Phone      │   │
  │          │      │  └─────────────────────────────┘   │
  │          │      │                                      │
  │          │      │  ┌─────────────────────────────┐   │
  │          │─────────►  View Services               │   │
  └──────────┘      │  └─────────────────────────────┘   │
                    │                                      │
  ┌──────────┐      │  ┌─────────────────────────────┐   │
  │          │      │  │  Login to Admin Panel        │   │
  │  Admin   │─────────►                              │   │
  │  (Actor) │      │  └─────────────────────────────┘   │
  │          │      │                                      │
  │          │      │  ┌─────────────────────────────┐   │
  │          │─────────►  View Dashboard Stats        │   │
  │          │      │  └─────────────────────────────┘   │
  │          │      │                                      │
  │          │      │  ┌─────────────────────────────┐   │
  │          │─────────►  Manage Repair Requests      │   │
  │          │      │  └─────────────────────────────┘   │
  │          │      │                                      │
  │          │      │  ┌─────────────────────────────┐   │
  │          │─────────►  Update Repair Status        │   │
  │          │      │  └─────────────────────────────┘   │
  │          │      │                                      │
  │          │      │  ┌─────────────────────────────┐   │
  │          │─────────►  View Customer Records       │   │
  │          │      │  └─────────────────────────────┘   │
  │          │      │                                      │
  │          │      │  ┌─────────────────────────────┐   │
  │          │─────────►  Manage Home Service Requests│   │
  └──────────┘      │  └─────────────────────────────┘   │
                    │                                      │
                    │  ┌─────────────────────────────┐   │
  ┌──────────┐      │  │  Change Password (OTP 2FA)  │   │
  │  Admin   │─────────►                              │   │
  │  (Actor) │      │  └─────────────────────────────┘   │
  │          │      │                                      │
  │          │      │  ┌─────────────────────────────┐   │
  │          │─────────►  Change Phone (OTP 2FA)      │   │
  └──────────┘      │  └─────────────────────────────┘   │
                    │                                      │
                    └─────────────────────────────────────┘
```

---

### 4.2 Class Diagram

The class diagram shows the main data classes and their relationships.

```
┌─────────────────────────┐
│         Admin           │
├─────────────────────────┤
│ - admin_id: int         │
│ - phone: string         │
│ - password_hash: string │
│ - created_at: datetime  │
├─────────────────────────┤
│ + verify_login(): bool  │
│ + update_password(): bool│
│ + update_phone(): bool  │
└──────────┬──────────────┘
           │ 1
           │ (phone FK)
           │ *
┌──────────▼──────────────┐
│        OTPCode          │
├─────────────────────────┤
│ - otp_id: int           │
│ - phone: string         │
│ - code: string          │
│ - purpose: string       │
│ - expires_at: datetime  │
│ - used: bool            │
├─────────────────────────┤
│ + create(): int         │
│ + verify(): bool        │
└─────────────────────────┘

┌─────────────────────────┐        ┌──────────────────────────────────┐
│       Customer          │        │          RepairRequest            │
├─────────────────────────┤        ├──────────────────────────────────┤
│ - customer_id: int      │1      *│ - request_id: int                │
│ - name: string          ├────────┤ - tracking_id: string            │
│ - phone: string         │        │ - customer_id: int (FK)          │
│ - address: string       │        │ - appliance_type: string         │
│ - created_at: datetime  │        │ - appliance_brand: string        │
├─────────────────────────┤        │ - problem_description: string    │
│ + getHistory(): list    │        │ - service_type: string           │
│ + create(): int         │        │ - status: string                 │
└─────────────────────────┘        │ - notes: string                  │
                                   │ - request_date: datetime         │
                                   │ - updated_at: datetime           │
                                   ├──────────────────────────────────┤
                                   │ + generateTrackingID(): string   │
                                   │ + updateStatus(): bool           │
                                   │ + searchByContact(): list        │
                                   └──────────────────────────────────┘
```

**Relationships:**
- One `Customer` can have **many** `RepairRequest` records (1 to Many).
- Each `RepairRequest` belongs to exactly **one** `Customer`.
- `Admin` is independent — manages the system but does not own repair requests.

---

### 4.3 Entity Relationship (ER) Diagram

```
┌──────────────┐              ┌─────────────────────────┐
│   CUSTOMERS  │              │     REPAIR_REQUESTS      │
├──────────────┤              ├─────────────────────────┤
│ PK customer_id│──────┐      │ PK request_id           │
│    name      │      │      │    tracking_id (UNIQUE)  │
│    phone     │      │ 1..* │ FK customer_id           │
│    address   │      └─────►│    appliance_type        │
│    created_at│             │    appliance_brand       │
└──────────────┘             │    problem_description   │
                             │    service_type          │
┌──────────────┐             │    status                │
│    ADMINS    │             │    notes                 │
├──────────────┤             │    request_date          │
│ PK admin_id  │             │    updated_at            │
│    phone(UQ) │             └─────────────────────────┘
│ password_hash│
│   created_at │──────┐
└──────────────┘      │ 1..*
                      ▼
              ┌──────────────────┐
              │    OTP_CODES     │
              ├──────────────────┤
              │ PK otp_id        │
              │    phone         │
              │    code          │
              │    purpose       │
              │    expires_at    │
              │    used          │
              │    created_at    │
              └──────────────────┘
```

---

### 4.4 Activity Diagram — Customer Submitting a Repair Request

```
         [START]
            │
            ▼
   Customer opens request.html
            │
            ▼
   Fills in the repair form
            │
            ▼
   Selects service type
     /              \
Home Service      Shop Repair
    │                  │
    ▼                  │
Enters address         │
    │                  │
    └──────────┬───────┘
               │
               ▼
     Clicks "Submit Request"
               │
               ▼
   JavaScript validates fields
        /            \
   Invalid           Valid
      │                │
      ▼                ▼
  Show error      Send POST /api/request
  messages          to Flask
                       │
                       ▼
             Flask validates data
                /          \
            Invalid        Valid
               │             │
               ▼             ▼
          Return 400    Create/find customer
          error JSON    in database
                             │
                             ▼
                    Generate Tracking ID
                             │
                             ▼
                    Save repair request
                    to database
                             │
                             ▼
                    Return Tracking ID
                    as JSON response
                             │
                             ▼
                  JavaScript shows
                  success modal with
                  Tracking ID
                             │
                          [END]
```

---

### 4.5 Activity Diagram — Admin Updating Repair Status

```
         [START]
            │
            ▼
   Admin opens admin/login.html
            │
            ▼
   Enters phone number and password
            │
            ▼
   JavaScript sends POST /api/admin/login  {phone, password}
            │
            ▼
     Flask checks credentials
        /           \
   Invalid          Valid
      │               │
      ▼               ▼
  Show error     Create session
  message        Redirect to dashboard
                       │
                       ▼
             Admin clicks Repair Requests
                       │
                       ▼
             Table loads all requests
                       │
                       ▼
             Admin clicks "Update" on a request
                       │
                       ▼
             Detail modal opens with request info
                       │
                       ▼
             Status dropdown shows options
             based on service type:
             - Shop: Under Inspection, Repairing...
             - Home: Scheduled, Dispatched...
                       │
                       ▼
             Admin selects new status
             (optionally adds notes)
                       │
                       ▼
             Clicks "Save Status"
                       │
                       ▼
             JavaScript sends PUT request
             to /api/admin/requests/<id>/status
                       │
                       ▼
             Flask updates database row
                       │
                       ▼
             Table refreshes with new status
                       │
                    [END]
```

---

### 4.6 Sequence Diagram — Customer Tracking a Repair

```
 Customer      Browser (JS)       Flask Server        MySQL DB
    │               │                  │                  │
    │ Enters ID     │                  │                  │
    │──────────────►│                  │                  │
    │               │ GET /api/track/  │                  │
    │               │  EFX4K2Z1        │                  │
    │               │─────────────────►│                  │
    │               │                  │ SELECT * FROM    │
    │               │                  │ repair_requests  │
    │               │                  │ JOIN customers   │
    │               │                  │ WHERE tracking_id│
    │               │                  │─────────────────►│
    │               │                  │                  │
    │               │                  │◄─────────────────│
    │               │                  │  Row returned    │
    │               │                  │                  │
    │               │◄─────────────────│                  │
    │               │  JSON response   │                  │
    │               │  {success:true,  │                  │
    │               │   data: {...}}   │                  │
    │               │                  │                  │
    │               │ Renders result   │                  │
    │               │ card + timeline  │                  │
    │◄──────────────│                  │                  │
    │  Sees repair  │                  │                  │
    │  status       │                  │                  │
```

---

### 4.7 Sequence Diagram — Admin Login

```
  Admin     Browser (JS)     Flask Server      MySQL DB
    │             │                │                │
    │ Types phone │                │                │
    │ + password  │                │                │
    │────────────►│                │                │
    │             │ POST           │                │
    │             │ /api/admin/    │                │
    │             │ login          │                │
    │             │ {phone, pass}  │                │
    │             │───────────────►│                │
    │             │                │ SELECT * FROM  │
    │             │                │ admins WHERE   │
    │             │                │ phone=?        │
    │             │                │───────────────►│
    │             │                │◄───────────────│
    │             │                │ Admin row      │
    │             │                │                │
    │             │                │ check_password │
    │             │                │ _hash()        │
    │             │                │ ─────────────  │
    │             │                │  True / False  │
    │             │                │                │
    │             │◄───────────────│                │
    │             │ {success:true} │                │
    │             │ + session      │                │
    │             │ cookie set     │                │
    │             │                │                │
    │             │ Redirect to    │                │
    │             │ dashboard.html │                │
    │◄────────────│                │                │
    │ Dashboard   │                │                │
    │ loads       │                │                │

---

### 4.7b Sequence Diagram — Admin OTP 2FA (Change Password)

```
  Admin     Browser (JS)     Flask Server      MySQL DB       Twilio
    │             │                │                │             │
    │ Clicks      │                │                │             │
    │ "Send OTP"  │                │                │             │
    │────────────►│                │                │             │
    │             │ POST /send-otp │                │             │
    │             │ {purpose}      │                │             │
    │             │───────────────►│                │             │
    │             │                │ generate 6-    │             │
    │             │                │ digit OTP      │             │
    │             │                │ INSERT otp_    │             │
    │             │                │ codes (used=0) │             │
    │             │                │───────────────►│             │
    │             │                │                │             │
    │             │                │ SMS via Twilio │             │
    │             │                │────────────────────────────►│
    │             │◄───────────────│ {success:true} │             │
    │ Receives    │                │                │             │
    │ SMS with    │                │                │             │
    │ OTP code    │                │                │             │
    │             │                │                │             │
    │ Enters OTP  │                │                │             │
    │ + new pass  │                │                │             │
    │────────────►│                │                │             │
    │             │ PUT /change-   │                │             │
    │             │ password       │                │             │
    │             │ {otp, newpw}   │                │             │
    │             │───────────────►│                │             │
    │             │                │ SELECT otp_    │             │
    │             │                │ codes WHERE    │             │
    │             │                │ code=? AND     │             │
    │             │                │ used=0 AND     │             │
    │             │                │ NOT expired    │             │
    │             │                │───────────────►│             │
    │             │                │◄───────────────│             │
    │             │                │ Mark used=1    │             │
    │             │                │ UPDATE admins  │             │
    │             │                │ SET password   │             │
    │             │                │───────────────►│             │
    │             │◄───────────────│ {success:true} │             │
    │ Password    │                │                │             │
    │ updated!    │                │                │             │
```

---

### 4.8 State Diagram — Repair Request Lifecycle

#### Shop Repair States

```
         ┌─────────┐
         │ PENDING │  ◄── Initial state when request is submitted
         └────┬────┘
              │ Admin reviews request
              ▼
   ┌──────────────────┐
   │ UNDER INSPECTION │  ◄── Technician diagnosing the appliance
   └────────┬─────────┘
            │ Problem identified, repair started
            ▼
       ┌──────────┐
       │ REPAIRING│  ◄── Active repair in progress
       └────┬─────┘
            │ Repair work done
            ▼
      ┌───────────┐
      │ COMPLETED │  ◄── Repair finished
      └─────┬─────┘
            │ Customer notified
            ▼
  ┌──────────────────┐
  │ READY FOR PICKUP │  ◄── Final state for shop repair
  └──────────────────┘
```

#### Home Service States

```
         ┌─────────┐
         │ PENDING │  ◄── Initial state when request is submitted
         └────┬────┘
              │ Admin schedules visit
              ▼
       ┌───────────┐
       │ SCHEDULED │  ◄── Visit date & time confirmed
       └─────┬─────┘
             │ Technician leaves for customer home
             ▼
  ┌──────────────────────┐
  │ TECHNICIAN DISPATCHED│  ◄── On the way to customer
  └──────────┬───────────┘
             │ Arrived and started repair
             ▼
       ┌──────────┐
       │ REPAIRING│  ◄── Repair in progress at home
       └────┬─────┘
            │ Repair done
            ▼
      ┌───────────┐
      │ COMPLETED │  ◄── Final state for home service
      └───────────┘
```

---

### 4.9 Component Diagram

Shows how the major software components connect:

```
┌─────────────────────────────────────────────────────────┐
│                      BROWSER                             │
│                                                          │
│  ┌────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │ index.html │  │ request.html│  │  tracking.html  │  │
│  └─────┬──────┘  └──────┬──────┘  └────────┬────────┘  │
│        │                │                   │            │
│  ┌─────▼──────────────────────────────────▼──────────┐ │
│  │               style.css + main.js                  │ │
│  └──────────────────────┬──────────────────────────── ┘ │
│                         │                                │
│  ┌──────────────────────▼───────────────────────────┐  │
│  │         request.js | tracking.js | admin.js       │  │
│  │         (fetch() API calls to Flask)              │  │
│  └──────────────────────┬───────────────────────────┘  │
└─────────────────────────│──────────────────────────────┘
                          │ HTTP / JSON
┌─────────────────────────▼──────────────────────────────┐
│                    FLASK SERVER                          │
│                                                          │
│  ┌──────────────┐       ┌──────────────────────────┐   │
│  │   app.py     │       │   customer_routes.py     │   │
│  │  (Entry)     ├──────►│   /api/request           │   │
│  │              │       │   /api/track/<id>        │   │
│  │              │       │   /api/track-by-contact  │   │
│  │              │       └──────────────────────────┘   │
│  │              │                                       │
│  │              │       ┌──────────────────────────┐   │
│  │              ├──────►│   admin_routes.py        │   │
│  │              │       │   /api/admin/login       │   │
│  │              │       │   /api/admin/requests    │   │
│  │              │       │   /api/admin/customers   │   │
│  │              │       │   /api/admin/send-otp    │   │
│  │              │       │   /api/admin/change-pw   │   │
│  │              │       │   /api/admin/change-phone│   │
│  └──────────────┘       └──────────────────────────┘   │
│                                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │                   Models Layer                   │   │
│  │  customer.py | repair_request.py | admin.py     │   │
│  │  otp.py   |   utils/sms.py                      │   │
│  └──────────────────────┬──────────────────────────┘   │
└─────────────────────────│──────────────────────────────┘
                          │ SQL via PyMySQL
┌─────────────────────────▼──────────────────────────────┐
│                   MySQL DATABASE                          │
│                                                          │
│  admins  |  customers  |  repair_requests  |  otp_codes │
└─────────────────────────────────────────────────────────┘
```

---

### 4.10 Deployment Diagram

```
┌───────────────────────────────────────────────────────┐
│                 LOCAL DEVELOPMENT                      │
│                                                        │
│  ┌─────────────────────┐   ┌──────────────────────┐  │
│  │   Python / Flask    │   │   XAMPP MySQL        │  │
│  │  localhost:5000     │   │  localhost:3306      │  │
│  └──────────┬──────────┘   └──────────────────────┘  │
│             │ PyMySQL connection ▲                     │
│             └────────────────────┘                     │
└───────────────────────────────────────────────────────┘

                  ── deploy to ──►

┌───────────────────────────────────────────────────────┐
│               RAILWAY CLOUD PRODUCTION                 │
│                                                        │
│  ┌──────────────────────────────────────────────┐    │
│  │  Railway Service — Python/Flask App          │    │
│  │  Gunicorn: gunicorn app:app --bind 0:$PORT   │    │
│  │  Env Vars: SECRET_KEY, MYSQLHOST, etc.       │    │
│  └───────────────────┬──────────────────────────┘    │
│                      │ PyMySQL                        │
│  ┌───────────────────▼──────────────────────────┐    │
│  │  Railway MySQL Plugin                        │    │
│  │  Auto-injects: MYSQLHOST, MYSQLPORT,         │    │
│  │  MYSQLUSER, MYSQLPASSWORD, MYSQLDATABASE     │    │
│  └──────────────────────────────────────────────┘    │
└───────────────────────────────────────────────────────┘
```

---

## 5. Data Flow Diagram (DFD)

### Level 0 — Context Diagram

```
              Repair Request
 ┌──────────┐────────────────►┌────────────────┐
 │          │                 │                │
 │ Customer │◄────────────────│  ElectroFix    │
 │          │  Tracking ID    │    System      │
 │          │  Repair Status  │                │
 └──────────┘                 │                │
                              │                │◄──────────┐
 ┌──────────┐                 │                │           │
 │          │────────────────►│                │     ┌─────────┐
 │  Admin   │  Login          │                │     │ MySQL   │
 │          │  Status Update  │                │────►│   DB    │
 │          │◄────────────────│                │     └─────────┘
 └──────────┘  Reports        └────────────────┘
               Stats
```

### Level 1 — Detailed DFD

```
Customer ──►[1.0 Submit Request]──► Validate Data ──► Save to DB
                                         │
                                         ▼
                                   Generate Tracking ID
                                         │
                                         ▼
Customer ◄── Tracking ID ◄──────── Return Response

Customer ──►[2.0 Track Repair]──► Query DB by Tracking ID
                                         │
                                         ▼
Customer ◄── Status + Timeline ◄── Format & Return

Admin ──────►[3.0 Admin Login]──► Verify Hash ──► Create Session
Admin ◄────── Session Cookie ◄─────────────────────────┘

Admin ──────►[4.0 Update Status]──► Auth Check ──► Update DB Row
Admin ◄────── Success Response ◄───────────────────────────┘

Admin ──────►[5.0 Send OTP]──► Generate Code ──► Save to otp_codes ──► Twilio SMS
Admin ◄────── OTP on phone  ◄──────────────────────────────────────────────────┘

Admin ──────►[6.0 Change Password]──► Verify OTP ──► Hash New PW ──► Update DB
Admin ◄────── Success / Error ◄─────────────────────────────────────────────────┘

Admin ──────►[7.0 Change Phone]──► Verify OTP ──► Update Phone in DB
Admin ◄────── Success / Error ◄──────────────────────────────────┘
```

---

## 6. Database Design — Normalization

The database follows **Third Normal Form (3NF)**:

### Why Two Tables (customers + repair_requests)?

If we stored customer name and phone in `repair_requests` directly, the same customer submitting 3 requests would have their name stored 3 times. This is called **data redundancy**.

By separating into two tables:
- Customer info stored once in `customers`
- Each repair request just stores a `customer_id` reference
- Changing a customer's phone number requires updating only one row

This is called **normalization** — removing redundancy by organizing data efficiently.

---

## 7. Security Design

### 7.1 Password Security

```
Registration:
plain_text_password ──► generate_password_hash() ──► hash_string
                                                          │
                                                          ▼
                                                    Stored in DB

Login:
typed_password + stored_hash ──► check_password_hash() ──► True/False
```

### 7.2 Session Management

```
Login Success:
  session['admin_logged_in'] = True
  session['admin_id']        = admin['admin_id']
  session['admin_phone']     = phone
       │
       ▼
  Flask signs session with SECRET_KEY
  Sends encrypted cookie to browser

Every Admin Request:
  Browser sends cookie automatically
       │
       ▼
  @admin_required checks session
  Grants or denies access
```

### 7.3 OTP 2FA Security

```
Properties enforced by the system:
  ✔  Single-use  — otp_codes.used set to 1 after first successful verify
  ✔  Time-limited — expires after 5 minutes (expires_at column)
  ✔  Purpose-isolated — OTP for change_password ≠ change_phone
  ✔  Session-gated — send-otp and change routes require admin_required
```

### 7.4 Input Validation

All input is validated at two levels:

| Level | Where | What |
|-------|-------|------|
| Client-side | JavaScript | Required fields, minimum length |
| Server-side | Flask routes | Field presence, valid enum values, required address for Home Service |

---

## 8. Development Phases

| Phase | Activities | Deliverables |
|-------|-----------|--------------|
| **Phase 1: Planning** | Define requirements, create SRS, draw UML diagrams | This document |
| **Phase 2: Database Design** | Design tables, write schema.sql, normalize data | schema.sql, ER diagram |
| **Phase 3: Backend** | Write Flask app, models, API routes | app.py, models/, routes/ |
| **Phase 4: Frontend** | Write HTML pages, CSS design system, JS logic | frontend/ folder |
| **Phase 5: Integration** | Connect frontend to backend via API calls | Working full-stack system |
| **Phase 6: Testing** | Test all use cases, fix bugs | Verified working system |

---

## 9. API Design Specification

### Request Format

All POST and PUT requests send data as JSON:
```
Content-Type: application/json
Body: {"key": "value", ...}
```

### Response Format

All responses return JSON:
```json
{
  "success": true,
  "data": { ... }
}
```
or on error:
```json
{
  "success": false,
  "error": "Description of what went wrong"
}
```

### HTTP Status Codes Used

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET or PUT |
| 201 | Created | Successful POST (new record created) |
| 400 | Bad Request | Missing or invalid input fields |
| 401 | Unauthorized | Not logged in / wrong credentials |
| 404 | Not Found | Tracking ID or record not found |
| 500 | Server Error | Unexpected database or server error |

---

*End of System Design Document*
*ElectroFix — Electronic Appliance Repair Service Management System*
