import matplotlib.pyplot as plt


def show_dashboard(
    protocol_stats,
    ip_traffic_stats
):
    plt.figure(
        "Protocol Distribution"
    )

    plt.pie(
        protocol_stats.values(),
        labels=protocol_stats.keys(),
        autopct="%1.1f%%"
    )

    plt.title(
        "Protocol Distribution"
    )

    top_ips = sorted(
        ip_traffic_stats.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    ips = [x[0] for x in top_ips]
    counts = [x[1] for x in top_ips]

    plt.figure(
        "Top Traffic IPs"
    )

    plt.bar(
        ips,
        counts
    )

    plt.title(
        "Top Traffic IPs"
    )

    plt.xticks(rotation=20)

    plt.show()

