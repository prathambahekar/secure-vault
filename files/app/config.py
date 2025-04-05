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
        "name" : "🔒 Secure Vault 1234🗝️",
        "version" : "v0.0.5",
        "build" : "dev"
    },
    "theme" : "default",
    "menu_bar_enabled" : True,
    "is_mica" : True
    
}

# thene

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
    "accent_color": "#c8b7e1",
    "accent_hover": "#b9a6d3",
    "accent_pressed": "#a996c5",
    "hover_bg": "#2d2d2d",
    "selected_bg": "#b9a6d3",
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
    "accent_color": "#185abd",
    "accent_hover": "#185abd",
    "accent_pressed": "#185abd",
    "hover_bg": "#e8e8e8",
    "selected_bg": "#185abd",
    "selected_text_color": "white"
}