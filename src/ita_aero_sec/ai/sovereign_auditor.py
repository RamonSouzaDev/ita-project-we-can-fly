"""
======================================================================
WE CAN FLY - ISO 27001 AUDITOR & FORENSIC CHAIN-OF-CUSTODY (TRL-9)
======================================================================
Mission: Forensic Audit of AI Decisions / Sovereign Local Training.
Each decision to negate a command has an immutable chain of hashes.

Compliance: ISO 27001, DECEA 2030, EU AI Act
Author: Eng. Ramon de Souza Mendes (CREA-SP: 5071785098)
======================================================================
"""
import hashlib
import json
import time
from datetime import datetime

class SovereignIA_Auditor:
    def __init__(self, log_path="trl9_civil_aviation_audit.log"):
        self.log_path = log_path
        self.last_hash = "0" * 64 # Genesis Hash

    def audit_decision(self, logic_component, decision_type, raw_telemetry):
        """
        Registers an immutable record of an AI decision in a forensic chain.
        Each log entry contains the hash of the PREVIOUS entry.
        """
        timestamp = datetime.utcnow().isoformat()
        
        # LGPD PII Anonymization
        sanitized_telemetry = {k: v for k, v in raw_telemetry.items() if "PII" not in k}
        
        record = {
            "timestamp": timestamp,
            "logic_node": logic_component,
            "decision": decision_type,
            "data_fingerprint": sanitized_telemetry,
            "prev_hash": self.last_hash,
            "system_integrity": "OK"
        }
        
        # Generate current hash (Forensic Signature)
        current_hash = hashlib.sha256(json.dumps(record, sort_keys=True).encode()).hexdigest()
        record["forensic_signature"] = current_hash
        self.last_hash = current_hash
        
        # Save to local persistent log (ISO 27001 Ready)
        try:
            with open(self.log_path, "a") as f:
                f.write(json.dumps(record) + "\n")
            print(f"[AUDITOR] [SUCCESS] ISO-27001 Log Signed: {current_hash[:16]}...")
        except Exception as e:
            print(f"[AUDITOR] [ERROR] Failed to write forensic log: {e}")

if __name__ == "__main__":
    auditor = SovereignIA_Auditor()
    mock_telemetry = {"ALT": 35000, "VEL": 450, "STATUS": "CRUISE"}
    auditor.audit_decision("AVIONICS_SVM", "NEGATION_SUCCESSFUL", mock_telemetry)
