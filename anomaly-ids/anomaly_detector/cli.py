import click
from .pipeline import run_all, run_logs, run_pcap, run_features, run_predict, run_report
from .live_capture import start_live_capture

@click.group()
def cli():
    """Anomaly Detection CLI Tool"""
    pass

@cli.command()
def run():
    """Run the full pipeline"""
    run_all()

@cli.command()
def logs():
    """Run log preprocessing"""
    run_logs()

@cli.command()
def pcap():
    """Extract PCAP features"""
    run_pcap()

@cli.command()
def features():
    """Build ML-ready dataset"""
    run_features()

@cli.command()
def predict():
    """Run ML anomaly predictions"""
    run_predict()

@cli.command()
def report():
    """Generate HTML anomaly report"""
    run_report()

@cli.command()
@click.option("--iface", default="en0", help="Network interface to capture from")
def live(iface):
    """Run real-time anomaly detection from live packet capture."""
    start_live_capture(interface=iface)

if __name__ == "__main__":
    cli()
