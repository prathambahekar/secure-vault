# xbutton.py
from PyQt6.QtWidgets import QPushButton

class xButton(QPushButton):
    def __init__(self, text, theme, parent=None):
        super().__init__(text, parent)
        self.theme = theme
        self.apply_theme()

    def apply_theme(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.theme['accent_color']};
                color: {self.theme['selected_text_color']};
                padding: 10px 20px;
                font: {self.theme['font_size_medium']} "{self.theme['font_family']}";
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {self.theme['accent_hover']};
            }}
            QPushButton:pressed {{
                background-color: {self.theme['accent_pressed']};
            }}
        """)

    def update_theme(self, new_theme):
        """Update the theme and reapply the stylesheet."""
        self.theme = new_theme
        self.apply_theme()