import subprocess
import sys
import os
from pathlib import Path

def start_backend():
    """Inicia o backend FastAPI"""
    print("🚀 Iniciando Backend (FastAPI)...")
    backend_path = Path(__file__).parent / "backend" / "app.py"
    subprocess.Popen([sys.executable, str(backend_path)], cwd=Path(__file__).parent)
    print("✅ Backend rodando em http://localhost:8000")

def start_frontend():
    """Inicia o frontend React"""
    print("🎨 Iniciando Frontend (React)...")
    frontend_path = Path(__file__).parent / "frontend"
    subprocess.Popen(["npm", "start"], shell=True, cwd=frontend_path)
    print("✅ Frontend rodando em http://localhost:3000")

if __name__ == "__main__":
    print("🎯 Iniciando WhatsApp Automation - Sistema Completo")
    print("=" * 50)
    
    start_backend()
    start_frontend()
    
    print("\n" + "=" * 50)
    print("✨ Sistema iniciado com sucesso!")
    print("📱 Frontend: http://localhost:3000")
    print("🔌 Backend API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("\nPressione Ctrl+C para parar tudo")
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n🛑 Sistema parado pelo usuário")
