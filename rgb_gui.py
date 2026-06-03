import sys
import serial
import sqlite3
from collections import deque
from datetime import datetime, timedelta

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QFrame, QGraphicsDropShadowEffect, QPushButton,
    QComboBox, QFileDialog
)

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QFont

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates

# =========================================================
# DATABASE SETUP
# =========================================================

def init_db():
    conn = sqlite3.connect('rgb_history.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rgb_data (
            timestamp TEXT,
            red INTEGER,
            green INTEGER,
            blue INTEGER
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# =========================================================
# UART CONNECTION
# =========================================================

try:
    ser = serial.Serial('COM4', 115200, timeout=0.1)
except Exception as e:
    print("UART ERROR :", e)
    ser = None

# =========================================================
# MAIN GUI
# =========================================================

class SmartRGBMonitor(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("SMART RGB MONITOR")
        self.setGeometry(100, 100, 1500, 900)

        self.setStyleSheet("""
            QWidget{
                background-color:#050816;
                color:white;
                font-family:Bahnschrift;
            }
        """)

        self.r = 0
        self.g = 0
        self.b = 0

        self.live_red = deque([0]*40, maxlen=40)
        self.live_green = deque([0]*40, maxlen=40)
        self.live_blue = deque([0]*40, maxlen=40)

        main_layout = QVBoxLayout()

        # =====================================================
        # TITLE
        # =====================================================

        title = QLabel("SMART RGB MONITOR")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Bahnschrift", 30))
        title.setStyleSheet("""
            color:#00e5ff;
            font-weight:bold;
        """)

        main_layout.addWidget(title)

        # =====================================================
        # RGB CARDS
        # =====================================================

        card_layout = QHBoxLayout()

        self.red_card = self.create_card("RED", "#ff3b3b")
        self.green_card = self.create_card("GREEN", "#00ff88")
        self.blue_card = self.create_card("BLUE", "#009dff")

        card_layout.addWidget(self.red_card)
        card_layout.addWidget(self.green_card)
        card_layout.addWidget(self.blue_card)

        main_layout.addLayout(card_layout)

        # =====================================================
        # COLOR BOX
        # =====================================================

        self.color_box = QFrame()
        self.color_box.setFixedHeight(120)

        self.color_box.setStyleSheet("""
            background-color:black;
            border:3px solid #00e5ff;
            border-radius:25px;
        """)

        self.add_glow(self.color_box, "#00e5ff")

        main_layout.addWidget(self.color_box)

        # =====================================================
        # STATUS
        # =====================================================

        info_layout = QHBoxLayout()

        self.dom_label = QLabel("DOMINANT : NONE")

        self.dom_label.setFont(QFont("Bahnschrift", 20))

        self.dom_label.setStyleSheet("""
            background-color:#111827;
            color:#00e5ff;
            padding:15px;
            border-radius:15px;
            border:2px solid #00e5ff;
        """)

        self.action_label = QLabel("Hardware Action : Waiting...")

        self.action_label.setFont(QFont("Bahnschrift", 18))

        self.action_label.setStyleSheet("""
            color:#ff66cc;
        """)

        info_layout.addWidget(self.dom_label)
        info_layout.addWidget(self.action_label)

        main_layout.addLayout(info_layout)

        # =====================================================
        # CONTROLS
        # =====================================================

        control_layout = QHBoxLayout()

        filter_label = QLabel("View Mode:")
        filter_label.setFont(QFont("Bahnschrift", 14))

        control_layout.addWidget(filter_label)

        self.time_filter = QComboBox()

        self.time_filter.addItems([
            "Live Stream",
            "Last 2 Hours",
            "Last 3 Days",
            "Last 5 Days"
        ])

        self.time_filter.setFont(QFont("Bahnschrift", 14))

        self.time_filter.setStyleSheet("""
            background-color:#111827;
            color:white;
            border:1px solid #00e5ff;
            padding:5px;
            border-radius:5px;
        """)

        self.time_filter.currentTextChanged.connect(
            self.on_filter_changed
        )

        control_layout.addWidget(self.time_filter)

        control_layout.addStretch()

        export_btn = QPushButton("Export CSV")

        export_btn.setFont(QFont("Bahnschrift", 14))

        export_btn.setStyleSheet("""
            QPushButton{
                background-color:#00e5ff;
                color:black;
                font-weight:bold;
                border-radius:10px;
                padding:8px 20px;
            }

            QPushButton:hover{
                background-color:#00b2cc;
            }
        """)

        export_btn.clicked.connect(self.export_to_csv)

        control_layout.addWidget(export_btn)

        main_layout.addLayout(control_layout)

        # =====================================================
        # GRAPH
        # =====================================================

        graph_frame = QFrame()

        graph_frame.setStyleSheet("""
            background-color:#081120;
            border:2px solid #00e5ff;
            border-radius:20px;
        """)

        self.add_glow(graph_frame, "#00e5ff")

        graph_layout = QVBoxLayout()

        self.graph_title = QLabel("LIVE RGB ANALYTICS")

        self.graph_title.setAlignment(Qt.AlignCenter)

        self.graph_title.setFont(QFont("Bahnschrift", 22))

        self.graph_title.setStyleSheet("""
            color:#00e5ff;
        """)

        graph_layout.addWidget(self.graph_title)

        self.figure = Figure(facecolor="#081120")

        self.canvas = FigureCanvas(self.figure)

        self.ax = self.figure.add_subplot(111)

        graph_layout.addWidget(self.canvas)

        graph_frame.setLayout(graph_layout)

        main_layout.addWidget(graph_frame)

        self.setLayout(main_layout)

        # =====================================================
        # TIMERS
        # =====================================================

        self.db_timer = QTimer()
        self.db_timer.timeout.connect(self.log_to_database)
        self.db_timer.start(1000)

        self.gui_timer = QTimer()
        self.gui_timer.timeout.connect(self.update_gui)
        self.gui_timer.start(100)

    # =====================================================
    # RGB CARD
    # =====================================================

    def create_card(self, title, color):

        frame = QFrame()

        frame.setFixedHeight(120)

        frame.setStyleSheet(f"""
            background-color:#111827;
            border:3px solid {color};
            border-radius:25px;
        """)

        self.add_glow(frame, color)

        layout = QVBoxLayout()

        label = QLabel(title)

        label.setAlignment(Qt.AlignCenter)

        label.setFont(QFont("Bahnschrift", 18))

        label.setStyleSheet(f"""
            color:{color};
            font-weight:bold;
        """)

        value = QLabel("0")

        value.setAlignment(Qt.AlignCenter)

        value.setFont(QFont("Bahnschrift", 30))

        value.setStyleSheet("""
            color:white;
            font-weight:bold;
        """)

        layout.addWidget(label)
        layout.addWidget(value)

        frame.setLayout(layout)

        frame.value_label = value

        return frame

    # =====================================================
    # GLOW
    # =====================================================

    def add_glow(self, widget, color):

        glow = QGraphicsDropShadowEffect()

        glow.setBlurRadius(25)

        glow.setColor(QColor(color))

        glow.setOffset(0)

        widget.setGraphicsEffect(glow)

    # =====================================================
    # FILTER
    # =====================================================

    def on_filter_changed(self, text):

        if text == "Live Stream":
            self.graph_title.setText("LIVE RGB ANALYTICS")
        else:
            self.graph_title.setText(
                f"HISTORICAL ANALYTICS ({text.upper()})"
            )

    # =====================================================
    # DATABASE LOG
    # =====================================================

    def log_to_database(self):

        conn = sqlite3.connect('rgb_history.db')

        cursor = conn.cursor()

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "INSERT INTO rgb_data VALUES (?, ?, ?, ?)",
            (now, self.r, self.g, self.b)
        )

        conn.commit()
        conn.close()

    # =====================================================
    # MAIN UPDATE LOOP
    # =====================================================

    def update_gui(self):

        # UART RECEIVE

        if ser and ser.in_waiting:

            try:
                line = ser.readline().decode().strip()

                if line:

                    values = line.split(",")

                    if len(values) == 3:

                        self.r = int(values[0])
                        self.g = int(values[1])
                        self.b = int(values[2])

            except:
                pass

        r_display = min(max(self.r, 0), 255)
        g_display = min(max(self.g, 0), 255)
        b_display = min(max(self.b, 0), 255)

        # UPDATE CARDS

        self.red_card.value_label.setText(str(self.r))
        self.green_card.value_label.setText(str(self.g))
        self.blue_card.value_label.setText(str(self.b))

        # COLOR PREVIEW BOX

        self.color_box.setStyleSheet(f"""
            background-color: rgb(
                {r_display},
                {g_display},
                {b_display}
            );

            border:3px solid #00e5ff;
            border-radius:25px;
        """)

        # =====================================================
        # DOMINANT COLOR DETECTION
        # =====================================================

        max_val = max(self.r, self.g, self.b)

        tolerance = 15

        # WHITE

        if (
            abs(self.r - self.g) <= tolerance and
            abs(self.r - self.b) <= tolerance and
            abs(self.g - self.b) <= tolerance and
            max_val > 40
        ):

            dominant = "WHITE"

            action = "RED ON   GREEN ON   BLUE ON"

            color = "#ffffff"

        # NO LIGHT

        elif max_val < 10:

            dominant = "NONE"

            action = "WAITING..."

            color = "#00e5ff"

        # RED

        elif self.r >= self.g and self.r >= self.b:

            dominant = "RED"

            action = "GREEN ON   BLUE ON"

            color = "#ff3b3b"

        # GREEN

        elif self.g >= self.r and self.g >= self.b:

            dominant = "GREEN"

            action = "RED ON   BLUE ON"

            color = "#00ff88"

        # BLUE

        else:

            dominant = "BLUE"

            action = "RED ON   GREEN ON"

            color = "#009dff"

        self.dom_label.setText(
            f"DOMINANT : {dominant}"
        )

        self.dom_label.setStyleSheet(f"""
            background-color:#111827;
            color:{color};
            padding:15px;
            border-radius:15px;
            border:2px solid {color};
        """)

        self.action_label.setText(
            f"Hardware Action : {action}"
        )

        # =====================================================
        # GRAPH
        # =====================================================

        current_view = self.time_filter.currentText()

        self.ax.clear()

        self.ax.set_facecolor("#081120")

        if current_view == "Live Stream":

            self.live_red.append(r_display)
            self.live_green.append(g_display)
            self.live_blue.append(b_display)

            self.ax.plot(
                list(self.live_red),
                color="#ff3b3b",
                linewidth=3,
                label="RED"
            )

            self.ax.plot(
                list(self.live_green),
                color="#00ff88",
                linewidth=3,
                label="GREEN"
            )

            self.ax.plot(
                list(self.live_blue),
                color="#009dff",
                linewidth=3,
                label="BLUE"
            )

            self.ax.set_xlabel(
                "Recent Rolling Samples",
                color="white"
            )

            self.ax.set_ylim(0, 260)

        else:

            now = datetime.now()

            if current_view == "Last 2 Hours":

                cutoff = now - timedelta(hours=2)

                date_fmt = '%H:%M'

            elif current_view == "Last 3 Days":

                cutoff = now - timedelta(days=3)

                date_fmt = '%b-%d %H:%M'

            else:

                cutoff = now - timedelta(days=5)

                date_fmt = '%b-%d'

            conn = sqlite3.connect('rgb_history.db')

            cursor = conn.cursor()

            cursor.execute("""
                SELECT timestamp, red, green, blue
                FROM rgb_data
                WHERE timestamp >= ?
                ORDER BY timestamp ASC
            """, (cutoff.strftime("%Y-%m-%d %H:%M:%S"),))

            rows = cursor.fetchall()

            conn.close()

            if rows:

                timestamps = [
                    datetime.strptime(
                        r[0],
                        "%Y-%m-%d %H:%M:%S"
                    )
                    for r in rows
                ]

                red_hist = [r[1] for r in rows]
                green_hist = [r[2] for r in rows]
                blue_hist = [r[3] for r in rows]

                self.ax.plot(
                    timestamps,
                    red_hist,
                    color="#ff3b3b",
                    linewidth=2,
                    label="RED"
                )

                self.ax.plot(
                    timestamps,
                    green_hist,
                    color="#00ff88",
                    linewidth=2,
                    label="GREEN"
                )

                self.ax.plot(
                    timestamps,
                    blue_hist,
                    color="#009dff",
                    linewidth=2,
                    label="BLUE"
                )

                self.ax.xaxis.set_major_formatter(
                    mdates.DateFormatter(date_fmt)
                )

                self.figure.autofmt_xdate(
                    bottom=0.2,
                    rotation=30,
                    ha='right'
                )

                self.ax.set_ylim(0, 260)

        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')

        self.ax.spines['bottom'].set_color('#00e5ff')
        self.ax.spines['left'].set_color('#00e5ff')

        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

        legend = self.ax.legend(loc="upper right")

        if legend:

            for text in legend.get_texts():
                text.set_color("white")

        self.canvas.draw()

    # =====================================================
    # EXPORT CSV
    # =====================================================

    def export_to_csv(self):

        options = QFileDialog.Options()

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export RGB Log Data",
            "",
            "CSV Files (*.csv)"
        )

        if filename:

            if not filename.endswith(".csv"):
                filename += ".csv"

            conn = sqlite3.connect('rgb_history.db')

            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM rgb_data
                ORDER BY timestamp DESC
            """)

            rows = cursor.fetchall()

            conn.close()

            with open(filename, 'w') as f:

                f.write(
                    "Timestamp,Red,Green,Blue\n"
                )

                for row in rows:

                    f.write(
                        f"{row[0]},{row[1]},{row[2]},{row[3]}\n"
                    )

            print("CSV EXPORTED")

# =========================================================
# RUN
# =========================================================

if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = SmartRGBMonitor()

    window.show()

    sys.exit(app.exec())