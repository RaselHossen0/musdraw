import sys
import socket
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QDialog, QMessageBox

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QImage

class NicknameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enter Nickname")
        layout = QVBoxLayout()
        label = QLabel("Choose a nickname:")
        self.nickname_entry = QLineEdit()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(label)
        layout.addWidget(self.nickname_entry)
        layout.addWidget(ok_button)
        self.setLayout(layout)

class DrawingArea(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StaticContents)
        self.setMinimumSize(500, 500)
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.last_pos = None
        self.drawing = False
        self.enabled = False
        self.brush_size = 3
        self.brush_color = Qt.black

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.enabled:
            self.drawing = True
            self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.drawing and self.enabled:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.last_pos, event.pos())
            print(f"Drawing line from {self.last_pos} to {event.pos()}")
            self.send_draw_message(self.last_pos, event.pos())
            self.last_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        print("Painting!")
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.image, self.image.rect())

    def send_draw_message(self, start, end):
        message = f'DRAW {start.x()} {start.y()} {end.x()} {end.y()}'
        client.send(message.encode('utf-8'))

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        threading.Thread(target=self.receive, daemon=True).start()

    def initUI(self):
        self.setWindowTitle("Network Drawing and Messaging App")
        layout = QHBoxLayout(self)
        self.drawing_area = DrawingArea()
        layout.addWidget(self.drawing_area)

        
        right_layout = QVBoxLayout()
        self.game_state_label = QLabel("Waiting for other players to join", self)
        self.game_state_label.setFixedHeight(30)
        self.game_state_label.setFixedWidth(200)
        right_layout.addWidget(self.game_state_label)
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        right_layout.addWidget(self.text_area)

        
        

        
        
        self.msg_entry = QLineEdit()
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        right_layout.addWidget(self.msg_entry)
        right_layout.addWidget(send_button)
        
        layout.addLayout(right_layout)
        
        self.drawing_area.enabled = False #-------------------------------

        self.get_nickname()

    def get_nickname(self):
        dialog = NicknameDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.nickname = dialog.nickname_entry.text()
            client.send(self.nickname.encode('utf-8'))

    def send_message(self):
        message = f'{self.nickname}: {self.msg_entry.text()}'
        client.send(message.encode('utf-8'))
        self.msg_entry.clear()

    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message.startswith('DRAW'):
                    if not self.drawing_area.enabled:  # Check if other client is drawing
                        _, x1, y1, x2, y2 = message.split()
                        print("Drawing!")
                        print(f"Coordinates: Start({x1}, {y1}), End({x2}, {y2})")
                        self.drawing_area.update()
                        self.draw_other(int(x1), int(y1), int(x2), int(y2))
                elif 'You are drawing now' in message:
                    print("You are drawing now!")
                    self.game_state_label.setText(message)
                    self.drawing_area.enabled = True
                elif 'is drawing!' in message or 'Draw' in message:
                    self.game_state_label.setText(message)
                    print("Someone is drawing!")
                    self.drawing_area.enabled = False
                else:
                    self.text_area.append(message)
            except Exception as e:
                print("Error receiving data:", e)
                client.close()
                break

    def draw_other(self, x1, y1, x2, y2):
        painter = QPainter(self.drawing_area.image)
        painter.setPen(QPen(Qt.black, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(x1, y1, x2, y2)
        print(f"Image updated: {self.drawing_area.image.size()}") 
        # Call update() to trigger a redraw of the widget
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = '127.0.0.1'
    port = 65432
    client.connect((host, port))
    ex = App()
    ex.show()
    sys.exit(app.exec_())
