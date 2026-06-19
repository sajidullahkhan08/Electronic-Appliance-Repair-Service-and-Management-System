-- ============================================================
-- ElectroFix Database Schema
-- Database: electrofix_db
-- ============================================================


-- ============================================================
-- Table: admins
-- ============================================================
CREATE TABLE IF NOT EXISTS admins (
    admin_id      INT AUTO_INCREMENT PRIMARY KEY,
    phone         VARCHAR(20) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ============================================================
-- Table: customers
-- ============================================================
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    phone       VARCHAR(20)  NOT NULL,
    address     TEXT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ============================================================
-- Table: repair_requests
-- ============================================================
CREATE TABLE IF NOT EXISTS repair_requests (
    request_id          INT AUTO_INCREMENT PRIMARY KEY,
    tracking_id         VARCHAR(12) UNIQUE NOT NULL,
    customer_id         INT NOT NULL,
    appliance_type      VARCHAR(100) NOT NULL,
    appliance_brand     VARCHAR(100),
    problem_description TEXT NOT NULL,
    service_type        ENUM('Home Service', 'Shop Repair') NOT NULL,
    status              VARCHAR(50) NOT NULL DEFAULT 'Pending',
    notes               TEXT,
    request_date        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================================
-- Table: otp_codes
-- Stores one-time passwords sent via SMS for 2FA actions
-- ============================================================
CREATE TABLE IF NOT EXISTS otp_codes (
    otp_id     INT AUTO_INCREMENT PRIMARY KEY,
    phone      VARCHAR(20) NOT NULL,
    code       VARCHAR(6)  NOT NULL,
    purpose    VARCHAR(30) NOT NULL,   -- 'change_password' or 'change_phone'
    expires_at DATETIME    NOT NULL,
    used       TINYINT(1)  DEFAULT 0,
    created_at TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_otp_phone_purpose (phone, purpose)
) ENGINE=InnoDB;
