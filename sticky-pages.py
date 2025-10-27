import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import QKeyEvent, QCloseEvent, QPainterPath, QBitmap, QPainter, QBrush
from PyQt5.QtWebEngineWidgets import QWebEngineView

# Configuration
WIDTH = 800
HEIGHT = 600
X_POS = 50  # X coordinate (top left origin), None for center
Y_POS = 50  # Y coordinate (top left origin), None for center
WEBPAGE_URL = "https://www.google.com"
CORNER_RADIUS = 10
BORDER_WIDTH = 8  # Border width in pixels
BORDER_COLOR = "rgba(255, 255, 255, 0.7)"  # Translucent white with higher opacity


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

        # Create central widget with border
        self.central_widget = QWidget(self)
        self.central_widget.setStyleSheet(
            f"""
                                     background-color: white;
                                     border: {BORDER_WIDTH}px solid {BORDER_COLOR};
                                     border-radius: {CORNER_RADIUS}px;
                                     """
        )
        self.setCentralWidget(self.central_widget)

        # Create and configure web view with padding for border
        self.web_view = QWebEngineView(self.central_widget)
        self.web_view.setUrl(QUrl(WEBPAGE_URL))
        # Position web view with padding to show the border
        padding = BORDER_WIDTH
        self.web_view.setGeometry(
            padding, padding, WIDTH - (padding * 2), HEIGHT - (padding * 2)
        )

        # Enable JavaScript for proper website functionality
        settings = self.web_view.settings()
        settings.setAttribute(settings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(settings.WebAttribute.PluginsEnabled, True)

        # Apply rounded mask to create actual rounded corners
        self.apply_rounded_mask()

    def apply_rounded_mask(self):
        """Apply rounded corners mask to the window"""
        # Window mask includes border
        path = QPainterPath()
        path.addRoundedRect(0, 0, WIDTH, HEIGHT, CORNER_RADIUS, CORNER_RADIUS)

        window_mask = QBitmap(WIDTH, HEIGHT)
        window_mask.fill(Qt.color0)  # Transparent

        painter = QPainter(window_mask)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(Qt.color1))  # Opaque
        painter.drawPath(path)
        painter.end()

        self.setMask(window_mask)

        # Web view mask (inner rounded corners)
        padding = BORDER_WIDTH
        inner_w = WIDTH - (padding * 2)
        inner_h = HEIGHT - (padding * 2)

        path2 = QPainterPath()
        path2.addRoundedRect(0, 0, inner_w, inner_h, CORNER_RADIUS, CORNER_RADIUS)

        web_mask = QBitmap(inner_w, inner_h)
        web_mask.fill(Qt.color0)

        painter2 = QPainter(web_mask)
        painter2.setRenderHint(QPainter.Antialiasing)
        painter2.setBrush(QBrush(Qt.color1))
        painter2.drawPath(path2)
        painter2.end()

        self.web_view.setMask(web_mask)

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

    # Get screen geometry
    screen = app.primaryScreen().geometry()

    # Determine window position
    if X_POS is not None and Y_POS is not None:
        # Use specified coordinates
        pos_x, pos_y = X_POS, Y_POS
    else:
        # Center window on screen
        pos_x = (screen.width() - WIDTH) // 2
        pos_y = (screen.height() - HEIGHT) // 2

    window = StickyPagesWindow()
    window.move(pos_x, pos_y)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
