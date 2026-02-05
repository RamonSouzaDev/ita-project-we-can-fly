import pytest
import pandas as pd
import numpy as np
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import MinMaxScaler
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from avionics_anomaly import simulate_arinc_bus, train_one_class_svm

class TestAvionicsAnomaly:
    def test_simulate_arinc_bus_basic(self):
        """Test basic bus simulation."""
        df = simulate_arinc_bus(n_samples=100, contamination=0.1)
        assert len(df) == 100
        assert 'airspeed' in df.columns
        assert 'altitude' in df.columns
        assert 'gear_status' in df.columns
        assert 'label' in df.columns
        assert df['label'].sum() == 10  # 10% contamination

    def test_simulate_arinc_bus_no_anomalies(self):
        """Test with no anomalies."""
        df = simulate_arinc_bus(n_samples=100, contamination=0.0)
        assert df['label'].sum() == 0
        assert (df['gear_status'] == 0).all()  # All gear up

    def test_simulate_arinc_bus_all_anomalies(self):
        """Test with all anomalies."""
        df = simulate_arinc_bus(n_samples=100, contamination=1.0)
        assert df['label'].sum() == 100
        assert (df['gear_status'] == 1).all()  # All gear down

    def test_train_one_class_svm(self):
        """Test model training."""
        df = simulate_arinc_bus(n_samples=100, contamination=0.1)
        model, scaler = train_one_class_svm(df)
        assert isinstance(model, OneClassSVM)
        assert isinstance(scaler, MinMaxScaler)

    def test_predictions_shape(self):
        """Test predictions match data size."""
        df = simulate_arinc_bus(n_samples=100, contamination=0.1)
        model, scaler = train_one_class_svm(df)
        X_test = scaler.transform(df[['airspeed', 'altitude', 'gear_status']])
        preds = model.predict(X_test)
        assert len(preds) == 100