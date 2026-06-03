<div align="center">

# 🌈 Real-Time RGB Color Sensing and Dominant Color Identification

### Using STM32F446RE • TCS34725 • RS485 • PyQt5

<img src="https://readme-typing-svg.herokuapp.com?font=Poppins&weight=600&size=24&pause=1000&color=36BCF7&center=true&vCenter=true&width=700&lines=Real-Time+RGB+Color+Detection;STM32F446RE+%2B+TCS34725;RS485+Communication;PyQt5+GUI+Monitoring" />

<br>

![STM32](https://img.shields.io/badge/STM32F446RE-03234B?style=for-the-badge&logo=stmicroelectronics&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![RS485](https://img.shields.io/badge/RS485-FF6F00?style=for-the-badge)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

</div>

---

# 🚀 Overview

This project implements a real-time RGB color detection system using the STM32F446RE microcontroller and TCS34725 RGB color sensor.

The system:

✅ Detects RGB values in real time

✅ Identifies dominant color

✅ Communicates using UART and RS485

✅ Visualizes data using a PyQt5 GUI

✅ Stores readings in SQLite database

✅ Generates live RGB graphs

---

# 🏗 Hardware Architecture

```text
🎨 Colored Object
        │
        ▼
🌈 TCS34725 Sensor
        │ I2C
        ▼
🔵 STM32F446RE
        │ UART
        ▼
🔄 MAX13487 RS485
        │
        ▼
🖥 PyQt5 GUI
        │
        ├── RGB Monitor
        ├── Color Preview
        ├── Live Graphs
        ├── Database Logging
        └── CSV Export
```

# 🔧 Hardware Components

| Component | Purpose |
|------------|------------|
| 🔵 STM32F446RE | Main Controller |
| 🌈 TCS34725 | RGB Color Detection |
| 💡 RGB LEDs | Color Indication |
| 🔄 MAX13487 | UART to RS485 Conversion |
| 🖥 PC/Laptop | GUI Monitoring |
| ⚡ Power Supply | System Power |

# 📸 Project Images

<p align="center">
  <img src="Images/setup.jpg" width="600">
</p>

<p align="center">
  <img src="Images/gui.png" width="700">
</p>

# 📊 Features

- 🌈 RGB Detection
- ⚡ Real-Time Monitoring
- 📡 UART Communication
- 🔄 RS485 Communication
- 🗄 SQLite Logging
- 📈 Live Graphs
- 📁 CSV Export
- 🎯 Dominant Color Detection

# 👨‍💻 Author

### Anora Sharon Tessie S

Electronics and Communication Engineering

Embedded Systems • IoT • AI/ML
