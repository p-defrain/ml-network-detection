#!/bin/bash

echo "================================================="
echo "  NETWORK ANOMALY DETECTION PIPELINE"
echo "================================================="
echo ""

# Step 1: Preprocess Windows event logs
echo "[1/5] Loading Windows Event Logs..."
python3 src/preprocess/log_loader.py
echo ""

# Step 2: Extract network flow features from PCAPs
echo "[2/5] Extracting PCAP features..."
python3 src/preprocess/pcap_features.py
echo ""

# Step 3: Build final ML feature dataset
echo "[3/5] Building combined feature dataset..."
python3 src/preprocess/feature_builder.py
echo ""

# Step 4: Run anomaly detection (using trained model)
echo "[4/5] Running ML model predictions..."
python3 src/models/predict.py
echo ""

# Step 5: Generate HTML anomaly report
echo "[5/5] Generating HTML report..."
python3 src/reporting/html_reporter.py
echo ""

echo "================================================="
echo "  PIPELINE COMPLETED!"
echo "  ✔ Predictions saved to: data/processed/predictions.csv"
echo "  ✔ HTML report saved to: reports/anomaly_report.html"
echo "================================================="
