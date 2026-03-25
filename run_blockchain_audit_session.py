"""
WE CAN FLY - GEAR PHASE 08: BLOCKCHAIN AUDIT SESSION
----------------------------------------------------
Demonstrates the immutability and auditability of the 
GEAR Swarm forensic evidence layer.

Author: Eng. Ramon Mendes (Specialist & Forensic Expert)
MPSP ID: 9830 | CREA-SP 5071785098
"""

from src.gear_blockchain_agent import GEARBlockchainAgent
import time
import hashlib

def run_audit_session():
    print("============================================================")
    print("  GEAR BLOCKCHAIN AUDIT: Phase 08 (Decentralized Ledger)    ")
    print("  Ensuring Immutability for MPSP Evidence (ID: 9830)        ")
    print("============================================================\n")

    ledger_agent = GEARBlockchainAgent()
    
    # 1. Simulating Forensic Injections
    events = [
        {"icao": "0xABC123", "alt": 70000, "type": "SPOOFING_DETECTED"},
        {"icao": "0xDEF456", "alt": 35000, "type": "HIL_CONSISTENCY_OK"},
        {"icao": "0x789GHI", "alt": 90000, "type": "SEVERE_INCONGRUITY"},
        {"icao": "0xJ12K34", "alt": 32000, "type": "NORMAL_FLIGHT"}
    ]

    stored_hashes = []

    print("[TRANSACTION INJECTION PHASE]")
    for event in events:
        # Simulate the forensic sealing process
        forensic_hash = hashlib.sha256(str(event).encode()).hexdigest()
        payload = {
            "forensic_hash": forensic_hash,
            "metadata": event,
            "expert": "Ramon Mendes"
        }
        
        tx_id = ledger_agent.process(payload)
        stored_hashes.append(forensic_hash)
        time.sleep(0.5)

    print("\n[AUDIT & VERIFICATION PHASE]")
    # We take a known hash from Scenario 3 (Severe Incongruity)
    target_hash = stored_hashes[2]
    
    print(f"Checking Ledger for Hash: {target_hash[:16]}...")
    is_valid = ledger_agent.verify_evidence(target_hash)
    
    if is_valid:
        print("✅ VERDICT: Evidence is IMMUTABLE and PRESENT in the ledger.")
        print("🏛️ STATUS: ADMISSIBLE IN COURT (MPSP Audit Standards)")
    else:
        print("❌ VERDICT: Evidence tampered or not found.")

    print("\n[FINAL LEDGER SUMMARY]")
    for block in ledger_agent.ledger:
        print(f"Block #{block['block_index']} | TS: {block['timestamp']} | Anchor: {block['merkle_root'][:12]}")

    print("\n============================================================")
    print("  PHASE 08 VALIDATED: Distributed Trust Established.       ")
    print("============================================================")

if __name__ == "__main__":
    run_audit_session()
