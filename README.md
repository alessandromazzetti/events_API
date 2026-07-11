# 🎟️ Events API Project

**Student Name:** Alessandro Mazzetti  
**Project Type:** REST API  
**Frameworks Used:** Django & Django REST Framework (DRF)  

---

## 📝 Project Description 
This project is a RESTful API designed to manage event ticketing and reservations. It handles event publication, seat availability tracking and user-specific ticket.

---

## ✨ Implemented Features Grouped by User Role

### 🌐 Anonymous Users (Public)
* **Browse Events:** View the full list of upcoming events.
* **Event Details:** Retrieve specific details of a single event using its ID.
* **Dynamic Seat Counting:** See real-time available seats (automatically updated based on active reservations).

### 👤 Regular Users
* **Book Tickets:** Reserve a seat for an event (the booking is automatically linked to the logged-in user).
* **Double-Booking Prevention:** Custom validation prevents booking the same event multiple times.
* **Overbooking Protection:** Bookings are automatically blocked if an event is sold out.
* **View Personal Reservations:** Access a private dashboard containing only the user's tickets.
* **Ticket Cancellation (Soft Delete):** Cancel a reservation. The ticket status shifts to `CANCELLED` to preserve historical metrics without modifying the physical row.

### 👤 Organizers
* **Create Events:** Create and update event details.
* **Monitoring:** See all the reservations for a specific event
* **Isolation:** Organizers can only modify their own events.
  
### 🔑 Superusers (Admin)
* **Full Administration:** Perform complete CRUD operations (Create, Read, Update, Delete) on Events and Reservations via the Django Admin Panel.
* **Global Overview:** Monitor all reservations across all users and events.

---

## 🗄️ Database Information & Demo Accounts

* **Database File:** `db.sqlite3`
* **Confirmation:** The included SQLite database file **contains pre-configured demo data**, including sample events, existing reservations, and active user profiles ready for testing.

### 👥 Demo Accounts
| Username | Password | Role |
| :--- | :--- | :--- | :--- |
| **admin** | `admin` | Superuser / Admin | 
| **bbianchi** | `password123` | Organizer |
| **frossi** | `password123` | Reg. User |
| **lverdi** | `password123` | Reg. User |

---

## ☁️ Online Deployment Link
The project is live and deployed on PythonAnywhere:  
🚀 **Live URL:** [https://mazzettialessandro.eu.pythonanywhere.com/api/](https://mazzettialessandro.eu.pythonanywhere.com/api/)

---

## 📡 API Endpoints Reference

| Method | URL | Auth Required | Allowed Role | Request Body | Response Example (Success) | Short Description |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`GET`** | `/api/events/` | No | Anyone | None | `[{"id":1,"name":"Festival","total_seats":250,"available_seats":249}]` | Lists all upcoming events with real-time seat availability. |
| **`GET`** | `/api/events/<id>/` | No | Anyone | None | `{"id":1,"name":"Festival","description":"Live show","date":"2026-06-21"}` | Retrieves detailed data for a specific event. |
| **`GET`** | `/api/reservations/` | **Yes** | Authenticated | None | `[{"id":4,"user":"frossi","event":1,"status":"CONFIRMED"}]` | Lists reservations belonging *only* to the logged-in user. |
| **`POST`** | `/api/reservations/` | **Yes** | Authenticated | `{"event": 1}` | `{"id":5,"user":"frossi","event":1,"status":"CONFIRMED"}` | Books a ticket for the specified event ID. |
| **`POST`** | `/api/reservations/<id>/cancel/` | **Yes** | Ticket Owner | None | `{"message":"Reservation successfully cancelled","status":"CANCELLED"}` | Cancels an owned reservation (Soft delete). |
| **`POST`** | `/api-token-auth/` | No | Anyone | `{"username":"","password":""}` | `{"token":"99442981abc345..."}` | Exchanges valid credentials for an HTTP Token. |

---

## 🛠️ Testing the API (Web Browser or cURL)

You can evaluate this API using either the built-in **Django Browsable API** directly from your web browser, or via the command line using **cURL**.

### Option A: Testing via Web Browser (Recommended)
This API utilizes the DRF Browsable API.
1. **Login:** Navigate to `https://mazzettialessandro.eu.pythonanywhere.com/admin/` and log in as:
   * `admin` (Password: `admin`) if you want to log as admin/superuser.
   * `bbianchi` (Password: `password123`) if you want to log as an organizer.
   * `frossi` (Password: `password123`) if you want to log as a regular user.
   * `lverdi` (Password: `password123`) if you want to log as a regular user.
3. **Navigate:** Go back to `https://mazzettialessandro.eu.pythonanywhere.com/api/events/` to browse data.
4. **Interact:** Use the HTML forms at the bottom of the endpoints (like `/api/reservations/`) to create new bookings or cancel them without writing code.

### Option B: Testing via cURL (Command Line)

**1. Obtain Token (Login)**
```bash
curl -X POST https://mazzettialessandro.eu.pythonanywhere.com/api-token-auth/ \
     -H "Content-Type: application/json" \
     -d '{"username":"bbianchi", "password":"password123"}'
```

**2. Call a Public Endpoint (Anonymous)**
```bash
curl https://mazzettialessandro.eu.pythonanywhere.com/api/events/
```

**3. Test a Forbidden Action (Lacking Permissions)**
```bash
curl https://mazzettialessandro.eu.pythonanywhere.com/api/reservations/
```

**4. Call an Authenticated Endpoint** \
Replace ```<YOUR_TOKEN_HERE>``` with the actual token obtained in step 1.
```bash
curl https://mazzettialessandro.eu.pythonanywhere.com/api/reservations/ \
     -H "Authorization: Token <YOUR_TOKEN_HERE>"
```

**5. Create Data (Book a Ticket)** \
Replace ```<YOUR_TOKEN_HERE>``` with the actual token obtained in step 1.
```bash
curl -X POST https://mazzettialessandro.eu.pythonanywhere.com/api/reservations/ \
     -H "Authorization: Token <YOUR_TOKEN_HERE>" \
     -H "Content-Type: application/json" \
     -d '{"event": 1}'
```

**6. Update/Delete Data (Cancel Reservation)** \
Replace ```<N>``` with the reservation id number
```bash
curl -X POST https://mazzettialessandro.eu.pythonanywhere.com/api/reservations/<N>/cancel/ \
     -H "Authorization: Token <YOUR_TOKEN_HERE>"
```
