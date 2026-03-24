from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool

# Cybersecurity Aeronautic Forensic Agent (TRL-9 We Can Fly Base)
# Replaced generic agent.py with MPSP & CREA-SP compliant AI

we_can_fly_forensic_agent = LlmAgent(
  name='Agente_Forense_ADSB_TRL9',
  model='gemini-3-flash-preview',
  description=(
      'Motor autônomo MPSP/CREA-SP para caçar táticas de Ghost Aircraft via data lake. Garante auditoria criptográfica e cadeia de custódia.'
  ),
  sub_agents=[],
  instruction=(
      "Você é um Agente de Segurança Aeronáutica Forense atuando na arquitetura 'We Can Fly'.\n\n"
      "OBJETIVO: Detectar e neutralizar tráfegos de 'Ghost Aircrafts' (Spoofing) através dos dados providos (ADS-B).\n"
      "REGRA 1: Não exclua dados vitais, apenas classifique-os como nível de risco (Risk Score).\n"
      "REGRA 2: Após detectar um ataque, emita um payload de alerta gerando um Hash SHA-256 no banco imutável.\n"
      "REGRA 3: Não altere planos de voo ATC legítimos."
  ),
  tools=[
      # OpenAPI or Custom Serverless tools should be appended here.
      # Exemplo genérico mantido para grounding (Google Search Tool):
      GoogleSearchTool()
  ],
)

root_agent = LlmAgent(
  name='We_Can_Fly_Controller',
  model='gemini-3-flash-preview',
  description=(
      'Controlador primário da suíte militar We Can Fly TRL-9.'
  ),
  sub_agents=[],
  instruction='Sua função é rotear eventos de simulação de voo (SDR) para o Agente_Forense_ADSB_TRL9 e aguardar a classificação (Risk Score).',
  tools=[
    agent_tool.AgentTool(agent=we_can_fly_forensic_agent)
  ],
)
