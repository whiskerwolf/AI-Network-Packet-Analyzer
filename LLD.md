# Low-Level Design (LLD)

## 1. Project Structure

```text
AI_Network_Packet_Analyzer/
├── main.py
├── gui.py
├── packet_sniffer.py
├── ai_detector.py
├── dashboard.py
├── requirements.txt
├── README.md
├── HLD.md
├── LLD.md
├── PRD.md
├── exports/
└── screenshots/
```

## 2. Entry Point — `main.py`

`main.py` imports `root` from `gui.py` and starts the Tkinter event loop:

```python
from gui import root

def main():
    root.mainloop()
```

## 3. GUI Module — `gui.py`

The GUI maintains:
- `running`
- `captured_logs`
- `protocol_stats`
- `ip_traffic_stats`

It creates the application window titled **AI Network Packet Analyzer**.

### Main Controls
- Start
- Stop
- Dashboard
- Export Logs
- Clear Logs

### Packet Analysis
`analyze_packet(packet)`:
1. Checks whether the application is running.
2. Checks for an IP layer.
3. Extracts source IP and destination IP.
4. Calculates packet size.
5. Identifies TCP, UDP, ICMP, or OTHER.
6. Identifies HTTPS, HTTP, or DNS where applicable.
7. Calls `detect_ai_anomaly(packet_size)`.
8. Updates protocol and IP statistics.
9. Appends the packet to captured logs.
10. Displays the packet log.
11. Displays AI alerts when the result is suspicious.
12. Displays high-traffic alerts at configured packet-count thresholds.

## 4. Packet Data Representation

Captured log records contain:

```text
Protocol
Source IP
Destination IP
Application Protocol
AI Result
```

These records are later converted into a Pandas DataFrame for CSV export.

## 5. Packet Sniffer — `packet_sniffer.py`

The function:

```python
start_packet_sniffing(callback)
```

uses Scapy:

```python
sniff(
    prn=callback,
    store=False
)
```

The callback receives each captured packet for analysis.

## 6. AI Detector — `ai_detector.py`

The project uses:

```python
IsolationForest(
    contamination=0.05,
    random_state=42
)
```

Packet size is stored in `traffic_data`.

### Detection Flow

```text
Packet Size
    ↓
Append to traffic_data
    ↓
Fewer than 50 samples?
    ├── Yes → "Learning..."
    └── No
          ↓
      Fit Isolation Forest
          ↓
      Predict packet size
          ↓
   -1 → "⚠ Suspicious"
    1 → "Normal"
```

The detector uses packet size as its current anomaly feature.

## 7. Dashboard — `dashboard.py`

`show_dashboard(protocol_stats, ip_traffic_stats)` generates two Matplotlib visualizations.

### Protocol Distribution
A pie chart represents protocol statistics.

### Top Traffic IPs
The source IP statistics are sorted in descending order and the top five are displayed in a bar chart.

## 8. Traffic Statistics

The GUI maintains:

```python
protocol_stats = defaultdict(int)
ip_traffic_stats = defaultdict(int)
```

For every analyzed packet:
- The detected protocol count is incremented.
- The source IP packet count is incremented.

## 9. Alert Logic

### AI Alert
When the AI detector returns:

```text
⚠ Suspicious
```

the GUI adds an AI security alert containing the source IP.

### High Traffic Alert
The GUI checks source-IP packet counts against:

```text
100
250
500
```

When a threshold is reached, a high-traffic alert is displayed.

## 10. CSV Export

`export_logs()` creates a Pandas DataFrame with:

```text
Protocol
Source IP
Destination IP
Application Protocol
AI Result
```

and writes:

```text
exports/packet_logs.csv
```

## 11. Threading

Packet sniffing is started in a daemon thread so that packet capture can operate without blocking the main GUI workflow.

## 12. Installation

```bash
pip install -r requirements.txt
```

## 13. Execution

```bash
python main.py
```

## 14. Dependencies

The project requirements include Scapy, Matplotlib, Pandas, and Scikit-learn. The provided requirements file pins Scikit-learn to version 1.5.2.

## 15. Future Technical Extensions
- Add real-time threat-intelligence feeds.
- Add cloud-based monitoring.
- Replace/augment Isolation Forest with deep-learning threat detection.
- Add network intrusion classification.
- Expand protocol/application detection.
