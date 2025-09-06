#!/usr/bin/env python3
"""
Smart Chatbot Quick Start Script
This script helps you get the Smart Chatbot up and running quickly
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_banner():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                   🤖 SMART CHATBOT SETUP                     ║
    ║                  AI-Powered ERP Assistant                    ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def check_requirements():
    """Check if required tools are installed"""
    print("🔍 Checking system requirements...")
    
    requirements = {
        'python': 'python --version',
        'node': 'node --version',
        'npm': 'npm --version',
        'pip': 'pip --version'
    }
    
    missing = []
    for tool, command in requirements.items():
        try:
            result = subprocess.run(command.split(), 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            if result.returncode == 0:
                print(f"  ✅ {tool}: {result.stdout.strip()}")
            else:
                missing.append(tool)
        except Exception:
            missing.append(tool)
    
    if missing:
        print(f"❌ Missing requirements: {', '.join(missing)}")
        return False
    
    print("✅ All requirements met!")
    return True

def setup_environment():
    """Set up environment variables"""
    print("\n🔧 Setting up environment...")
    
    env_file = Path("backend/.env")
    if not env_file.exists():
        print("📝 Creating .env file...")
        
        openai_key = input("Enter your OpenAI API key (or press Enter to skip): ")
        
        env_content = f"""
# Smart Chatbot Configuration
OPENAI_API_KEY={openai_key}
DJANGO_SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

# Security Settings
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# AI Configuration
CHATBOT_MODEL=gpt-3.5-turbo
CHATBOT_MAX_TOKENS=500
CHATBOT_TEMPERATURE=0.7
"""
        
        with open(env_file, 'w') as f:
            f.write(env_content.strip())
        
        print(f"✅ Environment file created at {env_file}")
        
        if not openai_key:
            print("⚠️  Warning: OpenAI API key not set. Add it to .env file later.")
    else:
        print("✅ Environment file already exists")

def install_backend_dependencies():
    """Install Python backend dependencies"""
    print("\n📦 Installing backend dependencies...")
    
    os.chdir("backend")
    
    # Check if virtual environment exists
    if not os.path.exists("venv"):
        print("🐍 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
    
    # Activate virtual environment and install packages
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix-like
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    packages = [
        "django",
        "djangorestframework",
        "django-cors-headers",
        "openai",
        "langchain",
        "langchain-openai",
        "faiss-cpu",
        "scikit-learn",
        "python-dotenv",
        "requests"
    ]
    
    print("📥 Installing Python packages...")
    for package in packages:
        try:
            subprocess.run([pip_cmd, "install", package], 
                         check=True, 
                         capture_output=True)
            print(f"  ✅ {package}")
        except subprocess.CalledProcessError:
            print(f"  ❌ Failed to install {package}")
    
    os.chdir("..")

def install_frontend_dependencies():
    """Install Node.js frontend dependencies"""
    print("\n🎨 Installing frontend dependencies...")
    
    os.chdir("frontend")
    
    print("📥 Installing Node.js packages...")
    try:
        subprocess.run(["npm", "install"], check=True, capture_output=True)
        print("✅ Frontend dependencies installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install frontend dependencies")
    
    os.chdir("..")

def setup_database():
    """Set up the database"""
    print("\n🗄️  Setting up database...")
    
    os.chdir("backend")
    
    if os.name == 'nt':  # Windows
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix-like
        python_cmd = "venv/bin/python"
    
    try:
        # Make migrations
        subprocess.run([python_cmd, "manage.py", "makemigrations"], 
                      check=True, capture_output=True)
        
        # Apply migrations
        subprocess.run([python_cmd, "manage.py", "migrate"], 
                      check=True, capture_output=True)
        
        print("✅ Database setup complete")
    except subprocess.CalledProcessError as e:
        print(f"❌ Database setup failed: {e}")
    
    os.chdir("..")

def run_tests():
    """Run basic tests"""
    print("\n🧪 Running tests...")
    
    # Test backend
    os.chdir("docs/chatbot-tests")
    try:
        subprocess.run([sys.executable, "test_chatbot_backend.py"], 
                      check=True, capture_output=True)
        print("✅ Backend tests passed")
    except subprocess.CalledProcessError:
        print("⚠️  Backend tests had issues (might need OpenAI API key)")
    
    os.chdir("../..")

def create_startup_scripts():
    """Create startup scripts for easy launching"""
    print("\n📝 Creating startup scripts...")
    
    # Backend startup script
    backend_script = """#!/bin/bash
# Smart Chatbot Backend Startup Script

echo "🚀 Starting Smart Chatbot Backend..."

cd backend

# Activate virtual environment
if [ "$OS" = "Windows_NT" ]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Start Django development server
python manage.py runserver 8000

echo "✅ Backend running at http://localhost:8000"
"""
    
    with open("start_backend.sh", "w") as f:
        f.write(backend_script)
    
    # Frontend startup script
    frontend_script = """#!/bin/bash
# Smart Chatbot Frontend Startup Script

echo "🎨 Starting Smart Chatbot Frontend..."

cd frontend

# Start React development server
npm start

echo "✅ Frontend running at http://localhost:3000"
"""
    
    with open("start_frontend.sh", "w") as f:
        f.write(frontend_script)
    
    # Windows batch files
    with open("start_backend.bat", "w") as f:
        f.write("""@echo off
echo 🚀 Starting Smart Chatbot Backend...
cd backend
call venv\\Scripts\\activate
python manage.py runserver 8000
echo ✅ Backend running at http://localhost:8000
pause
""")
    
    with open("start_frontend.bat", "w") as f:
        f.write("""@echo off
echo 🎨 Starting Smart Chatbot Frontend...
cd frontend
npm start
echo ✅ Frontend running at http://localhost:3000
pause
""")
    
    print("✅ Startup scripts created")

def main():
    """Main setup function"""
    print_banner()
    
    if not check_requirements():
        print("\n❌ Please install missing requirements and run again.")
        return
    
    try:
        setup_environment()
        install_backend_dependencies()
        install_frontend_dependencies()
        setup_database()
        run_tests()
        create_startup_scripts()
        
        print("""
        ╔══════════════════════════════════════════════════════════════╗
        ║                    🎉 SETUP COMPLETE!                        ║
        ╚══════════════════════════════════════════════════════════════╝
        
        🚀 Next Steps:
        
        1. Add your OpenAI API key to backend/.env file
        2. Start the backend: ./start_backend.sh (or .bat on Windows)
        3. Start the frontend: ./start_frontend.sh (or .bat on Windows)
        4. Open http://localhost:3000 in your browser
        5. Click "Smart Chatbot" in the sidebar to test!
        
        📚 Documentation: docs/Smart_Chatbot_Integration_Guide.md
        🧪 Tests: docs/chatbot-tests/
        
        Happy chatting! 🤖✨
        """)
    
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        print("Please check the logs and try again.")

if __name__ == "__main__":
    main()
