import sys
import os

# Add src to python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    print("\n[TEST] Running ADS-B Spoofing Simulation...")
    from src import adsb_spoofing
    adsb_df = adsb_spoofing.generate_flight_data(n_samples=500, contamination=0.1)
    model, scaler = adsb_spoofing.train_detector(adsb_df)
    print("✅ ADS-B Model Trained Successfully")
    
    print("\n[TEST] Running Avionics Bus Anomaly Simulation...")
    from src import avionics_anomaly
    avionics_df = avionics_anomaly.simulate_arinc_bus(n_samples=500, contamination=0.1)
    model_av, scaler_av = avionics_anomaly.train_one_class_svm(avionics_df)
    print("✅ Avionics Model Trained Successfully")

    print("\n🎉 ALL SYSTEMS GO: Aviation Cybersecurity Modules Verified.")
except Exception as e:
    print(f"\n❌ TEST FAILED: {e}")
    sys.exit(1)
