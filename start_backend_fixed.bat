@echo off
echo 🔧 Starting ERP Backend with CORS Fix...
echo.

cd /d "C:\Users\Xerxez Solutions\Desktop\ERP\backend"

echo 📋 Checking Django configuration...
python manage.py check --deploy

echo.
echo 🚀 Starting Django development server on port 8000...
echo ✅ CORS now allows: localhost:3000, localhost:3001, 127.0.0.1:3000, 127.0.0.1:3001
echo.
echo 🌐 Your frontend on http://localhost:3001 should now work!
echo 🔑 Login credentials: admin / admin123
echo.

python manage.py runserver 8000
