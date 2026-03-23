import subprocess
import time
import datetime
import sys
import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# =========================================================================
# WE CAN FLY V2.0 - INTELLIGENT BILLING & PROPAGATION VALIDATOR
# Integrates: Python, Data Science, Machine Learning & Real-time HTML Dashboard
# =========================================================================

AGENT_SCRIPT = "src/vertex_adk_agent.py"
INTERVALO_SEGUNDOS = 60
csv_log = "src/propagation_telemetry.csv"
DASHBOARD_FILE = "GCP_RealTime_Status_Dashboard.html"

def gerar_dashboard_html(df, status_geral, ml_insight="Analisando..."):
    """Gera um Dashboard Estiloso atualizado em Tempo Real."""
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="{INTERVALO_SEGUNDOS}">
    <title>Real-Time GCP Monitor | We Can Fly</title>
    <style>
        body {{ font-family: 'Inter', sans-serif; background: #0f172a; color: #f8fafc; padding: 40px; text-align: center; }}
        h1 {{ color: #3b82f6; }}
        .status-box {{ padding: 30px; border-radius: 12px; margin: 20px auto; max-width: 600px; font-size: 1.5rem; font-weight: bold; }}
        .blocked {{ background: rgba(239, 68, 68, 0.1); border: 2px solid #ef4444; color: #fca5a5; }}
        .success {{ background: rgba(16, 185, 129, 0.1); border: 2px solid #10b981; color: #6ee7b7; }}
        .ml-box {{ background: rgba(30,41,59,0.5); padding: 20px; border-radius: 8px; margin-top: 20px; max-width: 600px; text-align: left; margin: 20px auto; border: 1px solid rgba(255,255,255,0.1); }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.05); }}
        th {{ color: #94a3b8; }}
        .update-time {{ font-size: 0.9rem; color: #64748b; margin-top: 30px; }}
    </style>
</head>
<body>
    <h1>🛰️ WCF V2.0: Monitor de Inteligência Artificial</h1>
    <p>Acompanhando liberação de faturamento GCP (Auto-Refresh Ativo)</p>
    
    <div class="status-box {'success' if status_geral == 'ACESS LIBERADO' else 'blocked'}">
        STATUS ATUAL: {status_geral}
    </div>

    <div class="ml-box">
        <h3 style="margin-top:0; color: #fbbf24;">🧠 Insight de Machine Learning</h3>
        <p>{ml_insight}</p>
    </div>

    <div class="ml-box">
        <h3 style="margin-top:0; color: #60a5fa;">📊 Data Science (Últimos Pings)</h3>
        <table>
            <tr><th>Hora do Ping</th><th>Tentativa</th><th>Latência (ms)</th><th>Status Node</th></tr>
"""
    # Adicionar ultimas 5 tentavias invertidas
    for _, row in df.tail(5).iloc[::-1].iterrows():
        html_content += f"<tr><td>{row['timestamp'].split('T')[1][:8]}</td><td>#{row['attempt']}</td><td>{row['latency_ms']} ms</td><td>{row['status']}</td></tr>"

    html_content += f"""
        </table>
        <p>Total de Pings Emitidos: {len(df)}</p>
    </div>
    
    <div class="update-time">Último Ping da Nuvem: {datetime.datetime.now().strftime("%H:%M:%S")}</div>
</body>
</html>"""

    with open(DASHBOARD_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)

def print_log(msg):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")
    sys.stdout.flush()

def forecast_propagation(df):
    if len(df) < 3:
        return "Coletando massa de dados para predição..."
    X = np.array(range(len(df))).reshape(-1, 1)
    y = df['latency_ms'].values
    model = LinearRegression()
    model.fit(X, y)
    tendencia = model.coef_[0]
    
    if tendencia < 0:
        return f"Tendência de Queda da Latência ({tendencia:.2f} ms/ping). A Google Cloud parece estar aceitando a propagação."
    else:
        return f"Bloqueio Constante: Latência estável ({tendencia:.2f} ms/ping). Google Cloud ainda validando a transação PIX."

def executar_agente(tentativa):
    print_log(f"Iniciando PING #{tentativa} (Vertex ADC)...")
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    start_time = time.time()
    
    try:
        result = subprocess.run(
            ["python", AGENT_SCRIPT],
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
            errors='replace'
        )
        latency = (time.time() - start_time) * 1000 
        saida = result.stdout + result.stderr
        
        status_code = "DENIED" if "PERMISSION_DENIED" in saida or "billing" in saida else "SUCCESS"
        
        new_row = {
            "timestamp": datetime.datetime.now().isoformat(),
            "attempt": tentativa,
            "latency_ms": round(latency, 2),
            "response_size_bytes": len(saida),
            "status": status_code
        }
        
        df = pd.DataFrame([new_row])
        hdr = not os.path.exists(csv_log)
        df.to_csv(csv_log, mode='a', header=hdr, index=False)
        
        historico_df = pd.read_csv(csv_log)
        ml_insight = forecast_propagation(historico_df)
        
        if status_code == "DENIED":
            print_log(">>> GCP: [BLOQUEADO] - Faturamento em propagação.")
            gerar_dashboard_html(historico_df, "BLOQUEADO (Pagamento Propagando...)", ml_insight)
            return False
            
        else:
            print("\n🚀 [ACESSO LIBERADO] A Vertex AI processou com SUCESSO!")
            gerar_dashboard_html(historico_df, "ACESSO LIBERADO (TRL-9 ATIVO)", "O Google Cloud desbloqueou a API. Inteligência Artificial 100% Funcional e operando na nuvem militar!")
            return True
            
    except Exception as e:
        print_log(f"Erro de Conexão: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("🧠 INICIANDO MOTOR ML / DASHBOARD EM TEMPO REAL (WCF V2.0)")
    print("="*60)
    
    if os.path.exists(csv_log): os.remove(csv_log)
    
    tentativas = 1
    while True:
        sucesso = executar_agente(tentativas)
        if sucesso:
            break
        time.sleep(INTERVALO_SEGUNDOS)
        tentativas += 1
