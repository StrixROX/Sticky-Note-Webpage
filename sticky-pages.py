import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import (QKeyEvent, QCloseEvent, QPainterPath, QBitmap, 
                         QPainter, QBrush, QRegion)
from PyQt5.QtWebEngineWidgets import QWebEngineView

# Configuration
WIDTH = 800
HEIGHT = 600
WEBPAGE_URL = "https://www.google.com"


class StickyPagesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # Set window size
        self.setFixedSize(WIDTH, HEIGHT)
        
        # Apply frameless window with rounded corners
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Create central widget
        self.central_widget = QWidget(self)
        self.central_widget.setStyleSheet('''
                                     background-color: white;
                                     ''')
        self.setCentralWidget(self.central_widget)
        
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
        radius = 10
        path = QPainterPath()
        path.addRoundedRect(
            0, 0, 
            WIDTH, HEIGHT, 
            radius, radius
        )
        
        # Create a bitmap mask
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
        # Also set window mask for the overall shape
        self.setMask(mask)
    
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

