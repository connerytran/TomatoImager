
import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, 
                             QWidget, QVBoxLayout, QPushButton, QMessageBox)
from PyQt5.QtGui import QIcon, QFont


PI_IP_ADDRESS = "192.168.30.119"
PI_PORT = 5000


class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("HAWKEYE GUI")
    self.setGeometry(700, 300, 500, 500)
    self.initUI()
    # self.setWindowIcon(QIcon("pic.jpg"))

    # label = QLabel("Hello", self)
    # label.setFont(QFont("Arial", 40))
    # label.setGeometry(0, 0, 500, 100)
    # label.setStyleSheet("color: blue;")

  def initUI(self):
    central_widget = QWidget()
    self.setCentralWidget(central_widget)
    layout = QVBoxLayout()
    central_widget.setLayout(layout)

    self.pi_status_label = QLabel("Pi3 - Steve: UNAVAILABLE")
    layout.addWidget(self.pi_status_label)

    self.pic_button = QPushButton("Take pictures")
    self.pic_button.clicked.connect(self.hawkeye_capture_req)
    layout.addWidget(self.pic_button)

    self.stop_button = QPushButton("Stop pictures")
    self.stop_button.clicked.connect(self.hawkeye_stop_req)
    layout.addWidget(self.stop_button)


    self.output_label = QLabel("Click the button to start taking pictures.")
    layout.addWidget(self.output_label)

    self.check_status()





  def hawkeye_capture_req(self):
    """Sends a POST request to the Raspberry Pi to start taking pictures."""
    url = f"http://{PI_IP_ADDRESS}:{PI_PORT}/take_pictures"
    
    self.output_label.setText("Sending request to Pi...")
    self.pic_button.setEnabled(False) # Disable the button during the request

    try:
      # The requests.post() function sends an HTTP POST request
      response = requests.post(url, timeout=10) # Set a 10-second timeout
      
      # Check for a successful HTTP status code (200-299)
      if response.status_code == 200:
        result = response.json()
        self.output_label.setText(f"SUCCESS: {result.get('message')}")
      else:
        # Handle non-200 status codes (e.g., 500 server error)
        result = response.json()
        error_message = result.get('message', 'Unknown error occurred.')
        self.output_label.setText(f"ERROR: {error_message}")
        QMessageBox.warning(self, "API Error", f"The server returned an error: {error_message}")

    except requests.exceptions.RequestException as e:
      # Handle network errors (Pi is off, wrong IP, etc.)
      self.output_label.setText(f"ERROR: Could not connect to the Pi.")
      QMessageBox.critical(self, "Network Error", f"Failed to connect to the Raspberry Pi: {e}")

    finally:
      self.pic_button.setEnabled(True) # Re-enable the button



  def hawkeye_stop_req(self):
    """Sends a POST request to the Raspberry Pi to stop taking pictures."""
    url = f"http://{PI_IP_ADDRESS}:{PI_PORT}/stop_pictures"
    
    self.output_label.setText("Sending request to Pi...")
    self.stop_button.setEnabled(False) # Disable the button during the request

    try:
      # The requests.post() function sends an HTTP POST request
      response = requests.post(url, timeout=10) # Set a 10-second timeout
      
      # Check for a successful HTTP status code (200-299)
      if response.status_code == 200:
        result = response.json()
        self.output_label.setText(f"SUCCESS: {result.get('message')}")
      else:
        # Handle non-200 status codes (e.g., 500 server error)
        result = response.json()
        error_message = result.get('message', 'Unknown error occurred.')
        self.output_label.setText(f"ERROR: {error_message}")
        QMessageBox.warning(self, "API Error", f"The server returned an error: {error_message}")

    except requests.exceptions.RequestException as e:
      # Handle network errors (Pi is off, wrong IP, etc.)
      self.output_label.setText(f"ERROR: Could not connect to the Pi.")
      QMessageBox.critical(self, "Network Error", f"Failed to connect to the Raspberry Pi: {e}")

    finally:
      self.stop_button.setEnabled(True) # Re-enable the button



  def check_status(self):
    """Sends a GET request to pi to see if is available"""
    url = f"http://{PI_IP_ADDRESS}:{PI_PORT}/status"
    self.output_label.setText("Checking status...")
    
    try:
      response = requests.get(url, timeout=10)

      if response.status_code == 200:
        result = response.json()
        self.output_label.setText(f"SUCCESS: {result.get('message')}")
        self.pi_status_label.setText("Pi3 - Steve: AVAILABLE")
      else:
        # Handle non-200 status codes (e.g., 500 server error)
        result = response.json()
        error_message = result.get('message', 'Unknown error occurred.')
        self.output_label.setText(f"ERROR: {error_message}")
        QMessageBox.warning(self, "API Error", f"The server returned an error: {error_message}")

    except requests.exceptions.RequestException as e:
      # Handle network errors (Pi is off, wrong IP, etc.)
      self.output_label.setText(f"ERROR: Could not connect to the Pi.")
      QMessageBox.critical(self, "Network Error", f"Failed to connect to the Raspberry Pi: {e}")



def main():
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec_())




if __name__ == "__main__":
  main()