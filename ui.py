import usbserial4a
from rich.console import Console
from rich.panel import Panel
import time

console = Console()

# Replace with your device's actual IDs
VENDOR_ID = 0x1234  # e.g., 1027
PRODUCT_ID = 0x5678 # e.g., 24577

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
    panel = Panel(
        f"{status_text}\n\n{bar}\n\n{percent_text}\n{depth_text}",
        title="[b]Moisture Sensor Demo[/b]",
        subtitle="Created by Ishan Kaim",
        border_style=color
    )
    console.clear()
    console.print(panel)

def main():
    device = usbserial4a.get_usb_device(VENDOR_ID, PRODUCT_ID)
    if not device:
        print("No USB device found.")
        return

    with device.serial_port(baudrate=115200) as serial:
        print("Serial port opened successfully.")
        while True:
            data = serial.read(1024)
            if data:
                print(f"Received: {data.decode(errors='ignore')}")
            time.sleep(0.1)

if __name__ == "__main__":
    main()