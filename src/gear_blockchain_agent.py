"""
WE CAN FLY - GEAR PHASE 08: DECENTRALIZED LEDGER (BLOCKCHAIN)
---------------------------------------------------------------
Ensures absolute immutability of MPSP evidence through a mock
decentralized ledger (Hyperledger Fabric Pattern).

Author: Eng. Ramon Mendes (Specialist & Forensic Expert)
MPSP ID: 9830 | CREA-SP 5071785098
"""

from src.gear_adk_base import GEARBaseAgent
import hashlib
import time
import json

class GEARBlockchainAgent(GEARBaseAgent):
    """
    Simulates a blockchain validator that anchors forensic
    hashes into a decentralized ledger.
    """
    def __init__(self, agent_id: str = "BLOCKCHAIN_LEDGER_NODE"):
        super().__init__(agent_id)
        self.ledger = [] # Mock of the world state
        self.log("Hyperledger Mock Node Active. Awaiting Forensic Anchors.")

    def process(self, forensic_payload: dict):
        """
        Anchors a forensic hash into the ledger.
        """
        payload_str = json.dumps(forensic_payload, sort_keys=True)
        block_hash = hashlib.sha3_256(f"{len(self.ledger)}:{payload_str}:{time.time()}".encode()).hexdigest()
        
        block = {
            "block_index": len(self.ledger),
            "forensic_hash": forensic_payload.get("forensic_hash", "UNKNOWN"),
            "merkle_root": block_hash,
            "timestamp": time.time(),
            "status": "COMMITTED"
        }
        
        self.ledger.append(block)
        self.log(f"BLOCK COMMITTED: Index {block['block_index']} | Hash: {block['merkle_root'][:16]}...", "SUCCESS")
        
        return block["merkle_root"]

    def verify_evidence(self, forensic_hash: str) -> bool:
        """Verifies if a specific hash exists in the immutable ledger."""
        for block in self.ledger:
            if block["forensic_hash"] == forensic_hash:
                return True
        return False
