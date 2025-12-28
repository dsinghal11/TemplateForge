"""FastAPI Core Service Template - UPDATED with full structure"""

BASE_TEMPLATE = {
    "app/__init__.py": "",
    "app/main.py": """from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager
from app.config.settings import settings
from app.core.logger import setup_logger
from app.core.exceptions import AppException, handle_exception
from app.api.routes import router

# Setup logger
logger = setup_logger("fastapi_app", "app.log")


@asynccontextmanager
async def lifespan(app: FastAPI):
    \"\"\"Application lifespan events\"\"\"
    logger.info(f"Starting {settings.APP_NAME}")
    # Startup logic here
    yield
    # Shutdown logic here
    logger.info(f"Shutting down {settings.APP_NAME}")


app = FastAPI(
    title=settings.APP_NAME,
    description="High-performance REST API with async support",
    version=settings.VERSION,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    \"\"\"Handle custom application exceptions\"\"\"
    error_response = handle_exception(exc)
    return JSONResponse(
        status_code=400,
        content=error_response
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    \"\"\"Handle all unhandled exceptions\"\"\"
    logger.error(f"Unhandled exception: {exc}")
    error_response = handle_exception(exc)
    return JSONResponse(
        status_code=500,
        content=error_response
    )


@app.get("/")
async def root():
    \"\"\"Root endpoint\"\"\"
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    \"\"\"Health check endpoint\"\"\"
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
""",
    "app/config/__init__.py": '"""Configuration package"""',
    "app/config/settings.py": """from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "{{name}}"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # API
    API_PREFIX: str = "/api"
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # Security
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database (Optional)
    DATABASE_URL: Optional[str] = None
    MONGODB_URL: Optional[str] = None
    MONGODB_DB: Optional[str] = None
    
    # Paths
    LOG_DIR: str = "logs"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings()
""",
    "app/core/__init__.py": '"""Core functionality"""',
    "app/core/logger.py": """\"\"\"
Logging configuration with file rotation
\"\"\"
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(
    name: str = "app",
    log_file: str = "app.log",
    level: int = logging.INFO,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> logging.Logger:
    \"\"\"
    Setup logger with file rotation
    
    Args:
        name: Logger name
        log_file: Log file name
        level: Logging level
        max_bytes: Max file size before rotation
        backup_count: Number of backup files to keep
    
    Returns:
        Configured logger instance
    \"\"\"
    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_dir / log_file,
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    file_handler.setLevel(level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# Create default logger
logger = setup_logger()
""",
    "app/core/exceptions.py": """\"\"\"
Custom exception classes and handlers
\"\"\"
from typing import Any, Dict
import traceback
import logging

logger = logging.getLogger(__name__)


class AppException(Exception):
    \"\"\"Base application exception\"\"\"
    def __init__(self, message: str, code: str = "APP_ERROR", details: Dict[str, Any] = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(AppException):
    \"\"\"Validation error exception\"\"\"
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, "VALIDATION_ERROR", details)


class NotFoundError(AppException):
    \"\"\"Resource not found exception\"\"\"
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, "NOT_FOUND", details)


class AuthenticationError(AppException):
    \"\"\"Authentication error exception\"\"\"
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, "AUTH_ERROR", details)


class DatabaseError(AppException):
    \"\"\"Database error exception\"\"\"
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, "DATABASE_ERROR", details)


def handle_exception(exc: Exception) -> Dict[str, Any]:
    \"\"\"
    Handle exceptions and return formatted error response
    
    Args:
        exc: Exception instance
        
    Returns:
        Error response dictionary
    \"\"\"
    logger.error(f"Exception occurred: {str(exc)}")
    logger.error(traceback.format_exc())
    
    if isinstance(exc, AppException):
        return {
            "error": exc.code,
            "message": exc.message,
            "details": exc.details
        }
    
    return {
        "error": "INTERNAL_ERROR",
        "message": "An internal error occurred",
        "details": {}
    }
""",
    "app/utils/__init__.py": '"""Utility functions"""',
    "app/utils/constants.py": """\"\"\"
Application constants
\"\"\"
import os

# Application
APP_NAME = os.getenv("APP_NAME", "{{name}}")
VERSION = "1.0.0"

# API
API_PREFIX = os.getenv("API_PREFIX", "/api")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "")
MONGODB_URL = os.getenv("MONGODB_URL", "")
MONGODB_DB = os.getenv("MONGODB_DB", "")

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Debug
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Rate Limiting
RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

# Pagination
DEFAULT_PAGE_SIZE = int(os.getenv("DEFAULT_PAGE_SIZE", "20"))
MAX_PAGE_SIZE = int(os.getenv("MAX_PAGE_SIZE", "100"))
""",
    "app/utils/helpers.py": """\"\"\"
Helper utility functions
\"\"\"
import json
from typing import Any, Dict
from datetime import datetime
from pathlib import Path
import hashlib


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


def hash_password(password: str) -> str:
    \"\"\"Hash password using SHA-256\"\"\"
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    \"\"\"Verify password against hash\"\"\"
    return hash_password(password) == hashed


def paginate(items: list, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
    \"\"\"Paginate a list of items\"\"\"
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    
    return {
        "items": items[start:end],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }
""",
    "app/api/__init__.py": '"""API package"""',
    "app/api/routes.py": """\"\"\"
API route definitions
\"\"\"
from fastapi import APIRouter, HTTPException, Depends
from typing import List
import logging
from app.schemas.item import Item, ItemCreate
from app.services.item_service import ItemService

logger = logging.getLogger(__name__)

router = APIRouter()


def get_item_service():
    \"\"\"Dependency to get ItemService instance\"\"\"
    return ItemService()


@router.get("/items", response_model=List[Item])
async def get_items(service: ItemService = Depends(get_item_service)):
    \"\"\"Get all items\"\"\"
    logger.info("Retrieving all items")
    return service.get_all_items()


@router.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int, service: ItemService = Depends(get_item_service)):
    \"\"\"Get item by ID\"\"\"
    logger.info(f"Retrieving item {item_id}")
    item = service.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/items", response_model=Item, status_code=201)
async def create_item(item: ItemCreate, service: ItemService = Depends(get_item_service)):
    \"\"\"Create a new item\"\"\"
    logger.info(f"Creating item: {item.name}")
    return service.create_item(item)


@router.put("/items/{item_id}", response_model=Item)
async def update_item(
    item_id: int,
    item: ItemCreate,
    service: ItemService = Depends(get_item_service)
):
    \"\"\"Update an existing item\"\"\"
    logger.info(f"Updating item {item_id}")
    updated_item = service.update_item(item_id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item


@router.delete("/items/{item_id}")
async def delete_item(item_id: int, service: ItemService = Depends(get_item_service)):
    \"\"\"Delete an item\"\"\"
    logger.info(f"Deleting item {item_id}")
    success = service.delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": f"Item {item_id} deleted successfully"}
""",
    "app/schemas/__init__.py": '"""Pydantic schemas package"""',
    "app/schemas/item.py": """\"\"\"
Item schemas for request/response validation
\"\"\"
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class ItemCreate(ItemBase):
    \"\"\"Schema for creating an item\"\"\"
    pass


class Item(ItemBase):
    \"\"\"Schema for item response\"\"\"
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
""",
    "app/services/__init__.py": '"""Services package"""',
    "app/services/item_service.py": """\"\"\"
Item service for business logic
\"\"\"
import logging
from typing import List, Optional
from datetime import datetime
from app.schemas.item import Item, ItemCreate

logger = logging.getLogger(__name__)


class ItemService:
    \"\"\"Service for managing item operations\"\"\"
    
    def __init__(self):
        # In-memory storage (replace with database in production)
        self.items: List[Item] = []
        self.item_id_counter = 1
        logger.info("ItemService initialized")
    
    def create_item(self, item: ItemCreate) -> Item:
        \"\"\"Create a new item\"\"\"
        new_item = Item(
            id=self.item_id_counter,
            name=item.name,
            description=item.description,
            created_at=datetime.now()
        )
        self.items.append(new_item)
        self.item_id_counter += 1
        logger.info(f"Created item: {new_item.id}")
        return new_item
    
    def get_item(self, item_id: int) -> Optional[Item]:
        \"\"\"Get item by ID\"\"\"
        for item in self.items:
            if item.id == item_id:
                return item
        return None
    
    def get_all_items(self) -> List[Item]:
        \"\"\"Get all items\"\"\"
        return self.items
    
    def update_item(self, item_id: int, item_update: ItemCreate) -> Optional[Item]:
        \"\"\"Update an existing item\"\"\"
        for item in self.items:
            if item.id == item_id:
                item.name = item_update.name
                item.description = item_update.description
                item.updated_at = datetime.now()
                logger.info(f"Updated item: {item_id}")
                return item
        return None
    
    def delete_item(self, item_id: int) -> bool:
        \"\"\"Delete item by ID\"\"\"
        for i, item in enumerate(self.items):
            if item.id == item_id:
                self.items.pop(i)
                logger.info(f"Deleted item: {item_id}")
                return True
        return False
""",
    "app/models/__init__.py": "",
    "requirements.txt": """fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
python-dotenv>=1.0.0
""",
    ".env": """# Application
APP_NAME={{name}}
VERSION=1.0.0
DEBUG=True

# API
API_PREFIX=/api
ALLOWED_ORIGINS=*

# Security
SECRET_KEY=change-me-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Paths
LOG_DIR=logs
""",
    "run.py": """#!/usr/bin/env python3
\"\"\"
Run the FastAPI application
\"\"\"
import uvicorn
import logging
from app.config.settings import settings

logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info(f"Starting {settings.APP_NAME}")
    logger.info(f"API Documentation: http://localhost:8000/docs")
    logger.info(f"API Health Check: http://localhost:8000/health")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning"
    )
""",
    "README.md": """# {{name}}

High-performance REST API built with FastAPI and async support.

## Features

- 🚀 FastAPI framework with async support
- 📝 Automatic API documentation (Swagger/ReDoc)
- 🔒 Built-in security features
- 📊 Request validation with Pydantic
- 🗄️ Optional database integration (PostgreSQL/MongoDB)
- 📋 Logger with file rotation
- ⚠️ Exception handling
- 🎯 Service-based architecture
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

## Configuration

Edit `.env` file to customize settings:

```bash
APP_NAME={{name}}
DEBUG=True
SECRET_KEY=your-secret-key-here
```

## Running

### Development
```bash
python run.py
```

### Production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Development

### Project Structure

```
{{name}}/
├── architecture/           # Architecture documentation & design
│   ├── architecture.drawio # Visual architecture diagram
│   └── README.md           # Architecture documentation
├── app/
│   ├── api/               # API routes
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── config/            # Configuration
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── core/              # Core functionality (logger, exceptions)
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   └── exceptions.py
│   ├── db/                # Database (if configured)
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic schemas
│   │   ├── __init__.py
│   │   └── item.py
│   ├── services/          # Business logic
│   │   ├── __init__.py
│   │   └── item_service.py
│   ├── utils/             # Utility functions
│   │   ├── __init__.py
│   │   ├── constants.py
│   │   └── helpers.py
│   └── main.py            # Application entry point
├── logs/                  # Log files (auto-generated)
├── .env                   # Environment configuration
├── .gitignore             # Git ignore file
├── requirements.txt       # Python dependencies
├── run.py                 # Application runner
└── README.md              # This file
```

### Architecture

The `/architecture` folder contains design documentation:
- Open `architecture.drawio` with https://app.diagrams.net/ to design your system
- Document component relationships and data flows
- Keep architecture docs updated as your project evolves

### Adding New Features

1. **Add new endpoints**: Edit `app/api/routes.py`
2. **Add new schemas**: Create Pydantic models in `app/schemas/`
3. **Add new services**: Create service classes in `app/services/`
4. **Add database models**: Define models in `app/models/`
5. **Add utilities**: Add helper functions in `app/utils/`

### API Documentation

FastAPI automatically generates interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing

```bash
# Install testing dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables

Make sure to set production environment variables:
- `DEBUG=False`
- `SECRET_KEY=<strong-secret-key>`
- `DATABASE_URL=<your-database-url>` (if using database)

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

# FastAPI
.pytest_cache/
htmlcov/
.coverage
"""
}

# Optional Database Features
FEATURES = {
    "PostgreSQL": {
        "app/db/__init__.py": '"""Database package"""',
        "app/db/database.py": """\"\"\"
PostgreSQL database configuration
\"\"\"
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    \"\"\"Get database session\"\"\"
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    \"\"\"Initialize database tables\"\"\"
    Base.metadata.create_all(bind=engine)
""",
        "app/models/item_model.py": """\"\"\"
SQLAlchemy Item model
\"\"\"
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.database import Base


class ItemModel(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)
""",
        "requirements.txt": """fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
python-dotenv>=1.0.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
""",
        ".env": """# Application
APP_NAME={{name}}
VERSION=1.0.0
DEBUG=True

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# API
API_PREFIX=/api
ALLOWED_ORIGINS=*

# Security
SECRET_KEY=change-me-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
"""
    },
    "MongoDB": {
        "app/db/__init__.py": '"""Database package"""',
        "app/db/database.py": """\"\"\"
MongoDB database configuration
\"\"\"
from pymongo import MongoClient
from typing import Optional
from app.config.settings import settings

client: Optional[MongoClient] = None


def get_database():
    \"\"\"Get MongoDB database instance\"\"\"
    global client
    if client is None:
        client = MongoClient(settings.MONGODB_URL)
    return client[settings.MONGODB_DB]


def close_database():
    \"\"\"Close database connection\"\"\"
    global client
    if client:
        client.close()
        client = None


def init_db():
    \"\"\"Initialize database collections and indexes\"\"\"
    db = get_database()
    # Create indexes here if needed
    db.items.create_index("name")
""",
        "requirements.txt": """fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
python-dotenv>=1.0.0
pymongo>=4.5.0
motor>=3.3.0
""",
        ".env": """# Application
APP_NAME={{name}}
VERSION=1.0.0
DEBUG=True

# Database
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB={{name}}

# API
API_PREFIX=/api
ALLOWED_ORIGINS=*

# Security
SECRET_KEY=change-me-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
"""
    }
}