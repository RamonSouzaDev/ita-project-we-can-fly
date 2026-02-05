from src.ita_aero_sec.sensors.adsb import ADSBSensor
from src.ita_aero_sec.sensors.avionics import Arinc429Bus
from src.ita_aero_sec.utils.logger import logger
import time
import sys

def run_simulation_mission():
    """
    Main Mission Loop:
    Simulates a flight leg with active cyber-monitoring.
    """
    print("\n" + "="*60)
    print("   ITA PROJECT: WE CAN FLY - ENGINEERING SIMULATION   ")
    print("   CREA-SP ART: LC39711825-2620260207668             ")
    print("="*60 + "\n")
    
    logger.info("Initializing Flight Mission Simulation...")
    
    # 1. Initialize Subsystems
    adsb_sensor = ADSBSensor(sensor_id="RADAR-SBGR-01")
    fcs_bus = Arinc429Bus(bus_name="ARINC-429-BUS-A")
    
    # 2. Start Mission Loop (Real-Time Simulation)
    logger.info("Main Engines Start. Telemetry Stream Active.")
    
    try:
        # We zip the streams to run them concurrently (Sync)
        stream_duration = 50
        
        # ADS-B Stream
        adsb_stream = adsb_sensor.stream_flight_data(duration_sec=stream_duration, anomaly_prob=0.1)
        # Avionics Stream
        avionics_stream = fcs_bus.stream_bus_traffic(duration_cycles=stream_duration, injection_prob=0.05)
        
        cycle = 0
        for adsb_pkt, arinc_word in zip(adsb_stream, avionics_stream):
            cycle += 1
            
            # --- Anomaly Detection Logic (Simplified for Simulation) ---
            status = " [OK] "
            if adsb_pkt.is_spoofed:
                status = " [CRITICAL ALERT: GHOST AIRCRAFT] "
            if arinc_word.is_injection:
                status = " [CRITICAL ALERT: UNCOMMANDED ACTUATION] "
                
            # Dashboard Output
            sys.stdout.write(f"\rCycle {cycle:03d} | Alt: {adsb_pkt.altitude:.1f}ft | Vel: {adsb_pkt.velocity:.1f}kts | {status}")
            sys.stdout.flush()
            
            # Artificial delay for visual effect
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        logger.warning("Mission Aborted by User.")
        
    print("\n\n" + "="*60)
    print("   MISSION COMPLETE. BLACK BOX DATA SAVED.           ")
    print("   Log File: flight_blackbox.jsonl                   ")
    print("="*60)

if __name__ == "__main__":
    run_simulation_mission()
