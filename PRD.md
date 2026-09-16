# Product Requirements Document (PRD)

## 1. Product Name
**AI-Powered Network Packet Analyzer**

## 2. Product Overview
An advanced cybersecurity and AI-powered desktop application for live packet sniffing, anomaly detection, protocol analysis, and traffic analytics.

The system combines Computer Networks, Cybersecurity, and Machine Learning to monitor live network traffic, identify protocols, detect anomalies, and visualize traffic behavior.

## 3. Objective
Provide a desktop tool that can capture live network packets, identify network/application protocols, detect unusual packet behavior using Machine Learning, generate security alerts, visualize traffic statistics, and export captured logs.

## 4. Target Users
- Cybersecurity students and learners
- Network analysis learners
- Security researchers working in a controlled environment
- Developers demonstrating packet-analysis and anomaly-detection concepts

## 5. Core Features
1. Live packet sniffing using Scapy.
2. TCP, UDP, and ICMP protocol detection.
3. HTTP, HTTPS, and DNS application protocol identification.
4. AI anomaly detection using Isolation Forest.
5. Suspicious packet alerts.
6. High-traffic monitoring.
7. Real-time Tkinter desktop GUI.
8. Traffic analytics dashboard.
9. CSV log export.

## 6. Functional Requirements

### Packet Capture
The application shall capture live packets through Scapy and pass captured packets to the analysis pipeline.

### Protocol Analysis
The application shall identify:
- TCP
- UDP
- ICMP
- Other traffic

It shall additionally identify:
- HTTP
- HTTPS
- DNS
when the relevant ports/protocols are detected.

### AI Anomaly Detection
The system shall use packet size as an input to an Isolation Forest model. During the initial learning period, the detector reports `Learning...`; after sufficient observations, it classifies packet sizes as `Normal` or `⚠ Suspicious`.

### Security Alerts
The GUI shall display alerts for suspicious packets and high traffic from source IP addresses.

### Dashboard
The dashboard shall visualize protocol distribution and the top traffic-generating IP addresses.

### Log Export
Captured packet information shall be exportable to `exports/packet_logs.csv`.

## 7. Logged Information
The packet log contains:
- Protocol
- Source IP
- Destination IP
- Application Protocol
- AI Result

## 8. Technology Requirements
- Python
- Scapy
- Tkinter
- Pandas
- Matplotlib
- Scikit-learn
- Isolation Forest

## 9. Success Criteria
The project is complete when it can capture packets, identify protocols, run anomaly detection, show security alerts, display traffic analytics, and export packet logs.

## 10. Future Improvements
- Real-time threat intelligence
- Cloud monitoring dashboard
- Deep learning-based threat detection
- Network intrusion classification
