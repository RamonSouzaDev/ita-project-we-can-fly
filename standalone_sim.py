import sys
import time
import random
import hashlib

# ==========================================
# ENGINEERING MODULES (Inline)
# ==========================================

class ADSBSensor:
    def __init__(self, sensor_id="RADAR-1", external_endpoint=None):
        self.sensor_id = sensor_id
        self.external_endpoint = external_endpoint # Prepared for SDR/Hardware injection (HITL)

    def stream_flight_data(self, duration_sec=100, anomaly_prob=0.1):
        # Physics State Fallback (used when external_endpoint is None)
        alt = 32000.0
        vel = 480.0
        
        for _ in range(duration_sec):
            if self.external_endpoint:
                # Placeholder for Phase 4: Sockets/REST RF ingestion from SDR hardware
                pass 

            is_spoof = random.random() < anomaly_prob
            
            if is_spoof:
                # Anomaly: Physics Jump (Spoofing Attack)
                alt_out = alt + random.normalvariate(0, 2000)
                vel_out = vel + random.normalvariate(0, 500)
            else:
                # Normal Flight Envelope
                delta_alt = random.normalvariate(0, 50)
                delta_vel = random.normalvariate(0, 10)
                alt += delta_alt
                vel += delta_vel
                alt_out = alt
                vel_out = vel
                
            yield {
                "alt": alt_out,
                "vel": vel_out,
                "is_spoofed": is_spoof,
                "source": "EXTERNAL_SDR" if self.external_endpoint else "SIMULATED_FALLBACK"
            }

class Arinc429Bus:
    def __init__(self, bus_name="BUS-A", external_endpoint=None):
        self.bus_name = bus_name
        self.external_endpoint = external_endpoint # Prepared for HITL injection

    def stream_bus_traffic(self, duration_cycles=100, injection_prob=0.05):
        for _ in range(duration_cycles):
            if self.external_endpoint:
                 # Placeholder for Phase 4: ARINC 429 hardware bus listener
                 pass
            is_inject = random.random() < injection_prob
            yield {
                "is_injection": is_inject,
                "source": "EXTERNAL_BUS" if self.external_endpoint else "SIMULATED_FALLBACK"
            }

# ==========================================
# MAIN MISSION LOOP
# ==========================================
def main():
    print("\n" + "="*60)
    print("   ITA PROJECT: WE CAN FLY - CREA-SP SIMULATION")
    print("   CONTEXT: DECEA 2030 READINESS (ADS-B OUT MANDATE)")
    print("   RNP PGID 2026: AI-BASED IDENTITY MANAGEMENT TRACK")
    print("   ART CREA-SP: LC39711825-2620260207668")
    print("="*60 + "\n")
    
    adsb = ADSBSensor()
    bus = Arinc429Bus()
    
    try:
        iterator = zip(
            adsb.stream_flight_data(1000000), # Extended run for demo
            bus.stream_bus_traffic(1000000)
        )
        
        cycle = 0
        print("  STREAMING TELEMETRY (DECEA 2030 MODE)... CAUTION: LIVE DATA")
        print("-" * 65)
        
        for data_adsb, data_bus in iterator:
            cycle += 1
            status = "[OK]"
            if data_adsb['is_spoofed']: 
                status = "[ALERT: GHOST AIRCRAFT]"
            if data_bus['is_injection']: 
                status = "[ALERT: AVIONICS ATTACK]"
                
            out = f"Cycle {cycle:05d} | Alt: {data_adsb['alt']:05.0f} | Vel: {data_adsb['vel']:03.0f} | {status}"
            
            # --- FORENSIC CHAIN OF CUSTODY (MPSP REQUIREMENT) ---
            # Generating a cryptographic hash of the event data to ensure non-repudiation.
            custody_hash = hashlib.sha256(out.encode('utf-8')).hexdigest()[:16]
            
            print(f"{out} | HASH: {custody_hash}")
            sys.stdout.flush() # Ensure Docker logs see it immediately
            time.sleep(0.5) # Slower for better visual demo
            
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()
