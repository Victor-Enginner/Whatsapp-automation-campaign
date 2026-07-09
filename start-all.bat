@echo off
echo 🎯 Iniciando WhatsApp Automation - Sistema Completo
echo ==================================================

echo 🚀 Iniciando Backend (FastAPI)...
start python backend\app.py

echo 🎨 Iniciando Frontend (React)...
cd frontend
start npm start
cd ..

echo ==================================================
echo ✨ Sistema iniciado com sucesso!
echo 📱 Frontend: http://localhost:3000
echo 🔌 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo ==================================================
pause
