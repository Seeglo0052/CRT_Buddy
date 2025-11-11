"""
CRT Buddy - Pet Window
可拖拽的透明CRT显示器桌面宠物窗口
"""
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextEdit, QPushButton, QFileDialog
from PyQt6.QtCore import Qt, QPoint, QTimer, QPropertyAnimation, QRect, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen, QPixmap, QImage, QPalette
import random


class CRTBuddyWindow(QWidget):
    """主CRT宠物窗口"""
    
    image_dropped = pyqtSignal(str)  # 图片拖放信号
    
    def __init__(self):
        super().__init__()
        self.dragging = False
        self.offset = QPoint()
        self.mood = "idle"  # idle, happy, thinking, processing
        self.scan_line_offset = 0
        
        self.init_ui()
        self.setup_animations()
        
    def init_ui(self):
        """初始化Y2K风格UI"""
        # 窗口设置：置顶、无边框、透明背景
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAcceptDrops(True)
        
        # 设置窗口大小
        self.setFixedSize(350, 450)
        
        # 主布局
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # CRT屏幕标题
        self.title_label = QLabel("? CRT BUDDY ?")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                color: #00ff00;
                font-size: 20px;
                font-weight: bold;
                font-family: 'Courier New', monospace;
                text-shadow: 0 0 10px #00ff00;
                background: transparent;
                padding: 10px;
            }
        """)
        layout.addWidget(self.title_label)
        
        # 状态显示
        self.status_label = QLabel("? READY TO GENERATE Y2K VIBES ?")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #ff00ff;
                font-size: 12px;
                font-family: 'Courier New', monospace;
                background: transparent;
                padding: 5px;
            }
        """)
        layout.addWidget(self.status_label)
        
        # 输入框
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Type your message or drag an image here...")
        self.input_text.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0, 0, 0, 180);
                color: #00ffff;
                border: 2px solid #00ff00;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-family: 'Courier New', monospace;
                selection-background-color: #ff00ff;
            }
        """)
        self.input_text.setMaximumHeight(100)
        layout.addWidget(self.input_text)
        
        # 按钮容器
        button_layout = QVBoxLayout()
        button_layout.setSpacing(8)
        
        # Generate按钮
        self.generate_btn = QPushButton("? GENERATE MEME ?")
        self.generate_btn.setStyleSheet(self.get_button_style("#ff00ff", "#ff66ff"))
        self.generate_btn.clicked.connect(self.on_generate_clicked)
        button_layout.addWidget(self.generate_btn)
        
        # Upload按钮
        self.upload_btn = QPushButton("?? UPLOAD IMAGE ??")
        self.upload_btn.setStyleSheet(self.get_button_style("#00ffff", "#66ffff"))
        self.upload_btn.clicked.connect(self.on_upload_clicked)
        button_layout.addWidget(self.upload_btn)
        
        # 特效按钮
        self.effect_btn = QPushButton("? RANDOM Y2K EFFECT ?")
        self.effect_btn.setStyleSheet(self.get_button_style("#ffff00", "#ffff66"))
        self.effect_btn.clicked.connect(self.on_effect_clicked)
        button_layout.addWidget(self.effect_btn)
        
        layout.addLayout(button_layout)
        
        # 底部信息
        self.footer_label = QLabel("Drag me anywhere! ? Right-click to close")
        self.footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.footer_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 10px;
                font-family: 'Courier New', monospace;
                background: transparent;
            }
        """)
        layout.addWidget(self.footer_label)
        
        layout.addStretch()
        self.setLayout(layout)
        
    def get_button_style(self, color1, color2):
        """获取Y2K风格按钮样式"""
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color1}, stop:1 {color2});
                color: #000000;
                border: 2px solid #ffffff;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                font-weight: bold;
                font-family: 'Courier New', monospace;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color2}, stop:1 {color1});
                border: 2px solid {color1};
            }}
            QPushButton:pressed {{
                background: #ffffff;
                color: {color1};
            }}
        """
    
    def setup_animations(self):
        """设置动画效果"""
        # 扫描线动画定时器
        self.scan_timer = QTimer(self)
        self.scan_timer.timeout.connect(self.update_scan_lines)
        self.scan_timer.start(50)  # 50ms更新一次
        
        # 标题闪烁动画
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.blink_title)
        self.blink_timer.start(1000)
        
    def update_scan_lines(self):
        """更新扫描线位置"""
        self.scan_line_offset = (self.scan_line_offset + 2) % self.height()
        self.update()
        
    def blink_title(self):
        """标题闪烁效果"""
        colors = ["#00ff00", "#ff00ff", "#00ffff", "#ffff00"]
        color = random.choice(colors)
        self.title_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 20px;
                font-weight: bold;
                font-family: 'Courier New', monospace;
                text-shadow: 0 0 10px {color};
                background: transparent;
                padding: 10px;
            }}
        """)
    
    def paintEvent(self, event):
        """绘制CRT效果"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 绘制CRT外壳（深灰色圆角矩形）
        painter.setBrush(QColor(30, 30, 35, 240))
        painter.setPen(QPen(QColor(100, 100, 110), 3))
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 15, 15)
        
        # 绘制内屏幕边框
        painter.setPen(QPen(QColor(0, 255, 0, 100), 2))
        painter.drawRoundedRect(10, 10, self.width()-20, self.height()-20, 10, 10)
        
        # 绘制扫描线效果
        painter.setPen(QPen(QColor(0, 255, 0, 30), 1))
        for i in range(0, self.height(), 4):
            y = (i + self.scan_line_offset) % self.height()
            painter.drawLine(0, y, self.width(), y)
        
        # 绘制随机静态噪点（模拟CRT）
        if random.random() < 0.1:
            for _ in range(20):
                x = random.randint(0, self.width())
                y = random.randint(0, self.height())
                painter.setPen(QColor(255, 255, 255, random.randint(50, 150)))
                painter.drawPoint(x, y)
    
    # 拖拽功能
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.pos()
        elif event.button() == Qt.MouseButton.RightButton:
            self.close()
    
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(self.pos() + event.pos() - self.offset)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
    
    # 拖放功能
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.set_mood("happy")
    
    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                self.image_dropped.emit(file)
                self.set_status(f"? Image loaded: {file.split('/')[-1]}")
                break
    
    # 按钮事件
    def on_generate_clicked(self):
        text = self.input_text.toPlainText().strip()
        if text:
            self.set_mood("processing")
            self.set_status("? GENERATING Y2K MEME...")
        else:
            self.set_status("? Please enter some text first!")
    
    def on_upload_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg *.gif *.bmp)"
        )
        if file_path:
            self.image_dropped.emit(file_path)
            self.set_status(f"? Image loaded: {file_path.split('/')[-1]}")
    
    def on_effect_clicked(self):
        effects = [
            "? HOLOGRAPHIC GLITCH",
            "?? RAINBOW CHROME",
            "? VHS DISTORTION",
            "?? CD-ROM REFLECTION",
            "?? LASER GRID"
        ]
        effect = random.choice(effects)
        self.set_status(f"Applying: {effect}")
        self.set_mood("processing")
    
    # 辅助方法
    def set_mood(self, mood):
        """设置宠物心情"""
        self.mood = mood
        moods = {
            "idle": "?",
            "happy": "?",
            "thinking": "?",
            "processing": "?"
        }
        icon = moods.get(mood, "?")
        self.title_label.setText(f"{icon} CRT BUDDY {icon}")
    
    def set_status(self, message):
        """设置状态消息"""
        self.status_label.setText(message)
        
    def get_input_text(self):
        """获取输入文本"""
        return self.input_text.toPlainText()
    
    def clear_input(self):
        """清空输入"""
        self.input_text.clear()
