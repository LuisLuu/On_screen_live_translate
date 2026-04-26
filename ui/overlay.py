# ui/overlay.py
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor

class TranslationHUD(QWidget):
    def __init__(self, x, y, w, h):
        super().__init__()
        # 1. The "Ghost" Flags
        # Frameless + Stay on Top + Tool Window (no taskbar) + Transparent Input
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput 
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(x, y, w, h)

        # 2. UI Layout
        self.layout = QVBoxLayout()
        self.label = QLabel("Initializing...")
        self.label.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 150); padding: 5px; border-radius: 5px;")
        self.label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def update_text(self, text):
        self.label.setText(text)
        self.show()

    def clear(self):
        self.hide()
        