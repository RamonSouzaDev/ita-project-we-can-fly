"""
ADS-B Spoofing Detection using Machine Learning
------------------------------------------------
This module implements a simulation of ADS-B (Automatic Dependent Surveillance-Broadcast)
data to train an aircraft spoofing detector.

Threat Scenario:
Attackers inject "ghost aircraft" signals to confuse air traffic control (e.g., impossible speed/teleportation).

Technique:
- Generates synthetic ADS-B messages (normal vs. spoofed).
- Features: Altitude Delta, Velocity Delta, Signal Strength (RSSI).
- Model: Isolation Forest (Unsupervised Anomaly Detection).

Author: Ramon Mendes
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ADSBSpoofingDetector:
    """
    Class responsible for generating ADS-B data and training an anomaly detection model
    to identify spoofed aircraft signals.
    """
    
    def __init__(self, contamination: float = 0.1, random_state: int = 42):
        self.contamination = contamination
        self.random_state = random_state
        self.model = IsolationForest(contamination=self.contamination, random_state=self.random_state)
        self.scaler = StandardScaler()
        self.features = ['altitude_delta', 'velocity_delta', 'rssi']
        
    def generate_flight_data(self, n_samples: int = 1000) -> pd.DataFrame:
        """Generates synthetic flight data with injected spoofing anomalies."""
        np.random.seed(self.random_state)
        
        n_normal = int(n_samples * (1 - self.contamination))
        normal_data = pd.DataFrame({
            'altitude_delta': np.random.normal(0, 50, n_normal),
            'velocity_delta': np.random.normal(0, 10, n_normal),
            'rssi': np.random.normal(-50, 5, n_normal),
            'label': 0
        })
        
        n_spoof = int(n_samples * self.contamination)
        spoof_data = pd.DataFrame({
            'altitude_delta': np.random.normal(0, 2000, n_spoof),
            'velocity_delta': np.random.normal(0, 500, n_spoof),
            'rssi': np.random.normal(-90, 10, n_spoof),
            'label': 1
        })
        
        data = pd.concat([normal_data, spoof_data]).sample(frac=1).reset_index(drop=True)
        logging.info(f"Generated {len(data)} ADS-B messages ({n_spoof} spoofed).")
        return data

    def train_detector(self, data: pd.DataFrame) -> None:
        """Trains the Isolation Forest model on the provided data."""
        X = data[self.features]
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)
        logging.info("Isolation Forest model trained successfully.")

    def evaluate(self, data: pd.DataFrame) -> np.ndarray:
        """Evaluates the model against the provided dataset."""
        X_test = self.scaler.transform(data[self.features])
        preds = self.model.predict(X_test)
        # Map: -1 (anomaly) -> 1, 1 (normal) -> 0
        mapped_preds = np.where(preds == -1, 1, 0)
        
        print("\n--- Classification Report ---")
        print(classification_report(data['label'], mapped_preds, target_names=['Normal', 'Spoofed']))
        return mapped_preds
        
    def plot_results(self, data: pd.DataFrame, preds: np.ndarray, filename: str = 'adsb_detection_result.png') -> None:
        """Visualizes the decision boundaries and detected anomalies."""
        plt.figure(figsize=(10, 6))
        data['pred_label'] = preds
        
        sns.scatterplot(
            data=data, 
            x='velocity_delta', 
            y='altitude_delta', 
            hue='pred_label', 
            palette={0: 'blue', 1: 'red'},
            style='label'
        )
        
        plt.title('ADS-B Spoofing Detection: Normal vs. "Ghost" Aircraft')
        plt.xlabel('Velocity Change (knots/s)')
        plt.ylabel('Altitude Change (ft/s)')
        plt.axhline(500, color='gray', linestyle='--', alpha=0.5)
        plt.axhline(-500, color='gray', linestyle='--', alpha=0.5)
        plt.text(50, 600, 'Impossible Physics Zone', color='red')
        
        plt.savefig(filename)
        logging.info(f"Detection plot saved to {filename}")

if __name__ == "__main__":
    print("✈️  AVIATION CYBERSECURITY AI DEMO  ✈️")
    print("---------------------------------------")
    detector = ADSBSpoofingDetector(contamination=0.05)
    
    df = detector.generate_flight_data(n_samples=2000)
    detector.train_detector(df)
    
    predictions = detector.evaluate(df)
    detector.plot_results(df, predictions)
    print("\n✅ Simulation Complete.")
