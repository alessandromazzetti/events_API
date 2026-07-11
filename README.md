# 🎟️ Events API Project

**Student Name:** Alessandro Mazzetti

---

## 📌 Project Type
**REST API**

## 🛠️ Framework Used
**Django** & **Django REST Framework (DRF)**

---

## 📝 Project Description
This project is a secure, decoupled RESTful API designed to manage event ticketing and reservations. It handles event publication, seat availability tracking, and automated user-specific ticket bookings while enforcing strict data isolation and validation rules to simulate a real-world ticketing engine.

---

## ✨ Implemented Features Grouped by User Role

### 🌐 Anonymous Users (Public)
* **Browse Events:** View the full list of upcoming events.
* **Event Details:** Retrieve specific details of a single event using its ID.
* **Dynamic Seat Counting:** See real-time available seats (automatically updated based on active reservations).

### 👤 Authenticated Users (Regular Users)
* **Book Tickets:** Reserve a seat for an event (the booking is automatically linked to the logged-in user).
* **Double-Booking Prevention:** Custom validation prevents booking the same event multiple times.
* **Overbooking Protection:** Bookings are automatically blocked if an event is sold out.
* **View Personal Reservations:** Access a private dashboard containing only the user's tickets.
* **Ticket Cancellation (Soft Delete):** Cancel a reservation. The ticket status shifts to `CANCELLED` to preserve historical metrics without modifying the physical row.

### 🔑 Superusers (Admin)
* **Full Administration:** Perform complete CRUD operations (Create, Read, Update, Delete) on Events and Reservations via the Django Admin Panel.
* **Global Overview:** Monitor all reservations across all users and events.

---

## 💻 Local Installation Instructions

Follow these steps to run the project on your local machine.

### 1. Clone the repository
```bash
git clone <repository-url>
cd events_API
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# On macOS / Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install the requirements
```bash
pip install -r requirements.txt
```

### 4. Apply database migrations
> Not required if you're using the included `db.sqlite3` file (see next section), since it already contains the applied schema. Run this step only if you start from a clean database.
```bash
python manage.py migrate
```

### 5. Start the development server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/`.

---

## 🗄️ Database Information & Demo Accounts

* **Database File:** `db.sqlite3`
* **Confirmation:** The included SQLite database file **contains pre-configured demo data**, including sample events, existing reservations, and active user profiles ready for testing.

### 👥 Demo Accounts
| Username | Password | Role | Allowed Permissions |
| :--- | :--- | :--- | :--- |
| **admin** | `admin` | Superuser / Admin | Full CRUD on Admin Panel, view all reservations. |
| **bbianchi** | `password123` | Organizer | Create events, book tickets, view/cancel own reservations only. |
| **frossi** | `password123` | Regular | Book tickets, view/cancel own reservations only. |
| **lverdi** | `password123` | Regular | Book tickets, view/cancel own reservations only. |

---

## ☁️ Online Deployment Link
The project is live and deployed on PythonAnywhere:
🚀 **Live URL:** [[http://mazzettialessandro.eu.pythonanywhere.com/api/](http://mazzettialessandro.eu.pythonanywhere.com/api/)](https://mazzettialessandro.eu.pythonanywhere.com/)

---

## 📡 API Endpoints Reference

| Method | URL | Auth Required | Allowed Role | Request Body | Response Example (Success) | Short Description |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`GET`** | `/api/events/` | No | Anyone | None | `[{"id":1,"name":"Festival","total_seats":250,"available_seats":249}]` | Lists all upcoming events with real-time seat availability. |
| **`GET`** | `/api/events/<id>/` | No | Anyone | None | `{"id":1,"name":"Festival","description":"Live show","date":"2026-06-21"}` | Retrieves detailed data for a specific event. |
| **`GET`** | `/api/reservations/` | **Yes** | Authenticated | None | `[{"id":4,"user":"amazzetti","event":1,"status":"CONFIRMED"}]` | Lists reservations belonging *only* to the logged-in user. |
| **`POST`** | `/api/reservations/` | **Yes** | Authenticated | `{"event": 1}` | `{"id":5,"user":"amazzetti","event":1,"status":"CONFIRMED"}` | Books a ticket for the specified event ID. |
| **`POST`** | `/api/reservations/<id>/cancel/` | **Yes** | Ticket Owner | None | `{"message":"Reservation successfully cancelled","status":"CANCELLED"}` | Cancels an owned reservation (Soft delete). |
| **`POST`** | `/api-token-auth/` | No | Anyone | `{"username":"","password":""}` | `{"token":"99442981abc345..."}` | Exchanges valid credentials for an HTTP Token. |

---

## 🛠️ Testing the API with HTTPie

[HTTPie](https://httpie.io/) is a command-line HTTP client that makes interacting with web services seamless.

* **HTTPie Installation Link:** [https://httpie.io/docs/cli/installation](https://httpie.io/docs/cli/installation)
* **Base Production URL:** `http://mazzettialessandro.eu.pythonanywhere.com`

### 1. Login Command (Obtain Token)
To interact with protected endpoints, you must request an authentication token using your credentials:
```bash
http POST http://mazzettialessandro.eu.pythonanywhere.com/api-token-auth/ username="amazzetti" password="bananabread"
```
Response:
```json
{
    "token": "99442981abc345..."
}
```

### 2. Using the Token
Every request to a protected endpoint must include the token in the `Authorization` header, using the `Token` scheme:
```bash
http GET http://mazzettialessandro.eu.pythonanywhere.com/api/reservations/ "Authorization:Token 99442981abc345..."
```

### 3. Example Commands for the Main Operations

**Browse all events (public, no auth needed):**
```bash
http GET http://mazzettialessandro.eu.pythonanywhere.com/api/events/
```

**View a single event's details (public):**
```bash
http GET http://mazzettialessandro.eu.pythonanywhere.com/api/events/1/
```

**Book a ticket (authenticated):**
```bash
http POST http://mazzettialessandro.eu.pythonanywhere.com/api/reservations/ "Authorization:Token 99442981abc345..." event=1
```

**View my own reservations (authenticated):**
```bash
http GET http://mazzettialessandro.eu.pythonanywhere.com/api/reservations/ "Authorization:Token 99442981abc345..."
```

**Cancel a reservation (authenticated, owner only):**
```bash
http POST http://mazzettialessandro.eu.pythonanywhere.com/api/reservations/5/cancel/ "Authorization:Token 99442981abc345..."
```
