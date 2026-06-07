from scapy.all import sniff


def start_packet_sniffing(callback):
    sniff(
        prn=callback,
        store=False
    )