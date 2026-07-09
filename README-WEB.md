# WhatsApp Automation - Web Interface

Sistema completo de automação de WhatsApp com interface web moderna.

## 🏗️ Estrutura do Projeto

```
kling/
├── backend/
│   └── app.py              # API FastAPI
├── frontend/
│   ├── src/
│   │   ├── App.js          # Componente principal React
│   │   ├── App.css         # Estilos
│   │   └── index.js        # Entry point
│   ├── package.json        # Dependências React
│   └── tailwind.config.js  # Config TailwindCSS
├── auto_whatsapp_pro.py    # Script de automação
├── config.json             # Configurações
└── nexus-itapema.csv       # Arquivo de leads
```

## 🚀 Como Usar

### 1. Instalar Dependências do Backend

```bash
cd c:\Users\Victor Ads\Desktop\kling
pip install -r requirements-backend.txt
```

### 2. Instalar Dependências do Frontend

```bash
cd frontend
npm install
```

### 3. Iniciar o Backend

```bash
cd c:\Users\Victor Ads\Desktop\kling
python backend/app.py
```

O backend estará rodando em: `http://localhost:8000`

### 4. Iniciar o Frontend

```bash
cd frontend
npm start
```

O frontend estará rodando em: `http://localhost:3000`

## 🎯 Funcionalidades

### Dashboard
- Status em tempo real da campanha
- Estatísticas de envio (enviados, falhas, progresso)
- Visualização do arquivo carregado
- Prévia dos dados do CSV

### Upload CSV
- Interface drag & drop para upload
- Análise automática do arquivo
- Visualização de colunas e dados
- Validação de formato

### Configurações
- Ajuste de tamanho de lote
- Configuração de tempos de delay
- Definição de DDI padrão
- Ativação/desativação do modo teste

### Logs
- Visualização em tempo real dos logs
- Histórico de operações
- Identificação de erros

## 📡 API Endpoints

### GET `/api/status`
Retorna o status atual da campanha

### GET `/api/config`
Retorna a configuração atual

### POST `/api/config`
Atualiza a configuração

### POST `/api/upload-csv`
Faz upload do arquivo CSV

### POST `/api/start-campaign`
Inicia a campanha de envio

### POST `/api/stop-campaign`
Para a campanha em execução

### GET `/api/logs`
Retorna os logs da campanha

### GET `/api/statistics`
Retorna estatísticas detalhadas

## 🔧 Configuração

O arquivo `config.json` controla todos os parâmetros:

```json
{
  "arquivo_leads": "nexus-itapema.csv",
  "lote_tamanho": 20,
  "tempo_entre_msg_min": 15,
  "tempo_entre_msg_max": 30,
  "modo_teste": false
}
```

## 🎨 Interface

A interface web oferece:

- **Design moderno** com tema escuro
- **Responsivo** para diferentes dispositivos
- **Atualização em tempo real** do status
- **Fácil uso** com interface intuitiva
- **Monitoramento completo** da campanha

## ⚠️ Notas Importantes

1. **Primeiro uso**: O WhatsApp Web precisará escanear o QR Code
2. **Modo teste**: Use o modo teste para validar antes de enviar mensagens reais
3. **Limites**: Respeite os limites do WhatsApp para evitar bloqueios
4. **Monitoramento**: Acompanhe os logs em tempo real na interface

## 🛠️ Tecnologias

### Backend
- **FastAPI**: Framework web moderno
- **Uvicorn**: Servidor ASGI
- **Pandas**: Manipulação de dados CSV

### Frontend
- **React**: Biblioteca UI
- **TailwindCSS**: Framework CSS
- **Lucide React**: Ícones
- **Axios**: Cliente HTTP

## 📝 Próximos Passos

Para usar o sistema:

1. Instale as dependências (backend e frontend)
2. Inicie o backend: `python backend/app.py`
3. Inicie o frontend: `cd frontend && npm start`
4. Acesse `http://localhost:3000`
5. Faça upload do CSV na aba "Upload CSV"
6. Configure os parâmetros na aba "Configurações"
7. Inicie a campanha no botão "Iniciar Campanha"
8. Acompanhe o progresso em tempo real
