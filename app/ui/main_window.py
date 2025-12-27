from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QComboBox, QCheckBox, QPushButton, QVBoxLayout, QHBoxLayout,
    QMessageBox, QFileDialog, QGroupBox, QScrollArea, QTextEdit,
    QProgressBar, QRadioButton, QButtonGroup
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont
from pathlib import Path
import sys
import logging

from app.generator.engine import generate_project
from app.templates import TEMPLATES

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GeneratorThread(QThread):
    """Background thread for project generation"""
    finished = Signal(bool, str)
    progress = Signal(str)

    def __init__(self, template, name, output_dir, config):
        super().__init__()
        self.template = template
        self.name = name
        self.output_dir = output_dir
        self.config = config

    def run(self):
        try:
            self.progress.emit("Generating project structure...")
            generate_project(
                template=self.template,
                name=self.name,
                output_dir=self.output_dir,
                config=self.config
            )
            self.progress.emit("Project generated successfully!")
            self.finished.emit(True, "Project created successfully!")
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            self.finished.emit(False, str(e))


class TemplateBuilderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TemplateForge - Project Generator")
        self.setGeometry(100, 100, 750, 600)
        self.setMinimumSize(700, 550)
        self.setMaximumSize(900, 750)

        self.output_dir = Path.cwd()
        self.generator_thread = None
        self.current_theme = "dark"

        self.init_ui()
        self.apply_theme(self.current_theme)

    def apply_theme(self, theme):
        """Apply dark or light theme with compact styling"""
        if theme == "dark":
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #1e1e1e;
                    color: #e8e8e8;
                    font-size: 11px;
                }
                QGroupBox {
                    border: 1px solid #3a3a3a;
                    font-size: 11px;
                    border-radius: 4px;
                    margin-top: 8px;
                    padding-top: 12px;
                    font-weight: bold;
                    color: #ffffff;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 8px;
                    padding: 0 5px;
                    color: #ffffff;
                }
                QLineEdit, QComboBox, QTextEdit {
                    background-color: #2d2d2d;
                    border: 1px solid #3a3a3a;
                    border-radius: 3px;
                    padding: 4px 6px;
                    font-size: 11px;
                    min-height: 20px;
                    color: #ffffff;
                }
                QLineEdit:focus, QComboBox:focus {
                    border: 1px solid #0078d4;
                    background-color: #333333;
                }
                QComboBox {
                    padding-right: 25px;
                }
                QComboBox::drop-down {
                    border: none;
                    width: 25px;
                }
                QComboBox::down-arrow {
                    image: none;
                    border-left: 4px solid transparent;
                    border-right: 4px solid transparent;
                    border-top: 5px solid #ffffff;
                    margin-right: 8px;
                }
                QComboBox QAbstractItemView {
                    background-color: #2d2d2d;
                    color: #ffffff;
                    selection-background-color: #0078d4;
                    border: 1px solid #3a3a3a;
                    font-size: 11px;
                    padding: 3px;
                }
                QPushButton {
                    background-color: #3a3a3a;
                    border: 1px solid #4a4a4a;
                    border-radius: 3px;
                    padding: 5px 10px;
                    color: #ffffff;
                    font-weight: bold;
                    font-size: 11px;
                    min-height: 22px;
                }
                QPushButton:hover {
                    background-color: #4a4a4a;
                    border: 1px solid #5a5a5a;
                }
                QPushButton:pressed {
                    background-color: #2a2a2a;
                }
                QCheckBox, QRadioButton {
                    color: #ffffff;
                    font-size: 11px;
                    spacing: 6px;
                    padding: 2px;
                }
                QCheckBox::indicator, QRadioButton::indicator {
                    width: 14px;
                    height: 14px;
                    border: 1px solid #4a4a4a;
                    border-radius: 2px;
                    background-color: #2d2d2d;
                }
                QCheckBox::indicator:checked {
                    background-color: #0078d4;
                    border-color: #0078d4;
                }
                QRadioButton::indicator {
                    border-radius: 8px;
                }
                QRadioButton::indicator:checked {
                    background-color: #0078d4;
                    border-color: #0078d4;
                }
                QScrollArea {
                    border: 1px solid #3a3a3a;
                    border-radius: 3px;
                    background-color: #1e1e1e;
                }
                QScrollBar:vertical {
                    border: none;
                    background: #2d2d2d;
                    width: 10px;
                    margin: 0px;
                }
                QScrollBar::handle:vertical {
                    background: #4a4a4a;
                    min-height: 20px;
                    border-radius: 5px;
                }
                QScrollBar::handle:vertical:hover {
                    background: #5a5a5a;
                }
                QProgressBar {
                    border: 1px solid #3a3a3a;
                    border-radius: 3px;
                    text-align: center;
                    background-color: #2d2d2d;
                    color: #ffffff;
                    font-size: 11px;
                    min-height: 20px;
                }
                QProgressBar::chunk {
                    background-color: #0078d4;
                }
                QLabel {
                    color: #e8e8e8;
                    font-size: 11px;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #ffffff;
                    color: #000000;
                    font-size: 11px;
                }
                QGroupBox {
                    border: 1px solid #d0d0d0;
                    border-radius: 4px;
                    margin-top: 8px;
                    padding-top: 12px;
                    font-weight: bold;
                    color: #000000;
                    font-size: 11px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 8px;
                    padding: 0 5px;
                    color: #000000;
                }
                QLineEdit, QComboBox, QTextEdit {
                    background-color: #f9f9f9;
                    border: 1px solid #d0d0d0;
                    border-radius: 3px;
                    padding: 4px 6px;
                    font-size: 11px;
                    min-height: 20px;
                    color: #000000;
                }
                QLineEdit:focus, QComboBox:focus {
                    border: 1px solid #0078d4;
                    background-color: #ffffff;
                }
                QComboBox {
                    padding-right: 25px;
                }
                QComboBox::drop-down {
                    border: none;
                    width: 25px;
                }
                QComboBox::down-arrow {
                    image: none;
                    border-left: 4px solid transparent;
                    border-right: 4px solid transparent;
                    border-top: 5px solid #000000;
                    margin-right: 8px;
                }
                QComboBox QAbstractItemView {
                    background-color: #ffffff;
                    color: #000000;
                    selection-background-color: #0078d4;
                    selection-color: #ffffff;
                    border: 1px solid #d0d0d0;
                    font-size: 11px;
                    padding: 3px;
                }
                QPushButton {
                    background-color: #f0f0f0;
                    border: 1px solid #d0d0d0;
                    border-radius: 3px;
                    padding: 5px 10px;
                    color: #000000;
                    font-weight: bold;
                    font-size: 11px;
                    min-height: 22px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                    border: 1px solid #b0b0b0;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
                QCheckBox, QRadioButton {
                    color: #000000;
                    font-size: 11px;
                    spacing: 6px;
                    padding: 2px;
                }
                QCheckBox::indicator, QRadioButton::indicator {
                    width: 14px;
                    height: 14px;
                    border: 1px solid #d0d0d0;
                    border-radius: 2px;
                    background-color: #ffffff;
                }
                QCheckBox::indicator:checked {
                    background-color: #0078d4;
                    border-color: #0078d4;
                }
                QRadioButton::indicator {
                    border-radius: 8px;
                }
                QRadioButton::indicator:checked {
                    background-color: #0078d4;
                    border-color: #0078d4;
                }
                QScrollArea {
                    border: 1px solid #d0d0d0;
                    border-radius: 3px;
                    background-color: #ffffff;
                }
                QScrollBar:vertical {
                    border: none;
                    background: #f0f0f0;
                    width: 10px;
                    margin: 0px;
                }
                QScrollBar::handle:vertical {
                    background: #d0d0d0;
                    min-height: 20px;
                    border-radius: 5px;
                }
                QScrollBar::handle:vertical:hover {
                    background: #b0b0b0;
                }
                QProgressBar {
                    border: 1px solid #d0d0d0;
                    border-radius: 3px;
                    text-align: center;
                    background-color: #f9f9f9;
                    color: #000000;
                    font-size: 11px;
                    min-height: 20px;
                }
                QProgressBar::chunk {
                    background-color: #0078d4;
                }
                QLabel {
                    color: #000000;
                    font-size: 11px;
                }
            """)

    def init_ui(self):
        """Initialize the user interface"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        central_widget = QWidget()
        scroll.setWidget(central_widget)
        self.setCentralWidget(scroll)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(12, 12, 12, 12)

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("TemplateForge")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        header_layout.addStretch()

        theme_label = QLabel("Theme:")
        theme_label.setStyleSheet("font-size: 11px; font-weight: bold;")
        header_layout.addWidget(theme_label)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        self.theme_combo.setMinimumWidth(100)
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        header_layout.addWidget(self.theme_combo)

        main_layout.addLayout(header_layout)

        subtitle = QLabel("Generate production-ready project templates")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 11px; padding: 5px;")
        main_layout.addWidget(subtitle)

        # Project Name
        name_group = QGroupBox("Project Configuration")
        name_layout = QVBoxLayout()
        name_layout.setSpacing(4)
        name_label = QLabel("Project Name:")
        name_label.setStyleSheet("font-weight: bold;")
        name_layout.addWidget(name_label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., my-awesome-project")
        self.name_input.textChanged.connect(self.validate_project_name)
        name_layout.addWidget(self.name_input)

        self.name_hint = QLabel("")
        name_layout.addWidget(self.name_hint)

        name_group.setLayout(name_layout)
        main_layout.addWidget(name_group)

        # Template Selection
        template_group = QGroupBox("Template Type")
        template_layout = QVBoxLayout()
        template_layout.setSpacing(4)
        template_label = QLabel("Select Template:")
        template_label.setStyleSheet("font-weight: bold;")
        template_layout.addWidget(template_label)

        self.template_combo = QComboBox()
        self.template_combo.addItems(TEMPLATES.keys())
        template_layout.addWidget(self.template_combo)

        self.template_description = QLabel()
        self.template_description.setWordWrap(True)
        self.template_description.setStyleSheet("font-size: 10px; padding-top: 5px; font-style: italic;")
        self.template_combo.currentTextChanged.connect(self.on_template_changed)
        template_layout.addWidget(self.template_description)

        template_group.setLayout(template_layout)
        main_layout.addWidget(template_group)

        # Template Features (Template-specific optional features)
        self.features_group = QGroupBox("Template Features (Optional)")
        features_layout = QVBoxLayout()
        features_layout.setSpacing(3)

        # Desktop: API Integration
        self.api_integration_check = QCheckBox("API Integration (FastAPI Server)")
        features_layout.addWidget(self.api_integration_check)

        # Node.js: API Integration
        self.node_api_check = QCheckBox("Advanced API Integration")
        features_layout.addWidget(self.node_api_check)

        # Node.js: WebSocket
        self.node_websocket_check = QCheckBox("WebSocket Support")
        features_layout.addWidget(self.node_websocket_check)

        self.features_group.setLayout(features_layout)
        main_layout.addWidget(self.features_group)

        # Database Configuration
        db_group = QGroupBox("Database (Optional)")
        db_layout = QVBoxLayout()
        db_layout.setSpacing(4)
        db_label = QLabel("Select Database:")
        db_label.setStyleSheet("font-weight: bold;")
        db_layout.addWidget(db_label)

        db_options_layout = QHBoxLayout()
        self.db_button_group = QButtonGroup()

        self.db_none_radio = QRadioButton("None")
        self.db_none_radio.setChecked(True)
        self.db_button_group.addButton(self.db_none_radio)
        db_options_layout.addWidget(self.db_none_radio)

        self.db_postgres_radio = QRadioButton("PostgreSQL")
        self.db_button_group.addButton(self.db_postgres_radio)
        db_options_layout.addWidget(self.db_postgres_radio)

        self.db_mongo_radio = QRadioButton("MongoDB")
        self.db_button_group.addButton(self.db_mongo_radio)
        db_options_layout.addWidget(self.db_mongo_radio)

        db_options_layout.addStretch()
        db_layout.addLayout(db_options_layout)

        db_group.setLayout(db_layout)
        main_layout.addWidget(db_group)

        # Output Directory
        output_layout = QHBoxLayout()
        output_label = QLabel("Output:")
        output_label.setStyleSheet("font-weight: bold;")
        output_layout.addWidget(output_label)

        self.output_path_label = QLabel(str(self.output_dir))
        self.output_path_label.setStyleSheet("font-size: 10px;")
        output_layout.addWidget(self.output_path_label, 1)

        folder_btn = QPushButton("Browse...")
        folder_btn.clicked.connect(self.select_folder)
        output_layout.addWidget(folder_btn)

        main_layout.addLayout(output_layout)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        # Status
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(80)
        self.status_text.setVisible(False)
        main_layout.addWidget(self.status_text)

        # Generate Button
        self.generate_btn = QPushButton("Generate Project")
        self.generate_btn.setMinimumHeight(32)
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                font-size: 12px;
                font-weight: bold;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #006cc1;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #666666;
                color: #999999;
            }
        """)
        self.generate_btn.clicked.connect(self.generate)
        main_layout.addWidget(self.generate_btn)

        self.on_template_changed(self.template_combo.currentText())

    def on_theme_changed(self, theme):
        """Handle theme change"""
        self.current_theme = theme.lower()
        self.apply_theme(self.current_theme)

    def validate_project_name(self, text):
        """Validate project name"""
        if not text:
            self.name_hint.setText("")
            return

        valid = all(c.isalnum() or c in '-_' for c in text)

        if not valid:
            self.name_hint.setText("⚠ Use only letters, numbers, hyphens, underscores")
            self.name_hint.setStyleSheet("color: #e74c3c; font-weight: bold; font-size: 10px;")
        else:
            self.name_hint.setText("✓ Valid project name")
            self.name_hint.setStyleSheet("color: #27ae60; font-weight: bold; font-size: 10px;")

    def on_template_changed(self, template):
        """Handle template selection change"""
        descriptions = {
            "React Web Dashboard": "Modern React app with TypeScript and organized structure",
            "Node.js Application": "Express.js REST API with TypeScript and best practices",
            "FastAPI Core Service": "High-performance REST API with async support",
            "Mobile App Backend": "Backend service for mobile apps",
            "Python Core Service": "Generic Python service with logging and config",
            "Desktop Application": "Cross-platform desktop app with Qt/PySide6"
        }

        self.template_description.setText(descriptions.get(template, ""))

        # Show/hide features based on template
        is_desktop = "Desktop" in template
        is_nodejs = "Node.js" in template

        # Show template-specific features
        self.api_integration_check.setVisible(is_desktop)
        self.node_api_check.setVisible(is_nodejs)
        self.node_websocket_check.setVisible(is_nodejs)

        # Show features group only if there are features for this template
        self.features_group.setVisible(is_desktop or is_nodejs)

    def select_folder(self):
        """Open folder selection dialog"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
            str(self.output_dir)
        )
        if folder:
            self.output_dir = Path(folder)
            self.output_path_label.setText(str(self.output_dir))

    def get_config(self):
        """Get current configuration"""
        template = self.template_combo.currentText()

        db_type = None
        if self.db_postgres_radio.isChecked():
            db_type = "postgresql"
        elif self.db_mongo_radio.isChecked():
            db_type = "mongodb"

        # Check for template features
        features = []
        if "Desktop" in template:
            if self.api_integration_check.isChecked():
                features.append("API Integration")
        elif "Node.js" in template:
            if self.node_api_check.isChecked():
                features.append("API Integration")
            if self.node_websocket_check.isChecked():
                features.append("WebSocket")

        config = {
            "enable_logger": True,  # Always enabled for Python
            "enable_exception_handler": True,  # Always enabled
            "git_init": True,
            "database_type": db_type,
            "features": features
        }

        return config

    def generate(self):
        """Generate the project"""
        name = self.name_input.text().strip()

        if not name:
            QMessageBox.critical(self, "Error", "Please enter a project name")
            return

        if not all(c.isalnum() or c in '-_' for c in name):
            QMessageBox.critical(
                self,
                "Error",
                "Project name can only contain letters, numbers, hyphens, and underscores"
            )
            return

        project_path = self.output_dir / name
        if project_path.exists():
            reply = QMessageBox.question(
                self,
                "Directory Exists",
                f"Directory '{name}' already exists. Overwrite?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return

        config = self.get_config()

        self.generate_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.status_text.setVisible(True)
        self.status_text.clear()

        self.generator_thread = GeneratorThread(
            self.template_combo.currentText(),
            name,
            self.output_dir,
            config
        )
        self.generator_thread.progress.connect(self.on_progress)
        self.generator_thread.finished.connect(self.on_generation_finished)
        self.generator_thread.start()

    def on_progress(self, message):
        """Update progress message"""
        self.status_text.append(message)

    def on_generation_finished(self, success, message):
        """Handle generation completion"""
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)

        if success:
            config = self.get_config()

            included_features = [
                "✓ Architecture folder at project root with .drawio file"
            ]

            template = self.template_combo.currentText()
            if "React" not in template and "Node.js" not in template:
                included_features.append("✓ Logger (file rotation)")
                included_features.append("✓ Exception Handler")

            if config.get("database_type"):
                included_features.append(f"✓ Database: {config['database_type'].upper()}")

            for feature in config.get("features", []):
                included_features.append(f"✓ {feature}")

            features_text = "\n".join(included_features)

            api_info = ""
            if "API Integration" in config.get("features", []) and "Desktop" in template:
                api_info = "\n\n🚀 API Server:\n- Run: python run_api.py\n- Docs: http://localhost:8000/docs\n- Welcome: http://localhost:8000/welcome"

            QMessageBox.information(
                self,
                "Success",
                f"Project '{self.name_input.text()}' created!\n\n"
                f"Location: {self.output_dir / self.name_input.text()}\n\n"
                f"Included:\n{features_text}"
                f"{api_info}\n\n"
                "Check README.md and SETUP.md for instructions."
            )
            self.status_text.append("\n✓ Generation complete!")
        else:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to generate project:\n{message}"
            )
            self.status_text.append(f"\n✗ Error: {message}")


def run():
    """Run the application"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = TemplateBuilderApp()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run()