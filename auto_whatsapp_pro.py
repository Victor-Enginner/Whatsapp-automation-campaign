import os
import time
import random
import csv
import json
import logging
from datetime import datetime
import pywhatkit
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from tqdm import tqdm

class WhatsAppAuto:
    def __init__(self, arquivo_config='config.json'):
        self.config = self.carregar_config(arquivo_config)
        self.arquivo_csv = self.config['arquivo_leads']
        self.estatisticas = {
            'total_enviados': 0,
            'total_falhas': 0,
            'total_retries': 0,
            'inicio': None,
            'fim': None
        }
        self.erros = []
        self.configurar_logging()

    def carregar_config(self, arquivo_config):
        """Carrega configurações do arquivo JSON."""
        try:
            with open(arquivo_config, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Arquivo {arquivo_config} não encontrado. Usando configurações padrão.")
            return self.config_padrao()
        except json.JSONDecodeError:
            print(f"⚠️ Erro ao ler {arquivo_config}. Usando configurações padrão.")
            return self.config_padrao()

    def config_padrao(self):
        """Retorna configurações padrão."""
        return {
            'arquivo_leads': 'leads.csv',
            'lote_tamanho': 50,
            'tempo_entre_msg_min': 10,
            'tempo_entre_msg_max': 25,
            'tempo_espera_lotes_segundos': 1800,
            'max_tentativas': 3,
            'delay_erro_segundos': 5,
            'ddi_padrao': '55',
            'modo_teste': False,
            'log_arquivo': 'log_envio.txt',
            'relatorio_erros': 'erros.csv',
            'variaveis_personalizacao': ['nome', 'empresa', 'produto'],
            'padroes_anti_bloqueio': {
                'variacao_tempo_ativada': True,
                'pausas_aleatorias': True,
                'simulacao_digitacao': False,
                'limite_mensagens_hora': 60
            }
        }

    def configurar_logging(self):
        """Configura sistema de logging detalhado."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.config['log_arquivo'], encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def delay_inteligente(self, base_min=None, base_max=None):
        """Gera delay inteligente com padrões anti-bloqueio."""
        if base_min is None:
            base_min = self.config['tempo_entre_msg_min']
        if base_max is None:
            base_max = self.config['tempo_entre_msg_max']
        
        tempo = random.randint(base_min, base_max)
        
        # Adiciona variação extra se ativado
        if self.config['padroes_anti_bloqueio']['variacao_tempo_ativada']:
            variacao = random.uniform(-0.3, 0.5)  # -30% a +50%
            tempo = int(tempo * (1 + variacao))
            tempo = max(5, tempo)  # Mínimo de 5 segundos
        
        # Pausas aleatórias ocasionais
        if self.config['padroes_anti_bloqueio']['pausas_aleatorias']:
            if random.random() < 0.1:  # 10% de chance
                pausa_extra = random.randint(30, 60)
                self.logger.info(f"⏸️ Pausa extra anti-bloqueio: {pausa_extra}s")
                tempo += pausa_extra
        
        return tempo

    def validar_numero(self, numero):
        """Valida e formata número de telefone para E.164 (+55...)."""
        # Remove tudo que não é dígito
        numero_limpo = ''.join(filter(str.isdigit, str(numero).strip()))

        # Remove zero inicial se existir
        if numero_limpo.startswith('0'):
            numero_limpo = numero_limpo[1:]

        # Valida tamanho mínimo (10 = sem DDI, 12+ = com DDI)
        if len(numero_limpo) < 10:
            self.logger.warning(f"❌ Número muito curto: {numero}")
            return None

        # Adiciona DDI padrão se não tiver
        ddi = str(self.config.get('ddi_padrao', '55'))
        if not numero_limpo.startswith(ddi) and len(numero_limpo) <= 11:
            numero_limpo = ddi + numero_limpo

        # Se ainda não tem DDI e tem 12+ dígitos, algo está errado
        if len(numero_limpo) > 13:
            self.logger.warning(f"⚠️ Número muito longo (possível formatação errada): {numero_limpo}")
            # Tenta extrair apenas os últimos 11 dígitos (9 dígitos + 2 DDD)
            numero_limpo = numero_limpo[-11:]
            if not numero_limpo.startswith(ddi):
                numero_limpo = ddi + numero_limpo

        # FORÇA o prefixo + para garantir formato E.164 (crítico para pywhatkit)
        numero_final = '+' + numero_limpo if not numero_limpo.startswith('+') else numero_limpo
        self.logger.debug(f"✅ Número validado: {numero} → {numero_final}")
        return numero_final

    def ler_leads(self):
        """Lê o arquivo CSV e retorna uma lista de dicionários."""
        leads = []
        try:
            with open(self.arquivo_csv, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                # Obtém nomes das colunas do config com fallbacks
                coluna_telefone = self.config.get('coluna_telefone', 'telefone')
                coluna_mensagem = self.config.get('coluna_mensagem', 'mensagem')
                coluna_status = self.config.get('coluna_status', None)
                filtro_status = self.config.get('filtro_status', None)
                
                # Encontra a coluna de telefone testando várias opções
                coluna_telefone_detectada = None
                if reader.fieldnames:
                    opcoes = [coluna_telefone, 'phone', 'telefone', 'numero', 'número', 'celular', 'whatsapp']
                    for opcao in opcoes:
                        if opcao.lower() in [col.lower() for col in reader.fieldnames]:
                            coluna_telefone_detectada = next(col for col in reader.fieldnames if col.lower() == opcao.lower())
                            self.logger.info(f"📌 Coluna de telefone detectada: '{coluna_telefone_detectada}'")
                            break
                
                if not coluna_telefone_detectada:
                    self.logger.error(f"❌ Não foi possível encontrar coluna de telefone. Colunas disponíveis: {reader.fieldnames}")
                    return []
                
                # Reset do reader após fieldnames
                file.seek(0)
                reader = csv.DictReader(file)
                
                for row in reader:
                    # Filtra por status se configurado
                    if coluna_status and filtro_status:
                        status_atual = row.get(coluna_status, '').strip().lower()
                        if status_atual != filtro_status.lower():
                            continue
                    
                    # Obtém número de telefone da coluna detectada
                    numero_raw = (row.get(coluna_telefone_detectada, '') or row.get(coluna_telefone, '') or row.get('phone', '')).strip()
                    if not numero_raw:
                        self.logger.warning("Linha sem número de telefone ignorada")
                        continue
                    
                    # Valida e formata número
                    numero_validado = self.validar_numero(numero_raw)
                    if not numero_validado:
                        continue
                    
                    # Pega mensagem (tenta múltiplas variações)
                    msg = (row.get(coluna_mensagem, '') or row.get('mensagem', '') or row.get('message', '') or row.get('msg', '')).strip()
                    if not msg:
                        self.logger.warning(f"Linha sem mensagem ignorada: {numero_raw}")
                        continue
                    
                    # Coleta todas as variáveis de personalização
                    dados_lead = {'numero': numero_validado, 'msg': msg}
                    for var in self.config['variaveis_personalizacao']:
                        dados_lead[var] = row.get(var, var.capitalize())

                    leads.append(dados_lead)
                    
        except FileNotFoundError:
            self.logger.error(f"❌ Arquivo {self.arquivo_csv} não encontrado.")
            return []
        
        self.logger.info(f"📄 {len(leads)} leads carregados do CSV.")
        return leads

    def substituir_variaveis(self, mensagem, dados_lead):
        """Substitui variáveis dinâmicas na mensagem."""
        msg_final = mensagem
        for var in self.config['variaveis_personalizacao']:
            placeholder = f'{{{var}}}'
            valor = dados_lead.get(var, var.capitalize())
            msg_final = msg_final.replace(placeholder, valor)
        return msg_final

    def enviar_mensagem_para_contato(self, numero, mensagem, tentativa=1):
        """Envia uma mensagem com mecanismo de retry usando pywhatkit."""
        if self.config['modo_teste']:
            self.logger.info(f"🧪 [MODO TESTE] Enviaria para {numero}: '{mensagem[:50]}...'")
            return True
        
        try:
            # pywhatkit.sendwhatmsg(numero, mensagem, hora, min)
            # Para envio imediato, usa hora atual + 1 minuto
            # pywhatkit expects a phone number in E.164 format (ex: +5511999999999)
            from datetime import datetime, timedelta
            agora = datetime.now() + timedelta(minutes=1)
            hora = agora.hour
            minuto = agora.minute

            numero_para_envio = numero
            # Caso o número já venha sem '+', garantir o formato
            if not str(numero_para_envio).startswith('+'):
                numero_para_envio = '+' + str(numero_para_envio)

            self.logger.info(f"Chamando pywhatkit para {numero_para_envio} (envio agendado em {hora}:{minuto})")

            pywhatkit.sendwhatmsg(
                phone_no=numero_para_envio,
                message=mensagem,
                time_hour=hora,
                time_min=minuto,
                wait_time=15,
                tab_close=True
            )
            time.sleep(5)
            return True
        except Exception as e:
            self.logger.error(f"❌ Erro ao enviar para {numero} (tentativa {tentativa}): {e}")
            
            if tentativa < self.config['max_tentativas']:
                self.estatisticas['total_retries'] += 1
                delay = self.config['delay_erro_segundos'] * tentativa
                self.logger.info(f"🔄 Retry {tentativa + 1}/{self.config['max_tentativas']} em {delay}s...")
                time.sleep(delay)
                return self.enviar_mensagem_para_contato(numero, mensagem, tentativa + 1)
            else:
                self.erros.append({
                    'numero': numero,
                    'mensagem': mensagem,
                    'erro': str(e),
                    'timestamp': datetime.now().isoformat()
                })
                return False

    def processar_lote(self, lote, numero_lote):
        """Processa um grupo de leads com barra de progresso."""
        self.logger.info(f"\n📦 Iniciando envio do lote {numero_lote} com {len(lote)} contatos...")
        
        for i, lead in enumerate(tqdm(lote, desc=f"Lote {numero_lote}")):
            numero = lead['numero']
            msg_base = lead['msg']
            
            # Personaliza a mensagem
            msg_personalizada = self.substituir_variaveis(msg_base, lead)
            
            self.logger.info(f"➡️ [{i+1}/{len(lote)}] Enviando para {numero}")
            
            sucesso = self.enviar_mensagem_para_contato(numero, msg_personalizada)
            
            if sucesso:
                self.estatisticas['total_enviados'] += 1
                # Delay inteligente anti-bloqueio
                tempo_espera = self.delay_inteligente()
                self.logger.info(f"   ⏳ Aguardando {tempo_espera}s...")
                time.sleep(tempo_espera)
            else:
                self.estatisticas['total_falhas'] += 1
                self.logger.warning("   ⚠️ Falha no envio após retries. Continuando...")
                time.sleep(self.config['delay_erro_segundos'])

    def gerar_relatorio_erros(self):
        """Gera arquivo CSV com erros encontrados."""
        if not self.erros:
            return
        
        with open(self.config['relatorio_erros'], 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['numero', 'mensagem', 'erro', 'timestamp'])
            writer.writeheader()
            writer.writerows(self.erros)
        
        self.logger.info(f"📊 Relatório de erros gerado: {self.config['relatorio_erros']}")

    def mostrar_estatisticas(self):
        """Exibe estatísticas finais da execução."""
        self.estatisticas['fim'] = datetime.now()
        duracao = self.estatisticas['fim'] - self.estatisticas['inicio']
        
        self.logger.info("\n" + "="*50)
        self.logger.info("📊 ESTATÍSTICAS FINAIS")
        self.logger.info("="*50)
        self.logger.info(f"✅ Enviados com sucesso: {self.estatisticas['total_enviados']}")
        self.logger.info(f"❌ Falhas: {self.estatisticas['total_falhas']}")
        self.logger.info(f"🔄 Retries realizados: {self.estatisticas['total_retries']}")
        self.logger.info(f"⏱️ Duração total: {duracao}")
        self.logger.info(f"📈 Taxa de sucesso: {(self.estatisticas['total_enviados']/(self.estatisticas['total_enviados']+self.estatisticas['total_falhas'])*100):.1f}%" if (self.estatisticas['total_enviados']+self.estatisticas['total_falhas']) > 0 else "N/A")
        self.logger.info("="*50)

    def rodar(self):
        """Loop principal de execução."""
        self.estatisticas['inicio'] = datetime.now()
        
        if self.config['modo_teste']:
            self.logger.warning("🧪 MODO TESTE ATIVADO - Nenhuma mensagem será enviada!")
        
        leads = self.ler_leads()
        
        if not leads:
            self.logger.error("❌ Nenhum lead para processar.")
            return

        total_lotes = (len(leads) + self.config['lote_tamanho'] - 1) // self.config['lote_tamanho']
        
        # Divide os leads em lotes
        for i in range(0, len(leads), self.config['lote_tamanho']):
            lote_atual = leads[i:i + self.config['lote_tamanho']]
            numero_lote = i // self.config['lote_tamanho'] + 1
            
            self.logger.info(f"\n{'='*30}")
            self.logger.info(f"🚀 INICIANDO LOTE {numero_lote}/{total_lotes}")
            self.logger.info(f"{'='*30}")
            
            self.processar_lote(lote_atual, numero_lote)
            
            # Pausa entre lotes
            if i + self.config['lote_tamanho'] < len(leads):
                if self.config['modo_teste']:
                    self.logger.info("🧪 [MODO TESTE] Pausa entre lotes ignorada")
                else:
                    self.logger.info(f"\n⏳ Pausa entre lotes. Pressione Enter para continuar...")
                    input()

        self.gerar_relatorio_erros()
        self.mostrar_estatisticas()
        
        self.logger.info("\n🎉 Processamento concluído!")

if __name__ == "__main__":
    app = WhatsAppAuto()
    app.rodar()
