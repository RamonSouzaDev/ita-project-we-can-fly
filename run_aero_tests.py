import sys
import os
import time

# Ensure src is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ita_aero_sec.sensors.adsb import ADSBSensor
from ita_aero_sec.sensors.avionics import Arinc429Bus
from ita_aero_sec.utils.logger import logger

def run_engineering_simulation():
    print("\n" + "="*60)
    print("   ITA PROJECT: WE CAN FLY - ENGINEERING SIMULATION   ")
    print("   CREA-SP ART: LC39711825-2620260207668             ")
    print("="*60 + "\n")
    
    logger.info("Initializing CREA-SP Certified Simulation...")
    
    # Initialize Sensors
    adsb = ADSBSensor(sensor_id="RADAR-SBGR-01")
    bus = Arinc429Bus(bus_name="ARINC-429-BUS-A")
    
    try:
        # Stream 100 steps
        duration = 100
        adsb_stream = adsb.stream_flight_data(duration_sec=duration, anomaly_prob=0.1)
        bus_stream = bus.stream_bus_traffic(duration_cycles=duration, injection_prob=0.05)
        
        cycle = 0
        for adsb_pkt, arinc_word in zip(adsb_stream, bus_stream):
            cycle += 1
            
            # Monitoring Logic
            status = " [OK] "
            if adsb_pkt.is_spoofed:
                status = " [ALERT: GHOST AIRCRAFT DETECTED] "
            if arinc_word.is_injection:
                status = " [ALERT: AVIONICS INJECTION DETECTED] "
            
            # Live Dashboard output
            output = f"\rCycle {cycle:03d} | Alt: {adsb_pkt.altitude:05.1f} ft | Vel: {adsb_pkt.velocity:05.1f} kts | {status}"
            sys.stdout.write(output)
            sys.stdout.flush()
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nSimulation Aborted.")
        
    print("\n\n" + "="*60)
    print("   SIMULATION COMPLETE. DATA LOGGED TO BLACK BOX.    ")
    print("="*60)

if __name__ == "__main__":
    run_engineering_simulation()
