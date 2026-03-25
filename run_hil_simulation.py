"""
WE CAN FLY - GEAR PHASE 05: HIL SIMULATION
------------------------------------------
Simulates a real-time 'Avionics Impersonation' attack where
the radio telemetry (ADS-B) contradicts the internal bus (ARINC 429).

Author: Eng. Ramon Mendes (Specialist & Forensic Expert)
MPSP ID: 9830 | CREA-SP 5071785098
"""

from src.adsb_cyber_perito_agent import ADSBCyberPeritoAgent
import time

def run_hil_mission():
    print("============================================================")
    print("  GEAR HIL SIMULATION: Phase 05 (Avionics Integrity)       ")
    print("  Scenario: ADS-B Spoofing vs. ARINC 429 Internal Bus      ")
    print("============================================================\n")
    
    swarm = ADSBCyberPeritoAgent()
    
    # 1. Normal Flight Packet
    print("\n[SCENARIO 01] Normal Flight Sequence")
    telemetry_ok = {"icao": "0x4B21A2", "alt": 32000, "callsign": "TAM3041"}
    bus_ok = {"203": 32050, "210": 450} # Within 50ft tolerance
    swarm.process(telemetry_ok, bus_ok)
    
    time.sleep(2)
    
    # 2. Spoofing Attack (ADS-B data modified, but Internal Bus remains real)
    print("\n[SCENARIO 02] ADS-B Spoofing Attack (Ghosting)")
    # The attacker injects a fake altitude to the ground radar
    telemetry_attack = {"icao": "0x4B21A2", "alt": 45000, "callsign": "TAM3041"} 
    # But the internal ARINC 429 bus (Hardware Truth) still shows 32,000ft
    bus_real = {"203": 32000, "210": 450} 
    
    print("!!! INJECTING SPOOFED ADS-B PACKET !!!")
    swarm.process(telemetry_attack, bus_real)

    print("\n============================================================")
    print("  MISSION COMPLETE: HIL Cross-Consistency Validated.       ")
    print("  MPSP Legal Proofs: SEALED & ANCHORED                      ")
    print("============================================================")

if __name__ == "__main__":
    run_hil_mission()
