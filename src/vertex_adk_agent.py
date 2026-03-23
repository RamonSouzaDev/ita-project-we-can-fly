"""
We Can Fly V2.0 - GCP Vertex AI Agent (TRL-9)
Conectado e Autenticado diretamente ao seu Projeto Google Cloud!
"""
from google import genai
from google.genai import types
import json
import hashlib
import time
import os

# Força o SDK a usar as credenciais do seu login `gcloud auth application-default login`
os.environ["GOOGLE_CLOUD_PROJECT"] = "ita-wecanfly-v2-dev"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"

def block_sdr_port(mac_address: str, threat_type: str) -> str:
    """Tool: Bloqueia MAC malicioso no proxy SDR e gera Hash Militar."""
    print(f"\n[🛠️ TOOL CLOUD EXECUTED] Firewall block request for MAC: {mac_address}. Reason: {threat_type}")
    time.sleep(1)
    hash_record = hashlib.sha256(f"BLOCKED:{mac_address}:{time.time()}".encode()).hexdigest()
    return f"ACTION SUCCESS: MAC {mac_address} neutralized. Forensic Hash: {hash_record}"

# Inicia o Cliente Vertex AI apontando para o seu projeto recém-criado
client = genai.Client(vertexai=True, project="ita-wecanfly-v2-dev", location="us-central1")

suspicious_payload = {
    "flight_id": "GHOST-77",
    "mac_address": "00:1A:2B:3C:4D:5E",
    "altitude_ft": 35000,
    "kinematic_anomaly_score": 0.98
}

if __name__ == "__main__":
    print("="*60)
    print(" ☁️ WE CAN FLY V2.0: VERTEX AI AGENT (CLOUDSYNC ACTIVE)")
    print("="*60)
    print("\n[INGESTION] Receiving data from dump1090 SDR...")
    print(json.dumps(suspicious_payload, indent=2))

    # A Instrução base do Agente Autônomo
    system_instruction = "You are an autonomous aerospace defense agent. Analyze the physics of the telemetry. If 'kinematic_anomaly_score' > 0.85, you MUST unconditionally invoke the block_sdr_port tool to neutralize the MAC address and then report the outcome."

    print("\n[Vertex AI] Uploading Telemetry to Google Cloud for reasoning...")
    
    # Executa a IA diretamente na Nuvem corporativa do seu projeto ita-wecanfly-v2-dev
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Analyze this payload and take autonomous action if needed based on your system instructions: {json.dumps(suspicious_payload)}",
            config=types.GenerateContentConfig(
                tools=[block_sdr_port],
                system_instruction=system_instruction,
                temperature=0.1
            )
        )

        print("\n" + "="*50)
        
        # O modelo Gemini pode decidir chamar a Tool
        if response.function_calls:
            print("[CLOUD DECISION] Gemini decided to execute a Tool!")
            for fc in response.function_calls:
                # Simulando a execução da ferramenta que o Gemini na nuvem pediu
                kwargs = {k: v for k, v in fc.args.items()}
                result = block_sdr_port(**kwargs)
                print(f"[REACTION OVERRIDE] {result}")
        else:
            print(f"[FINAL CLOUD EVENT REPORT]\n{response.text}")
            
    except Exception as e:
        print(f"\n[ERRO DE CONEXÃO] A API GCP retornou uma falha de permissão ou configuração:\n{e}")

    print("="*60)
