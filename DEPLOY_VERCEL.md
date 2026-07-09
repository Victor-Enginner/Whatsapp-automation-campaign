# Deploy Frontend na Vercel

## Pré-requisitos

- Conta GitHub (necessária para deploy automático)
- Conta Vercel (pode usar GitHub login)
- Este repositório no GitHub

## Passos para Deploy

### 1. Prepare o Repositório GitHub

```bash
git init
git add .
git commit -m "Auto WhatsApp Pro - Initial commit"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/seu-repo.git
git push -u origin main
```

### 2. Conectar à Vercel

1. Acesse: https://vercel.com
2. Clique em "New Project"
3. Selecione "Import Git Repository"
4. Escolha seu repositório do GitHub
5. Clique em "Import"

### 3. Configurar Build Settings

**Framework**: Create React App  
**Build Command**: `npm run build`  
**Output Directory**: `build`  
**Install Command**: `npm install`

### 4. Adicionar Environment Variables

No dashboard da Vercel, adicione:

**Variável**: `REACT_APP_API_URL`  
**Valor**: `http://localhost:8000` (usuários finais sempre usarão localhost)

### 5. Deploy

Clique em "Deploy" - pronto! A Vercel deploy automaticamente

## Atualizações Futuras

Após fazer push para GitHub:
```bash
git add .
git commit -m "Sua mensagem"
git push
```

A Vercel fará deploy automático!

## Verificar Deploy

Após deploy, você terá URL como:
- `https://auto-whatsapp-pro.vercel.app` (customizado)
- ou `https://seu-projeto-xyz.vercel.app` (padrão)

## CORS e Localhost

A API backend está configurada com CORS aberto (`allow_origins=["*"]`), então o frontend da Vercel consegue se conectar ao `http://localhost:8000` do usuário sem problemas.

## Troubleshooting

### "API não responde"
- Certifique-se que `run_app.exe` está rodando
- Verifique firewall/antivírus

### "Dashboard carrega mas não conecta"
- Abra DevTools (F12)
- Veja Network tab para erros
- Confirme que localhost:8000 está acessível

## Dashboard URL

Compartilhe esta URL com seus usuários:
**https://auto-whatsapp-pro.vercel.app**

Eles apenas precisam:
1. Rodar `run_app.exe` localmente
2. Acessar o link acima
3. Pronto!
