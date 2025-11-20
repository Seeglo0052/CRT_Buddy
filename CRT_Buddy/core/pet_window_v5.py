# -*- coding: utf-8 -*-
"""
CRT Buddy - Pet Window v5.0
Y2K Desktop PC style with bar buttons and round power button
"""
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QFileDialog
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint, QRect
from PyQt6.QtGui import QPainter, QColor, QPen, QLinearGradient, QFont, QBrush, QPainterPath, QRadialGradient, QCursor
import random
import math


class CRTBuddyWindow(QWidget):
    """Y2K Desktop PC style with physical buttons"""
    
    # Signals
    image_dropped = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_animations()
        
        # Drag variables
        self.dragging = False
        self.drag_position = QPoint()
        
        # Current mood
        self.current_mood = "idle"
        
        # Global mouse tracking for eyes
        self.global_mouse_pos = QCursor.pos()
        
        # Mascot properties
        self.blink_timer = 0
        self.is_blinking = False
        
    def init_ui(self):
        """Initialize user interface - Y2K desktop PC style"""
        # Window settings
        self.setWindowTitle("CRT Buddy")
        self.setGeometry(100, 100, 320, 440)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Enable drag and drop
        self.setAcceptDrops(True)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 90, 12, 15)
        layout.setSpacing(6)
        
        # Status display
        self.status_label = QLabel("CRT BUDDY v5.0")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #00FFFF;
                background-color: rgba(0, 20, 40, 200);
                border: 2px solid #0088FF;
                border-radius: 4px;
                padding: 5px;
                font-family: 'Courier New', monospace;
                font-size: 10px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.status_label)
        
        # Input area
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Enter text...")
        self.input_text.setMaximumHeight(50)
        self.input_text.setStyleSheet("""
            QTextEdit {
                color: #00FFFF;
                background-color: rgba(0, 20, 40, 180);
                border: 2px solid #0066CC;
                border-radius: 4px;
                padding: 4px;
                font-family: 'Courier New', monospace;
                font-size: 9px;
            }
        """)
        layout.addWidget(self.input_text)
        
        # Buttons - Y2K desktop PC style
        # Generate button (long bar)
        self.generate_btn = QPushButton("�� GENERATE")
        self.generate_btn.setMinimumHeight(38)
        self.generate_btn.setStyleSheet(self.get_bar_button_style("#FF0080", "#FF66B3"))
        layout.addWidget(self.generate_btn)
        
        # Image button (long bar)
        self.upload_btn = QPushButton("�� IMAGE")
        self.upload_btn.setMinimumHeight(38)
        self.upload_btn.setStyleSheet(self.get_bar_button_style("#00CCFF", "#66E0FF"))
        self.upload_btn.clicked.connect(self.upload_image)
        layout.addWidget(self.upload_btn)
        
        # Random button (long bar)
        self.effect_btn = QPushButton("�� RANDOM")
        self.effect_btn.setMinimumHeight(38)
        self.effect_btn.setStyleSheet(self.get_bar_button_style("#FFD700", "#FFE766"))
        layout.addWidget(self.effect_btn)
        
        layout.addSpacing(5)
        
        # Close button (round power button)
        close_container = QHBoxLayout()
        close_container.addStretch()
        
        self.close_btn = QPushButton("��")
        self.close_btn.setFixedSize(42, 42)
        self.close_btn.setStyleSheet(self.get_round_button_style())
        self.close_btn.clicked.connect(self.close)
        close_container.addWidget(self.close_btn)
        close_container.addStretch()
        
        layout.addLayout(close_container)
        self.setLayout(layout)
        
    def get_bar_button_style(self, color1, color2):
        """Get long bar metallic button style - Y2K desktop PC"""
        return f"""
            QPushButton {{
                color: white;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(100, 100, 100, 200),
                    stop:0.2 rgba(140, 140, 140, 220),
                    stop:0.4 {color1},
                    stop:0.6 {color2},
                    stop:0.8 rgba(140, 140, 140, 220),
                    stop:1 rgba(100, 100, 100, 200));
                border: 2px solid rgba(160, 160, 160, 180);
                border-top: 3px solid rgba(220, 220, 220, 200);
                border-left: 2px solid rgba(200, 200, 200, 180);
                border-bottom: 3px solid rgba(80, 80, 80, 200);
                border-right: 2px solid rgba(100, 100, 100, 180);
                border-radius: 10px;
                padding: 10px;
                font-family: 'Arial', sans-serif;
                font-size: 11px;
                font-weight: bold;
                text-align: left;
                padding-left: 18px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(120, 120, 120, 220),
                    stop:0.2 rgba(180, 180, 180, 240),
                    stop:0.4 {color2},
                    stop:0.6 white,
                    stop:0.8 rgba(180, 180, 180, 240),
                    stop:1 rgba(120, 120, 120, 220));
                border-top: 3px solid rgba(255, 255, 255, 240);
                border-left: 2px solid rgba(240, 240, 240, 220);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(60, 60, 60, 220),
                    stop:0.2 rgba(80, 80, 80, 230),
                    stop:0.4 {color1},
                    stop:0.6 {color1},
                    stop:0.8 rgba(80, 80, 80, 230),
                    stop:1 rgba(60, 60, 60, 220));
                border-top: 2px solid rgba(60, 60, 60, 200);
                border-left: 2px solid rgba(70, 70, 70, 180);
                border-bottom: 2px solid rgba(180, 180, 180, 200);
                border-right: 2px solid rgba(160, 160, 160, 180);
                padding-left: 20px;
                padding-top: 12px;
            }}
        """
    
    def get_round_button_style(self):
        """Get round power button style - Y2K desktop PC"""
        return """
            QPushButton {
                color: white;
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                    fx:0.35, fy:0.35,
                    stop:0 rgba(255, 100, 100, 240),
                    stop:0.5 rgba(220, 50, 50, 240),
                    stop:0.85 rgba(160, 30, 30, 230),
                    stop:1 rgba(100, 20, 20, 220));
                border: 3px solid rgba(160, 160, 160, 200);
                border-top: 4px solid rgba(220, 220, 220, 220);
                border-left: 3px solid rgba(210, 210, 210, 210);
                border-bottom: 4px solid rgba(90, 90, 90, 220);
                border-right: 3px solid rgba(100, 100, 100, 210);
                border-radius: 21px;
                font-family: Arial;
                font-size: 22px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                    fx:0.35, fy:0.35,
                    stop:0 rgba(255, 140, 140, 250),
                    stop:0.5 rgba(255, 90, 90, 250),
                    stop:0.85 rgba(200, 50, 50, 240),
                    stop:1 rgba(140, 30, 30, 230));
                border-top: 4px solid rgba(255, 255, 255, 250);
                border-left: 3px solid rgba(240, 240, 240, 240);
            }
            QPushButton:pressed {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                    fx:0.5, fy:0.5,
                    stop:0 rgba(180, 30, 30, 240),
                    stop:0.5 rgba(140, 20, 20, 240),
                    stop:0.85 rgba(100, 15, 15, 230),
                    stop:1 rgba(60, 10, 10, 220));
                border-top: 2px solid rgba(90, 90, 90, 220);
                border-left: 2px solid rgba(100, 100, 100, 210);
                border-bottom: 3px solid rgba(200, 200, 200, 220);
                border-right: 3px solid rgba(180, 180, 180, 210);
            }
        """
        
    def setup_animations(self):
        """Setup animations"""
        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self.animate)
        self.anim_timer.start(50)
        self.blink_counter = 0
        self.frame_count = 0
        
    def animate(self):
        """Main animation loop"""
        self.frame_count += 1
        self.global_mouse_pos = QCursor.pos()
        
        self.blink_counter += 1
        if self.blink_counter > random.randint(60, 100):
            self.is_blinking = True
            self.blink_timer = 0
            self.blink_counter = 0
        
        if self.is_blinking:
            self.blink_timer += 1
            if self.blink_timer > 3:
                self.is_blinking = False
        
        self.update()
        
    def paintEvent(self, event):
        """Custom paint event"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        self.draw_metallic_body(painter)
        self.draw_crt_screen(painter)
        self.draw_mascot(painter)
        self.draw_scanlines(painter)
        self.draw_chrome_accents(painter)
        
    def draw_metallic_body(self, painter):
        """Draw metallic aluminum body"""
        width = self.width()
        height = self.height()
        
        body_gradient = QLinearGradient(0, 0, width, height)
        body_gradient.setColorAt(0, QColor(180, 190, 200, 250))
        body_gradient.setColorAt(0.5, QColor(220, 230, 240, 250))
        body_gradient.setColorAt(1, QColor(160, 170, 180, 250))
        painter.setBrush(body_gradient)
        painter.setPen(QPen(QColor(100, 110, 120), 3))
        painter.drawRoundedRect(5, 5, width - 10, height - 10, 12, 12)
        
        highlight = QLinearGradient(0, 5, 0, 30)
        highlight.setColorAt(0, QColor(255, 255, 255, 150))
        highlight.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setBrush(highlight)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(8, 8, width - 16, 25, 10, 10)
        
        painter.setPen(QColor(80, 90, 100))
        painter.setFont(QFont('Arial', 7, QFont.Weight.Bold))
        painter.drawText(QRect(width//2 - 35, 12, 70, 12), 
                        Qt.AlignmentFlag.AlignCenter, "CRT BUDDY")
        
        led_x = width - 20
        led_y = 15
        led_glow = QRadialGradient(led_x, led_y, 5)
        led_color = QColor(0, 255, 200, 180 + int(75 * math.sin(self.frame_count * 0.15)))
        led_glow.setColorAt(0, led_color)
        led_glow.setColorAt(1, QColor(0, 255, 200, 0))
        painter.setBrush(led_glow)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPoint(led_x, led_y), 5, 5)
        painter.setBrush(QColor(0, 255, 200))
        painter.drawEllipse(QPoint(led_x, led_y), 2, 2)
        
    def draw_crt_screen(self, painter):
        """Draw CRT screen"""
        width = self.width()
        
        bezel_rect = QRect(10, 30, width - 20, 85)
        bezel_gradient = QLinearGradient(0, 30, 0, 115)
        bezel_gradient.setColorAt(0, QColor(20, 25, 30))
        bezel_gradient.setColorAt(1, QColor(10, 15, 20))
        painter.setBrush(bezel_gradient)
        painter.setPen(QPen(QColor(5, 10, 15), 2))
        painter.drawRoundedRect(bezel_rect, 8, 8)
        
        screen_rect = QRect(14, 34, width - 28, 77)
        screen_gradient = QRadialGradient(width/2, 72, width/2)
        screen_gradient.setColorAt(0, QColor(0, 40, 80, 240))
        screen_gradient.setColorAt(0.7, QColor(0, 30, 60, 250))
        screen_gradient.setColorAt(1, QColor(0, 20, 40, 255))
        painter.setBrush(screen_gradient)
        painter.setPen(QPen(QColor(0, 100, 200), 2))
        painter.drawRoundedRect(screen_rect, 6, 6)
        
        reflection = QLinearGradient(0, 34, 0, 60)
        reflection.setColorAt(0, QColor(255, 255, 255, 50))
        reflection.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setBrush(reflection)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(16, 36, width - 32, 26, 5, 5)
        
    def draw_mascot(self, painter):
        """Draw mascot with global eye tracking"""
        width = self.width()
        mascot_x = width // 2
        mascot_y = 72
        
        window_pos = self.mapToGlobal(QPoint(0, 0))
        mascot_screen_x = window_pos.x() + mascot_x
        mascot_screen_y = window_pos.y() + mascot_y
        
        dx = self.global_mouse_pos.x() - mascot_screen_x
        dy = self.global_mouse_pos.y() - mascot_screen_y
        distance = math.sqrt(dx * dx + dy * dy)
        if distance > 0:
            eye_offset_x = (dx / distance) * 5
            eye_offset_y = (dy / distance) * 5
        else:
            eye_offset_x = 0
            eye_offset_y = 0
        
        head_glow = QRadialGradient(mascot_x, mascot_y, 30)
        head_glow.setColorAt(0, QColor(0, 150, 255, 200))
        head_glow.setColorAt(1, QColor(0, 100, 200, 0))
        painter.setBrush(head_glow)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPoint(mascot_x, mascot_y), 30, 30)
        
        painter.setBrush(QColor(0, 100, 200, 220))
        painter.setPen(QPen(QColor(0, 150, 255), 2))
        painter.drawRoundedRect(mascot_x - 22, mascot_y - 18, 44, 36, 8, 8)
        
        painter.setBrush(QColor(0, 40, 80, 240))
        painter.setPen(QPen(QColor(0, 200, 255), 1))
        painter.drawRoundedRect(mascot_x - 18, mascot_y - 14, 36, 28, 5, 5)
        
        if not self.is_blinking:
            eye_color = QColor(0, 255, 255)
            
            for offset_x in [-8, 8]:
                eye_x = mascot_x + offset_x + eye_offset_x
                eye_y = mascot_y - 4 + eye_offset_y
                
                eye_glow = QRadialGradient(eye_x, eye_y, 8)
                eye_glow.setColorAt(0, QColor(0, 255, 255, 200))
                eye_glow.setColorAt(1, QColor(0, 255, 255, 0))
                painter.setBrush(eye_glow)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(QPoint(int(eye_x), int(eye_y)), 8, 8)
                
                painter.setBrush(eye_color)
                painter.drawEllipse(QPoint(int(eye_x), int(eye_y)), 4, 5)
                
                painter.setBrush(QColor(0, 100, 200))
                painter.drawEllipse(QPoint(int(eye_x), int(eye_y)), 2, 3)
        else:
            painter.setPen(QPen(QColor(0, 255, 255), 2))
            painter.drawLine(mascot_x - 12, mascot_y - 3, mascot_x - 4, mascot_y - 3)
            painter.drawLine(mascot_x + 4, mascot_y - 3, mascot_x + 12, mascot_y - 3)
        
        painter.setPen(QPen(QColor(0, 255, 255), 2))
        if self.current_mood == "happy":
            path = QPainterPath()
            path.moveTo(mascot_x - 8, mascot_y + 6)
            path.quadTo(mascot_x, mascot_y + 12, mascot_x + 8, mascot_y + 6)
            painter.drawPath(path)
        elif self.current_mood == "processing":
            painter.drawEllipse(QPoint(mascot_x, mascot_y + 8), 4, 4)
        else:
            painter.drawLine(mascot_x - 8, mascot_y + 8, mascot_x + 8, mascot_y + 8)
        
        painter.setPen(QPen(QColor(0, 200, 255), 2))
        painter.drawLine(mascot_x, mascot_y - 18, mascot_x, mascot_y - 26)
        
        ball_glow = QRadialGradient(mascot_x, mascot_y - 30, 6)
        ball_color = QColor(255, 0, 255, 200 + int(55 * math.sin(self.frame_count * 0.1)))
        ball_glow.setColorAt(0, ball_color)
        ball_glow.setColorAt(1, QColor(255, 0, 255, 0))
        painter.setBrush(ball_glow)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPoint(mascot_x, mascot_y - 30), 6, 6)
        painter.setBrush(QColor(255, 0, 255))
        painter.drawEllipse(QPoint(mascot_x, mascot_y - 30), 3, 3)
        
    def draw_scanlines(self, painter):
        """Draw CRT scanlines"""
        width = self.width()
        painter.setPen(QPen(QColor(0, 255, 255, 15), 1))
        for y in range(34, 111, 3):
            painter.drawLine(14, y, width - 14, y)
        
        scanline_y = 34 + (self.frame_count * 2) % 77
        gradient = QLinearGradient(0, scanline_y - 15, 0, scanline_y + 15)
        gradient.setColorAt(0, QColor(0, 255, 255, 0))
        gradient.setColorAt(0.5, QColor(0, 255, 255, 60))
        gradient.setColorAt(1, QColor(0, 255, 255, 0))
        painter.fillRect(14, scanline_y - 15, width - 28, 30, gradient)
        
    def draw_chrome_accents(self, painter):
        """Draw chrome accents"""
        width = self.width()
        height = self.height()
        
        chrome_gradient = QLinearGradient(0, height - 30, 0, height - 10)
        chrome_gradient.setColorAt(0, QColor(150, 160, 170))
        chrome_gradient.setColorAt(0.5, QColor(200, 210, 220))
        chrome_gradient.setColorAt(1, QColor(150, 160, 170))
        painter.setBrush(chrome_gradient)
        painter.setPen(QPen(QColor(100, 110, 120), 1))
        painter.drawRoundedRect(15, height - 28, width - 30, 16, 4, 4)
        
        painter.setPen(QPen(QColor(80, 90, 100), 1))
        for i in range(6):
            x = width // 2 - 30 + i * 10
            y = height - 22
            painter.drawLine(x, y, x + 5, y)
            painter.drawLine(x, y + 4, x + 5, y + 4)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
    
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.drag_position)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                self.image_dropped.emit(file_path)
    
    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.gif *.bmp)")
        if file_path:
            self.image_dropped.emit(file_path)
    
    def set_status(self, text):
        self.status_label.setText(text)
    
    def set_mood(self, mood):
        self.current_mood = mood
    
    def get_input_text(self):
        return self.input_text.toPlainText()
    
    def clear_input(self):
        self.input_text.clear()
