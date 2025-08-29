# 🚀 BillSplit AI - Quick Setup Guide

## Prerequisites
- Python 3.8+
- Node.js 16+
- MySQL 8.0+
- OpenAI API key

## 🎯 One-Command Setup (Recommended)

```bash
./setup.sh
```

## 🔧 Manual Setup

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp env_template.txt .env
# Edit .env with your OpenAI API key and MySQL credentials

# Initialize database
mysql -u root -p < init_db.sql

# Run backend
python app.py
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

## 🌐 Access URLs
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:5000

## 🔑 Environment Variables (.env)

```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=mysql://username:password@localhost/billsplit_db
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

## 🗄️ Database Setup

```sql
CREATE DATABASE billsplit_db;
USE billsplit_db;
```

## 📱 Usage
1. Upload bill image
2. AI extracts items and totals
3. Select your consumed items
4. Calculate your share with tax

## 🆘 Troubleshooting

- **MySQL Connection**: Ensure MySQL is running
- **OpenAI API**: Verify API key and credits
- **Port Conflicts**: Check if ports 3000/5000 are free
- **Dependencies**: Clear node_modules and reinstall if needed

---

**Need help? Check the full README.md for detailed instructions!**
