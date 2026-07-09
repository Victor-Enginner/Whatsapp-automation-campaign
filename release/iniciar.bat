@echo off
REM Auto WhatsApp Pro - Iniciar Backend API
REM O Dashboard web está em: https://auto-whatsapp-pro.vercel.app

echo ===============================================
echo  Auto WhatsApp Pro - Backend API
echo ===============================================
echo.
echo. Iniciando a API em http://localhost:8000
echo.
echo. Após iniciar:
echo   1. Abra: https://auto-whatsapp-pro.vercel.app
echo   2. Importar seu CSV com contatos
echo   3. Clique em "Iniciar Campanha"
echo.
echo. MANTER ESTE TERMINAL ABERTO!
echo.
echo ===============================================
echo.

REM Inicia o backend API
start run_app.exe

REM Abre o dashboard na web (opcional)
timeout /t 2 /nobreak
start https://auto-whatsapp-pro.vercel.app

echo Dashboard aberto no navegador
echo Pressione CTRL+C neste terminal para parar a API
pause
