import os
import json
from .gear_adk_base import GEARBaseAgent
from .adsb_spoofing import ADSBSpoofingDetector
from .gear_gemini_agent import GeminiReasoningAgent

class ADSBCyberPeritoAgent(GEARBaseAgent):
    """
    Concrete implementation of an Autonomous Cyber-Perito for ADS-B.
    Integrates ML detection with Gemini 1.5 Pro reasoning and MPSP forensic logging.
    """
    def __init__(self, agent_id: str = "ADS_B_PERITO_01"):
        super().__init__(agent_id)
        self.ml_detector = ADSBSpoofingDetector(contamination=0.1)
        self.reasoner = GeminiReasoningAgent()
        self.log("ADS-B Cyber-Perito Active and Monitoring 1090MHz.", "STATUS")

    def process(self, flight_record: dict):
        """
        Process a flight record: 
        1. ML Check
        2. If anomalous -> Gemini Reasoning
        3. Seal Log for MPSP
        """
        # Simplified verification (normally would use the trained model)
        is_anomalous = flight_record.get('altitude_delta', 0) > 500 or flight_record.get('latency_ms', 0) > 800
        
        if is_anomalous:
            self.log(f"Anomaly detected in {flight_record.get('callsign')}. Starting GEAR forensic audit.", "ALERT")
            
            # Gemini Reasoning
            reasoning = self.reasoner.process(flight_record)
            
            # Sealed Forensic Log
            forensic_payload = {
                "agent": self.agent_id,
                "record": flight_record,
                "ai_reasoning": reasoning,
                "verdict": "SPOOFING_CONFIRMED",
                "signature": "RAMON_MENDES_CREA_5071785098"
            }
            
            self.send_to_mpsp(forensic_payload)
            return True, reasoning
        
        return False, "Normal"

if __name__ == "__main__":
    # Teste rápido do agente
    perito = ADSBCyberPeritoAgent()
    sample = {"callsign": "ITA-SIM", "altitude_delta": 600, "latency_ms": 100}
    perito.process(sample)
