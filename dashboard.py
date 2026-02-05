"""
ITA Project Dashboard: Aviation Cybersecurity Analysis
======================================================
Interactive dashboard for visualizing ADS-B spoofing and avionics anomaly detection.

Run with: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from adsb_spoofing import generate_flight_data, train_detector, plot_results
from avionics_anomaly import simulate_arinc_bus, train_one_class_svm

st.set_page_config(page_title="ITA Cybersecurity Dashboard", page_icon="✈️", layout="wide")

st.title("✈️ ITA Project: We Can Fly - Cybersecurity Dashboard")
st.markdown("**Aviation Threat Detection using Machine Learning**")

# Sidebar controls
st.sidebar.header("Simulation Parameters")
n_samples = st.sidebar.slider("Number of Samples", 500, 5000, 1000)
contamination = st.sidebar.slider("Anomaly Ratio (%)", 1, 20, 10) / 100.0

if st.button("Run Simulation"):
    with st.spinner("Generating data and training models..."):
        # ADS-B Section
        st.header("🛩️ ADS-B Spoofing Detection")
        adsb_df = generate_flight_data(n_samples=n_samples, contamination=contamination)
        model_adsb, scaler_adsb = train_detector(adsb_df)

        X_test_adsb = scaler_adsb.transform(adsb_df[['altitude_delta', 'velocity_delta', 'rssi']])
        preds_adsb = model_adsb.predict(X_test_adsb)
        mapped_preds_adsb = [1 if p == -1 else 0 for p in preds_adsb]

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Detection Metrics")
            report_adsb = classification_report(adsb_df['label'], mapped_preds_adsb, target_names=['Normal', 'Spoofed'], output_dict=True)
            st.metric("Precision (Spoofed)", f"{report_adsb['Spoofed']['precision']:.2f}")
            st.metric("Recall (Spoofed)", f"{report_adsb['Spoofed']['recall']:.2f}")
            st.metric("F1-Score (Spoofed)", f"{report_adsb['Spoofed']['f1-score']:.2f}")

        with col2:
            st.subheader("Data Summary")
            st.write(f"Total Samples: {len(adsb_df)}")
            st.write(f"Normal Flights: {len(adsb_df) - adsb_df['label'].sum()}")
            st.write(f"Spoofed Attacks: {adsb_df['label'].sum()}")

        # Plot
        fig, ax = plt.subplots(figsize=(8, 6))
        adsb_df['prediction'] = preds_adsb
        adsb_df['pred_label'] = adsb_df['prediction'].map({1: 0, -1: 1})
        sns.scatterplot(data=adsb_df, x='velocity_delta', y='altitude_delta', hue='pred_label', palette={0: 'blue', 1: 'red'}, ax=ax)
        ax.set_title('ADS-B Spoofing Detection')
        ax.axhline(500, color='gray', linestyle='--', alpha=0.5)
        ax.axhline(-500, color='gray', linestyle='--', alpha=0.5)
        st.pyplot(fig)

        # Avionics Section
        st.header("🛡️ Avionics Bus Anomaly Detection")
        avionics_df = simulate_arinc_bus(n_samples=n_samples, contamination=contamination)
        model_av, scaler_av = train_one_class_svm(avionics_df)

        X_test_av = scaler_av.transform(avionics_df[['airspeed', 'altitude', 'gear_status']])
        preds_av = model_av.predict(X_test_av)
        mapped_preds_av = [1 if p == -1 else 0 for p in preds_av]

        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Detection Metrics")
            report_av = classification_report(avionics_df['label'], mapped_preds_av, target_names=['Normal', 'Anomaly'], output_dict=True)
            st.metric("Precision (Anomaly)", f"{report_av['Anomaly']['precision']:.2f}")
            st.metric("Recall (Anomaly)", f"{report_av['Anomaly']['recall']:.2f}")
            st.metric("F1-Score (Anomaly)", f"{report_av['Anomaly']['f1-score']:.2f}")

        with col4:
            st.subheader("Data Summary")
            st.write(f"Total Bus Words: {len(avionics_df)}")
            st.write(f"Normal Traffic: {len(avionics_df) - avionics_df['label'].sum()}")
            st.write(f"Malicious Injections: {avionics_df['label'].sum()}")

        # Plot for avionics
        fig2, ax2 = plt.subplots(figsize=(8, 6))
        avionics_df['pred_label'] = mapped_preds_av
        sns.scatterplot(data=avionics_df, x='airspeed', y='altitude', hue='pred_label', palette={0: 'green', 1: 'orange'}, ax=ax2)
        ax2.set_title('Avionics Bus Anomaly Detection')
        st.pyplot(fig2)

st.sidebar.markdown("---")
st.sidebar.markdown("**About:** This dashboard simulates aviation cybersecurity threats and demonstrates ML-based detection.")

if __name__ == "__main__":
    st.write("Click 'Run Simulation' to start analysis.")