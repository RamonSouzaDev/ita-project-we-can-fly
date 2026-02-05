import numpy as np
from dataclasses import dataclass
from typing import Generator
import time
from ..utils.logger import logger

@dataclass
class ADSBPacket:
    icao24: str
    callsign: str
    altitude: float
    velocity: float
    rssi: float
    timestamp: float
    is_spoofed: bool = False

class ADSBSensor:
    """
    Simulates an ADS-B Receiver/Transponder environment.
    Generates realistic flight physics telemetry compatible with CREA-SP engineering standards for simulation.
    """
    def __init__(self, sensor_id: str = "SBGR-RADAR-01"):
        self.sensor_id = sensor_id
        logger.info(f"ADS-B Sensor initialized: {self.sensor_id}")
        
    def stream_flight_data(self, duration_sec=100, anomaly_prob=0.1) -> Generator[ADSBPacket, None, None]:
        """
        Yields ADS-B packets in a stream simulation.
        
        Args:
            duration_sec (int): Number of time steps to simulate.
            anomaly_prob (float): Probability of injecting a spoofed packet per step.
        """
        t = 0
        # Initial Physics State (Cruise Phase)
        current_alt = 32000.0
        current_vel = 480.0
        
        logger.info(f"Starting telemetry stream. Steps: {duration_sec}, Anomaly Prob: {anomaly_prob}")
        
        for t in range(duration_sec):
            is_spoof = np.random.random() < anomaly_prob
            
            if is_spoof:
                # ANOMALY: Physics violation (Impossible jump / Teleportation)
                # E.g., jumping 2000ft in 1 second
                alt_delta = np.random.normal(0, 2000) 
                vel_delta = np.random.normal(0, 500)
                rssi = np.random.normal(-90, 10) # Weak signal (distant attacker)
                
                # We do NOT update current_alt/vel permanently because spoofs are transient glitches usually
                packet_alt = current_alt + alt_delta
                packet_vel = current_vel + vel_delta
                
                logger.warning(f"Injector: Generating SPOOFED packet at step={t} | Alt Delta: {alt_delta:.2f}")
            else:
                # NORMAL: Smooth physics constraints
                alt_delta = np.random.normal(0, 50)
                vel_delta = np.random.normal(0, 10)
                rssi = np.random.normal(-50, 5) # Strong signal (authentic)
                
                # Update physics state (Momentum)
                current_alt += alt_delta
                current_vel += vel_delta
                packet_alt = current_alt
                packet_vel = current_vel
            
            packet = ADSBPacket(
                icao24="E48C01",
                callsign="FAB2026",
                altitude=packet_alt,
                velocity=packet_vel,
                rssi=rssi,
                timestamp=time.time(), # Real timestamp for logging
                is_spoofed=is_spoof
            )
            
            yield packet
