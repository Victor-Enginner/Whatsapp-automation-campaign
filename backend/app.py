from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
import pandas as pd
import json
import os
import uuid
from typing import Dict, List
import subprocess
import threading
from datetime import datetime
import webbrowser

app = FastAPI(title="WhatsApp Automation API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Estado global
campaign_state = {
    "status": "idle",  # idle, running, paused, completed
    "progress": 0,
    "total_leads": 0,
    "sent": 0,
    "failed": 0,
    "current_batch": 0,
    "total_batches": 0,
    "logs": [],
    "started_at": None,
    "completed_at": None
}

# Configuração padrão
default_config = {
    "arquivo_leads": "leads.csv",
    "coluna_telefone": "telefone",
    "coluna_mensagem": "mensagem_sugerida",
    "coluna_status": "status",
    "filtro_status": "não contatado",
    "lote_tamanho": 20,
    "tempo_entre_msg_min": 15,
    "tempo_entre_msg_max": 30,
    "tempo_espera_lotes_segundos": 300,
    "max_tentativas": 2,
    "delay_erro_segundos": 10,
    "ddi_padrao": "55",
    "modo_teste": False,
    "log_arquivo": "log_envio.txt",
    "relatorio_erros": "erros.csv",
    "variaveis_personalizacao": ["nome", "nicho", "cidade"],
    "padroes_anti_bloqueio": {
        "variacao_tempo_ativada": True,
        "pausas_aleatorias": False,
        "simulacao_digitacao": False,
        "limite_mensagens_hora": 40
    }
}

@app.get("/")
async def root():
    return {"message": "WhatsApp Automation API", "version": "1.0"}

@app.get("/api/status")
async def get_status():
    """Retorna o status atual da campanha"""
    return campaign_state

@app.get("/api/config")
async def get_config():
    """Retorna a configuração atual"""
    config_file = "config.json"
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return default_config

@app.post("/api/config")
async def update_config(config: Dict):
    """Atualiza a configuração"""
    with open("config.json", 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    return {"message": "Configuração atualizada com sucesso"}

@app.post("/api/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    """Faz upload do arquivo CSV"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Arquivo deve ser CSV")
    
    # Salva arquivo
    filename = f"leads_{uuid.uuid4().hex[:8]}.csv"
    filepath = os.path.join("uploads", filename)
    os.makedirs("uploads", exist_ok=True)
    
    with open(filepath, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Analisa CSV
    try:
        df = pd.read_csv(filepath)
        preview = df.head(5).to_dict('records')
        columns = list(df.columns)
        total_rows = len(df)
        
        return {
            "filename": filename,
            "filepath": filepath,
            "columns": columns,
            "total_rows": total_rows,
            "preview": preview
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ler CSV: {str(e)}")

@app.post("/api/start-campaign")
async def start_campaign(config: Dict):
    """Inicia a campanha de envio"""
    if campaign_state["status"] == "running":
        raise HTTPException(status_code=400, detail="Campanha já está em execução")
    
    # Atualiza configuração
    with open("config.json", 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    # Reseta estado
    campaign_state.update({
        "status": "running",
        "progress": 0,
        "sent": 0,
        "failed": 0,
        "current_batch": 0,
        "logs": [],
        "started_at": datetime.now().isoformat(),
        "completed_at": None
    })
    
    # Inicia script em background
    def run_script():
        try:
            process = subprocess.Popen(
                ["python", "auto_whatsapp_pro.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8'
            )
            
            for line in process.stdout:
                campaign_state["logs"].append({
                    "timestamp": datetime.now().isoformat(),
                    "message": line.strip()
                })
                if len(campaign_state["logs"]) > 100:
                    campaign_state["logs"].pop(0)
            
            process.wait()
            campaign_state["status"] = "completed"
            campaign_state["completed_at"] = datetime.now().isoformat()
            
        except Exception as e:
            campaign_state["status"] = "error"
            campaign_state["logs"].append({
                "timestamp": datetime.now().isoformat(),
                "message": f"Erro: {str(e)}"
            })
    
    thread = threading.Thread(target=run_script)
    thread.start()
    
    return {"message": "Campanha iniciada"}

@app.post("/api/stop-campaign")
async def stop_campaign():
    """Para a campanha em execução"""
    if campaign_state["status"] != "running":
        raise HTTPException(status_code=400, detail="Nenhuma campanha em execução")
    
    campaign_state["status"] = "stopped"
    campaign_state["completed_at"] = datetime.now().isoformat()
    
    return {"message": "Campanha parada"}

@app.get("/api/logs")
async def get_logs():
    """Retorna os logs da campanha"""
    return {"logs": campaign_state["logs"]}

@app.get("/api/statistics")
async def get_statistics():
    """Retorna estatísticas detalhadas"""
    # Lê arquivo de log se existir
    log_file = campaign_state.get("log_arquivo", "log_envio.txt")
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            logs = f.readlines()
    else:
        logs = []
    
    # Lê arquivo de erros se existir
    error_file = campaign_state.get("relatorio_erros", "erros.csv")
    errors = []
    if os.path.exists(error_file):
        try:
            df = pd.read_csv(error_file)
            errors = df.to_dict('records')
        except:
            pass
    
    return {
        "logs_count": len(logs),
        "errors_count": len(errors),
        "errors": errors[-10:] if errors else [],  # Últimos 10 erros
        "campaign_state": campaign_state
    }


@app.post('/api/open-whatsapp')
async def open_whatsapp():
    """Abre o WhatsApp Web no navegador padrão para que o usuário escaneie o QR Code."""
    try:
        url = 'https://web.whatsapp.com/'
        webbrowser.open(url)
        return JSONResponse({"message": "WhatsApp Web aberto no navegador."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Frontend is now deployed separately on Vercel
# This backend only provides API endpoints
# CORS is enabled above to allow requests from Vercel domain
