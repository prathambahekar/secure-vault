from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QApplication, QMainWindow, QWidget, QHBoxLayout
from PyQt6.QtCore import QSize, Qt, QPropertyAnimation

class SidebarButton(QPushButton):
    def __init__(self, icon, text, theme=None, parent=None):
        super().__init__(icon, parent)
        self.full_text = text
        self.theme = theme if theme else {}
        self.apply_style()

    def apply_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.theme.get('button_bg', 'transparent')};
                color: {self.theme.get('text_color', '#000000')};
                border: none;
                border-radius: 5px;
                padding: 5px;
                font-size: 20px;
                margin: 2px;
                text-align: center;
            }}
            QPushButton:hover {{
                background-color: {self.theme.get('button_hover', '#2d2d2d')};
            }}
            QPushButton:pressed {{
                background-color: {self.theme.get('button_pressed', 'rgba(0, 0, 0, 60)')};
            }}
        """)

    def update_theme(self, new_theme):
        self.theme = new_theme
        self.apply_style()

class xSidebar(QFrame):
    def __init__(self, parent=None, theme=None):
        super().__init__(parent)
        self.theme = theme if theme is not None else {}
        self.is_expanded = False
        self.min_width = 50
        self.max_width = 200
        self.setMinimumWidth(self.min_width)
        self.setMaximumWidth(self.max_width)
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(6)

        self.toggle_btn = SidebarButton("☰", "Menu", self.theme, self)
        self.toggle_btn.setFixedHeight(50)
        
        self.home_btn = SidebarButton("🏠", "Home", self.theme, self)
        self.home_btn.setFixedHeight(50)
        
        self.settings_btn = SidebarButton("⚙", "Settings", self.theme, self)
        self.settings_btn.setFixedHeight(50)

        self.layout.addWidget(self.toggle_btn)
        self.layout.addWidget(self.home_btn)
        self.layout.addStretch()
        self.layout.addWidget(self.settings_btn)

        self.toggle_btn.clicked.connect(self.toggle_sidebar)

    def apply_theme(self):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {self.theme.get('bg_color', 'rgba(243, 243, 243, 180)')};
                border: none;
                border-radius: 7px;
            }}
        """)
        for btn in [self.toggle_btn, self.home_btn, self.settings_btn]:
            btn.update_theme(self.theme)

    def toggle_sidebar(self):
        present_width = self.width()
        
        start_width = present_width
        end_width = self.max_width if present_width == self.min_width else self.min_width

        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(200)
        self.animation.setStartValue(start_width)
        self.animation.setEndValue(end_width)

        if not self.is_expanded:
            self.home_btn.setText("Home")
            self.settings_btn.setText("Settings")
            self.toggle_btn.setText("✖")
        else:
            self.home_btn.setText("🏠")
            self.settings_btn.setText("⚙")
            self.toggle_btn.setText("☰")

        self.animation.start()
        self.is_expanded = not self.is_expanded

    def connect_buttons(self, home_slot, settings_slot):
        self.home_btn.clicked.connect(home_slot)
        self.settings_btn.clicked.connect(settings_slot)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        self.sidebar = xSidebar(self)
        self.sidebar.connect_buttons(self.home_clicked, self.settings_clicked)
        main_layout.addWidget(self.sidebar)
        
        self.content = QWidget()
        self.content.setStyleSheet("background-color: white;")
        main_layout.addWidget(self.content, stretch=1)

    def home_clicked(self):
        print("Home button clicked!")

    def settings_clicked(self):
        print("Settings button clicked!")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())