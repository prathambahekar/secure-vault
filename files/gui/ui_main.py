from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel, QDialog, QMessageBox
from PyQt6.QtCore import Qt
import os
import shutil
import uuid
import hashlib
import base64, darkdetect
from files.gui.modules import *
from files.app.app_functions import *
import files.app.config as config
from files.gui.ui_components import *


  # Adjust the import path as needed

key_file = config.MASTER_KEY_FILE
locked_file = config.LOCKED_ITEMS_FILE
access_log = config.ACCESS_LOG_FILE
secure_dir = config.SECURE_DIR
theme_dark = config.STYLE_CONFIG_DARK
theme_light = config.STYLE_CONFIG_LIGHT
is_menubar = config.SETTINGS["menu_bar_enabled"]
passMinSize = 4  # Adjusted for example; original was 8

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔒 PySecureVault 🗝️")
        self.setGeometry(100, 100, 700, 500)
        self.locked_items = AppFunctions.load_locked_items()
        self.item_path = None
        self.current_theme = theme_dark if darkdetect.isDark() else theme_light
        self.setup_ui()

        if os.name == "nt":
            try:
                self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
                ApplyMica(self.winId(), MicaTheme.AUTO, MicaStyle.DEFAULT)
            except Exception as e:
                print(f"Failed to apply Mica effect: {e}")
                self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)

    def setup_ui(self):
        # Set up the menu bar
        if is_menubar:
            self.menu_bar = xMenuBar(self.current_theme, self)
            self.setMenuBar(self.menu_bar)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Top bar with title and theme toggle
        top_bar = QHBoxLayout()
        self.title_label = xLabel("🔒 Secure Vault 🔑", self.current_theme, self)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_bar.addWidget(self.title_label)
        top_bar.addStretch()
        self.theme_toggle = xButton("Light", self.current_theme, self)
        self.theme_toggle.setFixedWidth(100)
        self.theme_toggle.clicked.connect(self.toggle_theme)
        top_bar.addWidget(self.theme_toggle)
        layout.addLayout(top_bar)

        self.drop_area = DropArea(self, self.current_theme)
        self.drop_area.mousePressEvent = lambda event: self.select_item()
        layout.addWidget(self.drop_area, stretch=1)

        self.list_widget = xListWidget(self.current_theme, self)
        self.list_widget.list_widget.setVerticalScrollBar(xScrollBar(self.current_theme, self))
        self.update_list()
        layout.addWidget(self.list_widget, stretch=2)

        category_layout = QHBoxLayout()
        category_label = QLabel("Filter by Category:", self)
        category_layout.addWidget(category_label)
        self.category_combo = xComboBox(self.current_theme, self)
        self.category_combo.addItems(["All", "Personal", "Work", "Other"])
        self.category_combo.currentTextChanged.connect(self.filter_items)
        category_layout.addWidget(self.category_combo)
        layout.addLayout(category_layout)

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
        layout.addLayout(action_layout)

        self.apply_theme()

    def apply_theme(self):
        theme = self.current_theme
        self.drop_area.apply_theme(theme)
        self.list_widget.update_theme(theme)
        self.list_widget.list_widget.verticalScrollBar().update_theme(theme)
        self.category_combo.update_theme(theme)
        self.title_label.update_theme(theme)
        # Update all xButton instances
        self.theme_toggle.update_theme(theme)
        self.open_btn.update_theme(theme)
        self.lock_btn.update_theme(theme)
        self.unlock_btn.update_theme(theme)
        self.delete_btn.update_theme(theme)
        self.centralWidget().layout().itemAt(3).layout().itemAt(0).widget().setStyleSheet(
            f"font: {theme['font_size_medium']} \"{theme['font_family']}\"; color: {theme['text_color']};"
        )
        self.setStyleSheet(f"background-color: {theme['bg_color']};")

        # Update the menu bar theme
        if is_menubar:
            self.menu_bar.update_theme(theme)

    def toggle_theme(self):
        self.current_theme = theme_light if self.current_theme == theme_dark else theme_dark
        self.theme_toggle.setText("Dark" if self.current_theme == theme_light else "Light")
        self.apply_theme()
        if os.name == "nt":
            try:
                ApplyMica(
                    int(self.winId()),
                    Theme=MicaTheme.LIGHT if self.current_theme == theme_light else MicaTheme.DARK,
                    Style=MicaStyle.DEFAULT
                )
            except Exception as e:
                print(f"Failed to update Mica theme: {e}")

    def select_item(self):
        item_path, _ = QFileDialog.getOpenFileName(self, "Select File or Folder", "", "All Files (*)")
        if not item_path:
            item_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if item_path:
            self.item_path = item_path
            self.drop_area.setText(f"Selected: {os.path.basename(item_path)}")

    def lock_item(self):
        if not self.item_path:
            AppFunctions.show_message(self, "Please select an item!", "Error", self.current_theme)
            self.drop_area.setText("Drag and Drop Files or Folders Here\nor Click to Select")
            return
        dialog = PasswordDialog("Set Password", "Enter password for item:", self, self.current_theme)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            password = dialog.password_input.text()
            if not password or len(password) < passMinSize:
                AppFunctions.show_message(self, f"Password must be {passMinSize}+ characters!", "Error", self.current_theme)
                return
            try:
                salt = AppFunctions.encrypt_items(self.item_path, password)
                secure_path = os.path.join(secure_dir, str(uuid.uuid4()))
                shutil.move(self.item_path, secure_path)
                item_hash = hashlib.sha256(password.encode()).hexdigest()
                self.locked_items[os.path.basename(self.item_path)] = {
                    "original_path": self.item_path,
                    "secure_path": secure_path,
                    "salt": base64.b64encode(salt).decode(),
                    "hash": item_hash,
                    "category": self.category_combo.currentText() if self.category_combo.currentText() != "All" else "Uncategorized"
                }
                AppFunctions.save_locked_items(self.locked_items)
                AppFunctions.log_action(f"Locked item: {self.item_path}")
                AppFunctions.show_message(self, "Item locked successfully!", "Success", self.current_theme)
                self.update_list()
                self.item_path = None
                self.drop_area.setText("Drag and Drop Files or Folders Here\nor Click to Select")
            except Exception as e:
                AppFunctions.show_message(self, f"Error locking item: {str(e)}", "Error", self.current_theme)

    def unlock_item(self):
        selected = self.list_widget.current_item()
        if not selected:
            AppFunctions.show_message(self, "Please select an item to unlock!", "Error", self.current_theme)
            return
        item_name = selected.text().split(" (")[0]
        item_data = self.locked_items.get(item_name)
        if not item_data:
            AppFunctions.show_message(self, "Item not found!", "Error", self.current_theme)
            return
        dialog = PasswordDialog("Unlock Item", f"Enter password for {item_name}:", self, self.current_theme)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            password = dialog.password_input.text()
            if not password:
                AppFunctions.show_message(self, "Password required!", "Error", self.current_theme)
                return
            if hashlib.sha256(password.encode()).hexdigest() != item_data["hash"]:
                AppFunctions.show_message(self, "Incorrect password!", "Error", self.current_theme)
                AppFunctions.log_action(f"Failed unlock attempt: {item_name}")
                return
            try:
                salt = base64.b64decode(item_data["salt"])
                AppFunctions.decrypt_items(item_data["secure_path"], password, salt)
                shutil.move(item_data["secure_path"], item_data["original_path"])
                del self.locked_items[item_name]
                AppFunctions.save_locked_items(self.locked_items)
                AppFunctions.log_action(f"Unlocked item: {item_name}")
                AppFunctions.show_message(self, "Item unlocked successfully!", "Success", self.current_theme)
                self.update_list()
            except Exception as e:
                AppFunctions.show_message(self, f"Error unlocking item: {str(e)}", "Error", self.current_theme)

    def delete_item(self):
        selected = self.list_widget.current_item()
        if not selected:
            AppFunctions.show_message(self, "Please select an item to delete!", "Error", self.current_theme)
            return
        item_name = selected.text().split(" (")[0]
        item_data = self.locked_items.get(item_name)
        if not item_data:
            AppFunctions.show_message(self, "Item not found!", "Error", self.current_theme)
            return
        reply = QMessageBox.question(self, "Confirm Deletion", f"Permanently delete {item_name}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            dialog = PasswordDialog("Delete Item", f"Enter password for {item_name} to confirm deletion:",
                                    self, self.current_theme)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                password = dialog.password_input.text()
                if hashlib.sha256(password.encode()).hexdigest() == item_data["hash"]:
                    try:
                        AppFunctions.secure_delete(item_data["secure_path"])
                        del self.locked_items[item_name]
                        AppFunctions.save_locked_items(self.locked_items)
                        AppFunctions.log_action(f"Deleted item: {item_name}")
                        AppFunctions.show_message(self, "Item deleted successfully!", "Success", self.current_theme)
                        self.update_list()
                    except Exception as e:
                        AppFunctions.show_message(self, f"Error deleting item: {str(e)}", "Error", self.current_theme)
                else:
                    AppFunctions.show_message(self, "Incorrect password!", "Error", self.current_theme)
                    AppFunctions.log_action(f"Failed delete attempt: {item_name}")

    def update_list(self):
        self.list_widget.clear()
        for name, data in self.locked_items.items():
            self.list_widget.add_item(f"{name} ({data['category']})")

    def filter_items(self, category):
        self.list_widget.clear()
        for name, data in self.locked_items.items():
            if category == "All" or data["category"] == category:
                self.list_widget.add_item(f"{name} ({data['category']})")