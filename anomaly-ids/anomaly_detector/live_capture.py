from scapy.all import sniff, IP, TCP, UDP
import time
import numpy as np
import pickle
import pandas as pd
import csv
import os

# ===========================
# PATHS
# ===========================
MODEL_PATH = "model_outputs/iforest.pkl"
SCALER_PATH = "model_outputs/scaler.pkl"

LIVE_LOG_PATH = "data/live/live_predictions.csv"
os.makedirs("data/live", exist_ok=True)

# If live log does not exist, create with header
if not os.path.exists(LIVE_LOG_PATH):
    with open(LIVE_LOG_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "src_ip", "dst_ip", "proto", "sport", "dport",
            "anomaly_score", "label", "timestamp"
        ])

# ===========================
# LOAD MODEL + SCALER
# ===========================
model = pickle.load(open(MODEL_PATH, "rb"))
scaler = pickle.load(open(SCALER_PATH, "rb"))

# ===========================
# FLOW TABLE
# ===========================
flows = {}    # key → list of packets
FLOW_TIMEOUT = 5  # seconds since last packet before finalizing flow

# ===========================
# HELPER: Extract flow key
# ===========================
def get_flow_key(pkt):
    if IP not in pkt:
        return None

    proto = pkt[IP].proto
    sport = pkt.sport if hasattr(pkt, "sport") else 0
    dport = pkt.dport if hasattr(pkt, "dport") else 0

    return (pkt[IP].src, pkt[IP].dst, proto, sport, dport)

# ===========================
# PROCESS COMPLETED FLOW
# ===========================
def process_flow(key, pkts):

    timestamps = [float(p.time) for p in pkts]
    sizes = [len(p) for p in pkts]

    # Base PCAP-derived features
    features = {
        "proto": key[2],
        "sport": key[3],
        "dport": key[4],
        "packet_count": len(pkts),
        "byte_count": sum(sizes),
        "flow_duration": max(timestamps) - min(timestamps) if len(timestamps) > 1 else 0,
    }

    # avg interarrival
    if len(timestamps) > 1:
        features["avg_interarrival"] = np.mean(np.diff(sorted(timestamps)))
    else:
        features["avg_interarrival"] = 0

    # TCP flags
    features["syn_count"] = sum(1 for p in pkts if TCP in p and p[TCP].flags & 0x02)
    features["ack_count"] = sum(1 for p in pkts if TCP in p and p[TCP].flags & 0x10)

    # Windows log-derived features (none for live mode)
    features["failed_logins_from_ip"] = 0

    # internal IP flag
    def is_internal(ip):
        return (
            ip.startswith("10.") or
            ip.startswith("172.16.") or
            ip.startswith("192.168.")
        )
    features["ip"] = 1 if is_internal(key[0]) else 0

    # ---- enforce required model feature order ----
    FEATURE_ORDER = [
        "proto",
        "sport",
        "dport",
        "packet_count",
        "byte_count",
        "flow_duration",
        "avg_interarrival",
        "syn_count",
        "ack_count",
        "ip",
        "failed_logins_from_ip"
    ]

    df = pd.DataFrame(
        [[features[col] for col in FEATURE_ORDER]],
        columns=FEATURE_ORDER
    )

    # scale + predict
    X = scaler.transform(df)
    y_pred = model.predict(X)
    score = model.score_samples(X)[0]

    label = "anomaly" if y_pred[0] == -1 else "normal"

    print(f"\nFlow ended: {key}")
    print("Status:", label)
    print("Anomaly Score:", score)
    print("-" * 50)

    # append to live log
    with open(LIVE_LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            key[0], key[1], key[2], key[3], key[4],
            score, label, time.time()
        ])

# ===========================
# PACKET HANDLER
# ===========================
def handle_packet(pkt):
    key = get_flow_key(pkt)
    if key is None:
        return

    now = time.time()

    if key not in flows:
        flows[key] = {"pkts": [], "last_seen": now}

    flows[key]["pkts"].append(pkt)
    flows[key]["last_seen"] = now

    # Finalize expired flows
    expired = []
    for k, flow in flows.items():
        if now - flow["last_seen"] > FLOW_TIMEOUT:
            process_flow(k, flow["pkts"])
            expired.append(k)

    for k in expired:
        del flows[k]

# ===========================
# START CAPTURE
# ===========================
def start_live_capture(interface):
    print(f"\n🚀 Starting live capture on interface: {interface}")
    print("Press CTRL+C to stop.\n")

    sniff(iface=interface, prn=handle_packet, store=False)
