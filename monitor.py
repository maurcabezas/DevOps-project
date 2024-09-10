# import psutil
# import datetime

# def get_system_metrics():
#     # Fetch CPU, Memory, and Disk Usage
#     cpu_usage = psutil.cpu_percent(interval=1)
#     memory = psutil.virtual_memory()
#     disk = psutil.disk_usage('/')

#     metrics = {
#         'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         'cpu_usage': cpu_usage,
#         'memory_used': memory.used,
#         'memory_total': memory.total,
#         'disk_used': disk.used,
#         'disk_total': disk.total
#     }
#     return metrics

# if __name__ == "__main__":
#     metrics = get_system_metrics()
#     print(metrics)
import sys
import psutil
import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QSpinBox, QLineEdit

class SystemMetrics:
    """Class to encapsulate system metrics gathering."""
    
    def __init__(self):
        self.update_interval = 1  # Default update interval in seconds

    def get_metrics(self):
        """Fetches the system metrics."""
        cpu_usage = psutil.cpu_percent(interval=self.update_interval)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        num_processors = psutil.cpu_count()
        wifi = psutil.net_if_addrs().get('Wi-Fi', None)
        
        wifi_status = "Connected" if wifi else "Not Connected"

        metrics = {
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'cpu_usage': cpu_usage,
            'memory_used': memory.used,
            'memory_total': memory.total,
            'disk_used': disk.used,
            'disk_total': disk.total,
            'num_processors': num_processors,
            'wifi_status': wifi_status
        }
        return metrics

    def display_metrics(self):
        """Displays the metrics line by line in the terminal."""
        metrics = self.get_metrics()
        for key, value in metrics.items():
            print(f"{key}: {value}")


class MetricsGUI(QWidget):
    """PyQt5 GUI for displaying system metrics."""
    
    def __init__(self, metrics_obj):
        super().__init__()
        self.metrics_obj = metrics_obj
        self.initUI()

    def initUI(self):
        self.setWindowTitle('System Metrics Monitor')
        self.layout = QVBoxLayout()

        self.metrics_labels = {}
        for key in ['timestamp', 'cpu_usage', 'memory_used', 'memory_total', 'disk_used', 'disk_total', 'num_processors', 'wifi_status']:
            label = QLabel(f"{key}: ")
            self.metrics_labels[key] = label
            self.layout.addWidget(label)

        # Add scan interval input
        self.interval_input = QSpinBox()
        self.interval_input.setValue(1)
        self.interval_input.setMinimum(1)
        self.interval_input.setSuffix(" s")
        self.interval_input.valueChanged.connect(self.update_interval)
        self.layout.addWidget(QLabel("Scan Interval:"))
        self.layout.addWidget(self.interval_input)

        # Add Update button
        self.update_button = QPushButton('Update Values')
        self.update_button.clicked.connect(self.update_metrics)
        self.layout.addWidget(self.update_button)

        # Add Quit button
        self.quit_button = QPushButton('Quit')
        self.quit_button.clicked.connect(self.close)
        self.layout.addWidget(self.quit_button)

        self.setLayout(self.layout)
        self.update_metrics()  # Initial display

    def update_metrics(self):
        """Updates the metrics displayed in the GUI."""
        metrics = self.metrics_obj.get_metrics()
        for key, label in self.metrics_labels.items():
            label.setText(f"{key}: {metrics[key]}")

    def update_interval(self):
        """Updates the interval for scanning the metrics."""
        self.metrics_obj.update_interval = self.interval_input.value()


if __name__ == "__main__":
    metrics = SystemMetrics()

    if '-u' in sys.argv:  # Launch PyQt5 GUI
        app = QApplication(sys.argv)
        gui = MetricsGUI(metrics)
        gui.show()
        sys.exit(app.exec_())
    else:  # Run in terminal mode
        metrics.display_metrics()
