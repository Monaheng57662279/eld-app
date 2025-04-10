# ELD Application

![Project Banner](https://via.placeholder.com/800x200?text=ELD+Application) <!-- Replace with actual image later -->

A modern Electronic Logging Device (ELD) solution with:
- Django REST backend
- React.js frontend
- Map visualization
- Real-time tracking

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- PostgreSQL (recommended) or SQLite

### 🛠 Installation

#### Backend Setup (Django)
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate environment
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env  # Update with your actual values

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

#### Frontend Setup (React)
```bash
# Navigate to frontend
cd ../frontend

# Install dependencies
npm install

# Configure environment variables
cp .env.example .env  # Update with your actual values
```

## 🏃 Running the Application

1. **Start Backend**:
```bash
cd backend
python manage.py runserver
```

2. **Start Frontend** (in another terminal):
```bash
cd frontend
npm start
```

3. Access the application:
- Frontend: http://localhost:3000
- Admin: http://localhost:8000/admin

## 🏗 Project Structure
```
eld-app/
├── backend/          # Django project
│   ├── config/       # Django settings
│   ├── apps/         # Django applications
│   └── manage.py
└── frontend/         # React project
    ├── public/       # Static files
    └── src/          # React components
```

## 🌐 Deployment


## 📄 License


## 📬 Contact
Monaheng Mothabeng - monahengmothabeng@gmail.com