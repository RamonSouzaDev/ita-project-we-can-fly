"""
Configuration file for ITA Project
===================================
Centralized settings for data generation, models, and visualization.
"""

import os

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
TESTS_DIR = os.path.join(PROJECT_ROOT, 'tests')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'outputs')

# Data generation settings
DEFAULT_N_SAMPLES = 1000
DEFAULT_CONTAMINATION = 0.1

# ADS-B settings
ADSB_FEATURES = ['altitude_delta', 'velocity_delta', 'rssi']
ADSB_SCALER = 'StandardScaler'
ADSB_MODEL_PARAMS = {
    'contamination': 0.1,
    'random_state': 42
}

# Avionics settings
AVIONICS_FEATURES = ['airspeed', 'altitude', 'gear_status']
AVIONICS_SCALER = 'MinMaxScaler'
AVIONICS_MODEL_PARAMS = {
    'nu': 0.05,
    'kernel': 'rbf',
    'gamma': 0.1
}

# Visualization settings
PLOT_STYLE = 'seaborn'
FIGURE_SIZE = (10, 6)
COLOR_PALETTE = {0: 'blue', 1: 'red'}

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = os.path.join(OUTPUT_DIR, 'ita_project.log')