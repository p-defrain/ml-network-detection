📡 Machine Learning–Based Network Anomaly Detection (Prototype IDS)

This repository contains a prototype machine learning–based intrusion detection system (IDS) designed to analyze Windows Security Event Logs and network flow data extracted from PCAP files. The system applies unsupervised anomaly detection (Isolation Forest) to identify unusual authentication and network behavior.

The goal of this project is to explore how log-based and flow-based features can be engineered, combined, and operationalized into a practical detection pipeline, rather than to provide a production-ready IDS.

----

🔍 Project Motivation

Traditional IDS tools rely heavily on signatures and static rules. This project explores whether unsupervised machine learning can help surface anomalous behavior in environments where labeled attack data is limited or unavailable.

Key objectives:

Work with real security-relevant signals (Windows event IDs, network flows)

Engineer interpretable features from logs and PCAPs

Apply an anomaly detection model suitable for unlabeled data

Package the pipeline into a usable command-line tool

Evaluate how retraining affects anomaly rates and false positives

----

⚙️ Current Capabilities
1. Windows Security Log Processing

Parses Windows Security logs (CSV format) focusing on:

4624 – Successful logon

4625 – Failed logon

4688 – Process creation

Extracted features include:

Failed login counts by IP

Successful login activity

User/IP associations

Process execution frequency

Output:

data/processed/logs.pkl

2. PCAP Flow Feature Extraction

Processes PCAP / PCAPNG files and aggregates packets into network flows.

Flow-level features include:

Source and destination IP

Protocol and ports

Packet count

Byte count

Flow duration

Average interarrival time

TCP SYN / ACK flag counts

PCAP parsing is implemented using PyShark (tshark backend) to support large captures efficiently.

Output:

data/processed/pcap_features.csv

3. Feature Engineering & Merging

Log-based and network-based features are merged into a unified dataset suitable for machine learning.

Output:

data/processed/features.csv

4. Anomaly Detection Model

An Isolation Forest model is trained on the engineered features to assign:

An anomaly score (continuous)

A binary prediction (normal / anomalous)

The model is retrained as needed to reflect changes in baseline behavior (e.g., new network captures).

Model artifacts:

model_outputs/iforest.pkl
model_outputs/scaler.pkl

5. Command-Line Interface

The project provides a CLI tool, anomaly-detect, which orchestrates the pipeline.

Available commands:

anomaly-detect logs       # Process raw Windows logs
anomaly-detect pcap       # Extract PCAP flow features
anomaly-detect features   # Merge features
anomaly-detect predict    # Train model and generate predictions
anomaly-detect live       # Live packet capture + anomaly scoring

6. Live Capture Mode (Experimental)

A real-time capture mode monitors live network traffic using Scapy, aggregates packets into flows, and applies the trained Isolation Forest model.

Live mode:

Builds flows incrementally

Scores completed flows

Outputs anomaly scores to terminal and CSV logs

This mode is intended for experimentation and learning, not continuous production deployment.

7. Reporting

An HTML anomaly report can be generated using Jinja2 templates to summarize detected anomalies.

Output:

reports/anomaly_report.html

----

🧠 Model Evaluation & Observations

The model is unsupervised, meaning no labeled attack data is required.

Retraining the model on a recent baseline capture significantly reduced false positives in live testing.

Anomaly scores form a continuous distribution and require thresholding to map to operational severity.

The model is sensitive to feature scaling and environment-specific behavior.

This project emphasizes understanding model behavior and limitations, not treating ML as a black box.

----

⚠️ Limitations

No ground-truth labels; evaluation is qualitative and exploratory

Isolation Forest is sensitive to feature selection and contamination assumptions

Live capture mode is not optimized for high-throughput production environments

Not a replacement for signature-based IDS (e.g., Suricata, Zeek)

----

🚀 Future Enhancements

Labeled or synthetic attack datasets for quantitative evaluation

Severity classification and alerting thresholds

Streamlit-based visualization dashboard

Integration with Zeek logs

Model versioning and automated retraining workflows

Unit tests for log parsing, PCAP processing, and CLI commands

----

🛠️ Tech Stack

Python

Pandas / NumPy

Scikit-learn

PyShark (tshark)

Scapy

Click (CLI)

Jinja2 (reporting)

----

👤 Author

Paul DeFrain
Cybersecurity & Machine Learning Enthusiast

----

📌 Summary

This project is intended as a learning-focused prototype demonstrating how security telemetry, feature engineering, and anomaly detection models can be combined into an operational pipeline. It prioritizes clarity, experimentation, and reproducibility over production readiness.
