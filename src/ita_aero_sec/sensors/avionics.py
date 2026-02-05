import numpy as np
from dataclasses import dataclass
from typing import Generator
from ..utils.logger import logger

@dataclass
class ArincWord:
    label: int      # 8-bit Label (e.g., 310 for Lat)
    sdi: int        # Source/Destination Identifier
    data: float     # The payload
    ssm: int        # Sign/Status Matrix
    parity: int     # Odd Parity bit
    timestamp: float
    is_injection: bool = False

class Arinc429Bus:
    """
    Simulates an ARINC 429 Data Bus (Standard for Commercial/Transport Aircraft).
    Generates data words for Flight Control Systems (FCS).
    """
    def __init__(self, bus_name: str = "BUS-A-NAV"):
        self.bus_name = bus_name
        logger.info(f"Avionics Bus Initialized: {self.bus_name}")
        
    def stream_bus_traffic(self, duration_cycles=100, injection_prob=0.05) -> Generator[ArincWord, None, None]:
        """
        Yields ARINC 429 words simulating bus traffic.
        """
        logger.info(f"Starting Bus Traffic Stream on {self.bus_name}")
        
        for t in range(duration_cycles):
            is_attack = np.random.random() < injection_prob
            
            # --- Normal Channel Data ---
            current_airspeed = 480 + np.random.normal(0, 2)
            current_alt = 32000 + np.random.normal(0, 20)
            
            if is_attack:
                # INJECTION ATTACK: Critical Command Confusion
                # Sending "GEAR DOWN" (Bit set to 1) while at Cruise (Mach 0.8)
                # This could cause structural failure if actuated
                logger.critical(f"BUS ALERT: Malicious Injection Detected on Cycle {t}")
                
                # Malicious payload: Speed is high, but Gear Status is DOWN
                word = ArincWord(
                    label=270, # Landing Gear Discrete
                    sdi=0,
                    data=1.0,  # 1 = DOWN
                    ssm=3,     # Normal Operation (Spoofed to look valid)
                    parity=1,
                    timestamp=t,
                    is_injection=True
                )
            else:
                # NORMAL: Gear is UP (0)
                word = ArincWord(
                    label=270,
                    sdi=0,
                    data=0.0,
                    ssm=3,
                    parity=1,
                    timestamp=t,
                    is_injection=False
                )
            
            yield word
