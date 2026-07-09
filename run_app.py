import os
import sys
from backend import app
import uvicorn

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Auto WhatsApp Pro - Backend API")
    print("="*60)
    print("\n📡 API iniciando em http://localhost:8000")
    print("✅ Dashboard disponível em: https://auto-whatsapp-pro.vercel.app")
    print("\n⚠️ Mantenha este terminal aberto para que a API funcione")
    print("="*60 + "\n")
    
    uvicorn.run(app, host='0.0.0.0', port=8000)
