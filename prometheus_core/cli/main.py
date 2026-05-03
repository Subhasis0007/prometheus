import typer
from rich import print
import requests
import json

app = typer.Typer(help="PROMETHEUS - Self-Correcting AI Agent Platform")

DAEMON_URL = "http://127.0.0.1:8000"

@app.command()
def start():
    print("[bold green]Starting PROMETHEUS daemon...[/bold green]")

@app.command()
def stop():
    print("[bold red]Stopping PROMETHEUS daemon...[/bold red]")

@app.command()
def status():
    try:
        r = requests.get(f"{DAEMON_URL}/")
        print("[bold green]PROMETHEUS Status: Running[/bold green]")
    except:
        print("[bold red]PROMETHEUS Status: Not Running[/bold red]")

@app.command()
def chat(message: str):
    try:
        r = requests.post(f"{DAEMON_URL}/chat?message={message}")
        if r.status_code == 200:
            print(f"[bold yellow]PROMETHEUS:[/bold yellow] {r.json()['response']}")
        else:
            print(f"[bold red]Error: {r.text}[/bold red]")
    except Exception as e:
        print(f"[bold red]Error: {e}[/bold red]")

@app.command()
def history():
    """Show agent history and mistakes"""
    try:
        with open("prometheus_state.json", "r") as f:
            state = json.load(f)
        print("[bold cyan]Agent History:[/bold cyan]")
        print(json.dumps(state, indent=2))
    except:
        print("No history available yet.")

if __name__ == "__main__":
    app()
