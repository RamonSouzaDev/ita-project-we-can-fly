"""
ADS-B Spoofing Detection using Machine Learning
------------------------------------------------
This module implements a simulation of ADS-B (Automatic Dependent Surveillance–Broadcast)
data to train an aircraft spoofing detector.

Threat Scenario:
Attackers inject "ghost aircraft" signals to confuse air traffic control (e.g., impossible speed/teleportation).

Technique:
- Generates synthetic ADS-B messages (normal vs. spoofed).
- Features: Altitude Delta, Velocity Delta, Signal Strength (RSSI), Time gap.
- Model: Isolation Forest (Unsupervised Anomaly Detection).

Author: Ramon Mendes
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# ============================
# 1. Synthetic Data Generation
# ============================
def generate_flight_data(n_samples=1000, contamination=0.1):
    """
    Generates synthetic flight data with some injected anomalies (spoofing).
    """
    np.random.seed(42)
    
    # Normal flight data (consistent physics)
    n_normal = int(n_samples * (1 - contamination))
    normal_data = pd.DataFrame({
        'altitude_delta': np.random.normal(0, 50, n_normal),  # ft change per sec
        'velocity_delta': np.random.normal(0, 10, n_normal),  # knots change per sec
        'rssi': np.random.normal(-50, 5, n_normal),           # Signal strength (strong = close)
        'label': 0  # 0 = Normal
    })
    
    # Spoofed data (Impossible physics / "Teleportation")
    n_spoof = int(n_samples * contamination)
    spoof_data = pd.DataFrame({
        'altitude_delta': np.random.normal(0, 2000, n_spoof), # Impossible climbs/drops
        'velocity_delta': np.random.normal(0, 500, n_spoof),  # Mach 1 acceleration anomalies
        'rssi': np.random.normal(-90, 10, n_spoof),           # Weak/Variable signal
        'label': 1  # 1 = Anomaly / Spoof
    })
    
    data = pd.concat([normal_data, spoof_data]).sample(frac=1).reset_index(drop=True)
    return data

# ============================
# 2. Model Training
# ============================
def train_detector(data):
    """
    Trains an Isolation Forest model to detect anomalies.
    """
    # Features for training
    features = ['altitude_delta', 'velocity_delta', 'rssi']
    X = data[features]
    
    # Scale data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train Isolation Forest (Unsupervised)
    # contamination='auto' allows the model to estimate the % of outliers
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(X_scaled)
    
    return model, scaler

# ============================
# 3. Visualization
# ============================
def plot_results(data, preds):
    """
    Visualizes the decision boundary and detected anomalies.
    """
    plt.figure(figsize=(10, 6))
    
    # Add predictions to dataframe
    data['prediction'] = preds
    # Isiolation forest returns -1 for outlier, 1 for inlier. Map to 0/1.
    data['pred_label'] = data['prediction'].map({1: 0, -1: 1})
    
    sns.scatterplot(
        data=data, 
        x='velocity_delta', 
        y='altitude_delta', 
        hue='pred_label', 
        palette={0: 'blue', 1: 'red'},
        style='label' # Real label shape
    )
    
    plt.title('ADS-B Spoofing Detection: Normal vs. "Ghost" Aircraft')
    plt.xlabel('Velocity Change (knots/s)')
    plt.ylabel('Altitude Change (ft/s)')
    plt.axhline(500, color='gray', linestyle='--', alpha=0.5)
    plt.axhline(-500, color='gray', linestyle='--', alpha=0.5)
    plt.text(50, 600, 'Impossible Physics Zone', color='red')
    
    print("\n[INFO] Saving plot to 'adsb_detection_result.png'...")
    plt.savefig('adsb_detection_result.png')
    # plt.show()

# ============================
# 4. Main Execution
# ============================
if __name__ == "__main__":
    print("✈️  AVIATION CYBERSECURITY AI DEMO  ✈️")
    print("---------------------------------------")
    print("[1] Simulating ADS-B datalink traffic...")
    df = generate_flight_data(n_samples=2000, contamination=0.05)
    print(f"    - Generated {len(df)} messages")
    print(f"    - Injected {df['label'].sum()} spoofing attacks (Ghost Aircraft)")
    
    print("\n[2] Training Anomaly Detection Model (Isolation Forest)...")
    clf, scaler = train_detector(df)
    
    print("\n[3] Evaluating Detection Capability...")
    X_test = scaler.transform(df[['altitude_delta', 'velocity_delta', 'rssi']])
    preds = clf.predict(X_test)
    
    # Map predictions: -1 (anomaly) -> 1, 1 (normal) -> 0
    mapped_preds = [1 if p == -1 else 0 for p in preds]
    
    print("\n--- Classification Report ---")
    print(classification_report(df['label'], mapped_preds, target_names=['Normal', 'Spoofed']))
    
    print("\n[4] Visualizing Attack Surface...")
    plot_results(df, preds)
    print("\n✅ Simulation Complete.")
