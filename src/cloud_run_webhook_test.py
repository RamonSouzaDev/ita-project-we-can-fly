import requests
import json
import time

# =========================================================================
# WE CAN FLY V2.0 - TESTE DE ARTILHARIA (CLOUD RUN)
# Envia a telemetria do Avião Pirata para a Nuvem de Produção.
# =========================================================================

CLOUD_RUN_URL = "https://ita-project-we-can-fly-git-650456447874.us-central1.run.app/ingest_telemetry"

# Simulacro do pacote JSON ADS-B que o SDR mandaria via rádio.
pacote_malicioso = {
  "flight_id": "GHOST-77",
  "mac_address": "00:1A:2B:3C:4D:5E",
  "altitude_ft": 35000,
  "kinematic_anomaly_score": 0.98,
  "origin": "Simulador de Ataque do Terminal Windows"
}

print(f"============================================================")
print(f"📡 PREPARANDO DISPARO EM ALTA ÓRBITA PARA O CLOUD RUN")
print(f"Alvo: {CLOUD_RUN_URL}")
print(f"============================================================")

print("\n1. Injetando dados anômalos JSON pela Internet...")
print(json.dumps(pacote_malicioso, indent=2))
time.sleep(1)

try:
    print("\n2. Disparando POST Request... (O Gemini da Nuvem vai raciocinar)")
    start_time = time.time()
    
    headers = {"Content-Type": "application/json"}
    
    # POST público enviando o JSON malicioso para a API
    response = requests.post(CLOUD_RUN_URL, json=pacote_malicioso, headers=headers)
    
    end_time = time.time()
    
    print(f"\n3. Resposta do Quartel General (Status {response.status_code}) recebida em {end_time - start_time:.2f} segundos!")
    
    if response.status_code == 200:
        resposta_json = response.json()
        print("\n🏆 RESULTADO MILITAR DO AGENTE:")
        print(json.dumps(resposta_json, indent=4, ensure_ascii=False))
        
        if "Ação Extrema Autônoma" in str(resposta_json.get("status")):
            print("\n🚨 SUCESSO ABSOLUTO TRL-9: O Vertex AI capturou sua URL de produção e acionou a Defesa Autônoma do Firewall via Cloud Run remotamente!")
    else:
        print(f"\n⚠️ Falha na API. O Servidor respondeu:")
        print(response.text)
        print("\nVerifique se a barra verde do Google Cloud 'Implantando do Repositório' já deu como CONCLUÍDO na aba.")

except requests.exceptions.ConnectionError:
    print("\n❌ ERRO DE CONEXÃO: O servidor Cloud Run pode estar subindo ainda ou o link está errado.")
except Exception as e:
    print(f"\n❌ ERRO DESCONHECIDO DE PYTHON: {e}")
