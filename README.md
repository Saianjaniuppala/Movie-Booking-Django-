# 🎬 Movie Ticket Booking System (Django + DRF)

A simple yet production-grade **Movie Ticket Booking Backend** built using **Django**, **Django REST Framework (DRF)**, **JWT Authentication**, and **Swagger API Documentation**.

---

## 🧠 Objective

This project implements a **Movie Ticket Booking System** with authentication, movie/show management, seat booking, and cancellation. All APIs are documented using Swagger UI.

---

## ⚙️ Tech Stack

* Python 3.10+
* Django 4.x
* Django REST Framework (DRF)
* Simple JWT (for authentication)
* drf-yasg (for Swagger documentation)

---

## 📦 Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/movie-booking-backend.git
cd movie-booking-backend
```

### 2️⃣ Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 6️⃣ Run the development server

```bash
python manage.py runserver
```

Visit **[http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)** to open the Swagger API documentation.

---

## 🔐 Authentication (JWT)

### ➕ Signup

**POST** `/api/signup/`

```json
{
  "username": "john",
  "password": "john123",
  "email": "john@example.com"
}
```

### 🔑 Login

**POST** `/api/login/`

```json
{
  "username": "john",
  "password": "john123"
}
```

Response:

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

Use the token in headers:

```
Authorization: Bearer <access_token>
```

---

## 🎟️ API Endpoints

| Endpoint                     | Method | Description                        | Auth |
| ---------------------------- | ------ | ---------------------------------- | ---- |
| `/api/signup/`               | POST   | Register a new user                | ❌    |
| `/api/login/`                | POST   | Obtain JWT token                   | ❌    |
| `/api/movies/`               | GET    | List all movies                    | ❌    |
| `/api/movies/<id>/shows/`    | GET    | List shows for a movie             | ❌    |
| `/api/shows/<id>/book/`      | POST   | Book a seat (requires seat_number) | ✅    |
| `/api/my-bookings/`          | GET    | List user's bookings               | ✅    |
| `/api/bookings/<id>/cancel/` | POST   | Cancel a booking                   | ✅    |
| `/swagger/`                  | GET    | Swagger API Docs                   | ❌    |

---

## 📖 Business Rules

✅ **Prevent double booking** → a seat cannot be booked twice for the same show.
✅ **Prevent overbooking** → bookings cannot exceed total seats for a show.
✅ **Cancel frees seat** → cancelling sets status to `cancelled`, allowing rebooking.
✅ **Security** → users cannot cancel others’ bookings.

---

## 💡 Bonus Features

* Retry logic for concurrent seat booking.
* Transactional seat booking using `select_for_update()`.
* Input validation for invalid seat numbers.
* Friendly error messages with status codes.

---

## 🧪 Example API Flow

1. `POST /api/signup/` → register user
2. `POST /api/login/` → get JWT token
3. `GET /api/movies/` → fetch movies
4. `GET /api/movies/<id>/shows/` → list shows
5. `POST /api/shows/<id>/book/` → book seat `{ "seat_number": 5 }`
6. `GET /api/my-bookings/` → view user's bookings
7. `POST /api/bookings/<id>/cancel/` → cancel a booking

---

## 🧰 Example Curl Commands

```bash
# Signup
curl -X POST http://127.0.0.1:8000/api/signup/ -H "Content-Type: application/json" -d '{"username":"user1","password":"pass"}'

# Login
curl -X POST http://127.0.0.1:8000/api/login/ -H "Content-Type: application/json" -d '{"username":"user1","password":"pass"}'

# Use token to access secure endpoint
curl -H "Authorization: Bearer <access_token>" http://127.0.0.1:8000/api/my-bookings/
```

---

## 🧪 Unit Tests (suggested)

Run tests (if added):

```bash
python manage.py test
```

---

## 📘 Project Structure

```
movie_booking/
│
├── movie_booking/           # Project folder
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── movies/                  # App folder
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── requirements.txt
├── README.md
└── manage.py
```

---

## 🌟 Future Enhancements

* Add seat map visualization.
* Integrate payment gateway.
* Add caching or async booking queue.

---

## 🧑‍💻 Author

**Your Name**
📧 [your.email@example.com](mailto:your.email@example.com)
🌐 [GitHub Profile](https://github.com/<your-username>)

---

> **Note:** Swagger UI available at `/swagger/`. All JWT-protected endpoints are documented there automatically.
