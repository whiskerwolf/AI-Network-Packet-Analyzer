import tkinter as tk
from tkinter import scrolledtext, messagebox
from threading import Thread
from collections import defaultdict
import pandas as pd

from scapy.all import IP, TCP, UDP, ICMP

from ai_detector import detect_ai_anomaly
from dashboard import show_dashboard
from packet_sniffer import start_packet_sniffing


running = False
captured_logs = []

protocol_stats = defaultdict(int)
ip_traffic_stats = defaultdict(int)


def analyze_packet(packet):
    global running

    if not running:
        return

    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        packet_size = len(packet)

        protocol = "OTHER"
        app_protocol = "Unknown"

        if TCP in packet:
            protocol = "TCP"

            if packet[TCP].dport == 443:
                app_protocol = "HTTPS"

            elif packet[TCP].dport == 80:
                app_protocol = "HTTP"

        elif UDP in packet:
            protocol = "UDP"

            if packet[UDP].dport == 53:
                app_protocol = "DNS"

        elif ICMP in packet:
            protocol = "ICMP"

        # AI Detection
        ai_result = detect_ai_anomaly(
            packet_size
        )

        # Statistics
        protocol_stats[protocol] += 1
        ip_traffic_stats[src_ip] += 1

        log = (
            f"[{protocol}] "
            f"{src_ip} → {dst_ip} "
            f"| {app_protocol} "
            f"| AI: {ai_result}"
        )

        captured_logs.append(
            [
                protocol,
                src_ip,
                dst_ip,
                app_protocol,
                ai_result
            ]
        )

        packet_box.insert(
            tk.END,
            log + "\n"
        )

        packet_box.see(tk.END)

        # AI Alert
        if ai_result == "⚠ Suspicious":
            alert_box.insert(
                tk.END,
                f"🚨 AI ALERT: "
                f"Suspicious packet "
                f"from {src_ip}\n"
            )

            alert_box.see(
                tk.END
            )

        # High Traffic Alert
        if ip_traffic_stats[src_ip] in [
            100, 250, 500
        ]:
            alert_box.insert(
                tk.END,
                f"⚠ High Traffic: "
                f"{src_ip} "
                f"({ip_traffic_stats[src_ip]} packets)\n"
            )

            alert_box.see(
                tk.END
            )


def sniff_packets():
    start_packet_sniffing(
        analyze_packet
    )


def start_sniffing():
    global running

    if running:
        return

    running = True

    status_label.config(
        text="Status: Running",
        fg="green"
    )

    thread = Thread(
        target=sniff_packets,
        daemon=True
    )

    thread.start()


def stop_sniffing():
    global running

    running = False

    status_label.config(
        text="Status: Stopped",
        fg="red"
    )


def clear_logs():
    packet_box.delete(
        1.0,
        tk.END
    )

    alert_box.delete(
        1.0,
        tk.END
    )


def export_logs():
    if not captured_logs:
        messagebox.showwarning(
            "No Data",
            "No logs to export."
        )
        return

    df = pd.DataFrame(
        captured_logs,
        columns=[
            "Protocol",
            "Source IP",
            "Destination IP",
            "Application Protocol",
            "AI Result"
        ]
    )

    df.to_csv(
        "exports/packet_logs.csv",
        index=False
    )

    messagebox.showinfo(
        "Success",
        "Logs exported to exports/packet_logs.csv"
    )


def open_dashboard():
    show_dashboard(
        protocol_stats,
        ip_traffic_stats
    )


# ---------------- GUI ---------------- #
root = tk.Tk()

root.title(
    "AI Network Packet Analyzer"
)

root.geometry(
    "1000x700"
)

tk.Label(
    root,
    text="AI Network Packet Analyzer",
    font=("Arial", 20, "bold")
).pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack()

buttons = [
    ("Start", start_sniffing),
    ("Stop", stop_sniffing),
    ("Dashboard", open_dashboard),
    ("Export Logs", export_logs),
    ("Clear Logs", clear_logs)
]

for i, (text, cmd) in enumerate(buttons):
    tk.Button(
        button_frame,
        text=text,
        command=cmd,
        width=18
    ).grid(
        row=0,
        column=i,
        padx=5
    )

status_label = tk.Label(
    root,
    text="Status: Stopped",
    fg="red",
    font=("Arial", 12)
)

status_label.pack(
    pady=10
)

tk.Label(
    root,
    text="Live Packet Logs",
    font=("Arial", 12, "bold")
).pack()

packet_box = scrolledtext.ScrolledText(
    root,
    width=120,
    height=18
)

packet_box.pack(
    padx=10,
    pady=5
)

tk.Label(
    root,
    text="Security + AI Alerts",
    font=("Arial", 12, "bold")
).pack()

alert_box = scrolledtext.ScrolledText(
    root,
    width=120,
    height=8
)

alert_box.pack(
    padx=10,
    pady=5
)

if __name__ == "__main__":
    root.mainloop()