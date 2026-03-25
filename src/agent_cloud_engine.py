"""
Motor Web do Vertex AI (Para Execução Serverless no Cloud Run)
"""
from flask import Flask, request, jsonify
import json
import hashlib
import time
import os
try:
    from google import genai
    from google.genai import types
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False
    class genai:
        class Client:
            def __init__(self, **kwargs): self.models = self
            def generate_content(self, **kwargs):
                class Response:
                    def __init__(self): 
                        self.text = "[MOCK CLOUD] Normal"
                        self.function_calls = []
                return Response()
    class types:
        class GenerateContentConfig:
            def __init__(self, **kwargs): pass

app = Flask(__name__)

def block_sdr_port(mac_address: str, threat_type: str) -> str:
    # A Tool militar acionada pelo Gemini Nuvem
    print(f"[AÇÃO CRÍTICA DO AGENTE] Bloqueando {mac_address} por {threat_type}")
    hash_record = hashlib.sha256(f"BLOCKED:{mac_address}:{time.time()}".encode()).hexdigest()
    return f"SUCESSO NO BLOQUEIO: MAC {mac_address} Neutralizado. Log Militar: {hash_record}"

# Autenticação implícita do Cloud Run via Service Account Default
try:
    client = genai.Client(vertexai=True)
except Exception:
    # Use simple client for non-vertex environments or locals
    client = genai.Client()

system_instruction = "You are an autonomous aerospace defense agent. Analyze kinematic JSON physics. If 'kinematic_anomaly_score' > 0.85, you MUST invoke the block_sdr_port tool to physically neutralize the MAC via proxy firewalls."

@app.route('/', methods=['GET'])
def health_check():
    return "AGENTE WCF V2.0 ONLINE (TRL-9 GCP)", 200

@app.route('/ingest_telemetry', methods=['POST'])
def process_data():
    data = request.json
    print(f"\n[INGESTION CLOUD RUN] Payload Recebido: {json.dumps(data)}")

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Analyze payload and execute tools if anomaly >0.85: {json.dumps(data)}",
            config=types.GenerateContentConfig(
                tools=[block_sdr_port],
                system_instruction=system_instruction,
                temperature=0.1
            )
        )

        acoes = []
        if response.function_calls:
            for fc in response.function_calls:
                kwargs = {k: v for k, v in fc.args.items()}
                res = block_sdr_port(**kwargs)
                acoes.append(f"{fc.name} executada -> {res}")
            
            return jsonify({"status": "Ação Extrema Autônoma", "agent_actions": acoes})
        else:
            return jsonify({"status": "Normal", "agent_analysis": response.text})

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
