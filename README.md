📡 Machine Learning Network Intrusion Detection System (IDS)
A full ML-powered Intrusion Detection System that analyzes Windows security logs, 
PCAP network captures, 
and real-time packet flows to detect anomalies using an Isolation Forest model.

This project includes:
  🔍 Log ingestion + feature engineering
  📦 PCAP flow extraction via Scapy
  🤖 Machine learning anomaly detection
  🛰️ Real-time network monitoring engine
  💻 Command-line interface (anomaly-detect)
  📊 Auto-generated HTML anomaly reports
  🚨 Live anomaly scoring from packet captures
---------
🚀 Features
1. Log Preprocessing
  Parses Windows Security Event Logs (4624, 4625, 4688)
  Extracts:
    Failed logins
    Successful logins
    User/IP correlations
   Process execution patterns
Output → logs.pkl

2. PCAP Flow Feature Extraction
Using Scapy:
  src / dst IP
  protocol
  packet count
  byte count
  flow duration
  interarrival times
  SYN / ACK flag counts
Output → pcap_features.csv

3. Feature Builder
Merges log + network features into one dataset:
Output → features.csv

4. Machine Learning Model
Trains an Isolation Forest on engineered features.
Outputs:
model_outputs/iforest.pkl
model_outputs/scaler.pkl

5. CLI Tool: anomaly-detect
Available commands:
anomaly-detect run          # full pipeline (logs + pcap + model)
anomaly-detect logs         # process raw logs
anomaly-detect pcap         # extract pcap features
anomaly-detect features     # merge features
anomaly-detect predict      # model predictions
anomaly-detect live         # REAL-TIME CAPTURE MODE

⭐ 6. Real-Time Packet Capture Mode
anomaly-detect live --iface en0
Features:
  Captures packets using Scapy sniff()
  Builds flows on the fly
  Applies ML anomaly scoring
  Streams results to terminal
  Logs all events to:
    live_capture_log.csv
Example output:
  Flow ended: ('192.168.4.81', '142.251.111.138', 6, 59339, 443)
  Status: normal
  Anomaly Score: -0.472

📊 7. Auto-Generated HTML Report
Uses Jinja2 templating to build a professional incident report:
  reports/anomaly_report.html
🔧 Tech Stack
  Python 3
  Scapy
  Pandas
  NumPy
  Scikit-Learn
  Click (CLI)
  Jinja2 (reporting)
  Streamlit (dashboard, optional add-on)

 🗂 Project Structure
├── anomaly_detector/      # Python package (CLI + live capture)
├── data/                  # raw + processed data
├── model_outputs/         # trained ML models + scaler
├── reports/               # auto-generated HTML reports
├── src/                   # preprocessing + modeling code
├── setup.py               # pip-installable package
└── README.md

▶ Running the Pipeline
Install
  pip install -e .
Run the full pipeline
  anomaly-detect run
Real-time monitoring
  anomaly-detect live --iface en0

📈 Future Enhancements
  Live Streamlit dashboard (real-time anomaly visualization)
  MITRE ATT&CK mapping of anomalies
  Slack / Discord alerting
  PCAP extraction of anomalous flows
  Threat intelligence enrichment (IP reputation lookups

🧑‍💻 Author
Paul DeFrain
Cybersecurity Analyst & ML Security Engineer
