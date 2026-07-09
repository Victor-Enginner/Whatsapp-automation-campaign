# Auto WhatsApp Pro - Release

## 🎯 Como Funciona

Arquitetura híbrida:
- **Dashboard Web**: Hospedado na Vercel (https://auto-whatsapp-pro.vercel.app)
- **API Backend**: Roda localmente na sua máquina (port 8000)
- **Vantagem**: Acesse de qualquer navegador, mas a automação funciona localmente com WhatsApp Web

## 🚀 Começar Rápido

### Passo 1: Iniciar a API Backend
```
run_app.exe
```

Você verá:
```
============================================================
🚀 Auto WhatsApp Pro - Backend API
============================================================

📡 API iniciando em http://localhost:8000
✅ Dashboard disponível em: https://auto-whatsapp-pro.vercel.app

⚠️ Mantenha este terminal aberto para que a API funcione
============================================================
```

### Passo 2: Acessar o Dashboard
1. Abra seu navegador
2. Acesse: **https://auto-whatsapp-pro.vercel.app**
3. O dashboard se conectará automaticamente à sua API local

### Passo 3: Usar a Aplicação
1. **Importar contatos**: Clique em "Escolher Arquivo"
2. **Selecione seu CSV** com números de telefone
3. **Clique em "Iniciar Campanha"**
4. **Escaneie o QR code** do WhatsApp Web
5. **Mensagens serão enviadas automaticamente**

## 📋 Requisitos do Sistema

- **Windows 10 ou superior** (64 bits)
- **Chrome instalado** (necessário para WhatsApp Web)
- **Conexão com internet** (para Vercel + WhatsApp Web)
- **Porta 8000 livre** (a API usa esta porta)

## 📁 Formato do CSV

Seu arquivo CSV deve conter colunas com:
- **phone** (ou telefone, numero, celular): Números com DDD
- **message** (ou mensagem): Texto a enviar

Exemplo:
```
phone,name,message
16999990732,João,Olá João! Testando
21987654321,Maria,Olá Maria!
```

## ⚙️ Configuração

Edite `config.json` para personalizar:
- `lote_tamanho`: Quantos contatos enviar por lote
- `tempo_entre_msg_min/max`: Delay entre mensagens (anti-bloqueio)
- `modo_teste`: true = simula, false = envia real
- `ddi_padrao`: DDI padrão (ex: 55 para Brasil)

## 🔧 Troubleshooting

### "Não consegue conectar à API"
- Certifique-se que `run_app.exe` está rodando
- Verifique se porta 8000 está livre: `netstat -ano | findstr :8000`
- Se ocupada: feche outro app que usa porta 8000

### "Mensagens não enviam"
- Abra https://web.whatsapp.com em outro navegador
- Escaneie o QR code
- Volte ao dashboard e tente novamente

### "Erro de autenticação WhatsApp"
- Feche todos os navegadores com WhatsApp Web aberto
- Execute novamente
- Deixe a janela do browser aberta enquanto as mensagens estão sendo enviadas

## 📊 Modo Teste

Para testar sem enviar mensagens reais:
1. No `config.json`, altere: `"modo_teste": true`
2. Ao enviar, verá: "🧪 [MODO TESTE] Enviaria para..."
3. Perfeito para validar antes de enviar para VERD

## ✨ Características

✅ Interface moderna e responsiva  
✅ Importação automática de CSV  
✅ Normalização de números internacionais (E.164)  
✅ Modo teste para validação  
✅ Logs detalhados em tempo real  
✅ Anti-bloqueio com delays aleatórios  
✅ Retry automático em caso de falha  
✅ Resumo de estatísticas  

## 📞 Suporte

Se encontrar problemas:
1. Verifique `log_envio.txt` para detalhes
2. Confirme requisitos de sistema
3. Teste modo teste primeiro
4. Reinicie a API e tente novamente

**Versão v1.0 - WhatsApp Web Integration**
