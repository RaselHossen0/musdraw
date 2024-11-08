import sys
import socket
import threading
import json
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
            self.send_draw_message(self.last_pos, event.pos())
            self.last_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.image, self.image.rect())

    def send_draw_message(self, start, end):
        message = {
            'type': 'draw',
            'start': {'x': start.x(), 'y': start.y()},
            'end': {'x': end.x(), 'y': end.y()}
        }
        client.send(json.dumps(message).encode('utf-8'))

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        threading.Thread(target=self.receive, daemon=True).start()

    def initUI(self):
        self.setWindowTitle("Network Drawing and Messaging App")
        layout = QHBoxLayout(self)
        left_layout = QVBoxLayout()
        layout.addLayout(left_layout)
        self.drawing_area = DrawingArea()
        layout.addWidget(self.drawing_area)
        self.current_word = None

        right_layout = QVBoxLayout()
        self.game_state_label = QLabel("Waiting for other players to join", self)
        self.game_state_label.setMaximumWidth(200)
        self.game_state_label.setAlignment(Qt.AlignCenter)
        self.game_state_label.setWordWrap(True)

        self.stop_button = QPushButton("Stop Drawing", self)
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_drawing)
        self.logout_button = QPushButton("Logout", self)
        self.logout_button.clicked.connect(self.logout)

        self.clear_board_button = QPushButton("Clear Board", self)
        self.clear_board_button.clicked.connect(self.clear_board)
        self.clear_board_button.setEnabled(True)
        left_layout.addWidget(self.clear_board_button)
        left_layout.addWidget(self.game_state_label)
        left_layout.addWidget(self.stop_button)
        left_layout.addWidget(self.logout_button)

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        right_layout.addWidget(self.text_area)

        self.msg_entry = QLineEdit()
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        right_layout.addWidget(self.msg_entry)
        right_layout.addWidget(send_button)
        layout.addLayout(right_layout)

        self.drawing_area.enabled = False

        self.get_nickname()
    def clear_board(self):
        self.drawing_area.image.fill(Qt.white)
        self.drawing_area.update()

    def get_nickname(self):
        dialog = NicknameDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.nickname = dialog.nickname_entry.text()
            client.send(json.dumps({'type': 'nickname', 'nickname': self.nickname}).encode('utf-8'))
    def logout(self):
        client.send(json.dumps({'type': 'leave', 'nickname': self.nickname}).encode('utf-8'))
        client.close()
        self.close()
    def send_message(self):
        message = f'{self.nickname}: {self.msg_entry.text()}'
        print(message)
        self.text_area.append(message)
        try:
            client.send(json.dumps({'type': 'message', 'message': message,'sender': f'{self.nickname}' }).encode('utf-8'))
            print("Message sent")
        except Exception as e:
            print("Error sending message:", e)
        
        self.msg_entry.clear()

    def receive(self):
        while True:
            try:
                data = client.recv(1024)
                # print(data)
                if not data:
                    break
                
                messages = data.decode('utf-8').split('\n')
                for message in messages:
                    try:
                        if message.strip():
                            message = json.loads(message)
                            self.handle_message(message)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {message}")
                        print(f"Error details: {str(e)}")
                        continue
            except Exception as e:
                print("Error receiving data:", e)
                client.close()
                break

    def handle_message(self, message):
        # print(message)
        if message['type'] == 'draw':
            if not self.drawing_area.enabled:
                start = QPoint(message['start']['x'], message['start']['y'])
                end = QPoint(message['end']['x'], message['end']['y'])
                # self.game_state_label.clear()
                # self.game_state_label.setText(f'{message["nickname"]} is drawing')
                self.current_word = message.get('word')
                self.draw_other(start, end)
        elif message['type'] == 'draw_start':
            self.game_state_label.clear()
            self.current_word = message.get('word')
            self.game_state_label.setText(message['message']+f' Word: {message["word"]}')
            if message['nickname'] == self.nickname:
                
                self.drawing_area.enabled = True
                self.stop_button.setEnabled(True)
            else:
                self.drawing_area.enabled = False
                
        elif message['type'] == 'draw_info':
            
            self.game_state_label.clear()
            self.game_state_label.setText(message['message'])
            
            
        elif message['type'] == 'drawing_end':
            self.game_state_label.clear()
            self.game_state_label.setText(message['message'])
            self.drawing_area.enabled = False
            self.stop_button.setEnabled(False)
        elif message['type'] == 'request_nickname':
            client.send(json.dumps({'type': 'nickname', 'nickname': self.nickname}).encode('utf-8'))
        elif message['type'] == 'word':
            self.current_word = message.get('word')
        elif message['type'] == 'leave':
            self.text_area.append(message['message'])
        elif message['type'] == 'message':
            self.text_area.append(message['message'])
            print(message['message'])
        elif message['type'] == 'guess':
            self.drawing_area.enabled = False
            self.stop_button.setEnabled(False)
           
            
            self.text_area.append(message['message'])
        else:
            try:
               
                self.text_area.append(message['message'])
            except:
                print(message)
                print(f"Unknown message type: {message}")
            

    def draw_other(self, start, end):
        painter = QPainter(self.drawing_area.image)
        painter.setPen(QPen(Qt.black, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(start, end)
        self.drawing_area.update()

    def stop_drawing(self):
        self.stop_button.setEnabled(False)
        self.drawing_area.enabled = False
        
        if client:
            print("Stopped drawing")
            client.send(json.dumps({'type': 'drawing_end', 'message': f'{self.nickname} stopped drawing'}).encode('utf-8'))

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
