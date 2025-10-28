import argparse
import json
import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtCore import Qt, QUrl, QTimer, QRect
from PyQt6.QtGui import (
    QKeyEvent,
    QCloseEvent,
    QPainterPath,
    QPainter,
    QColor,
    QRegion,
    QPen,
)
from PyQt6.QtWebEngineWidgets import QWebEngineView

# Default configuration
DEFAULT_CONFIG = {
    "width": 800,
    "height": 600,
    "xPos": 50,
    "yPos": 50,
    "webpageUrl": "https://www.google.com",
    "cornerRadius": 10,
    "borderWidth": 8,
    "borderColor": "rgba(255, 255, 255, 0.5)",
    "windowOpacity": 1.0,
}

# Declare globals (initialized with defaults)
WIDTH = DEFAULT_CONFIG["width"]
HEIGHT = DEFAULT_CONFIG["height"]
X_POS = DEFAULT_CONFIG["xPos"]
Y_POS = DEFAULT_CONFIG["yPos"]
WEBPAGE_URL = DEFAULT_CONFIG["webpageUrl"]
CORNER_RADIUS = DEFAULT_CONFIG["cornerRadius"]
BORDER_WIDTH = DEFAULT_CONFIG["borderWidth"]
BORDER_COLOR = DEFAULT_CONFIG["borderColor"]
WINDOW_OPACITY = DEFAULT_CONFIG["windowOpacity"]


def load_config(path="config.json"):
    """Load configuration from a JSON file with camelCase keys and update global vars."""
    global WIDTH, HEIGHT, X_POS, Y_POS, WEBPAGE_URL, CORNER_RADIUS, BORDER_WIDTH, BORDER_COLOR, WINDOW_OPACITY

    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON in {path}. Using defaults.")
            data = {}
    else:
        print(f"Warning: {path} not found. Using defaults.")
        data = {}

    # CLI args can override config.json values
    cli_arg_parser = argparse.ArgumentParser(
        prog="StickyPages",
        description="Stick webpages to your desktop like post-it notes.",
    )
    cli_arg_parser.add_argument(
        "-u",
        "--url",
        type=str,
        default="",
        help="specify URL of the webpage rendered",
    )

    webpage_url_from_cli = cli_arg_parser.parse_args().url

    if webpage_url_from_cli != "":
        data["webpageUrl"] = webpage_url_from_cli

    # Apply loaded or default values
    WIDTH = data.get("width", DEFAULT_CONFIG["width"])
    HEIGHT = data.get("height", DEFAULT_CONFIG["height"])
    X_POS = data.get("xPos", DEFAULT_CONFIG["xPos"])
    Y_POS = data.get("yPos", DEFAULT_CONFIG["yPos"])
    WEBPAGE_URL = data.get("webpageUrl", DEFAULT_CONFIG["webpageUrl"])
    CORNER_RADIUS = data.get("cornerRadius", DEFAULT_CONFIG["cornerRadius"])
    BORDER_WIDTH = data.get("borderWidth", DEFAULT_CONFIG["borderWidth"])
    BORDER_COLOR = data.get("borderColor", DEFAULT_CONFIG["borderColor"])
    WINDOW_OPACITY = data.get("windowOpacity", DEFAULT_CONFIG["windowOpacity"])


class StickyPagesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window size
        self.setFixedSize(WIDTH, HEIGHT)

        # Apply frameless window with rounded corners
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowOpacity(WINDOW_OPACITY)

        # Create central widget with border
        self.central_widget = QWidget(self)
        self.central_widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setCentralWidget(self.central_widget)

        # Web view (smaller than total area so border space is visible)
        self.web_view = QWebEngineView(self.central_widget)
        padding = BORDER_WIDTH
        self.web_view.setGeometry(
            QRect(padding, padding, WIDTH - padding * 2, HEIGHT - padding * 2)
        )
        self.web_view.setUrl(QUrl(WEBPAGE_URL))

        # Slight delay to ensure proper window mask
        QTimer.singleShot(0, self.apply_rounded_mask)

    def apply_rounded_mask(self):
        """Apply rounded-corner mask to the window."""
        path = QPainterPath()
        path.addRoundedRect(0, 0, WIDTH, HEIGHT, CORNER_RADIUS, CORNER_RADIUS)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def paintEvent(self, event):
        """Draw translucent rounded border on top of the web view."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        def parse_rgba(s):
            if s.startswith("rgba"):
                vals = [x.strip() for x in s[5:-1].split(",")]
                r, g, b, a = map(float, vals)
                return QColor(int(r), int(g), int(b), int(a * 255))
            return QColor(s)

        color = parse_rgba(BORDER_COLOR)
        pen = QPen(color)
        pen.setWidth(BORDER_WIDTH)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        rect = self.rect().adjusted(
            BORDER_WIDTH // 2,
            BORDER_WIDTH // 2,
            -BORDER_WIDTH // 2,
            -BORDER_WIDTH // 2,
        )

        painter.drawRoundedRect(rect, CORNER_RADIUS, CORNER_RADIUS)
        painter.end()

    def keyPressEvent(self, event: QKeyEvent):
        """Handle keyboard shortcuts"""
        # Alt+F4 to close the window
        if (
            event.key() == Qt.Key.Key_F4
            and event.modifiers() == Qt.KeyboardModifier.AltModifier
        ):
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

    sys.exit(app.exec())


if __name__ == "__main__":
    load_config(path="config.json")
    main()
