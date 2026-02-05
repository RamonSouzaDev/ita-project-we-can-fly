import pytest
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from adsb_spoofing import generate_flight_data, train_detector, plot_results

class TestADSSpoofing:
    def test_generate_flight_data_basic(self):
        """Test basic data generation."""
        df = generate_flight_data(n_samples=100, contamination=0.1)
        assert len(df) == 100
        assert 'altitude_delta' in df.columns
        assert 'velocity_delta' in df.columns
        assert 'rssi' in df.columns
        assert 'label' in df.columns
        assert df['label'].sum() == 10  # 10% contamination

    def test_generate_flight_data_no_anomalies(self):
        """Test with no anomalies."""
        df = generate_flight_data(n_samples=100, contamination=0.0)
        assert df['label'].sum() == 0

    def test_generate_flight_data_all_anomalies(self):
        """Test with all anomalies."""
        df = generate_flight_data(n_samples=100, contamination=1.0)
        assert df['label'].sum() == 100

    def test_train_detector(self):
        """Test model training."""
        df = generate_flight_data(n_samples=100, contamination=0.1)
        model, scaler = train_detector(df)
        assert isinstance(model, IsolationForest)
        assert isinstance(scaler, StandardScaler)

    def test_predictions_shape(self):
        """Test predictions match data size."""
        df = generate_flight_data(n_samples=100, contamination=0.1)
        model, scaler = train_detector(df)
        X_test = scaler.transform(df[['altitude_delta', 'velocity_delta', 'rssi']])
        preds = model.predict(X_test)
        assert len(preds) == 100

    def test_plot_results_no_error(self):
        """Test plotting doesn't raise errors."""
        df = generate_flight_data(n_samples=100, contamination=0.1)
        model, scaler = train_detector(df)
        X_test = scaler.transform(df[['altitude_delta', 'velocity_delta', 'rssi']])
        preds = model.predict(X_test)
        # Should not raise exception
        plot_results(df, preds)