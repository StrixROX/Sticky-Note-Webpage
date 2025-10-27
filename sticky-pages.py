import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import (QKeyEvent, QCloseEvent, QPainterPath, QBitmap, 
                         QPainter, QBrush, QRegion, QColor)
from PyQt5.QtWebEngineWidgets import QWebEngineView

# Configuration
WIDTH = 800
HEIGHT = 600
WEBPAGE_URL = "https://www.google.com"
CORNER_RADIUS = 10
# Shadow configuration: matches CSS "box-shadow: 0 0 10px rgba(0,0,0,0.3)"
SHADOW_BLUR_RADIUS = 10  # 10px blur
SHADOW_OFFSET_X = 0       # 0px horizontal offset
SHADOW_OFFSET_Y = 0       # 0px vertical offset
SHADOW_COLOR = (0, 0, 0, 76)  # rgba(0,0,0,0.3) = 0.3 * 255 ≈ 76


class StickyPagesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # Set window size (add padding for shadow)
        shadow_padding = SHADOW_BLUR_RADIUS * 2
        self.setFixedSize(WIDTH + shadow_padding, HEIGHT + shadow_padding)
        
        # Apply frameless window with rounded corners
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Calculate shadow padding for positioning
        shadow_padding = SHADOW_BLUR_RADIUS * 2
        
        # Create central widget with shadow
        self.central_widget = QWidget(self)
        self.central_widget.setStyleSheet('''
                                     background-color: white;
                                     ''')
        self.central_widget.setGeometry(shadow_padding // 2, shadow_padding // 2, WIDTH, HEIGHT)
        
        # Apply shadow effect
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(SHADOW_BLUR_RADIUS)
        self.shadow.setOffset(SHADOW_OFFSET_X, SHADOW_OFFSET_Y)
        self.shadow.setColor(QColor(*SHADOW_COLOR))
        self.central_widget.setGraphicsEffect(self.shadow)
        
        # Create and configure web view
        self.web_view = QWebEngineView(self.central_widget)
        self.web_view.setUrl(QUrl(WEBPAGE_URL))
        self.web_view.setGeometry(0, 0, WIDTH, HEIGHT)
        
        # Enable JavaScript for proper website functionality
        settings = self.web_view.settings()
        settings.setAttribute(settings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(settings.WebAttribute.PluginsEnabled, True)
        
        # Apply rounded mask to create actual rounded corners
        self.apply_rounded_mask()
    
    def apply_rounded_mask(self):
        """Apply rounded corners mask to the window"""
        path = QPainterPath()
        path.addRoundedRect(
            0, 0, 
            WIDTH, HEIGHT, 
            CORNER_RADIUS, CORNER_RADIUS
        )
        
        # Create a bitmap mask for the central widget
        mask = QBitmap(WIDTH, HEIGHT)
        mask.fill(Qt.color0)  # Transparent
        
        painter = QPainter(mask)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(Qt.color1))  # Opaque
        painter.drawPath(path)
        painter.end()
        
        # Apply mask to the central widget to clip background and web content
        self.central_widget.setMask(mask)
        self.web_view.setMask(mask)
        
        # Create window mask to include shadow
        shadow_padding = SHADOW_BLUR_RADIUS * 2
        window_mask = QBitmap(WIDTH + shadow_padding, HEIGHT + shadow_padding)
        window_mask.fill(Qt.color0)
        
        painter2 = QPainter(window_mask)
        painter2.setRenderHint(QPainter.Antialiasing)
        painter2.setBrush(QBrush(Qt.color1))
        window_path = QPainterPath()
        window_path.addRoundedRect(
            shadow_padding // 2, shadow_padding // 2,
            WIDTH, HEIGHT,
            CORNER_RADIUS, CORNER_RADIUS
        )
        painter2.drawPath(window_path)
        painter2.end()
        
        self.setMask(window_mask)
    
    def keyPressEvent(self, event: QKeyEvent):
        """Handle keyboard shortcuts"""
        # Alt+F4 to close the window
        if event.key() == Qt.Key_F4 and event.modifiers() == Qt.AltModifier:
            self.close()
        else:
            super().keyPressEvent(event)
    
    def showEvent(self, event):
        """When shown, ensure mask is properly applied"""
        super().showEvent(event)
        # Reapply mask after widgets are laid out
        QTimer.singleShot(0, self.apply_rounded_mask)
    
    def closeEvent(self, event: QCloseEvent):
        """Handle window close event"""
        QApplication.instance().quit()
        event.accept()


def main():
    app = QApplication(sys.argv)
    
    window = StickyPagesWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

