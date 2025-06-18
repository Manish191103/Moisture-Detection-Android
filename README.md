# Pico Moisture Sensor Project

This project provides a complete solution for reading soil moisture data from a sensor connected to a Raspberry Pi Pico and visualizing it on your PC using a rich terminal UI.

## Features
- **Pico-side script** (`sensortest.py`): Reads moisture sensor data and outputs it over serial.
- **PC-side UI** (`ui.py`): Reads serial data from the Pico and displays a live, color-coded moisture bar with alerts.

---

## Requirements
- **Hardware:**
  - Raspberry Pi Pico
  - Soil moisture sensor (analog output)
  - Jumper wires
- **Software:**
  - Python 3.12+
  - [mpremote](https://github.com/micropython/micropython/tree/master/tools/mpremote)
  - [pyserial](https://pyserial.readthedocs.io/en/latest/)
  - [rich](https://rich.readthedocs.io/en/stable/)

Install dependencies:
```bash
pip install mpremote pyserial rich
```

---

## Setup
### 1. Flashing the Pico
- Connect your Pico to your PC.
- Use `mpremote` or Thonny to copy `sensortest.py` to the Pico.

### 2. Wiring
- Connect the moisture sensor's analog output to GP26 (ADC0) on the Pico.

### 3. Running the Sensor Script
- On the Pico, run `sensortest.py` (it will continuously output moisture readings over serial).

### 4. Running the UI on PC
- Edit `SERIAL_PORT` in `ui.py` to match your Pico's port (e.g., `COM3` on Windows, `/dev/ttyACM0` on Linux).
- Run:
  ```bash
  python ui.py
  ```
- You should see a live moisture bar and alerts in your terminal.

---

## File Descriptions
- `sensortest.py`: MicroPython script for the Pico. Reads analog values, converts to percent, and prints as CSV.
- `ui.py`: Python script for PC. Reads serial data, parses, and displays a rich UI.
- `pyproject.toml`: Project metadata and dependencies.

---

## Troubleshooting
- **Serial port not found:** Double-check the `SERIAL_PORT` in `ui.py` and your OS device manager.
- **No data in UI:** Ensure the Pico is running `sensortest.py` and is properly connected.
- **Permission errors:** On Linux, you may need to add your user to the `dialout` group or use `sudo`.

---

## License
MIT

---

## Credits
- UI by Ishan Kaim
