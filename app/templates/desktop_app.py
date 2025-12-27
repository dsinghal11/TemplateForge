"""Desktop Application Template with Optional API Integration - UPDATED"""

BASE_TEMPLATE = {
    "app/__init__.py": "",
    "app/main.py": """from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
import sys
import logging
from app.ui.main_window import MainWindow
from app.config.settings import settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    logger.info(f"Starting {settings.APP_NAME}")
    
    app = QApplication(sys.argv)
    app.setApplicationName(settings.APP_NAME)
    app.setOrganizationName(settings.ORGANIZATION)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
""",
    "app/config/__init__.py": '"""Configuration package"""',
    "app/config/settings.py": """from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "{{name}}"
    ORGANIZATION: str = "MyOrganization"
    VERSION: str = "1.0.0"
    
    # Window settings
    WINDOW_WIDTH: int = 1024
    WINDOW_HEIGHT: int = 768
    
    # Paths
    DATA_DIR: str = "data"
    LOG_DIR: str = "logs"
    
    # Optional Database settings
    DATABASE_URL: Optional[str] = None
    MONGODB_URL: Optional[str] = None
    MONGODB_DB: Optional[str] = None
    
    # Optional settings
    DEBUG: bool = False
    SECRET_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields from .env

settings = Settings()
""",
    "app/services/__init__.py": '"""Services package"""',
    "app/services/data_service.py": """\"\"\"
Data service for business logic
\"\"\"
import logging
from typing import List, Optional
from app.models.data_model import DataItem

logger = logging.getLogger(__name__)


class DataService:
    \"\"\"Service for managing data operations\"\"\"
    
    def __init__(self):
        self.items: List[DataItem] = []
        logger.info("DataService initialized")
    
    def add_item(self, item: DataItem) -> bool:
        \"\"\"Add a new item\"\"\"
        try:
            self.items.append(item)
            logger.info(f"Added item: {item.name}")
            return True
        except Exception as e:
            logger.error(f"Error adding item: {e}")
            return False
    
    def get_item(self, item_id: int) -> Optional[DataItem]:
        \"\"\"Get item by ID\"\"\"
        for item in self.items:
            if item.id == item_id:
                return item
        return None
    
    def get_all_items(self) -> List[DataItem]:
        \"\"\"Get all items\"\"\"
        return self.items
    
    def delete_item(self, item_id: int) -> bool:
        \"\"\"Delete item by ID\"\"\"
        for i, item in enumerate(self.items):
            if item.id == item_id:
                self.items.pop(i)
                logger.info(f"Deleted item: {item_id}")
                return True
        return False
""",
    "app/utils/__init__.py": '"""Utility functions"""',
    "app/utils/constants.py": """\"\"\"
Application constants
\"\"\"
import os

# Application
APP_NAME = os.getenv("APP_NAME", "{{name}}")
VERSION = "1.0.0"
ORGANIZATION = os.getenv("ORGANIZATION", "MyOrganization")

# Window Settings
DEFAULT_WINDOW_WIDTH = int(os.getenv("WINDOW_WIDTH", "1024"))
DEFAULT_WINDOW_HEIGHT = int(os.getenv("WINDOW_HEIGHT", "768"))

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "")
MONGODB_URL = os.getenv("MONGODB_URL", "")
MONGODB_DB = os.getenv("MONGODB_DB", "")

# Debug
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
""",
    "app/utils/helpers.py": """\"\"\"
Helper utility functions
\"\"\"
import json
from typing import Any, Dict
from datetime import datetime
from pathlib import Path


def format_date(date: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    \"\"\"Format datetime to string\"\"\"
    return date.strftime(format_str)


def load_json(file_path: str) -> Dict[str, Any]:
    \"\"\"Load JSON file\"\"\"
    with open(file_path, 'r') as f:
        return json.load(f)


def save_json(data: Dict[str, Any], file_path: str) -> None:
    \"\"\"Save data to JSON file\"\"\"
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


def ensure_dir(directory: str) -> None:
    \"\"\"Ensure directory exists\"\"\"
    Path(directory).mkdir(parents=True, exist_ok=True)


def generate_id() -> str:
    \"\"\"Generate unique ID\"\"\"
    import uuid
    return str(uuid.uuid4())
""",
    "app/ui/__init__.py": "",
    "app/ui/main_window.py": """from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QMenuBar, QMenu, QStatusBar,
    QMessageBox, QTabWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QFont
import logging
from app.config.settings import settings

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{settings.APP_NAME} v{settings.VERSION}")
        self.setMinimumSize(settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        
        self.init_ui()
        self.create_menu_bar()
        self.create_status_bar()
        
        logger.info("Main window initialized")
    
    def init_ui(self):
        \"\"\"Initialize the user interface\"\"\"
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel(f"Welcome to {settings.APP_NAME}")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Description
        description = QLabel("Desktop Application Template")
        description.setAlignment(Qt.AlignCenter)
        description.setStyleSheet("color: #666; font-size: 14px;")
        layout.addWidget(description)
        
        # Tab Widget for different sections
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Home Tab
        home_tab = self.create_home_tab()
        self.tabs.addTab(home_tab, "Home")
        
        # Action Buttons
        button_layout = QHBoxLayout()
        
        self.action_btn = QPushButton("Run Action")
        self.action_btn.clicked.connect(self.on_action_clicked)
        self.action_btn.setMinimumHeight(40)
        button_layout.addWidget(self.action_btn)
        
        self.settings_btn = QPushButton("Settings")
        self.settings_btn.clicked.connect(self.on_settings_clicked)
        self.settings_btn.setMinimumHeight(40)
        button_layout.addWidget(self.settings_btn)
        
        layout.addLayout(button_layout)
    
    def create_home_tab(self):
        \"\"\"Create the home tab\"\"\"
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        label = QLabel("This is your main workspace.")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 16px; padding: 20px;")
        layout.addWidget(label)
        
        info_label = QLabel(
            "• Add your custom widgets here\\n"
            "• Connect to your business logic\\n"
            "• Create intuitive user interfaces"
        )
        info_label.setStyleSheet("font-size: 14px; padding: 20px;")
        layout.addWidget(info_label)
        
        layout.addStretch()
        return widget
    
    def create_menu_bar(self):
        \"\"\"Create the menu bar\"\"\"
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("&File")
        
        new_action = QAction("&New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.on_new)
        file_menu.addAction(new_action)
        
        open_action = QAction("&Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.on_open)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help Menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_status_bar(self):
        \"\"\"Create the status bar\"\"\"
        self.statusBar().showMessage("Ready")
    
    def on_action_clicked(self):
        \"\"\"Handle action button click\"\"\"
        logger.info("Action button clicked")
        self.statusBar().showMessage("Action executed successfully", 3000)
        QMessageBox.information(self, "Action", "Action executed successfully!")
    
    def on_settings_clicked(self):
        \"\"\"Handle settings button click\"\"\"
        logger.info("Settings button clicked")
        QMessageBox.information(self, "Settings", "Settings dialog coming soon!")
    
    def on_new(self):
        \"\"\"Handle File -> New\"\"\"
        logger.info("New file action")
        self.statusBar().showMessage("New file created", 3000)
    
    def on_open(self):
        \"\"\"Handle File -> Open\"\"\"
        logger.info("Open file action")
        self.statusBar().showMessage("Open file dialog", 3000)
    
    def show_about(self):
        \"\"\"Show about dialog\"\"\"
        QMessageBox.about(
            self,
            f"About {settings.APP_NAME}",
            f"{settings.APP_NAME} v{settings.VERSION}\\n\\n"
            f"A desktop application built with PySide6.\\n\\n"
            f"Organization: {settings.ORGANIZATION}"
        )
""",
    "app/models/__init__.py": "",
    "app/models/data_model.py": """from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class DataItem:
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    def __str__(self):
        return f"{self.name} ({self.id})"
""",
    "requirements.txt": """PySide6>=6.5.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
python-dotenv>=1.0.0
""",
    ".env": """# Application
APP_NAME={{name}}
ORGANIZATION=MyOrganization
VERSION=1.0.0
WINDOW_WIDTH=1024
WINDOW_HEIGHT=768
""",
    "run.py": """#!/usr/bin/env python3
\"\"\"
Run the desktop application
\"\"\"
from app.main import main

if __name__ == "__main__":
    main()
""",
    "README.md": """# {{name}}

Desktop application built with PySide6 (Qt for Python).

## Features

- 🖥️ Modern Qt-based user interface
- 🌐 Cross-platform (Windows, macOS, Linux)
- 📋 Menu bar with common actions
- 📊 Status bar for feedback
- 🗂️ Tabbed interface
- ⚙️ Configuration management
- 📐 Architecture folder at project root with .drawio file for design

## Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\\Scripts\\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running

### Desktop Application
```bash
python run.py
```

## Development

### Project Structure

```
{{name}}/
├── architecture/           # Architecture documentation & design
│   ├── architecture.drawio # Visual architecture diagram
│   └── README.md           # Architecture documentation
├── app/
│   ├── config/            # Configuration files
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── ui/                # User interface components
│   │   ├── __init__.py
│   │   └── main_window.py
│   ├── models/            # Data models
│   │   ├── __init__.py
│   │   └── data_model.py
│   ├── services/          # Business logic services
│   │   ├── __init__.py
│   │   └── data_service.py
│   ├── core/              # Core functionality (logger, exceptions)
│   ├── utils/             # Utility functions
│   │   ├── __init__.py
│   │   ├── constants.py
│   │   └── helpers.py
│   ├── db/                # Database (if configured)
│   └── main.py            # Application entry point
├── run.py                 # Desktop app runner
├── .env                   # Environment configuration
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

### Architecture

The `/architecture` folder contains design documentation:
- Open `architecture.drawio` with https://app.diagrams.net/ to design your system
- Document component relationships and data flows
- Keep architecture docs updated as your project evolves

### Adding New Features

1. **Add new tabs**: Edit `app/ui/main_window.py` and add to QTabWidget
2. **Add new widgets**: Create new files in `app/ui/`
3. **Add services**: Create service classes in `app/services/`
4. **Add models**: Define data models in `app/models/`
5. **Add core logic**: Implement core functionality in `app/core/`
6. **Customize settings**: Edit `.env` file

## Building Executable

Install PyInstaller:
```bash
pip install pyinstaller
```

Create executable:
```bash
pyinstaller --onefile --windowed --name {{name}} run.py
```

The executable will be in the `dist/` folder.

## Configuration

Edit `.env` file to customize:
- APP_NAME: Application name
- ORGANIZATION: Organization name
- VERSION: Version number
- WINDOW_WIDTH: Default window width
- WINDOW_HEIGHT: Default window height

## License

MIT License
""",
    ".gitignore": """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# Environment
.env

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
*.log
logs/

# Database
*.db
*.sqlite3

# OS
.DS_Store
Thumbs.db

# PyInstaller
*.spec
"""
}

# Template-specific features
FEATURES = {
    "API Integration": {
        "api/__init__.py": "",
        "api/main.py": """from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="{{name}} API",
    description="REST API for {{name}} Desktop Application",
    version="1.0.0"
)

# Data Models
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None

class WelcomeResponse(BaseModel):
    message: str
    application: str
    version: str
    timestamp: datetime

# In-memory storage (replace with database in production)
items_db: List[Item] = []
item_id_counter = 1

@app.get("/", response_model=WelcomeResponse)
async def root():
    \"\"\"Welcome endpoint\"\"\"
    return WelcomeResponse(
        message="Welcome to {{name}} API",
        application="{{name}}",
        version="1.0.0",
        timestamp=datetime.now()
    )

@app.get("/welcome", response_model=WelcomeResponse)
async def welcome():
    \"\"\"Welcome endpoint with detailed information\"\"\"
    logger.info("Welcome endpoint accessed")
    return WelcomeResponse(
        message="Welcome! This is the {{name}} REST API. Visit /docs for API documentation.",
        application="{{name}}",
        version="1.0.0",
        timestamp=datetime.now()
    )

@app.get("/health")
async def health_check():
    \"\"\"Health check endpoint\"\"\"
    return {
        "status": "healthy",
        "timestamp": datetime.now()
    }

@app.get("/items", response_model=List[Item])
async def get_items():
    \"\"\"Get all items\"\"\"
    logger.info(f"Retrieving {len(items_db)} items")
    return items_db

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    \"\"\"Get item by ID\"\"\"
    for item in items_db:
        if item.id == item_id:
            logger.info(f"Retrieved item {item_id}")
            return item
    
    logger.warning(f"Item {item_id} not found")
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items", response_model=Item, status_code=201)
async def create_item(item: ItemCreate):
    \"\"\"Create a new item\"\"\"
    global item_id_counter
    
    new_item = Item(
        id=item_id_counter,
        name=item.name,
        description=item.description,
        created_at=datetime.now()
    )
    
    items_db.append(new_item)
    item_id_counter += 1
    
    logger.info(f"Created item {new_item.id}: {new_item.name}")
    return new_item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item_update: ItemCreate):
    \"\"\"Update an existing item\"\"\"
    for item in items_db:
        if item.id == item_id:
            item.name = item_update.name
            item.description = item_update.description
            logger.info(f"Updated item {item_id}")
            return item
    
    logger.warning(f"Item {item_id} not found for update")
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    \"\"\"Delete an item\"\"\"
    global items_db
    
    for i, item in enumerate(items_db):
        if item.id == item_id:
            deleted_item = items_db.pop(i)
            logger.info(f"Deleted item {item_id}: {deleted_item.name}")
            return {"message": f"Item {item_id} deleted successfully"}
    
    logger.warning(f"Item {item_id} not found for deletion")
    raise HTTPException(status_code=404, detail="Item not found")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    \"\"\"Global exception handler\"\"\"
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
""",
        "run_api.py": """#!/usr/bin/env python3
\"\"\"
Run the FastAPI server
\"\"\"
import uvicorn
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting FastAPI server...")
    logger.info("API Documentation: http://localhost:8000/docs")
    logger.info("Welcome endpoint: http://localhost:8000/welcome")
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
""",
        "requirements.txt": """PySide6>=6.5.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
python-dotenv>=1.0.0
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
"""
    }
}