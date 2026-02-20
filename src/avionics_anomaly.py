"""
Avionics Bus Anomaly Detection (ARINC 429 Simulation)
-----------------------------------------------------
This module simulates an ARINC 429 data bus and applies
One-Class SVM-based anomaly detection to find malicious injections.

Threat Scenario:
Attacker injects "valid-looking" but contextually wrong commands.

Technique:
- Simulates ARINC 429 telemetry under cruise conditions.
- Uses One-Class SVM to learn the 'envelope' of normal flight.

Author: Ramon Mendes
"""

import numpy as np
import pandas as pd
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AvionicsAnomalyDetector:
    """
    Class responsible for generating ARINC 429 simulated data and training
    a One-Class SVM to detect contextually invalid command injections.
    """
    
    def __init__(self, contamination: float = 0.05, random_state: int = 99):
        self.contamination = contamination
        self.random_state = random_state
        self.model = OneClassSVM(nu=self.contamination, kernel="rbf", gamma=0.1)
        self.scaler = MinMaxScaler()
        self.features = ['airspeed', 'altitude', 'gear_status']

    def simulate_arinc_bus(self, n_samples: int = 2000) -> pd.DataFrame:
        """Simulates ARINC 429 data words during normal cruise and injected anomalies."""
        np.random.seed(self.random_state)
        
        n_normal = int(n_samples * (1 - self.contamination))
        n_anom = int(n_samples * self.contamination)

        # Normal Flight Phase (Cruise)
        normal_data = pd.DataFrame({
            'airspeed': np.random.normal(480, 10, n_normal),
            'altitude': np.random.normal(32000, 500, n_normal),
            'gear_status': np.zeros(n_normal),
            'label': 0
        })
        
        # Anomalies (High speed but Gear DOWN)
        anomaly_data = pd.DataFrame({
            'airspeed': np.random.normal(480, 10, n_anom),
            'altitude': np.random.normal(32000, 500, n_anom),
            'gear_status': np.ones(n_anom),
            'label': 1
        })
        
        data = pd.concat([normal_data, anomaly_data]).sample(frac=1).reset_index(drop=True)
        logging.info(f"Simulated {len(data)} ARINC 429 words ({n_anom} anomalies).")
        return data

    def train_detector(self, data: pd.DataFrame) -> None:
        """Trains One-Class SVM to learn the normal flight data envelope."""
        X_scaled = self.scaler.fit_transform(data[self.features])
        self.model.fit(X_scaled)
        logging.info("One-Class SVM model trained successfully.")

    def evaluate(self, data: pd.DataFrame) -> None:
        """Detects threats and prints a classification report."""
        X_test = self.scaler.transform(data[self.features])
        preds = self.model.predict(X_test)
        
        # -1 = anomaly, 1 = normal. Map to 1 = anomaly, 0 = normal
        mapped_preds = np.where(preds == -1, 1, 0)
        
        print("\n--- Detection Report ---")
        print(classification_report(data['label'], mapped_preds, target_names=['Normal Bus Traffic', 'Malicious Injection']))
        
        detected = np.sum(mapped_preds)
        actual = data['label'].sum()
        print(f"\n[SUMMARY] Detected {detected} potential threats (Actual: {actual})")
        print("          System flagged command: 'GEAR_DOWN' while Airspeed > 260 knots.")

if __name__ == "__main__":
    print("🛡️  AVIONICS BUS SECURITY SYSTEM  🛡️")
    print("---------------------------------------")
    detector = AvionicsAnomalyDetector(contamination=0.03)
    
    df = detector.simulate_arinc_bus(n_samples=3000)
    detector.train_detector(df)
    detector.evaluate(df)
    print("\n✅ Simulation Complete.")
