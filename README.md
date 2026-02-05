# ✈️ Aviation Cybersecurity & AI Study

> **"Securing the Skies with Artificial Intelligence"**

## 📜 Regulatory Compliance (DECEA 2030)

This project is aligned with the **DECEA (Departamento de Controle do Espaço Aéreo)** strategic roadmap for CNS/ATM (Communication, Navigation, Surveillance / Air Traffic Management).

-   **ADS-B Out Mandate (2030):** Addresses the upcoming requirement for ADS-B Out in Brazilian Airspace (postponed to 2030), ensuring infrastructure readiness.
-   **Cybersecurity Provision:** Proactive defense mechanisms for the ADS-B transition period, protecting against spoofing during mixed-mode operations (Radar + ADS-B).
-   **Standards:**
    -   **ICAO Doc 9985:** ATM Security Manual.
    -   **DECEA AIC-N:** Circulars regarding ADS-B implementation phases.

This project explores the intersection of **Aeronautic Cybersecurity** and **Artificial Intelligence**, demonstrating how Machine Learning can defend modern avionics against sophisticated cyber threats.

Created by **Ramon Mendes** - *First Software Engineer in São Paulo State* 🇧🇷

> **CREA-SP Registered Project** 🛡️
> **ART:** LC39711825-2620260207668
> **Status:** REGISTERED & ACTIVE ✅


---

## 🛡️ Project Overview

Modern aviation relies heavily on digital communication (ADS-B, ARINC 429, ACARS), which were often designed before the era of advanced cyber warfare. This repository enables:

1.  **Detection of Ghost Aircraft**: Using ML to flag spoofed ADS-B signals.
2.  **Avionics Bus Protection**: Identifying malicious command injections in flight control systems.

### 🌍 Real-World Context
With initiatives like the **FAB's Aerospace Cyber Defense Center (CDCAER)** and **Embraer's** growing focus on cyber-resilience, the need for AI-driven security in aviation is critical in 2026.

---

## 🚀 Key Modules

### 1. ADS-B Spoofing Detector (`src/adsb_spoofing.py`)
**Threat**: Attackers broadcasting fake aircraft positions ("Ghost Aircraft") to confuse Air Traffic Control (ATC) or TCAS systems.
**Solution**: An **Isolation Forest** model that analyzes flight physics (velocity delta, altitude delta, signal strength).
**Outcome**: Flags "Impossible Physics" (e.g., an aircraft teleporting or accelerating to Mach 5 instantly).

### 2. Avionics Anomaly Hunter (`src/avionics_anomaly.py`)
**Threat**: Malware injecting malicious commands into the **ARINC 429** data bus (e.g., commanding "Landing Gear DOWN" while cruising at 35,000 ft).
**Solution**: A **One-Class SVM** that learns the "contextual envelope" of normal flight phases.
**Outcome**: Detects contextually dangerous commands that standard firewalls might miss.

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Start-Ramon/cybersecurity-ai-study.git
cd cybersecurity-ai-study

# Install dependencies
pip install -r requirements.txt
```

## 🛠️ Usage Simulator

Run the simulations to see AI defense in action:

**1. Detect ADS-B Spoofing:**
```bash
python src/adsb_spoofing.py
```
*Output: classification report of Real vs. Fake signals and a visualization plot.*

**2. Scan Avionics Bus:**
```bash
python src/avionics_anomaly.py
```
*Output: Detection of malicious 'Gear Down' injections during high-speed cruise.*

## 🐳 Run with Docker

You can run the entire simulation in a container without installing Python locally.

### Option A: Docker Compose (Recommended)
This method allows generated charts (PNGs) to be saved to your local folder.

```bash
docker compose up
```

### Option B: Standard Docker
```bash
# 1. Build the image
docker build -t ita-project-we-can-fly .

# 2. Run the simulations
docker run ita-project-we-can-fly
```

---

## 📊 Technologies Used
- **Python 3.12+**
- **Scikit-Learn** (Isolation Forest, One-Class SVM)
- **Pandas & NumPy** (Data Simulation)
- **Seaborn** (Visualization)

---

## 🔗 Connect
**Ramon Mendes**
*Software Engineer | Aviation Security Enthusiast*
[LinkedIn Profile](https://www.linkedin.com/in/ramon-mendes-b44456164/)

*"Innovation distinguishes between a leader and a follower."*
