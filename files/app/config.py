import os

# Constants and Initial Setup
MASTER_KEY_FILE = "master.key"
LOCKED_ITEMS_FILE = "locked_items.enc"
ACCESS_LOG_FILE = "access.log.enc"
SECURE_DIR = os.path.join(os.path.expanduser("~"), ".pysecurevault", "locked_items")
os.makedirs(SECURE_DIR, exist_ok=True)
if os.name == "nt":  # Windows: Make directory hidden
    os.system(f'attrib +h "{os.path.dirname(SECURE_DIR)}"')

SETTINGS = {
    "app" : {
        "name" : "🔒 Secure Vault 🗝️",
        "version" : "v0.0.5",
        "build" : "dev"
    },
    "menu_bar_enabled" : False,
    "is_mica" : True
    
}

# Centralized Style Configurations
STYLE_CONFIG_DARK = {
    "font_family": "Segoe UI Variable",
    "font_size_large": "14pt",
    "font_size_medium": "12pt",
    "font_size_title": "24pt",
    "text_color": "#e0e0e0",
    "bg_color": "transparent",
    "secondary_bg": "#252525",
    "def_bg": "#2c2c2c",
    "border_color": "#3a3a3a",
    "accent_color": "#f984a2",
    "accent_hover": "#f984a2",
    "accent_pressed": "#f984a2",
    "hover_bg": "#2d2d2d",
    "selected_bg": "#f984a2",
    "selected_text_color": "#1e1e1e"
}

STYLE_CONFIG_LIGHT = {
    "font_family": "Segoe UI Variable",
    "font_size_large": "14pt",
    "font_size_medium": "12pt",
    "font_size_title": "24pt",
    "text_color": "#333333",
    "bg_color": "transparent",
    "secondary_bg": "#ffffff",
    "def_bg": "#ffffff",
    "border_color": "#d0d0d0",
    "accent_color": "#f984a2",
    "accent_hover": "#f984a2",
    "accent_pressed": "#f984a2",
    "hover_bg": "#e8e8e8",
    "selected_bg": "#f984a2",
    "selected_text_color": "white"
}