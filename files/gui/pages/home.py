# files/gui/home_page.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel
from PyQt6.QtCore import Qt
from files.gui.ui_components import *
from files.app.app_functions import *

class HomePage(QWidget):
    def __init__(self, parent, theme):
        super().__init__(parent)
        self.parent = parent  # Reference to MainWindow
        self.current_theme = theme
        self.item_path = None
        self.setup_ui()

    def setup_ui(self):
        central_layout = QVBoxLayout(self)
        central_layout.setContentsMargins(20, 20, 20, 20)
        central_layout.setSpacing(10)

        # Top bar with title and theme toggle
        top_bar = QHBoxLayout()
        self.title_label = xLabel("🔒 Secure Vault 🔑", self.current_theme, self)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_bar.addWidget(self.title_label)
        top_bar.addStretch()
        self.theme_toggle = xButton("Light", self.current_theme, self)
        self.theme_toggle.setFixedWidth(100)
        self.theme_toggle.clicked.connect(self.parent.toggle_theme)  # Delegate to MainWindow
        top_bar.addWidget(self.theme_toggle)
        central_layout.addLayout(top_bar)

        self.drop_area = DropArea(self, self.current_theme)
        self.drop_area.mousePressEvent = lambda event: self.select_item()
        central_layout.addWidget(self.drop_area, stretch=1)

        self.list_widget = xListWidget(self.current_theme, self)
        self.list_widget.list_widget.setVerticalScrollBar(xScrollBar(self.current_theme, self))
        self.update_list()
        central_layout.addWidget(self.list_widget, stretch=2)

        category_layout = QHBoxLayout()
        category_label = QLabel("Filter by Category:", self)
        category_layout.addWidget(category_label)
        self.category_combo = xComboBox(self.current_theme, self)
        self.category_combo.addItems(["All", "Personal", "Work", "Other"])
        self.category_combo.currentTextChanged.connect(self.filter_items)
        category_layout.addWidget(self.category_combo)
        central_layout.addLayout(category_layout)

        action_layout = QHBoxLayout()
        action_layout.setSpacing(10)

        self.open_btn = xButton("Open Folder", self.current_theme, self)
        self.open_btn.clicked.connect(self.select_item)
        action_layout.addWidget(self.open_btn)

        self.lock_btn = xButton("Lock Folder", self.current_theme, self)
        self.lock_btn.clicked.connect(self.lock_item)
        action_layout.addWidget(self.lock_btn)

        self.unlock_btn = xButton("Unlock Folder", self.current_theme, self)
        self.unlock_btn.clicked.connect(self.unlock_item)
        action_layout.addWidget(self.unlock_btn)

        self.delete_btn = xButton("Secure Delete", self.current_theme, self)
        self.delete_btn.clicked.connect(self.delete_item)
        action_layout.addWidget(self.delete_btn)

        action_layout.addStretch()
        central_layout.addLayout(action_layout)

    def apply_theme(self, theme):
        self.current_theme = theme
        self.drop_area.apply_theme(theme)
        self.list_widget.update_theme(theme)
        self.list_widget.list_widget.verticalScrollBar().update_theme(theme)
        self.category_combo.update_theme(theme)
        self.title_label.update_theme(theme)
        self.theme_toggle.update_theme(theme)
        self.open_btn.update_theme(theme)
        self.lock_btn.update_theme(theme)
        self.unlock_btn.update_theme(theme)
        self.delete_btn.update_theme(theme)
        self.layout().itemAt(3).layout().itemAt(0).widget().setStyleSheet(
            f"font: {theme['font_size_medium']} \"{theme['font_family']}\"; color: {theme['text_color']};"
        )
        self.setStyleSheet(f"background-color: {theme['def_bg']}; border-radius: 5px;")

    def select_item(self):
        item_path, _ = QFileDialog.getOpenFileName(self, "Select File or Folder", "", "All Files (*)")
        if not item_path:
            item_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if item_path:
            self.item_path = item_path
            self.drop_area.setText(f"Selected: {os.path.basename(item_path)}")

    def lock_item(self):
        # Delegate to parent (MainWindow) for shared logic
        self.parent.lock_item(self)

    def unlock_item(self):
        self.parent.unlock_item(self)

    def delete_item(self):
        self.parent.delete_item(self)

    def update_list(self):
        self.list_widget.clear()
        for name, data in self.parent.locked_items.items():
            self.list_widget.add_item(f"{name} ({data['category']})")

    def filter_items(self, category):
        self.list_widget.clear()
        for name, data in self.parent.locked_items.items():
            if category == "All" or data["category"] == category:
                self.list_widget.add_item(f"{name} ({data['category']})")