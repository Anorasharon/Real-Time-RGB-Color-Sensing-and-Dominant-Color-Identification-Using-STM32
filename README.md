<div align="center">

# 🌈 Real-Time RGB Color Sensing and Dominant Color Identification

### Embedded Systems Project | STM32F446RE • TCS34725 • UART • RS485 • PyQt5

<img src="https://readme-typing-svg.herokuapp.com?font=Poppins&weight=600&size=24&pause=1000&color=36BCF7&center=true&vCenter=true&width=850&lines=STM32F446RE+Based+RGB+Color+Detection;I2C+Sensor+Interfacing+with+TCS34725;UART+and+RS485+Industrial+Communication;Real-Time+Embedded+Firmware+Development" />

<br>

![STM32](https://img.shields.io/badge/STM32F446RE-Microcontroller-03234B?style=for-the-badge&logo=stmicroelectronics&logoColor=white)
![Embedded C](https://img.shields.io/badge/Embedded_C-00599C?style=for-the-badge&logo=c&logoColor=white)
![I2C](https://img.shields.io/badge/I2C-Communication-1E88E5?style=for-the-badge)
![UART](https://img.shields.io/badge/UART-Communication-43A047?style=for-the-badge)
![RS485](https://img.shields.io/badge/RS485-Industrial_Bus-F57C00?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-HMI_GUI-41CD52?style=for-the-badge&logo=qt&logoColor=white)

</div>

---

# 🚀 Overview

This project implements a real-time Embedded RGB Color Detection and Monitoring System using the STM32F446RE microcontroller and the TCS34725 RGB color sensor.

The STM32 acquires Red, Green, Blue, and Clear channel values through the I2C communication protocol and performs real-time color processing. The RGB values are normalized using the Clear channel to reduce ambient light dependency and improve detection accuracy. The processed values are analyzed to identify the dominant color of the target object.

The system supports both UART communication and RS485 industrial communication using the MAX13487 transceiver. UART is used for direct serial monitoring, while RS485 enables reliable long-distance communication with improved noise immunity. A PyQt5-based desktop application provides real-time visualization, database logging, graphical analysis, and CSV export functionality.

---

# ✨ Key Features

- Real-Time RGB Color Detection
- Dominant Color Classification
- TCS34725 Sensor Interfacing using I2C
- Embedded C Firmware Development
- UART Communication
- RS485 Industrial Communication
- GPIO-Based RGB LED Control
- PyQt5 GUI Monitoring
- SQLite Database Logging
- Live RGB Graph Visualization
- Historical Data Analysis
- CSV Export Support

---

# 🔧 Hardware Components

| Component | Purpose |
|------------|------------|
| STM32F446RE Nucleo Board | Main Processing Unit |
| TCS34725 RGB Color Sensor | RGB and Clear Light Sensing |
| RGB LEDs | Visual Color Indication |
| MAX13487 RS485 Module | UART to RS485 Conversion |
| PC/Laptop | GUI Monitoring |
| Jumper Wires | Hardware Interconnections |
| USB Power Supply | System Power |

---

# 🔌 Hardware Connections

## TCS34725 RGB Sensor

| TCS34725 Pin | STM32F446RE Pin |
|-------------|-----------------|
| VIN | 3.3V |
| GND | GND |
| SDA | PB9 |
| SCL | PB8 |

## RGB LEDs

| RGB LED Pin | STM32 Pin |
|-------------|------------|
| Red | PB6 |
| Green | PB4 |
| Blue | PB10 |

## MAX13487 RS485 Module

| MAX13487 Pin | STM32F446RE Pin |
|--------------|-----------------|
| DI | PA2 (USART2_TX) |
| RO | PA3 (USART2_RX) |
| VCC | 5V |
| GND | GND |

### RS485 Differential Side

| MAX13487 | RS485 Converter |
|-----------|----------------|
| A | A (+) |
| B | B (-) |

---


# 📊 Results

- Successfully detected Red, Green, and Blue colored objects.
- Performed RGB normalization using the Clear channel.
- Verified dominant color classification through RGB LED indication.
- Successfully transmitted sensor data through UART communication.
- Successfully transmitted sensor data through RS485 communication using MAX13487.
- Displayed RGB values in real time using a PyQt5 GUI.
- Logged data into an SQLite database.
- Exported historical records to CSV format.

---

# 🛠 Software Stack

### Embedded Side

- STM32CubeIDE
- Embedded C
- STM32 HAL Drivers
- I2C Communication
- UART Communication
- RS485 Communication

### Desktop Side

- Python
- PyQt5
- PySerial
- SQLite3
- Matplotlib

---

# 🎯 Applications

- Industrial Color Sorting Systems
- Product Quality Inspection
- Robotics and Automation
- Smart Manufacturing
- Embedded Monitoring Systems
- Industrial Communication Demonstrations
- Educational and Research Applications

---

# 👨‍💻 Author

### Anora Sharon Tessie S

Electronics and Communication Engineering

**Embedded Systems • AIML**

---

⭐ If you found this project useful, consider giving it a star.
