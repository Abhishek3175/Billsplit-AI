#!/bin/bash

echo "🍽️  Welcome to BillSplit AI Setup!"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Check if MySQL is running
if ! mysqladmin ping -h localhost --silent; then
    echo "⚠️  MySQL is not running. Please start MySQL first."
    echo "   On macOS: brew services start mysql"
    echo "   On Ubuntu: sudo systemctl start mysql"
    echo "   On Windows: Start MySQL service from Services"
    echo ""
    read -p "Press Enter to continue anyway..."
fi

echo "✅ Prerequisites check completed!"
echo ""

# Backend Setup
echo "🔧 Setting up Backend..."
cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file from template
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp env_template.txt .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit the .env file with your actual values:"
    echo "   - OpenAI API key"
    echo "   - MySQL database credentials"
    echo "   - Flask secret key"
    echo ""
    read -p "Press Enter after you've configured the .env file..."
else
    echo "✅ .env file already exists"
fi

echo "✅ Backend setup completed!"
echo ""

# Frontend Setup
echo "🎨 Setting up Frontend..."
cd ../frontend

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

echo "✅ Frontend setup completed!"
echo ""

# Return to root directory
cd ..

echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Configure your .env file in the backend directory"
echo "2. Create the MySQL database: CREATE DATABASE billsplit_db;"
echo "3. Start the backend: cd backend && source venv/bin/activate && python app.py"
echo "4. Start the frontend: cd frontend && npm run dev"
echo ""
echo "🌐 The application will be available at:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:5000"
echo ""
echo "Happy Bill Splitting! 🍽️"
