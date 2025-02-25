# files/gui/settings_page.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from files.gui.ui_components import *
from PyQt6.QtCore import Qt

class SettingsPage(QWidget):
    def __init__(self, parent, theme):
        super().__init__(parent)
        self.parent = parent  # Reference to MainWindow
        self.current_theme = theme
        self.setup_ui()

    def setup_ui(self):
        settings_layout = QVBoxLayout(self)
        settings_layout.setContentsMargins(20, 20, 20, 20)

        settings_label = xLabel("Settings", self.current_theme, self)
        settings_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # settings_label.setAlignment(Qt.AlignCenter)

        settings_layout.addWidget(settings_label)

        # Placeholder for settings content
        placeholder = xLabel("Settings content goes here", self.current_theme, self)
        settings_layout.addWidget(placeholder)
        settings_layout.addStretch()

    def apply_theme(self, theme):
        self.current_theme = theme
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if hasattr(widget, 'update_theme'):
                widget.update_theme(theme)
        self.setStyleSheet(f"background-color: {theme['def_bg']}; border-radius: 5px;")