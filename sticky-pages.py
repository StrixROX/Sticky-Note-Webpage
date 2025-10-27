import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import Qt, QUrl
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
        self.setStyleSheet('''
                           QMainWindow {
                               background-color: transparent;
                               border-radius: 10px;
                           }
                           ''')
        
        # Create central widget
        central_widget = QWidget(self)
        central_widget.setStyleSheet('''
                                     background-color: white;
                                     border-radius: 10px;
                                     ''')
        self.setCentralWidget(central_widget)
        
        # Create and configure web view
        self.web_view = QWebEngineView(central_widget)
        self.web_view.setUrl(QUrl(WEBPAGE_URL))
        self.web_view.setGeometry(0, 0, WIDTH, HEIGHT)
        
        # Make web view readonly (disable interaction)
        settings = self.web_view.settings()
        settings.setAttribute(settings.WebAttribute.JavascriptEnabled, False)
        settings.setAttribute(settings.WebAttribute.PluginsEnabled, False)


def main():
    app = QApplication(sys.argv)
    
    window = StickyPagesWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

