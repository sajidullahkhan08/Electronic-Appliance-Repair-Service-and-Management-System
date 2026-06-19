# ElectroFix - Electronic Appliance Repair Service & Management System

## Introduction

This proposal outlines the development of a web-based repair service management system for a local electronic appliance repair shop located in Shangla, Khyber Pakhtunkhwa, Pakistan. The system will be named **ElectroFix**.

## Problem Statement

The repair shop currently operates on a fully manual workflow. Customers can only request services by physically visiting the shop or calling the owners, and there is no structured way to record, track, or manage repair jobs. This leads to:

- Lost repair records
- Missed customer requests
- Unnecessary back-and-forth communication
- No digital presence
- Inefficient handling of multiple repair jobs

## Proposed Solution

ElectroFix will be a web-based platform that digitizes the complete workflow of the repair shop. It will provide:

- A **customer-facing website** for submitting and tracking repair requests
- A **secure admin panel** for the shop owner to manage all operations from a single dashboard

### Technology Stack

| Layer    | Technology            |
| -------- | --------------------- |
| Frontend | HTML, CSS, JavaScript |
| Backend  | Python (Flask)        |
| Database | SQLite / MySQL        |

## Key Features

### Customer Side

1. **Online Repair Request Form**
   - Customers can submit repair requests online with:
     - Name, phone number
     - Appliance details and problem description
     - Preferred service type
   - A unique **Tracking ID** is generated upon submission

2. **Two Service Types**
   - **Shop Repair**: Bring appliance to the shop
   - **Home Service**: Technician visits customer's home

3. **Repair Status Tracking**
   - Real-time progress tracking using Tracking ID
   - Step-by-step timeline view

   **Shop Repair Status Flow:**

   ```
   Pending → Under Inspection → Repairing → Completed → Ready for Pickup
   ```

   **Home Service Status Flow:**

   ```
   Pending → Scheduled → Technician Dispatched → Repairing → Completed
   ```

4. **Track by Name or Phone**
   - Search for repair requests using name or phone number if Tracking ID is forgotten

5. **Services Page**
   - Lists all appliance types serviced, including:
     - Washing Machines
     - Refrigerators
     - Freezers
     - Stabilizers
     - Electric Irons
     - Water Dispensers
     - Fans
     - Microwave Ovens
     - Other household appliances

6. **Contact Page**
   - Owner phone numbers
   - WhatsApp contact link
   - Shop address and location

### Admin Side

1. **Secure Admin Login**
   - Protected login system for authorized users only
   - Access to repair records and management features

2. **Dashboard**
   - Real-time summary displaying:
     - Total requests
     - Pending repairs
     - Repairs in progress
     - Completed repairs
     - Home service requests
     - Total customers
     - Settings for Password Update

3. **Manage Repair Requests**
   - View all submitted requests in a searchable table
   - Open any request for full details
   - Update repair status
   - Add technician notes visible to customers

4. **Customer Records**
   - Maintain database of all customers
   - Search functionality
   - View complete repair history per customer

5. **Home Services Management**
   - Separate section for home-visit requests
   - Efficient management of scheduled technician visits

## Business Owners

| Owner               | Contact      | Alternate    |
| ------------------- | ------------ | ------------ |
| **Nizamullah Khan** | 0344-0025964 | 0326-0025964 |
| **Imranullah Khan** | 0344-3771782 | —            |

### Shop Location

📍 **Besham Road, Near AbuBakr Masjid, Koz Bazaar, Belay Baba, Shangla, KPK**

---

## Getting Started

### Prerequisites

- **Python 3.8+**
- **MySQL** (recommended) or SQLite-style setup (schema is in `backend/database/schema.sql`)
- A modern web browser

### Setup (Local Development)

1. **Clone** this repository
2. Create a backend environment:

   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Create `backend/.env` (or set variables directly in your system environment).
   - At minimum, set `SECRET_KEY`.

   Example (MySQL local):

   ```env
   SECRET_KEY=change-me
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=root
   MYSQL_PASSWORD=
   MYSQL_DB=electrofix_db
   SESSION_COOKIE_SECURE=false
   ```

5. Initialize the database:

   ```bash
   python init_db.py
   ```

6. Run the backend:

   ```bash
   python app.py
   ```

7. Open the app in your browser:
   - Customer app: `http://localhost:5000/`
   - Admin login: `http://localhost:5000/admin/login.html`

### Production / Deployment

#### Railway (Recommended)

- Use the `Procfile`/`Dockerfile` already provided in `backend/`.
- Add a **MySQL** plugin on Railway.
- Railway will inject `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DB` automatically.
- Set at least:
  - `SECRET_KEY`
  - (optional) `CORS_ORIGINS` if needed
  - (optional) Twilio variables if OTP SMS is required

#### Docker (Backend)

Build and run the backend container using `backend/Dockerfile`.
(You may also serve the frontend via the backend, since `backend/app.py` serves `frontend/`.)

### Project Structure

```
.
├── frontend/
│   ├── index.html
│   ├── services.html
│   ├── request.html
│   ├── tracking.html
│   ├── contact.html
│   ├── admin/
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── requests.html
│   │   ├── customers.html
│   │   ├── home-services.html
|   |   └── settings.html
│   ├── css/
│   │   ├── style.css
│   │   └── admin.css
│   └── js/
│       ├── main.js
│       ├── request.js
│       ├── tracking.js
│       └── admin.js
└── backend/
    ├── app.py
    ├── config.py
    ├── db.py
    ├── init_db.py
    ├── migrate.py
    ├── requirements.txt
    ├── database/
    │   └── schema.sql
    ├── models/
    │   ├── customer.py
    │   ├── repair_request.py
    │   └── admin.py
    └── routes/
        ├── auth.py
        ├── customer_routes.py
        └── admin_routes.py
```

## License

This project is developed for ElectroFix repair service, Shangla, KPK.
