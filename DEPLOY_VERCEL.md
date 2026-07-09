# Deploy no Vercel - Frontend React

## Problema Identificado
O Vercel estava detectando arquivos `.py` na raiz e tentando compilar como Python.

## Solução Aplicada

### 1. Arquivo `vercel.json` criado
Configuração que instrui o Vercel a:
- Usar framework React
- Buildar apenas a pasta `frontend/`
- Ignorar arquivos Python e backend
- Fazer rewrite de rotas para o React Router

### 2. Arquivo `.vercelignore` atualizado
Ignora todos os arquivos desnecessários:
- Todos os arquivos `.py`
- Pastas `backend/`, `uploads/`, `pack/`, `release/`
- Arquivos de configuração Python
- Arquivos de dados e logs

## Como Fazer o Deploy

### Pré-requisito: Build Local Funcionou ✅
Executei `npm run build` localmente e funcionou perfeitamente!

### Opção 1: Via Dashboard da Vercel
1. Acesse https://vercel.com
2. Clique em "Add New..." → "Project"
3. Conecte seu repositório GitHub: `Victor-Enginner/Whatsapp-automation-campaign`
4. **IMPORTANTE**: Configure:
   - **Root Directory**: `frontend`
   - **Framework Preset**: React
5. Clique em "Deploy"

### Opção 2: Via Vercel CLI (Local)
```bash
# Instalar Vercel CLI (se não tiver)
npm i -g vercel

# Fazer deploy (execute da raiz do projeto)
cd frontend
vercel
```

### Opção 2: Via Vercel CLI
```bash
# Instalar Vercel CLI (se não tiver)
npm i -g vercel

# Fazer deploy
cd frontend
vercel
```

## Após o Deploy

1. **URL do Frontend**: `https://seu-projeto.vercel.app`
2. **API Backend**: 
   - **Desenvolvimento local**: Backend roda em `http://localhost:8000`
   - **Produção**: Use Railway/Render para hospedar o backend
   - Configure `REACT_APP_API_URL` nas Environment Variables da Vercel

### Configurar Variável de Ambiente na Vercel
1. Vá no Dashboard do seu projeto na Vercel
2. Settings → Environment Variables
3. Adicione:
   - **Name**: `REACT_APP_API_URL`
   - **Value**: `http://localhost:8000` (ou URL do seu backend na nuvem)
4. Clique em "Save"

## Arquivos Modificados

✅ **vercel.json** - Configuração do Vercel para build correto do React
✅ **.vercelignore** - Ignora arquivos Python e backend
✅ **frontend/.env.production** - Variável de ambiente para produção
✅ **DEPLOY_VERCEL.md** - Este guia

## Próximos Passos

1. **Commit e push das alterações**:
   ```bash
   git add .
   git commit -m "Fix: Configurar Vercel para deploy do React frontend"
   git push
   ```

2. **Acesse o Dashboard da Vercel**:
   - O redeploy automático deve começar em alguns segundos
   - Ou clique em "Redeploy" manualmente

3. **Se ainda der erro**, verifique:
   - Root Directory está como `frontend`
   - Framework Preset está como React
   - Veja os logs de build na Vercel para detalhes do erro

## Troubleshooting

### Erro: "Build failed"
- Verifique se o Root Directory está como `frontend`
- Verifique se o Framework está como React
- Veja os logs de build na Vercel para detalhes do erro

### Erro: "Cannot find module"
- Rode `cd frontend && npm install` localmente
- Verifique se o `package-lock.json` está commitado no git

### Erro de CORS
- Quando o frontend (vercel.app) acessar o backend localhost, ocorrerá erro de CORS
- Solução: Use Railway/Render para hospedar o backend também, ou configure CORS no backend

## Troubleshooting

### Erro: "Build failed"
- Verifique se o Root Directory está como `frontend`
- Verifique se o Framework está como React
- Veja os logs de build no Vercel

### Erro: "Cannot find module"
- Rode `cd frontend && npm install` localmente antes do primeiro deploy
- Verifique se o `package-lock.json` está commitado

### Erro de CORS
- Quando o frontend (vercel.app) acessar o backend localhost, ocorrerá erro de CORS
- Solução: Use Railway/Render para o backend também, ou configure CORS no backend