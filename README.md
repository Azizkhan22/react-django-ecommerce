# 🛒 react-django-ecommerce

A full-stack eCommerce web application built using **React** for the frontend and **Django + Django REST Framework** for the backend. This project demonstrates a modern architecture with API-driven development, JWT-based authentication, and a modular, scalable codebase.

---

## 🚀 Features

- 🛍️ Product listing, detail view, and category filtering  
- 🔐 JWT Authentication (login, register, logout)  
- 🛒 Shopping cart and order placement  
- 🧾 Admin dashboard (optional: for managing products & orders)  
- 💳 (Optional) Stripe/PayPal integration for payments  
- 📦 Backend REST API with Django REST Framework  
- ⚛️ Frontend with React and React Router  
- 🌐 CORS-enabled cross-origin communication

---

## 🛠️ Tech Stack

**Frontend:**
- React.js
- Axios
- React Router DOM
- Tailwind CSS

**Backend:**
- Django
- Django REST Framework
- Simple JWT for authentication
- SQLite / PostgreSQL

---

## 📁 Folder Structure

```
react-django-ecommerce/
├── backend/         # Django project
│   ├── manage.py
│   ├── core/        # API logic, models, views
│   └── ...
├── frontend/        # React project
│   ├── src/
│   └── ...
├── README.md
```

---

## 📦 Installation & Setup

### 🔧 Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Use source venv/bin/activate on Linux/macOS
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### ⚛️ Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## 🚧 Future Improvements

- Product search & filtering
- Order history
- Admin user management
- Pagination & advanced error handling
- Responsive UI improvements

---

## 🧠 Author

Made with ❤️ by Aziz Ullah  
Feel free to fork or contribute.
