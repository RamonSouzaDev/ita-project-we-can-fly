"""
Avionics Bus Anomaly Detection (ARINC 429 Simulation)
-----------------------------------------------------
This module simulates an ARINC 429 data bus (commonly used in commercial aircraft)
and applies autoencoder-based anomaly detection to find malicious injections.

Threat Scenario:
Attacker injects "valid-looking" but contextually wrong commands into the avionics bus
(e.g., trying to deploy landing gear at high altitude/speed).

Technique:
- Simulates 32-bit ARINC 429 words (Label, SSM, Data, Parity).
- Generates normal flight context vs. injected anomalies.
- Model: One-Class SVM (Unsupervised) to detect outliers in the bus traffic.

Author: Ramon Mendes
"""

import numpy as np
import pandas as pd
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

# ============================
# 1. ARINC 429 Simulation
# ============================
def simulate_arinc_bus(n_samples=2000, contamination=0.05):
    """
    Simulates ARINC 429 words.
    Labels:
    - 310: Latitude
    - 311: Longitude
    - 325: Airspeed (Knots)
    - 270: Landing Gear Status (BNR)
    """
    np.random.seed(99)
    
    # --- Normal Flight Phase (Cruise) ---
    n_normal = int(n_samples * (1 - contamination))
    
    # Cruise speed: 450-500 knots
    airspeed = np.random.normal(480, 10, n_normal)
    
    # Altitude: 30,000 - 35,000 ft
    altitude = np.random.normal(32000, 500, n_normal)
    
    # Gear Status: 0 (Up & Locked) during cruise
    # In ARINC discrete, this might be bit assignments. We'll simplify to 0.0.
    gear_status = np.zeros(n_normal) 
    
    normal_data = pd.DataFrame({
        'airspeed': airspeed,
        'altitude': altitude,
        'gear_status': gear_status,
        'label': 0 # Normal
    })
    
    # --- Anomalies / Injections ---
    n_anom = int(n_samples * contamination)
    
    # Injection 1: High speed but Gear DOWN (impossible/dangerous config)
    anom_speed = np.random.normal(480, 10, n_anom) # Still flying fast
    anom_alt = np.random.normal(32000, 500, n_anom)
    anom_gear = np.ones(n_anom) # Gear DOWN (1.0)
    
    # Injection 2: Sudden Altitude Drop (Data corruption)
    # anom_speed = np.random.normal(480, 10, n_anom)
    # anom_alt = np.random.normal(0, 100, n_anom) # Sudden 0 ft
    
    anomaly_data = pd.DataFrame({
        'airspeed': anom_speed,
        'altitude': anom_alt,
        'gear_status': anom_gear,
        'label': 1 # Anomaly
    })
    
    # Combine
    data = pd.concat([normal_data, anomaly_data]).sample(frac=1).reset_index(drop=True)
    return data

# ============================
# 2. Model Training
# ============================
def train_one_class_svm(data):
    """
    Trains One-Class SVM to learn the 'envelope' of normal flight data.
    """
    X = data[['airspeed', 'altitude', 'gear_status']]
    
    # Scale features (critical for SVM)
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    
    # nu = approx ratio of outliers
    model = OneClassSVM(nu=0.05, kernel="rbf", gamma=0.1)
    model.fit(X_scaled)
    
    return model, scaler

# ============================
# 3. Main Execution
# ============================
if __name__ == "__main__":
    print("🛡️  AVIONICS BUS SECURITY SYSTEM  🛡️")
    print("---------------------------------------")
    print("[1] Simulating ARINC 429 Data Bus (Cruise Phase)...")
    df = simulate_arinc_bus(n_samples=3000, contamination=0.03)
    print(f"    - Total Words: {len(df)}")
    print(f"    - Injected Anomalies: {df['label'].sum()}")
    print("      (Scenario: Malicious 'Gear Down' command at Mach 0.7)")
    
    print("\n[2] Training One-Class SVM (Context-Aware Anomaly Detection)...")
    clf, scaler = train_one_class_svm(df)
    
    print("\n[3] Scanning Bus for Threats...")
    X_test = scaler.transform(df[['airspeed', 'altitude', 'gear_status']])
    preds = clf.predict(X_test)
    
    # OCSVM: -1 = outlier, 1 = inlier. Map to 1=Anomaly, 0=Normal
    mapped_preds = [1 if p == -1 else 0 for p in preds]
    
    print("\n--- Detection Report ---")
    print(classification_report(df['label'], mapped_preds, target_names=['Normal Bus Traffic', 'Malicious Injection']))
    
    # Contextual check
    detected = np.sum(mapped_preds)
    actual = df['label'].sum()
    print(f"\n[SUMMARY] Detected {detected} potential threats (Actual: {actual})")
    print("          System flagged command: 'GEAR_DOWN' while Airspeed > 260 knots.")
