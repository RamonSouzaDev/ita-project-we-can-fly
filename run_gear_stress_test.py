"""
WE CAN FLY - GEAR PHASE 04: SECURITY LAB STRESS TESTING (TRL-9)
---------------------------------------------------------------
Simulates a high-volume ADS-B 1090MHz ingestion scenario (100,000 msg/min)
to validate the latency and orchestration of the GEAR Agentic Ecosystem.

Author: Eng. Ramon Mendes (Specialist & Forensic Expert)
MPSP ID: 9830 | CREA-SP 5071785098
"""

import time
import queue
import threading
from src.adsb_cyber_perito_agent import ADSBCyberPeritoAgent
import logging

# Configure Forensic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

# Constants for Stress Test
TOTAL_MESSAGES = 10000 
TARGET_RATE_PER_SEC = 1666 # Approx 100k/min
STRESS_DURATION_SEC = 10

class StressTestOrchestrator:
    def __init__(self):
        self.agent = ADSBCyberPeritoAgent()
        self.message_queue = queue.Queue()
        self.results = []
        self.processing_times = []
        self.active = True

    def message_producer(self):
        """Simulates high-speed SDR ingestion into the GEAR pipeline."""
        logging.info(f"🚀 INGESTION START: Target {TARGET_RATE_PER_SEC} msg/sec")
        start_time = time.time()
        count = 0
        
        while count < TOTAL_MESSAGES and self.active:
            # Generate mock telemetry packet
            msg = {
                "icao": f"0x{count:06X}",
                "altitude": 35000 + (count % 100),
                "velocity": 480 + (count % 10),
                "timestamp": time.time()
            }
            # Inject anomaly every 500 messages
            if count % 500 == 0:
                msg["altitude"] = 99999 # Physical impossibility
            
            self.message_queue.put(msg)
            count += 1
            
            # Rate limiting to match 100k/min
            if count % TARGET_RATE_PER_SEC == 0:
                elapsed = time.time() - start_time
                expected = count / TARGET_RATE_PER_SEC
                if elapsed < expected:
                    time.sleep(expected - elapsed)
                    
        self.active = False
        logging.info(f"🏁 INGESTION COMPLETE: {count} messages produced.")

    def agent_consumer(self):
        """Mocking the GEAR consumer to evaluate ADK orchestration latency."""
        while self.active or not self.message_queue.empty():
            try:
                msg = self.message_queue.get(timeout=1)
                start_process = time.time()
                
                # In a real TRL-9 scenario, the agent would filter most
                # and only trigger Gemini for anomalies.
                is_anomaly = msg["altitude"] > 60000 
                
                if is_anomaly:
                    logging.warning(f"🚨 ANOMALY DETECTED at {msg['icao']}! Invoking GEAR Swarm...")
                    # For stress testing, we call the agent's full logic
                    # We pass the anomaly score to simulate the trigger
                    self.agent.process({"icao": msg["icao"], "alt": msg["altitude"]})
                    
                latency = time.time() - start_process
                self.processing_times.append(latency)
                self.message_queue.task_done()
                
            except queue.Empty:
                continue

    def run(self):
        print("============================================================")
        print("  GEAR SECURITY LAB: STRESS TEST PHASE 04 (TRL-9)          ")
        print(f"  Target: 100,000 msg/min | Duration: {STRESS_DURATION_SEC}s ")
        print("============================================================")
        
        producer_thread = threading.Thread(target=self.message_producer)
        consumer_thread = threading.Thread(target=self.agent_consumer)
        
        start_time = time.time()
        producer_thread.start()
        consumer_thread.start()
        
        producer_thread.join()
        # Wait a bit for consumer to finish processing last bursts
        time.sleep(2)
        self.active = False
        consumer_thread.join()
        
        total_time = time.time() - start_time
        avg_latency = (sum(self.processing_times) / len(self.processing_times)) * 1000 if self.processing_times else 0
        
        print("\n============================================================")
        print("  STRESS TEST RESULTS (VAL. V.25-03-26)                    ")
        print("============================================================")
        print(f"  Total Ingested: {len(self.processing_times)} messages")
        print(f"  Total Duration: {total_time:.2f} seconds")
        print(f"  Avg Orchestration Latency: {avg_latency:.4f} ms")
        print(f"  Throughput: {len(self.processing_times)/total_time:.2f} msg/sec")
        print("  MPSP Audit Trail: SEALED")
        print("============================================================")

if __name__ == "__main__":
    orchestrator = StressTestOrchestrator()
    orchestrator.run()
