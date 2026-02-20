# RentFlow - Landlord-Tenant Management System

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)

**RentFlow** is a comprehensive property management solution designed to streamline the relationship between landlords and tenants. It automates rent collection, property maintenance tracking, and provides real-time dashboards for both parties.

## 🚀 Key Features

### 🧑 User Management (Accounts)

- **Role-Based Access**: Specialized dashboards for Landlords and Tenants.
- **Auto-Profile Creation**: Automatic profile setup upon user registration using Django signals.
- **Extended Profiles**: Track phone numbers, addresses, and roles seamlessly.

### 🏢 Property & Tenancy Management

- **Property Tracking**: Manage multiple properties, buildings, and individual rooms.
- **Tenancy Lifecycle**: Track active tenancies, start/end dates, and occupancy rates.
- **Occupancy Insights**: Real-time stats on vacant vs. occupied units.

### 💰 Automated Payments & Billing

- **Invoice Generation**: Automated monthly rent invoices.
- **Payment Tracking**: Record payments via Cash, Bank, or Online gateways (eSewa integration).
- **Due Date Alerts**: Notifications for pending and late payments.

### 📊 Professional Dashboards

- **Landlord View**: Overview of total properties, expected vs. collected rent, and occupancy trends.
- **Tenant View**: Quick access to current rent status, payment history, and upcoming due dates.

## 🛠 Tech Stack

- **Backend**: Django 6.0+
- **API**: Django REST Framework (DRF)
- **Database**: PostgreSQL (Production) / SQLite (Development)
- **Automation**: Django Signals & Management Commands

## ⚙️ Installation

To get started with RentFlow locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/sameer9860/-RentFlow-Landlord-Tenant-Management-System.git
   cd Landlord–Tenant Management System
   ```

2. **Set up a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate(Linux/Mac)  or  venv\Scripts\activate(Windows)
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**

   ```bash
   python3 manage.py migrate
   ```

5. **Create a superuser:**

   ```bash
   python3 manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python3 manage.py runserver
   ```

## 📂 Project Structure

- `accounts/`: User profiles and authentication.
- `properties/`: Properties, rooms, and tenancy logic.
- `payments/`: Invoicing and payment processing.
- `dashboard/`: Logic for statistics and UI data.
- `core/`: Shared utilities and base classes.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

_Developed by [Sameer khatiwada](https://github.com/sameer9860)_
