# AI Coding Agent Instructions for ITA Project: We Can Fly

## Project Overview
This is a Python-based aviation cybersecurity simulation using machine learning to detect ADS-B spoofing and avionics bus anomalies. The project consists of two main ML modules in `src/` that generate synthetic data, train unsupervised models, and evaluate detection performance.

## Architecture
- **ADS-B Spoofing Detector** (`src/adsb_spoofing.py`): Uses Isolation Forest to flag "impossible physics" in flight data (altitude/velocity deltas, RSSI).
- **Avionics Anomaly Hunter** (`src/avionics_anomaly.py`): Uses One-Class SVM to detect contextual anomalies in ARINC 429 bus traffic (e.g., gear commands during cruise).
- **Test Runner** (`run_aero_tests.py`): Imports and executes both modules for integration testing.
- **Dockerized Environment**: `Dockerfile` and `docker-compose.yml` enable containerized runs with volume mounts for output files.

## Key Patterns
- **Synthetic Data Generation**: Each module defines a function (e.g., `generate_flight_data()`) that creates pandas DataFrames with normal and anomalous samples using numpy random distributions. Contamination ratio controls anomaly percentage.
- **Feature Scaling**: Always scale features before ML training using `StandardScaler` (ADS-B) or `MinMaxScaler` (Avionics) - critical for model performance.
- **Model Prediction Mapping**: Isolation Forest returns -1/1; map to 0/1 labels as `mapped_preds = [1 if p == -1 else 0 for p in preds]`. One-Class SVM similarly maps -1 to anomaly.
- **Visualization**: Use seaborn scatterplots with hue for predictions, save as PNG with `plt.savefig()`. Include reference lines for "impossible zones" (e.g., `plt.axhline(500)`).
- **Evaluation**: Use `classification_report()` with `target_names` for readable output. Print contextual summaries like detected threats vs. actual.

## Workflows
- **Local Run**: `python src/adsb_spoofing.py` or `python src/avionics_anomaly.py` - generates plots and reports to console.
- **Full Test**: `python run_aero_tests.py` - runs both modules and saves ADS-B plot to current directory.
- **Docker**: `docker compose up` - mounts workspace for persistent outputs; default command runs tests.
- **Dependencies**: Install via `pip install -r requirements.txt` (includes scikit-learn, pandas, seaborn).

## Conventions
- **Random Seeds**: Set `np.random.seed()` for reproducible synthetic data (e.g., 42 for ADS-B, 99 for Avionics).
- **Data Structure**: Pandas DataFrames with 'label' column (0=normal, 1=anomaly) and feature columns.
- **Threat Scenarios**: Code comments describe real-world attacks (ghost aircraft, bus injections) with specific examples like "Gear Down at Mach 0.7".
- **Output Files**: Plots saved as `adsb_detection_result.png` in working directory; no cleanup needed.

## Integration Points
- No external APIs; standalone simulations.
- Volume mounts in Docker preserve generated images on host.
- Jupyter included for exploratory analysis (though not used in main scripts).</content>
<parameter name="filePath">c:\Users\dwmom\OneDrive\Documentos\ibm-interview-studies\cybersecurity-ai-study\.github\copilot-instructions.md