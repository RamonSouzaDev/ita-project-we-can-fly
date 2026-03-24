import os
import json
import hashlib
from datetime import datetime

# =========================================================================
# WE CAN FLY V2.0 - INTEGRAÇÃO NATIVA VERTEX AI (GCP) VIA TERMINAL
# Chamada Real de Nuvem via SDK Oficial de Python
# =========================================================================

# NOTA: Requer `pip install google-cloud-aiplatform` e autenticação gcloud.
try:
    import vertexai
    from vertexai.generative_models import GenerativeModel, Part, SafetySetting
    VERTEX_AVAILABLE = True
except ImportError:
    VERTEX_AVAILABLE = False


class AgenteVertexNuvem:
    def __init__(self, project_id="ita-wecanfly-v2-dev", location="us-central1"):
        self.project_id = project_id
        self.location = location
        self.system_prompt = (
            "Você é um Agente de Segurança Aeronáutica Forense atuando na arquitetura 'We Can Fly'.\n"
            "OBJETIVO: Detectar e neutralizar tráfegos de 'Ghost Aircrafts' (Spoofing) através dos dados providos (ADS-B).\n"
            "REGRA 1: Não exclua dados vitais, apenas classifique-os como nível de risco (Risk Score).\n"
            "REGRA 2: Após detectar um ataque, emita um alerta gerando a chave AÇÃO: HASHSpoofing.\n"
            "REGRA 3: Não altere planos de voo ATC legítimos."
        )
        
        if VERTEX_AVAILABLE:
            try:
                vertexai.init(project=self.project_id, location=self.location)
                self.model = GenerativeModel("gemini-1.5-pro", system_instruction=[self.system_prompt])
                print("✔️ SDK do Google Vertex AI Nuvem Inicializado com Sucesso (gemini-1.5-pro).")
            except Exception as e:
                print(f"⚠️ Aviso: SDK Vertex instalado, mas falta autenticação GCP local: {e}")
                self.model = None
        else:
            print("⚠️ Aviso: Biblioteca `google-cloud-aiplatform` não encontrada no ambiente local Python.")
            self.model = None

    def gerar_hash_forense(self, log_dict):
        log_string = json.dumps(log_dict, sort_keys=True)
        return hashlib.sha256(log_string.encode('utf-8')).hexdigest()

    def enviar_para_VertexAI(self, pacote_adsb):
        print("\n======================================================")
        print(f"📡 Disparando Telemetria ADS-B para Nuvem VERTEX AI...")
        print("======================================================")
        
        prompt_tecnico = f"Analise este radar ADS-B recebido via SDR:\n{json.dumps(pacote_adsb)}"
        
        relatorio = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "flight_id": pacote_adsb["flight_id"]
        }
        
        if self.model:
            try:
                # Fazendo o ping real na Nuvem Google (Vertex AI Data Centers)
                resposta_nuvem = self.model.generate_content(prompt_tecnico)
                analise_texto = resposta_nuvem.text
                
                print("☁️ [NUVEM RETORNOU]:", analise_texto)
                
                if "Ghost" in analise_texto or "Spoofing" in analise_texto or "Risco" in analise_texto:
                    print("\n🚨 VERTEX AI DETECTOU ANOMALIA HÍBRIDA NAS NUVENS!")
                    relatorio["diagnostico_nuvem"] = "Spoofing Detectado pela IA do Google"
                    relatorio["hash_imutavel"] = self.gerar_hash_forense(relatorio)
                else:
                    relatorio["diagnostico_nuvem"] = "ATC Voo Seguro (Aprovado pela Vertex)"

                return relatorio
            except Exception as e:
                print(f"❌ Erro de Conexão com Vertex AI: {e}")
                
        else:
            print("❌ Falha de Recursos: Rodando sem SDK ativado. Use a simulação offline `terminal_agent_TRL9.py`.")
            return relatorio

if __name__ == "__main__":
    agente_gcp = AgenteVertexNuvem()
    
    # Testando Payload para a Nuvem
    pacote_hacker = {
        "flight_id": "GHOST-77",
        "mac_address": "00:1A:2B:3C:4D:5E",
        "altitude_ft": 35000,
        "kinematic_anomaly_score": 0.98,
        "origin": "SDR Terminal Local Python"
    }
    
    agente_gcp.enviar_para_VertexAI(pacote_hacker)
