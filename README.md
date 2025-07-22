# 🗑️ Waste Management System

A **Flask**‑based web application to manage waste pickup requests, track their status, and enable admin & driver workflows. It supports:

- **Regular Users**: register, schedule pickups, view status, file complaints  
- **Drivers**: view assigned pickups, update status (On the Way → Arrived → Completed)  
- **Admins**: view & manage all pickups & complaints, assign drivers, generate analytics reports  

---

## 📖 Table of Contents

1. [Features](#-features)  
2. [Tech Stack](#-tech-stack)  
3. [Installation](#-installation)  
4. [Configuration](#-configuration)  
5. [Database Migrations](#-database-migrations)  
6. [Creating Admin Users](#-creating-admin-users)  
7. [Running the App](#-running-the-app)  
8. [Usage](#-usage)  
9. [Dependencies](#-dependencies)  
10. [License](#-license)  

---

## 🔥 Features

- **User Registration & Login**  
  - Choose role at signup: **Regular User** or **Driver**  
  - Secure password hashing with Werkzeug  
- **Pickup Scheduling**  
  - Select PIN code, waste type, date & time slot  
  - Client‑side & server‑side guard against past dates, holidays, and double‑booking  
- **Complaint Filing**  
  - Submit text complaint + photo upload  
  - Prevent duplicate complaints for same user & location  
- **Driver Dashboard**  
  - View only assigned pickups  
  - Cycle status: Pending → On the Way → Arrived → Completed  
- **Admin Dashboard**  
  - CRUD for **all** pickups & complaints  
  - Assign drivers to pickups via dropdown  
  - Analytics & reports with Chart.js (bar & pie charts)  
- **Role‑Aware Navigation**  
  - Hides irrelevant pages based on role (user/driver/admin)  
- **Flask‑Migrate** for DB migrations  

---

## 🛠️ Tech Stack

- **Python 3.9+**  
- **Flask** – web framework  
- **Flask‑Login** – authentication  
- **Flask‑WTF** / **WTForms** – form handling & validation  
- **Flask‑SQLAlchemy** – ORM  
- **Flask‑Migrate** (Alembic) – database migrations  
- **Bootstrap 5** & **Jinja2** – frontend templating & styling  
- **Chart.js** – client‑side charts (via CDN)  
- **SQLite** – default development database  

---

## ⚙️ Installation

1. **Clone** the repo  
   ```bash
   git clone https://github.com/YOUR_USERNAME/waste-management-system.git
   cd waste-management-system
