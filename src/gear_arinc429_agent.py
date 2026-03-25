"""
WE CAN FLY - GEAR PHASE 05: ARINC 429 HIL (HARDWARE-IN-THE-LOOP)
---------------------------------------------------------------
Simulates the monitoring of a physical ARINC 429 avionics bus.
Decodes Label 203 (Altitude) and Label 210 (Velocity) to verify
cross-consistency with ADS-B data.

Author: Eng. Ramon Mendes (Specialist & Forensic Expert)
MPSP ID: 9830 | CREA-SP 5071785098
"""

from src.gear_adk_base import GEARBaseAgent
import random
import time

class GEARArinc429Agent(GEARBaseAgent):
    """
    Decodes and validates ARINC 429 bus data for cross-platform
    consistency checks (ADS-B vs. Avionics).
    """
    def __init__(self, agent_id: str = "ARINC_429_BUS_MONITOR"):
        super().__init__(agent_id)
        self.log("ARINC 429 HIL Layer Active. Monitoring Labels 203, 204, 210.")

    def decode_word(self, label: str, raw_value: float):
        """
        Simulates decoding an ARINC 429 32-bit word.
        Label 203: Pressure Altitude
        Label 210: True Airspeed
        """
        # In a real scenario, this would involve bitwise shifts and PARITY checks.
        return {
            "label": label,
            "value": raw_value,
            "unit": "ft" if label == "203" else "knots",
            "state": "VALID" if random.random() > 0.01 else "FAILURE"
        }

    def process(self, bus_data: dict):
        """
        Processes a block of ARINC 429 bus data.
        """
        results = []
        for label, val in bus_data.items():
            decoded = self.decode_word(label, val)
            results.append(decoded)
            
        return results

    def verify_consistency(self, adsb_telemetry: dict, arinc_data: dict) -> bool:
        """
        CRITICAL HIL TASK: Verify if ADS-B Altitude matches ARINC 203.
        Max allowed discrepancy for TRL-9: 250ft.
        """
        adsb_alt = adsb_telemetry.get("alt", 0)
        arinc_alt = arinc_data.get("203", 0)
        
        diff = abs(adsb_alt - arinc_alt)
        
        if diff > 250:
            self.log(f"HIL INCONSISTENCY DETECTED! ADS-B: {adsb_alt}ft | ARINC 203: {arinc_alt}ft.", "CRITICAL")
            return False
        
        return True
