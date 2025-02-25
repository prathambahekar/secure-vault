# main.py
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from PyQt6.QtCore import Qt
import os
import shutil
import uuid
import hashlib
import base64
import darkdetect
from files.gui.modules import *
from files.app.app_functions import *
import files.app.config as config
from files.gui.ui_components import *
from files.gui.pages.home import HomePage
from files.gui.pages.settings import SettingsPage

key_file = config.MASTER_KEY_FILE
locked_file = config.LOCKED_ITEMS_FILE
access_log = config.ACCESS_LOG_FILE
secure_dir = config.SECURE_DIR
theme_dark = config.STYLE_CONFIG_DARK
theme_light = config.STYLE_CONFIG_LIGHT
is_menubar = config.SETTINGS["menu_bar_enabled"]
is_mica = config.SETTINGS["is_mica"]
passMinSize = 4

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(config.SETTINGS["app"]["name"])
        self.setGeometry(100, 100, 700, 500)
        self.locked_items = AppFunctions.load_locked_items()
        self.current_theme = theme_dark if darkdetect.isDark() else theme_light
        self.setup_ui()

        if os.name == "nt":
            try:
                if is_mica:
                    self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
                    ApplyMica(self.winId(), MicaTheme.AUTO, MicaStyle.DEFAULT)
            except Exception as e:
                print(f"Failed to apply Mica effect: {e}")
                self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)

    def setup_ui(self):
        if is_menubar:
            self.menu_bar = xMenuBar(self.current_theme, self)
            self.setMenuBar(self.menu_bar)

        container = QWidget()
        main_layout = QHBoxLayout(container)
        main_layout.setSpacing(10)

        self.sidebar = xSidebar(self, self.current_theme)
        self.sidebar.setFixedWidth(50)
        main_layout.addWidget(self.sidebar)

        self.stack_widget = QStackedWidget()
        self.home_page = HomePage(self, self.current_theme)
        self.settings_page = SettingsPage(self, self.current_theme)
        self.stack_widget.addWidget(self.home_page)
        self.stack_widget.addWidget(self.settings_page)

        self.sidebar.buttons["home"].clicked.connect(self.show_home_page)
        self.sidebar.buttons["settings"].clicked.connect(self.show_settings_page)

        main_layout.addWidget(self.stack_widget)
        self.setCentralWidget(container)
        self.apply_theme()

    def show_home_page(self):
        self.stack_widget.setCurrentWidget(self.home_page)
        print("Home page displayed")

    def show_settings_page(self):
        self.stack_widget.setCurrentWidget(self.settings_page)
        print("Settings page displayed")

    def apply_theme(self):
        self.current_theme = theme_light if self.current_theme == theme_dark else theme_dark
        self.home_page.apply_theme(self.current_theme)
        self.settings_page.apply_theme(self.current_theme)
        self.setStyleSheet(f"background-color: {self.current_theme['bg_color']};")
        if is_menubar:
            self.menu_bar.update_theme(self.current_theme)

    def toggle_theme(self):
        self.current_theme = theme_light if self.current_theme == theme_dark else theme_dark
        self.home_page.theme_toggle.setText("Dark" if self.current_theme == theme_light else "Light")
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

    def lock_item(self, page):
        if not page.item_path:
            AppFunctions.show_message(self, "Please select an item!", "Error", self.current_theme)
            page.drop_area.setText("Drag and Drop Files or Folders Here\nor Click to Select")
            return
        dialog = PasswordDialog("Set Password", "Enter password for item:", self, self.current_theme)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            password = dialog.password_input.text()
            if not password or len(password) < passMinSize:
                AppFunctions.show_message(self, f"Password must be {passMinSize}+ characters!", "Error", self.current_theme)
                return
            try:
                salt = AppFunctions.encrypt_items(page.item_path, password)
                secure_path = os.path.join(secure_dir, str(uuid.uuid4()))
                shutil.move(page.item_path, secure_path)
                item_hash = hashlib.sha256(password.encode()).hexdigest()
                self.locked_items[os.path.basename(page.item_path)] = {
                    "original_path": page.item_path,
                    "secure_path": secure_path,
                    "salt": base64.b64encode(salt).decode(),
                    "hash": item_hash,
                    "category": page.category_combo.currentText() if page.category_combo.currentText() != "All" else "Uncategorized"
                }
                AppFunctions.save_locked_items(self.locked_items)
                AppFunctions.log_action(f"Locked item: {page.item_path}")
                AppFunctions.show_message(self, "Item locked successfully!", "Success", self.current_theme)
                page.update_list()
                page.item_path = None
                page.drop_area.setText("Drag and Drop Files or Folders Here\nor Click to Select")
            except Exception as e:
                AppFunctions.show_message(self, f"Error locking item: {str(e)}", "Error", self.current_theme)

    def unlock_item(self, page):
        selected = page.list_widget.current_item()
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
                page.update_list()
            except Exception as e:
                AppFunctions.show_message(self, f"Error unlocking item: {str(e)}", "Error", self.current_theme)

    def delete_item(self, page):
        selected = page.list_widget.current_item()
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
                        page.update_list()
                    except Exception as e:
                        AppFunctions.show_message(self, f"Error deleting item: {str(e)}", "Error", self.current_theme)
                else:
                    AppFunctions.show_message(self, "Incorrect password!", "Error", self.current_theme)
                    AppFunctions.log_action(f"Failed delete attempt: {item_name}")

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())