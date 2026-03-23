# ✈️ We Can Fly V2.0 | Aeronautic Cybersecurity & AI
**Trilha de Defesa Cibernética do DECEA/FAB - Nível TRL-9**

## 🌐 Visão Global (Arquitetura Atualizada)
Este repositório consolida o **Motor Web de Inteligência Artificial** para a defesa do espaço aéreo. 
A infraestrutura migrou do ambiente local de simulação para o **Google Cloud Platform (GCP)** utilizando o protocolo *Application Default Credentials (ADC)* e APIs TRL-9.

O sistema autônomo é capaz de monitorar sinais ADS-B (físicos via Dump1090) e utilizar a base de dados Vertex AI Gemini-2.5-Flash para analisar anomalias físicas complexas e tomar decisões de bloqueio em milissegundos.

## 🚀 Como Funciona o Agente ADK na Nuvem
1. Um transponder "malicioso" (ex: MAC `00:1A:2B:3C:4D:5E`) envia posições cinemáticas impossíveis para uma aeronave comercial.
2. O servidor ingestor intercepta essa JSON.
3. A requisição HTTP REST vai para o nosso servidor **Cloud Run** (`/ingest_telemetry`).
4. O *Google Agent Development Kit (ADK)* analisa a anomalia via API Gemini TRL-9.
5. Em casos de `kinematic_anomaly_score` massivo, a ferramenta militar `block_sdr_port` é invocada remotamente pela Vertex AI.

## 🛠️ Stack Tecnológica
* **Motor Cognitivo:** Google Vertex AI (Gemini 2.5 Flash / Pro)
* **Backend Autônomo:** Python 3.11, Flask, Google GenAI SDK
* **Automação de Infra:** Dockerfile + Google Cloud Run (Serverless CI/CD)
* **Data Science Forense:** Pandas, Scikit-learn (Validação de Dispersão e Ping Loggings)

## 🐳 Desdobramento (Deploy) em Produção
O projeto foi redesenhado para hospedar CI/CD nativo com o **GitHub**.

1. Atualize este código na ramificação `main` ou `development`.
2. O Google Cloud Build interceptará o commit.
3. O `Dockerfile` criará a imagem imutável de defesa em Container Linux.
4. O Cloud Run substituirá as instâncias sem derrubar a API (`Zero Downtime`).

## 📁 Estrutura do Código
* `/src/vertex_adk_agent.py`: Script autônomo mestre para validar a permissão Vertex usando ADC.
* `/src/billing_validator_cron.py`: Algoritmo de metrificação Data Science e Machine Learning que monitora os backends do Google.
* `/src/agent_cloud_engine.py`: A Web-API Serverless final enviada ao Cloud Run.
* `/Dockerfile`: Mapa de empacotamento militar na nuvem.

## ⚖️ Conformidade e Cadeia de Custódia
* **ISO 27001:** Hashing de SHA-256 no log de ações do Agente no Firewall para non-repudiation.
* Projetos Segregados via GitHub Connector sem exposição de Credentials/Chaves KMS ativas no repositório.
