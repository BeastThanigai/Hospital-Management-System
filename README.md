# 🏥 Hospital Management System (Role-Based Access Control)

A **Role-Based Hospital Management System (HMS)** built using **HTML, CSS, JavaScript, and MySQL**, designed to digitize the major operations inside a hospital.
The system includes **multiple dashboards**, each dedicated to a specific staff role such as Doctor, Receptionist, Lab Technician, Inventory Manager, Finance Manager, and Patient.

This project centralizes hospital operations to improve workflow, reduce manual errors, and maintain structured digital records.


## 🚀 Key Highlights

### 🔐 **Multi-Role Authentication System**

Users log in based on their assigned role:

* Doctor
* Receptionist
* Lab Technician
* Inventory Manager
* Finance Manager
* Patient / Visitor
* Admin (optional in your structure)

Each role automatically redirects to its own dashboard.


## 📊 **Dashboards Included**

### 👨‍⚕️ Doctor Dashboard

* View daily appointments
* Update patient diagnosis
* Enter prescription notes

### 🧑‍💼 Receptionist Dashboard

* Register new patients
* Manage appointments
* Update admission status
* Forward patient cases to doctors

### 🧪 Lab Technician Dashboard

* Record lab test results
* Update reports
* View pending lab test requests
* Upload final lab results

### 📦 Inventory Dashboard

* Track medicines & equipment
* Update stock levels
* Low-stock notifications 

### 💰 Finance Dashboard

* Manage billing data
* Generate invoices
* Track payments
* View daily/weekly financial summary

### 🧑‍🤝‍🧑 Patient Dashboard

* View appointment details
* Check lab results 

### 🔒 Login & Registration Pages

* Secure login
* Registration for new staff or patients
* Role assignment (handled from backend)


## 🛠️ Tech Stack

| Component       | Technology                                                     |
| --------------- | -------------------------------------------------------------- |
| Frontend        | HTML, CSS, JavaScript                                          |
| Backend         | Python flask                                                   |  
| Database        | MySQL (based on SQL files uploaded)                            |
| Architecture    | Role-based access system                                       |
| Version Control | Git & GitHub                                                   |


## 🎯 Purpose of This System

This HMS helps hospitals manage:

* Patient records
* Appointments
* Billing
* Medicine & equipment inventory
* Lab reports
* Role-based operations

All staff members access only what they are authorized for.


## 🔮 Future Improvements

* Fully connect dashboards to backend (Flask/PHP/Node)
* JWT-based auth
* Email/SMS notifications
* Generate PDF bills & lab reports
* Dark mode UI
* Cloud-hosted database


Ayy got it Beast — **your HMS is actually way more advanced** than a basic one.
I checked your repo + this screenshot → and now I clearly see the structure:

You have **separate dashboards for each role**:

* 👨‍⚕️ doctor
* 👩‍💼 finance
* 🧪 lab technician
* 🧑‍💻 receptionist
* 📦 inventory
* 🧑‍🤝‍🧑 patients
* 🛂 register / login

This means your project is a **Role-Based Access Control Hospital Management System (RBAC HMS)** — which is way more impressive.

So here you go, bro — your **updated, correct, perfect README.md** based on the *actual* project contents you uploaded.
Just paste this into your GitHub.

---

# 🏥 Hospital Management System (Role-Based Access Control)

A **Role-Based Hospital Management System (HMS)** built using **HTML, CSS, JavaScript, and MySQL**, designed to digitize the major operations inside a hospital.
The system includes **multiple dashboards**, each dedicated to a specific staff role such as Doctor, Receptionist, Lab Technician, Inventory Manager, Finance Manager, and Patient.

This project centralizes hospital operations to improve workflow, reduce manual errors, and maintain structured digital records.

---

## 🚀 Key Highlights

### 🔐 **Multi-Role Authentication System**

Users log in based on their assigned role:

* Doctor
* Receptionist
* Lab Technician
* Inventory Manager
* Finance Manager
* Patient / Visitor
* Admin (optional in your structure)

Each role automatically redirects to its own dashboard.

---

## 📊 **Dashboards Included**

### 👨‍⚕️ Doctor Dashboard

* View daily appointments
* Update patient diagnosis
* Enter prescription notes
* Access patient history (if implemented)

### 🧑‍💼 Receptionist Dashboard

* Register new patients
* Manage appointments
* Update admission status
* Forward patient cases to doctors

### 🧪 Lab Technician Dashboard

* Record lab test results
* Update reports
* View pending lab test requests
* Upload final lab results

### 📦 Inventory Dashboard

* Track medicines & equipment
* Update stock levels
* Low-stock notifications (if implemented)

### 💰 Finance Dashboard

* Manage billing data
* Generate invoices
* Track payments
* View daily/weekly financial summary

### 🧑‍🤝‍🧑 Patient Dashboard

* View appointment details
* Check lab results (optional)
* View doctor notes (optional)

### 🔒 Login & Registration Pages

* Secure login
* Registration for new staff or patients
* Role assignment (handled from backend)

---

## 🛠️ Tech Stack

| Component       | Technology                                                     |
| --------------- | -------------------------------------------------------------- |
| Frontend        | HTML, CSS, JavaScript                                          |
| Backend         | (Your system uses HTML files; add Flask/PHP if backend exists) |
| Database        | MySQL (based on SQL files uploaded)                            |
| Architecture    | Role-based access system                                       |
| Version Control | Git & GitHub                                                   |

---

## 📂 Project Structure (Based on Your Repo)

```
Hospital-Management-System/
│── login.html
│── register.html
│── index.html
│── doctor_dashboard.html
│── finance_dashboard.html
│── inventory_dashboard.html
│── lab_dashboard.html
│── receptionist_dashboard.html
│── patient_dashboard.html
│── .gitignore
│── (SQL files, backend files if added later)
```

---

## ⚙️ How to Run This Project (General)

### 1️⃣ Set Up MySQL Database

* Create a database
* Import your SQL file(s) (if included)

Example:

```sql
CREATE DATABASE hms;
USE hms;
SOURCE hospital.sql;
```

---

### 2️⃣ Launch Backend (if you add Flask/PHP)

Example for Flask:

```bash
python app.py
```

Then open:

```
http://localhost:5000
```

Or if the system is purely front-end, you can directly open `index.html`.

---

## 🎯 Purpose of This System

This HMS helps hospitals manage:

* Patient records
* Appointments
* Billing
* Medicine & equipment inventory
* Lab reports
* Role-based operations

All staff members access only what they are authorized for.

---

## 🔮 Future Improvements

* Fully connect dashboards to backend (Flask/PHP/Node)
* JWT-based auth
* Email/SMS notifications
* Generate PDF bills & lab reports
* Dark mode UI
* Cloud-hosted database

**Author**
THANIGAIVEL V

## 📜 License

This project is for educational and demonstration purposes.


