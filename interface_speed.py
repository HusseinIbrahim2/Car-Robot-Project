import sqlite3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSerialPort import QSerialPort
from pyqtgraph import PlotWidget, mkPen, AxisItem
from datetime import datetime

class TimeAxisItem(AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLabel(text='Time(HH:mm:ss)', units='s', color=(255, 255, 0), bold=True)

    def tickStrings(self, values, scale, spacing):
        return [datetime.fromtimestamp(value).strftime('%H:%M:%S') for value in values]

class StyledButton(QtWidgets.QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet(
            "QPushButton {"
            "   background-color: #4e6bff;"
            "   border: 2px solid #4e6bff;"
            "   color: #f0f0f0;"
            "   padding: 10px 20px;"
            "   text-align: center;"
            "   font-size: 16px;"
            "   border-radius: 8px;"
            "}"
            "QPushButton:hover {background-color: #3a4da9;}"
            "QPushButton:pressed {background-color: #2e3c80;}"
        )

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(800, 600)
        self.setWindowTitle("Robot speed")
        self.setStyleSheet("background-color: #293955;")
        self.showMaximized()

        self.serial = QSerialPort()
        self.openSerialPort()

        self.graphWidget = PlotWidget(axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.graphWidget.setLabel('left', 'Speed', color=(200, 200, 200))
        
        self.left_curve = self.graphWidget.plot(pen=mkPen(color='lightgray'), name="Left Wheel Speed")
        self.right_curve = self.graphWidget.plot(pen=mkPen(color='lightgray'), name="Right Wheel Speed")
        self.left_data = []
        self.right_data = []
        self.timestamps = []

        self.graphWidget.setBackground('#3c4858')

        self.btn_z = StyledButton('Z')
        self.btn_q = StyledButton('Q')
        self.btn_s = StyledButton('S')
        self.btn_d = StyledButton('D')
        self.btn_c = StyledButton('Automatique')
        self.btn_h = StyledButton('Stop')

        self.text_box = QtWidgets.QLineEdit()
        self.text_box.setStyleSheet("color: white;")
        self.btn_send = StyledButton('Send')

        widget = QtWidgets.QWidget()
        self.setCentralWidget(widget)
        vb = QtWidgets.QVBoxLayout(widget)

        vb.addWidget(self.graphWidget)

        vb_buttons = QtWidgets.QGridLayout()
        vb_buttons.addWidget(self.btn_q, 1, 0)
        vb_buttons.addWidget(self.btn_s, 1, 1)
        vb_buttons.addWidget(self.btn_d, 1, 2)
        vb_buttons.addWidget(self.btn_z, 0, 1)
        vb_buttons.addWidget(self.btn_h, 0, 3)
        vb_buttons.addWidget(self.btn_c, 1, 3)
        vb.addLayout(vb_buttons)

        vb.addWidget(self.text_box)
        vb.addWidget(self.btn_send)

        self.btn_z.clicked.connect(lambda: self.send_text_data('z'))
        self.btn_q.clicked.connect(lambda: self.send_text_data('q'))
        self.btn_s.clicked.connect(lambda: self.send_text_data('s'))
        self.btn_d.clicked.connect(lambda: self.send_text_data('d'))
        self.btn_h.clicked.connect(lambda: self.send_text_data('h'))
        self.btn_c.clicked.connect(lambda: self.send_text_data('c'))
        self.serial.readyRead.connect(self.readData)

        self.btn_send.clicked.connect(self.send)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updatePlot)
        self.timer.start(1000)

        y_axis = self.graphWidget.getAxis('left')
        y_axis.setPen(color=QtGui.QColor(255, 255, 0))
        y_axis.setStyle(tickFont=QtGui.QFont("Arial", weight=QtGui.QFont.Bold))

        x_axis = self.graphWidget.getAxis('bottom')
        x_axis.setPen(color=QtGui.QColor(255, 255, 0))
        x_axis.setStyle(tickFont=QtGui.QFont("Arial", weight=QtGui.QFont.Bold))
        
        self.previous = ''
        self.init_database()
        
    def send(self):
        self.send_text_data(self.previous)

    def init_database(self):
        self.connection = sqlite3.connect("wheel_speeds.db")
        self.cursor = self.connection.cursor()

        # Create table if not exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS wheel_speeds (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                left_speed INTEGER,
                                right_speed INTEGER,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                              )''')
        self.connection.commit()

    def send_data(self, data):
        self.serial.write(data.encode())

    def send_text_data(self,value):
            if self.text_box.text()=='':
                speed = 255
            else:
                speed = int(self.text_box.text())
               
            print(str(value))
            print(speed)
            #QtCore.QTimer.singleShot(50, lambda: self.send_data(chr(0)))
            #QtCore.QTimer.singleShot(100, lambda: self.send_data(chr(0)))
            QtCore.QTimer.singleShot(50, lambda: self.send_data(value))
            QtCore.QTimer.singleShot(100, lambda: self.send_data(chr(speed)))
            #QtCore.QTimer.singleShot(200, lambda: self.send_data(self.previous))
                

    def openSerialPort(self):
        self.serial.setPortName('COM9')
        if not self.serial.open(QtCore.QIODevice.ReadWrite):
            print('Port open error')
        else:
            print('Port opened')
            self.serial.setBaudRate(115200)
            self.serial.setStopBits(1)
            self.serial.setParity(0)
            self.serial.setDataBits(8)
            self.serial.setFlowControl(0)

    def readData(self):
        data = self.serial.readAll().data().decode()
        try:
            speed_left, speed_right = map(int, data.split(','))
            self.left_data.append(speed_left)
            self.right_data.append(speed_right)
            self.timestamps.append(datetime.now().timestamp())

            if speed_left != 0 or speed_right != 0:
                self.cursor.execute("INSERT INTO wheel_speeds (left_speed, right_speed) VALUES (?, ?)", (speed_left, speed_right))
                self.connection.commit()
        except ValueError:
            pass

    def updatePlot(self):
        current_time = datetime.now().timestamp()
        if not self.timestamps or self.timestamps[-1] != current_time:
            if self.left_data and self.right_data:
                self.left_data.append(self.left_data[-1])
                self.right_data.append(self.right_data[-1])
            else:
                self.left_data.append(0)
                self.right_data.append(0)
            self.timestamps.append(current_time)
        if len(self.timestamps) > 1 and self.timestamps[-1] == self.timestamps[-2]:
            return
        self.left_curve.setData(self.timestamps, self.left_data)
        self.right_curve.setData(self.timestamps, self.right_data)
        self.graphWidget.setXRange(current_time - 6, current_time)
        min_y = min(min(self.left_data), min(self.right_data))
        max_y = max(max(self.left_data), max(self.right_data))
        padding = 0.1 * (max_y - min_y)
        self.graphWidget.setYRange(min_y - padding, max_y + padding)

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Z:
            self.pevious='z'
            self.btn_z.click()
            
        elif key == QtCore.Qt.Key_Q:
            self.pevious='q'
            self.btn_q.click()
            
        elif key == QtCore.Qt.Key_S:
            self.pevious='s'
            self.btn_s.click()
            
        elif key == QtCore.Qt.Key_D:
            self.pevious='d'
            self.btn_d.click()
            
        elif key == QtCore.Qt.Key_H:
            self.pevious='h'
            self.btn_h.click()

        elif key == QtCore.Qt.Key_C:
            self.pevious='c'
            self.btn_c.click()

        elif key == QtCore.Qt.Key_B:
            self.btn_send.click()

       

    def closeEvent(self, event):
        # Close database connection when closing the application
        self.connection.close()
        event.accept()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
