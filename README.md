# WhatsApp Auto Sender PRO - Automação Avançada de Envio de Mensagens

Sistema automatizado profissional para envio de mensagens em massa via WhatsApp Web usando Python. Gratuito, baseado em QR Code com recursos avançados anti-bloqueio e relatórios detalhados.

## 🚀 Características Avançadas

### Core Features
- **100% Gratuito**: Usa seu WhatsApp Web pessoal (sem API da Meta)
- **Envio em Lotes**: Processa mensagens em lotes configuráveis
- **Personalização Multi-Variável**: Substitui `{nome}`, `{empresa}`, `{produto}` e mais
- **Limpeza Automática**: Valida e formata números de telefone automaticamente

### Anti-Bloqueio Inteligente
- **Delays Dinâmicos**: Variação de tempo entre mensagens (-30% a +50%)
- **Pausas Aleatórias**: 10% de chance de pausas extras (30-60s)
- **Retry Automático**: Até 3 tentativas para mensagens falhadas
- **Validação de Números**: Verifica formato e adiciona DDI automaticamente

### Monitoramento e Logs
- **Logging Detalhado**: Registra todas as operações em arquivo e terminal
- **Barra de Progresso**: Visualização em tempo real com tqdm
- **Estatísticas Completas**: Taxa de sucesso, retries, duração total
- **Relatório de Erros**: CSV com números falhados e motivos

### Configuração Flexível
- **Arquivo JSON**: Todas configurações em `config.json`
- **Modo Teste**: Execute sem enviar mensagens reais
- **Parâmetros Ajustáveis**: Tempos, lotes, retries, DDI padrão

## 📋 Pré-requisitos

- Python 3.7 ou superior instalado
- Google Chrome instalado
- Conta WhatsApp ativa com número verificado

## 🔧 Instalação

1. Clone ou baixe este projeto para sua máquina

2. Navegue até a pasta do projeto:
```bash
cd kling
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 📄 Preparar o Arquivo de Leads

Crie ou edite o arquivo `leads.csv` com o seguinte formato:

```csv
nome,telefone,mensagem,empresa,produto
João Silva,+5511999999999,Olá {nome} da {empresa}, vi que você tem interesse em nossos serviços. Podemos conversar?,Tech Solutions,Consultoria
Maria Souza,+5511876543210,Oi {nome} da {empresa}, temos uma oferta especial do {produto} hoje. Gostaria de saber mais?,Inovação Ltda,Software ERP
```

**Colunas obrigatórias:**
- `nome`: Nome do contato (usado para personalização)
- `telefone`: Número com DDI (ex: +5511999999999)
- `mensagem`: Texto da mensagem (use variáveis para personalização)

**Colunas opcionais (configuráveis em `config.json`):**
- `empresa`: Nome da empresa para personalização
- `produto`: Nome do produto/serviço para personalização
- Adicione mais campos conforme necessário

## ⚙️ Configuração

Todas as configurações estão no arquivo `config.json`:

```json
{
  "arquivo_leads": "leads.csv",
  "lote_tamanho": 50,
  "tempo_entre_msg_min": 10,
  "tempo_entre_msg_max": 25,
  "tempo_espera_lotes_segundos": 1800,
  "max_tentativas": 3,
  "delay_erro_segundos": 5,
  "ddi_padrao": "55",
  "modo_teste": false,
  "log_arquivo": "log_envio.txt",
  "relatorio_erros": "erros.csv",
  "variaveis_personalizacao": ["nome", "empresa", "produto"],
  "padroes_anti_bloqueio": {
    "variacao_tempo_ativada": true,
    "pausas_aleatorias": true,
    "simulacao_digitacao": false,
    "limite_mensagens_hora": 60
  }
}
```

**Parâmetros principais:**
- `arquivo_leads`: Nome do arquivo CSV com os contatos
- `lote_tamanho`: Quantidade de mensagens por lote (recomendado: 50)
- `tempo_entre_msg_min/max`: Intervalo entre mensagens em segundos
- `max_tentativas`: Número de retries para mensagens falhadas
- `modo_teste`: Ative para testar sem enviar mensagens reais
- `variaveis_personalizacao`: Lista de variáveis para substituir nas mensagens

## 🎯 Como Executar

1. Execute o script:
```bash
python auto_whatsapp_pro.py
```

2. Um navegador Chrome abrirá automaticamente

3. Escaneie o QR Code do WhatsApp Web com seu celular

4. Aguarde a mensagem "✅ Conectado com sucesso!"

5. O sistema começará a enviar mensagens automaticamente com barra de progresso

6. Entre lotes, pressione **Enter** para continuar ou aguarde

7. Ao final, verifique as estatísticas e o relatório de erros (se houver)

## 📊 Estatísticas e Relatórios

### Estatísticas Finais
Ao final da execução, o sistema exibe:
- ✅ Total de mensagens enviadas com sucesso
- ❌ Total de falhas
- 🔄 Total de retries realizados
- ⏱️ Duração total da execução
- 📈 Taxa de sucesso (%)

### Arquivos Gerados
- **log_envio.txt**: Log detalhado de todas as operações
- **erros.csv**: Relatório de números que falharam com motivos e timestamps

### Modo Teste
Para testar sem enviar mensagens reais, edite `config.json`:
```json
{
  "modo_teste": true
}
```

## 📊 Estimativa de Tempo

Para 500 leads com configuração padrão:
- **10 lotes** de 50 mensagens cada
- **~14-17 minutos** por lote (com variação anti-bloqueio)
- **Total ativo**: ~2.5 - 3 horas

## ⚠️ Recomendações de Segurança

- **Não envie mais de 500 mensagens por dia** para evitar bloqueios
- **Mantenha intervalos entre mensagens** de pelo menos 10 segundos
- **Use pausas entre lotes** para simular comportamento humano
- **Varie as mensagens** para evitar padrões suspeitos
- **Monitore o terminal** para erros durante o envio

## 🔍 Solução de Problemas

### Erro: Arquivo não encontrado
- Certifique-se que `leads.csv` está na mesma pasta do script
- Verifique o nome do arquivo em `config.json`

### Erro ao conectar
- Verifique sua conexão com a internet
- Certifique-se que o Chrome está instalado
- Tente escanear o QR Code novamente

### Números muito curtos
- Verifique se os números têm DDI + DDD (mínimo 10 dígitos)
- O script adiciona automaticamente o DDI configurado em `config.json`

### Mensagens não enviadas
- Verifique se o número está correto e tem WhatsApp
- Confirme que a mensagem não está vazia
- Veja `log_envio.txt` para detalhes do erro
- Verifique `erros.csv` para relatório de falhas

### Configuração não carregada
- Se `config.json` tiver erro de sintaxe, o sistema usa configurações padrão
- Verifique se o JSON está válido (use um validador JSON online)

### Muitas falhas
- Reduza o `lote_tamanho` em `config.json`
- Aumente `tempo_entre_msg_min/max` para delays mais longos
- Ative `modo_teste` para validar dados antes de enviar

## 📝 Personalização Avançada

O sistema suporta múltiplas variáveis dinâmicas configuradas em `config.json`:

### Adicionar Nova Variável

1. Adicione a coluna no CSV:
```csv
nome,telefone,mensagem,empresa,produto,cidade
João,+5511999999999,Olá {nome} da {empresa} em {cidade},Tech Solutions,Consultoria,São Paulo
```

2. Adicione a variável em `config.json`:
```json
{
  "variaveis_personalizacao": ["nome", "empresa", "produto", "cidade"]
}
```

3. Use na mensagem:
```csv
mensagem
Olá {nome} da {empresa} em {cidade}, temos novidades sobre {produto}!
```

O sistema substituirá automaticamente todas as variáveis configuradas.

## 🛠️ Tecnologias Utilizadas

- **Python 3.7+**: Linguagem principal
- **whatsapp-web.py**: Biblioteca de automação do WhatsApp
- **Selenium**: Controle do navegador Chrome
- **webdriver-manager**: Gerenciamento automático do ChromeDriver
- **BeautifulSoup4**: Parsing HTML (opcional)
- **pandas**: Manipulação de dados CSV
- **tqdm**: Barra de progresso visual
- **logging**: Sistema de logging detalhado

## 📄 Licença

Este projeto é open-source e gratuito. Use por sua conta e risco.

## ⚖️ Aviso Legal

Este ferramenta é para fins educacionais e de automação legítima. O uso indevido pode violar os termos de serviço do WhatsApp. Respeite as políticas de anti-spam e obtenha consentimento dos contatos antes de enviar mensagens.

## 🤝 Contribuições

Sugestões e melhorias são bem-vindas!
