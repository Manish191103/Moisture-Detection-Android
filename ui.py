import sys
import platform
import time
import os
from rich.console import Console
from rich.panel import Panel

console = Console()

# Detect platform and import appropriate serial library
is_android = hasattr(sys, 'getandroidapilevel') or 'ANDROID_ROOT' in os.environ

if is_android:
    try:
        import usbserial4a
        from usb4a import usb
        PLATFORM = "android"
    except ImportError:
        print("Android detected but usbserial4a not available. Install with: pip install usbserial4a usb4a")
        sys.exit(1)
else:
    try:
        import serial
        PLATFORM = "desktop"
    except ImportError:
        print("Desktop platform detected but pyserial not available. Install with: pip install pyserial")
        sys.exit(1)

# Configuration
if PLATFORM == "desktop":
    SERIAL_PORT = 'COM3'  # Change this to your Pico's serial port
    BAUDRATE = 115200
else:  # Android
    VENDOR_ID = 0x2E8A  # Raspberry Pi Foundation (Pico)
    PRODUCT_ID = 0x000A # Pico
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
    panel = Panel(
        f"{status_text}\n\n{bar}\n\n{percent_text}\n{depth_text}",
        title="[b]Moisture Sensor Demo[/b]",
        subtitle="Created by Ishan Kaim",
        border_style=color
    )
    console.clear()
    console.print(panel)

def connect_desktop():
    """Connect using pyserial on desktop platforms"""
    try:
        ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
        print(f"Connected to {SERIAL_PORT} at {BAUDRATE} baud")
        return ser
    except serial.SerialException as e:
        print(f"Failed to connect to {SERIAL_PORT}: {e}")
        return None

def connect_android():
    """Connect using usbserial4a on Android"""
    try:
        # Get USB device manager
        usb_manager = usb.get_usb_manager()
        device_list = usb_manager.getDeviceList()
        
        if not device_list:
            print("No USB devices found.")
            return None
        
        # Find our target device
        target_device = None
        for device in device_list.values():
            if (device.getVendorId() == VENDOR_ID and 
                device.getProductId() == PRODUCT_ID):
                target_device = device
                break
        
        if not target_device:
            print(f"Device with VID:PID {VENDOR_ID:04X}:{PRODUCT_ID:04X} not found.")
            print("Available devices:")
            for device in device_list.values():
                print(f"  VID:PID {device.getVendorId():04X}:{device.getProductId():04X}")
            return None

        # Create serial connection
        serial_port = usbserial4a.get_serial_port(
            target_device.getDeviceName(),
            BAUDRATE,
            8,  # data bits
            1,  # stop bits
            0,  # parity
            timeout=1
        )
        
        if serial_port:
            print("Connected via USB serial")
            return serial_port
        else:
            print("Failed to open serial port.")
            return None
            
    except Exception as e:
        print(f"Android connection error: {e}")
        return None

def read_data(connection):
    """Read data from serial connection (cross-platform)"""
    if PLATFORM == "desktop":
        line = connection.readline().decode('utf-8').strip()
        return line
    else:  # Android
        data = connection.readline()
        if data:
            return data.decode('utf-8').strip()
        return ""

def main():
    print(f"Running on {PLATFORM} platform")
    
    # Connect based on platform
    if PLATFORM == "desktop":
        connection = connect_desktop()
    else:
        connection = connect_android()
    
    if not connection:
        return
    
    try:
        while True:
            line = read_data(connection)
            if line and ',' in line:
                try:
                    percent, depth, value = line.split(",")
                    percent = float(percent)
                    depth = int(depth)
                    value = int(value)
                    status = "Wet" if value < 60000 else "Dry"
                    draw_moisture(percent, depth, status)
                except ValueError:
                    print(f"Invalid data format: {line}")
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()
            print("Connection closed.")

if __name__ == "__main__":
    main()