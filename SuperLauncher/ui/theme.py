from PyQt6.QtGui import QColor, QFont

class ThemeManager:
    DARK = {
        "bg_primary": "#1a1a2e",
        "bg_secondary": "#16213e",
        "bg_card": "rgba(255,255,255,0.05)",
        "fg_primary": "#cdd6f4",
        "fg_secondary": "#a0a0b0",
        "accent": "#4facfe",
        "accent_gradient": ("#667eea", "#764ba2"),
        "border": "#313244",
        "success": "#4caf50",
        "warning": "#ff9800",
        "error": "#f44336",
        "sidebar_bg": ("#14141e", "#0c0c14"),
        "glass_bg": "rgba(25,25,35,0.85)",
        "glass_border": "rgba(255,255,255,0.1)",
    }

    LIGHT = {
        "bg_primary": "#f5f7fa",
        "bg_secondary": "#ffffff",
        "bg_card": "rgba(0,0,0,0.03)",
        "fg_primary": "#2c3e50",
        "fg_secondary": "#7f8c8d",
        "accent": "#4facfe",
        "accent_gradient": ("#667eea", "#764ba2"),
        "border": "#dcdde1",
        "success": "#27ae60",
        "warning": "#f39c12",
        "error": "#e74c3c",
        "sidebar_bg": ("#f0f2f5", "#e8ecf1"),
        "glass_bg": "rgba(255,255,255,0.85)",
        "glass_border": "rgba(0,0,0,0.1)",
    }

    def __init__(self):
        self._theme = self.DARK

    @property
    def colors(self):
        return self._theme

    def set_dark(self, dark=True):
        self._theme = self.DARK if dark else self.LIGHT

    def stylesheet(self):
        c = self._theme
        return f"""
            QWidget {{ font-family: 'Segoe UI'; font-size: 13px; color: {c['fg_primary']}; }}
            QPushButton {{
                background-color: {c['accent']}; color: white; border-radius: 8px;
                padding: 8px 16px; font-weight: bold; border: none;
            }}
            QPushButton:hover {{ background-color: #6db8ff; }}
            QPushButton:pressed {{ background-color: #3d8fd4; }}
            QLineEdit {{
                background: rgba(255,255,255,0.08); color: {c['fg_primary']};
                border: 1px solid {c['border']}; border-radius: 6px; padding: 8px;
            }}
            QLineEdit:focus {{ border-color: {c['accent']}; }}
            QComboBox {{
                background: rgba(255,255,255,0.08); color: {c['fg_primary']};
                border: 1px solid {c['border']}; border-radius: 6px; padding: 6px;
            }}
            QComboBox QAbstractItemView {{
                background: #2a2a3a; color: white;
                selection-background-color: {c['accent']};
                border: 1px solid {c['border']};
            }}
            QListWidget {{
                background: rgba(255,255,255,0.03); border: 1px solid {c['border']};
                border-radius: 8px; color: {c['fg_primary']}; outline: none;
            }}
            QListWidget::item {{ padding: 8px; }}
            QListWidget::item:hover {{ background: rgba(255,255,255,0.05); }}
            QListWidget::item:selected {{ background: rgba(79,172,254,0.2); }}
            QScrollBar:vertical {{
                background: transparent; width: 8px;
            }}
            QScrollBar::handle:vertical {{
                background: rgba(255,255,255,0.15); border-radius: 4px; min-height: 30px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
            QProgressBar {{
                background: rgba(255,255,255,0.05); border: none; border-radius: 4px;
                text-align: center; color: white; height: 8px;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #7C4DFF, stop:1 #448AFF);
                border-radius: 4px;
            }}
            QTextEdit, QTextBrowser {{
                background: rgba(0,0,0,0.3); border: 1px solid {c['border']};
                border-radius: 8px; color: {c['fg_primary']}; padding: 8px;
            }}
            QScrollArea {{ border: none; background: transparent; }}
            QGroupBox {{
                color: white; font-size: 14px; font-weight: bold;
                border: 1px solid {c['border']}; border-radius: 8px;
                margin-top: 12px; padding-top: 16px;
            }}
            QGroupBox::title {{ subcontrol-origin: margin; left: 12px; padding: 0 4px; }}
            QCheckBox {{ color: {c['fg_primary']}; }}
            QSpinBox {{
                background: rgba(255,255,255,0.08); color: {c['fg_primary']};
                border: 1px solid {c['border']}; border-radius: 4px; padding: 4px;
            }}
        """
