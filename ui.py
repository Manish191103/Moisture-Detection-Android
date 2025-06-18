import serial
from rich.console import Console
from rich.panel import Panel
import time

console = Console()

# Change this to your Pico's serial port (e.g., 'COM3' on Windows, '/dev/ttyACM0' on Linux)
SERIAL_PORT = 'COM3'
BAUDRATE = 115200

def get_icon_and_color(percent):
    if percent > 70:
        return "💧", "blue"
    elif percent > 40:
        return "🪴", "green"
    else:
        return "🌵", "yellow"

def draw_moisture(percent, depth, status):
    icon, color = get_icon_and_color(percent)
    bar_length = 30
    filled = int(bar_length * percent / 100)
    bar = f"[{color}]" + "█" * filled + "[/]" + "─" * (bar_length - filled)
    status_text = f"[bold {color}]{icon} {status}[/bold {color}]"
    percent_text = f"[bold]{percent:.1f}%[/bold] Moisture"
    depth_text = f"Depth: [bold]{depth}/6[/bold]"
    alert_text = ""
    if depth >= 6:
        alert_text = "[bold red blink]CRITICAL: Sensor at maximum depth! Risk of drowning![/bold red blink]\n"
    panel = Panel(
        f"{alert_text}{status_text}\n\n{bar}\n\n{percent_text}\n{depth_text}",
        title="[b]Moisture Sensor Demo[/b]",
        subtitle="Created by Ishan Kaim",
        border_style=color
    )
    console.clear()
    console.print(panel)

with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1) as ser:
    while True:
        line = ser.readline().decode().strip()
        if not line:
            continue
        try:
            percent, depth, value = line.split(",")
            percent = float(percent)
            depth = int(depth)
            value = int(value)
            status = "Wet" if value < 60000 else "Dry"
            draw_moisture(percent, depth, status)
        except Exception as e:
            console.print(f"[red]Error parsing line:[/red] {line} ({e})")
        time.sleep(0.5)