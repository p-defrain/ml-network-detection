import os
import subprocess

def run_logs():
    subprocess.run(["python3", "src/preprocess/log_loader.py"])

def run_pcap():
    subprocess.run(["python3", "src/preprocess/pcap_features.py"])

def run_features():
    subprocess.run(["python3", "src/preprocess/feature_builder.py"])

def run_predict():
    subprocess.run(["python3", "src/models/predict.py"])

def run_report():
    subprocess.run(["python3", "src/reporting/html_reporter.py"])

def run_all():
    print("\n=== Running Full Anomaly Detection Pipeline ===\n")
    run_logs()
    run_pcap()
    run_features()
    run_predict()
    run_report()
    print("\n=== Pipeline Complete ===\n")
