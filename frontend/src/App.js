import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Send, Upload, Settings, Square, BarChart3, FileText, TrendingUp, Clock, CheckCircle, XCircle, Activity, Database, Layers, Terminal, Rocket, Target, ChevronRight } from 'lucide-react';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const API_URL = `${API_BASE_URL}/api`;

function App() {
  const [status, setStatus] = useState('idle');
  const [config, setConfig] = useState(null);
  const [logs, setLogs] = useState([]);
  const [statistics] = useState(null);
  const [activeView, setActiveView] = useState('overview');
  const [uploadedFile, setUploadedFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [isStarting, setIsStarting] = useState(false);
  const [isStopping, setIsStopping] = useState(false);

  useEffect(() => {
    fetchStatus();
    fetchConfig();
    const interval = setInterval(fetchStatus, 2000);
    return () => clearInterval(interval);
  }, []);

  const fetchStatus = async () => {
    try {
      const response = await axios.get(`${API_URL}/status`);
      setStatus(response.data.status);
      setLogs(response.data.logs || []);
    } catch (error) {
      console.error('Erro ao buscar status:', error);
    }
  };

  const fetchConfig = async () => {
    try {
      const response = await axios.get(`${API_URL}/config`);
      setConfig(response.data);
    } catch (error) {
      console.error('Erro ao buscar config:', error);
    }
  };

  const startCampaign = async () => {
    try {
      setIsStarting(true);
      await axios.post(`${API_URL}/start-campaign`, config);
      await fetchStatus();
    } catch (error) {
      console.error('Erro ao iniciar campanha:', error);
    } finally {
      setIsStarting(false);
    }
  };

  const stopCampaign = async () => {
    try {
      setIsStopping(true);
      await axios.post(`${API_URL}/stop-campaign`);
      await fetchStatus();
    } catch (error) {
      console.error('Erro ao parar campanha:', error);
    } finally {
      setIsStopping(false);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_URL}/upload-csv`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      setUploadedFile(response.data);
      
      const newConfig = { ...config, arquivo_leads: response.data.filepath };
      await axios.post(`${API_URL}/config`, newConfig);
      setConfig(newConfig);
      
    } catch (error) {
      console.error('Erro ao fazer upload:', error);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = async (e) => {
    e.preventDefault();
    setIsDragging(false);
    
    const file = e.dataTransfer.files[0];
    if (!file || !file.name.endsWith('.csv')) {
      alert('Por favor, selecione um arquivo CSV');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_URL}/upload-csv`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      setUploadedFile(response.data);
      
      const newConfig = { ...config, arquivo_leads: response.data.filepath };
      await axios.post(`${API_URL}/config`, newConfig);
      setConfig(newConfig);
      
    } catch (error) {
      console.error('Erro ao fazer upload:', error);
    }
  };

  const updateConfig = async (key, value) => {
    const newConfig = { ...config, [key]: value };
    setConfig(newConfig);
    await axios.post(`${API_URL}/config`, newConfig);
  };

  const getStatusInfo = () => {
    switch (status) {
      case 'running': return { color: '#10b981', label: 'Em Execução', icon: Activity };
      case 'completed': return { color: '#3b82f6', label: 'Concluído', icon: CheckCircle };
      case 'error': return { color: '#ef4444', label: 'Erro', icon: XCircle };
      case 'stopped': return { color: '#f59e0b', label: 'Parado', icon: Square };
      default: return { color: '#6b7280', label: 'Aguardando', icon: Clock };
    }
  };

  const statusInfo = getStatusInfo();
  const StatusIcon = statusInfo.icon;

  const menuItems = [
    { id: 'overview', icon: BarChart3, label: 'Visão Geral' },
    { id: 'upload', icon: Upload, label: 'Importar Dados' },
    { id: 'config', icon: Settings, label: 'Configurações' },
    { id: 'logs', icon: Terminal, label: 'Logs do Sistema' },
    { id: 'campaigns', icon: Target, label: 'Campanhas' },
    { id: 'analytics', icon: TrendingUp, label: 'Analytics' }
  ];

  const readinessChecks = [
    { label: 'Arquivo CSV importado', done: Boolean(uploadedFile) },
    { label: 'Modo teste desativado', done: Boolean(config && !config.modo_teste) },
    { label: 'WhatsApp Web pronto para conectar', done: status !== 'idle' }
  ];

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className={`sidebar ${sidebarCollapsed ? 'collapsed' : ''}`}>
        <div className="sidebar-header">
          <div className="logo-container">
            <div className="logo-icon">
              <Send size={24} />
            </div>
            {!sidebarCollapsed && (
              <div className="logo-text">
                <h1>NEXUS</h1>
                <span>Automation</span>
              </div>
            )}
          </div>
          <button 
            className="collapse-btn"
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
          >
            <ChevronRight size={20} />
          </button>
        </div>

        <nav className="sidebar-nav">
          {menuItems.map(item => (
            <button
              key={item.id}
              onClick={() => setActiveView(item.id)}
              className={`nav-item ${activeView === item.id ? 'active' : ''}`}
            >
              <item.icon size={20} />
              {!sidebarCollapsed && <span>{item.label}</span>}
            </button>
          ))}
        </nav>

        {!sidebarCollapsed && (
          <div className="sidebar-footer">
            <div className="status-indicator">
              <div className="status-dot" style={{ backgroundColor: statusInfo.color }} />
              <span>{statusInfo.label}</span>
            </div>
          </div>
        )}
      </aside>

      {/* Main Content */}
      <main className="main-content">
        {/* Top Bar */}
        <header className="top-bar">
          <div className="top-bar-left">
            <h2 className="page-title">
              {menuItems.find(item => item.id === activeView)?.label}
            </h2>
            <p className="page-subtitle">Gerenciamento de campanhas WhatsApp</p>
          </div>
          
          <div className="top-bar-right">
            <div className="action-buttons">
              {status !== 'running' ? (
                <button onClick={startCampaign} className="btn-primary" disabled={isStarting}>
                  <Rocket size={18} />
                  <span>{isStarting ? 'Abrindo WhatsApp...' : 'Iniciar Campanha'}</span>
                </button>
              ) : (
                <button onClick={stopCampaign} className="btn-danger" disabled={isStopping}>
                  <Square size={18} />
                  <span>{isStopping ? 'Parando...' : 'Parar Campanha'}</span>
                </button>
              )}
            </div>
          </div>
        </header>

        {/* Content Area */}
        <div className="content-area">
          {activeView === 'overview' && (
            <div className="overview-shell">
              <section className="hero-panel">
                <div className="hero-copy">
                  <span className="eyebrow">Fluxo de campanha</span>
                  <h3>Conecte, confirme e envie com menos ruído</h3>
                  <p>Esta tela foi reorganizada para guiar o processo de forma objetiva: importar os leads, validar a configuração e iniciar a campanha com o WhatsApp Web.</p>
                  <div className="hero-actions">
                    {status !== 'running' ? (
                      <button onClick={startCampaign} className="btn-primary" disabled={isStarting}>
                        <Rocket size={18} />
                        <span>{isStarting ? 'Abrindo WhatsApp...' : 'Iniciar Campanha'}</span>
                      </button>
                    ) : (
                      <button onClick={stopCampaign} className="btn-danger" disabled={isStopping}>
                        <Square size={18} />
                        <span>{isStopping ? 'Parando...' : 'Parar Campanha'}</span>
                      </button>
                    )}
                    <button onClick={() => setActiveView('config')} className="btn-secondary">
                      <Settings size={18} />
                      <span>Ajustar Configuração</span>
                    </button>
                  </div>
                  <div className="status-pill" style={{ borderColor: `${statusInfo.color}55`, color: statusInfo.color }}>
                    <StatusIcon size={16} />
                    <span>{statusInfo.label}</span>
                  </div>
                </div>

                <div className="hero-side-card">
                  <h4>Checklist de prontidão</h4>
                  <ul className="readiness-list">
                    {readinessChecks.map((item) => (
                      <li key={item.label} className={`readiness-item ${item.done ? 'done' : ''}`}>
                        {item.done ? <CheckCircle size={16} /> : <Clock size={16} />}
                        <span>{item.label}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </section>

              <section className="overview-cards">
                <div className="info-card">
                  <div className="mini-stat-icon success">
                    <CheckCircle size={20} />
                  </div>
                  <div>
                    <span className="mini-stat-value">{statistics?.campaign_state?.sent || 0}</span>
                    <span className="mini-stat-label">Enviados</span>
                  </div>
                </div>

                <div className="info-card">
                  <div className="mini-stat-icon error">
                    <XCircle size={20} />
                  </div>
                  <div>
                    <span className="mini-stat-value">{statistics?.campaign_state?.failed || 0}</span>
                    <span className="mini-stat-label">Falhas</span>
                  </div>
                </div>

                <div className="info-card">
                  <div className="mini-stat-icon info">
                    <Activity size={20} />
                  </div>
                  <div>
                    <span className="mini-stat-value">{uploadedFile?.total_rows || 0}</span>
                    <span className="mini-stat-label">Leads carregados</span>
                  </div>
                </div>
              </section>

              <section className="guide-grid">
                <div className="guide-card">
                  <h4>Antes de iniciar</h4>
                  <ol>
                    <li>Importe o CSV na aba de dados.</li>
                    <li>Desative o modo teste para envio real.</li>
                    <li>Clique em “Iniciar Campanha”.</li>
                    <li>Escaneie o QR Code no WhatsApp Web.</li>
                  </ol>
                </div>

                <div className="guide-card">
                  <h4>O que esperar</h4>
                  <ul>
                    <li>A primeira mensagem pode demorar cerca de 1 minuto.</li>
                    <li>O sistema envia em lotes de 20 mensagens com pausas.</li>
                    <li>Você acompanha o progresso e os logs em tempo real.</li>
                  </ul>
                </div>
              </section>
            </div>
          )}

          {activeView === 'upload' && (
            <div className="upload-view">
              <div className="upload-container">
                <div 
                  className={`upload-zone ${isDragging ? 'dragging' : ''}`}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                >
                  <div className="upload-content">
                    <div className="upload-icon">
                      <Upload size={64} />
                    </div>
                    <h3>Arraste seu arquivo CSV aqui</h3>
                    <p>ou clique para selecionar</p>
                    <input
                      type="file"
                      accept=".csv"
                      onChange={handleFileUpload}
                      className="hidden"
                      id="file-upload"
                    />
                    <label htmlFor="file-upload" className="upload-btn">
                      Selecionar Arquivo
                    </label>
                  </div>
                </div>

                {uploadedFile && (
                  <div className="file-preview">
                    <div className="file-header">
                      <Database size={24} />
                      <h3>Arquivo Carregado</h3>
                    </div>
                    <div className="file-stats">
                      <div className="file-stat">
                        <span className="stat-label">Nome</span>
                        <span className="stat-value">{uploadedFile.filename}</span>
                      </div>
                      <div className="file-stat">
                        <span className="stat-label">Total de Leads</span>
                        <span className="stat-value">{uploadedFile.total_rows}</span>
                      </div>
                      <div className="file-stat">
                        <span className="stat-label">Colunas</span>
                        <span className="stat-value">{uploadedFile.columns.length}</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeView === 'config' && config && (
            <div className="config-view">
              <div className="config-hero">
                <div>
                  <span className="eyebrow">Configuração</span>
                  <h3>Defina o ritmo do envio antes de começar</h3>
                  <p>Valores mais lentos reduzem o risco de bloqueios e conferem mais controle no processo.</p>
                </div>
                <div className="config-warning">
                  <Settings size={18} />
                  <span>Desative o modo teste para enviar mensagens reais.</span>
                </div>
              </div>

              <div className="config-grid">
                <div className="config-card">
                  <h3>Envio e ritmo</h3>
                  <div className="config-form">
                    <div className="form-group">
                      <label>Tamanho do lote</label>
                      <input
                        type="number"
                        value={config.lote_tamanho}
                        onChange={(e) => updateConfig('lote_tamanho', parseInt(e.target.value))}
                      />
                    </div>
                    <div className="form-group">
                      <label>Tempo mínimo entre mensagens (s)</label>
                      <input
                        type="number"
                        value={config.tempo_entre_msg_min}
                        onChange={(e) => updateConfig('tempo_entre_msg_min', parseInt(e.target.value))}
                      />
                    </div>
                    <div className="form-group">
                      <label>Tempo máximo entre mensagens (s)</label>
                      <input
                        type="number"
                        value={config.tempo_entre_msg_max}
                        onChange={(e) => updateConfig('tempo_entre_msg_max', parseInt(e.target.value))}
                      />
                    </div>
                  </div>
                </div>

                <div className="config-card">
                  <h3>Operação geral</h3>
                  <div className="config-form">
                    <div className="form-group">
                      <label>DDI padrão</label>
                      <input
                        type="text"
                        value={config.ddi_padrao}
                        onChange={(e) => updateConfig('ddi_padrao', e.target.value)}
                      />
                    </div>
                    <div className="form-group checkbox">
                      <label className="checkbox-label">
                        <input
                          type="checkbox"
                          checked={config.modo_teste}
                          onChange={(e) => updateConfig('modo_teste', e.target.checked)}
                        />
                        <span>Modo teste</span>
                      </label>
                      <p className="checkbox-desc">Mantém a campanha em execução apenas para validação sem envio real.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeView === 'logs' && (
            <div className="logs-view">
              <div className="logs-container">
                <div className="logs-header">
                  <Terminal size={24} />
                  <div>
                    <h3>Logs do Sistema</h3>
                    <p>Acompanhe cada etapa do processo em tempo real.</p>
                  </div>
                </div>
                <div className="logs-content">
                  {logs.length === 0 ? (
                    <div className="empty-logs">
                      <FileText size={48} />
                      <p>Nenhum log disponível</p>
                    </div>
                  ) : (
                    logs.map((log, idx) => (
                      <div key={idx} className="log-entry">
                        <span className="log-time">{log.timestamp}</span>
                        <span className="log-message">{log.message}</span>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>
          )}

          {activeView === 'campaigns' && (
            <div className="campaigns-view">
              <div className="campaigns-header">
                <Target size={24} />
                <h3>Campanhas</h3>
              </div>
              <div className="campaigns-content">
                <div className="empty-campaigns">
                  <Layers size={48} />
                  <p>Nenhuma campanha configurada</p>
                  <button onClick={() => setActiveView('upload')} className="btn-secondary">
                    Criar Nova Campanha
                  </button>
                </div>
              </div>
            </div>
          )}

          {activeView === 'analytics' && (
            <div className="analytics-view">
              <div className="analytics-header">
                <TrendingUp size={24} />
                <h3>Analytics</h3>
              </div>
              <div className="analytics-content">
                <div className="empty-analytics">
                  <BarChart3 size={48} />
                  <p>Dados de analytics em desenvolvimento</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
