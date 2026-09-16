# High-Level Design (HLD)

## 1. System Overview
The AI-Powered Network Packet Analyzer uses a modular desktop architecture:

**Packet Capture → Packet Analysis → AI Detection → Statistics/Alerts → Dashboard/CSV Export**

## 2. Architecture

```text
                    +----------------+
                    |     User       |
                    +-------+--------+
                            |
                            v
                  +--------------------+
                  |   Tkinter GUI      |
                  |      gui.py        |
                  +---------+----------+
                            |
              +-------------+-------------+
              |                           |
              v                           v
   +--------------------+       +-------------------+
   | Packet Sniffer     |       | User Controls     |
   | packet_sniffer.py  |       | Start / Stop      |
   +---------+----------+       +-------------------+
             |
             v
   +----------------------------+
   | Packet Analysis            |
   | IP / TCP / UDP / ICMP      |
   | HTTP / HTTPS / DNS         |
   +-------------+--------------+
                 |
        +--------+---------+
        |                  |
        v                  v
+---------------+   +--------------------+
| AI Detector   |   | Traffic Statistics |
| Isolation     |   | Protocol / IP      |
| Forest        |   +---------+----------+
+-------+-------+             |
        |                     v
        v             +---------------+
+---------------+     | Dashboard     |
| Security      |     | Matplotlib    |
| Alerts        |     +---------------+
+---------------+
        |
        v
+--------------------+
| CSV Log Export     |
| Pandas             |
+--------------------+
```

## 3. Main Components

### 3.1 GUI Layer
`gui.py` creates the Tkinter interface and controls packet capture, dashboards, alerts, log display, and export.

### 3.2 Application Entry Point
`main.py` imports the GUI root and starts the Tkinter event loop.

### 3.3 Packet Sniffer
`packet_sniffer.py` uses Scapy's `sniff()` and passes each captured packet to a callback.

### 3.4 Packet Analysis
The GUI analysis pipeline extracts source/destination IPs, packet size, network protocol, and application protocol.

### 3.5 AI Detector
`ai_detector.py` uses an Isolation Forest model with packet size as the anomaly-detection feature.

### 3.6 Dashboard
`dashboard.py` generates:
- Protocol distribution
- Top five traffic-generating IP addresses

### 3.7 Log Export
Pandas converts captured logs into a DataFrame and exports them as CSV.

## 4. Data Flow
1. User starts sniffing.
2. A background thread starts packet capture.
3. Scapy captures packets.
4. Each packet is sent to the analysis callback.
5. IP/protocol information is extracted.
6. Packet size is sent to the AI anomaly detector.
7. Protocol and source-IP statistics are updated.
8. Logs and alerts are displayed in the GUI.
9. Dashboard data can be visualized.
10. Captured logs can be exported as CSV.

## 5. Technology Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Packet Capture | Scapy |
| GUI | Tkinter |
| Data Processing | Pandas |
| Visualization | Matplotlib |
| Machine Learning | Scikit-learn |
| Anomaly Detection | Isolation Forest |

## 6. Non-Functional Requirements
- Modular code organization.
- Interactive desktop interface.
- Clear security alerts.
- Reproducible anomaly detection configuration.
- CSV-compatible exported logs.
- Statistics should update as packets are processed.

## 7. Security Scope
Packet capture and analysis should be used only on networks/interfaces where the user has authorization to monitor traffic.
