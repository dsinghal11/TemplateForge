"""Mobile App Backend Template - UPDATED VERSION"""

BASE_TEMPLATE = {
    "app/__init__.py": "",
    "app/main.py": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from app.api import router
from app.config.settings import settings
from app.core.logger import logger

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    yield
    # Shutdown
    logger.info(f"Shutting down {settings.APP_NAME}")

app = FastAPI(
    title=f"{settings.APP_NAME} Mobile Backend",
    description="Mobile backend service for iOS and Android applications",
    version=settings.VERSION,
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "service": f"{settings.APP_NAME} Mobile Backend",
        "version": settings.VERSION,
        "status": "running",
        "environment": settings.ENVIRONMENT
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.VERSION
    }
""",
    "app/api/__init__.py": """from fastapi import APIRouter
from app.api import users, auth

router = APIRouter()

# Include sub-routers
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
""",
    "app/api/users.py": """from fastapi import APIRouter, HTTPException, Depends, status, File, UploadFile
from typing import List
import logging
from app.models.user import User, UserCreate, UserUpdate
from app.services.user_service import UserService
from app.core.exceptions import NotFoundError, ValidationError
from app.utils.helpers import save_uploaded_file

logger = logging.getLogger(__name__)
router = APIRouter()
user_service = UserService()

@router.get("/", response_model=List[User])
async def get_users():
    \"\"\"Get all users\"\"\"
    try:
        users = await user_service.get_all_users()
        logger.info(f"Retrieved {len(users)} users")
        return users
    except Exception as e:
        logger.error(f"Error retrieving users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving users"
        )

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    \"\"\"Get user by ID\"\"\"
    try:
        user = await user_service.get_user(user_id)
        if not user:
            raise NotFoundError(f"User with ID {user_id} not found")
        return user
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error retrieving user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user"
        )

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    \"\"\"Create a new user\"\"\"
    try:
        new_user = await user_service.create_user(user)
        logger.info(f"Created user: {new_user.username}")
        return new_user
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate):
    \"\"\"Update user\"\"\"
    try:
        updated_user = await user_service.update_user(user_id, user_update)
        if not updated_user:
            raise NotFoundError(f"User with ID {user_id} not found")
        logger.info(f"Updated user: {user_id}")
        return updated_user
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user"
        )

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    \"\"\"Delete user\"\"\"
    try:
        deleted = await user_service.delete_user(user_id)
        if not deleted:
            raise NotFoundError(f"User with ID {user_id} not found")
        logger.info(f"Deleted user: {user_id}")
        return None
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting user"
        )

@router.post("/{user_id}/avatar")
async def upload_avatar(user_id: int, file: UploadFile = File(...)):
    \"\"\"Upload user avatar\"\"\"
    try:
        file_path = await save_uploaded_file(file, f"avatars/user_{user_id}")
        logger.info(f"Uploaded avatar for user {user_id}: {file_path}")
        return {
            "user_id": user_id,
            "avatar_path": file_path,
            "filename": file.filename
        }
    except Exception as e:
        logger.error(f"Error uploading avatar: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error uploading avatar"
        )
""",
    "app/api/auth.py": """from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    \"\"\"Login endpoint\"\"\"
    # TODO: Implement actual authentication logic
    logger.info(f"Login attempt for user: {credentials.username}")
    
    # Placeholder authentication
    if credentials.username == "demo" and credentials.password == "demo":
        return TokenResponse(access_token="demo_token_12345")
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )

@router.post("/logout")
async def logout():
    \"\"\"Logout endpoint\"\"\"
    logger.info("User logged out")
    return {"message": "Successfully logged out"}
""",
    "app/models/__init__.py": "",
    "app/models/user.py": """from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)

class User(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
""",
    "app/services/__init__.py": "",
    "app/services/user_service.py": """import logging
from typing import List, Optional
from datetime import datetime
from app.models.user import User, UserCreate, UserUpdate
from app.core.exceptions import ValidationError, NotFoundError

logger = logging.getLogger(__name__)

class UserService:
    \"\"\"Service for user management\"\"\"
    
    def __init__(self):
        # In-memory storage (replace with database in production)
        self.users: List[User] = []
        self.next_id = 1
        logger.info("UserService initialized")
    
    async def get_all_users(self) -> List[User]:
        \"\"\"Get all users\"\"\"
        return self.users
    
    async def get_user(self, user_id: int) -> Optional[User]:
        \"\"\"Get user by ID\"\"\"
        for user in self.users:
            if user.id == user_id:
                return user
        return None
    
    async def create_user(self, user_data: UserCreate) -> User:
        \"\"\"Create a new user\"\"\"
        # Check if username already exists
        for user in self.users:
            if user.username == user_data.username:
                raise ValidationError(f"Username '{user_data.username}' already exists")
            if user.email == user_data.email:
                raise ValidationError(f"Email '{user_data.email}' already exists")
        
        new_user = User(
            id=self.next_id,
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            is_active=True,
            created_at=datetime.now()
        )
        
        self.users.append(new_user)
        self.next_id += 1
        logger.info(f"Created user: {new_user.username} (ID: {new_user.id})")
        return new_user
    
    async def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        \"\"\"Update user\"\"\"
        user = await self.get_user(user_id)
        if not user:
            return None
        
        # Update fields
        if user_update.username is not None:
            user.username = user_update.username
        if user_update.email is not None:
            user.email = user_update.email
        if user_update.full_name is not None:
            user.full_name = user_update.full_name
        
        user.updated_at = datetime.now()
        logger.info(f"Updated user: {user_id}")
        return user
    
    async def delete_user(self, user_id: int) -> bool:
        \"\"\"Delete user\"\"\"
        for i, user in enumerate(self.users):
            if user.id == user_id:
                self.users.pop(i)
                logger.info(f"Deleted user: {user_id}")
                return True
        return False
""",
    "app/config/__init__.py": "",
    "app/config/settings.py": """from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "{{name}}"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "change-me-in-production"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    
    # Database
    DATABASE_URL: Optional[str] = None
    MONGODB_URL: Optional[str] = None
    MONGODB_DB: Optional[str] = None
    
    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "app.log"
    
    # JWT (if needed)
    JWT_SECRET_KEY: Optional[str] = None
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

settings = Settings()
""",
    "app/core/__init__.py": "",
    "app/core/logger.py": """import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from app.config.settings import settings

def setup_logger(
    name: str = "app",
    log_file: str = None,
    level: str = None,
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
    
    # Use settings if not provided
    log_file = log_file or settings.LOG_FILE
    level = level or settings.LOG_LEVEL
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_dir / log_file,
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    file_handler.setLevel(getattr(logging, level.upper()))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, level.upper()))
    
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
    "app/core/exceptions.py": """from typing import Any, Dict
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
    "app/utils/__init__.py": "",
    "app/utils/constants.py": """import os

# Application
APP_NAME = os.getenv("APP_NAME", "{{name}}")
VERSION = "1.0.0"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Server
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "")
MONGODB_URL = os.getenv("MONGODB_URL", "")
MONGODB_DB = os.getenv("MONGODB_DB", "")

# File Upload
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", str(10 * 1024 * 1024)))  # 10MB

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "app.log")

# JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Debug
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_401_UNAUTHORIZED = 401
HTTP_403_FORBIDDEN = 403
HTTP_404_NOT_FOUND = 404
HTTP_500_INTERNAL_SERVER_ERROR = 500
""",
    "app/utils/helpers.py": """import os
import uuid
from pathlib import Path
from typing import Optional
from fastapi import UploadFile
from datetime import datetime
import json

def generate_id() -> str:
    \"\"\"Generate unique ID\"\"\"
    return str(uuid.uuid4())

def format_date(date: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    \"\"\"Format datetime to string\"\"\"
    return date.strftime(format_str)

def ensure_dir(directory: str) -> None:
    \"\"\"Ensure directory exists\"\"\"
    Path(directory).mkdir(parents=True, exist_ok=True)

async def save_uploaded_file(file: UploadFile, subfolder: str = "") -> str:
    \"\"\"
    Save uploaded file and return the file path
    
    Args:
        file: UploadFile object
        subfolder: Subfolder name within uploads directory
    
    Returns:
        File path where file was saved
    \"\"\"
    # Create upload directory
    upload_dir = Path("uploads")
    if subfolder:
        upload_dir = upload_dir / subfolder
    ensure_dir(str(upload_dir))
    
    # Generate unique filename
    file_ext = Path(file.filename).suffix
    unique_filename = f"{generate_id()}{file_ext}"
    file_path = upload_dir / unique_filename
    
    # Save file
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return str(file_path)

def load_json(file_path: str) -> dict:
    \"\"\"Load JSON file\"\"\"
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(data: dict, file_path: str) -> None:
    \"\"\"Save data to JSON file\"\"\"
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def validate_file_extension(filename: str, allowed_extensions: list) -> bool:
    \"\"\"Validate file extension\"\"\"
    file_ext = Path(filename).suffix.lower()
    return file_ext in allowed_extensions

def get_file_size_mb(file_path: str) -> float:
    \"\"\"Get file size in MB\"\"\"
    size_bytes = os.path.getsize(file_path)
    return size_bytes / (1024 * 1024)
""",
    "requirements.txt": """fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
python-multipart==0.0.6
email-validator==2.1.0
""",
    ".env": """# Application
APP_NAME={{name}}
VERSION=1.0.0
ENVIRONMENT=development
DEBUG=True
SECRET_KEY=change-me-in-production

# Server
HOST=0.0.0.0
PORT=8000

# CORS
CORS_ORIGINS=*

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log

# File Upload
UPLOAD_DIR=uploads
MAX_UPLOAD_SIZE=10485760

# JWT (Optional)
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
""",
    "run.py": """#!/usr/bin/env python3
import uvicorn
from app.config.settings import settings
from app.core.logger import logger

if __name__ == "__main__":
    logger.info(f"Starting {settings.APP_NAME} v{settings.VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Server: http://{settings.HOST}:{settings.PORT}")
    logger.info(f"API Docs: http://{settings.HOST}:{settings.PORT}/docs")
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
""",
    "README.md": """# {{name}} Mobile Backend

FastAPI-based backend service for mobile applications (iOS & Android).

## Features

- 🚀 FastAPI framework with async support
- 📱 RESTful API for mobile apps
- 🔐 Authentication endpoints
- 👤 User management
- 📁 File upload support
- 📝 Comprehensive logging
- ⚙️ Configuration management
- 🔒 Exception handling
- 📊 API documentation (Swagger/ReDoc)
- 🌐 CORS support
- 📐 Architecture folder at project root with .drawio file

## Installation

### 1. Create Virtual Environment
```bash
python -m venv venv

# On Windows:
venv\\Scripts\\activate

# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Setup
Copy `.env.example` to `.env` and configure:
```bash
cp .env .env.local
# Edit .env.local with your settings
```

## Running

### Development Server
```bash
python run.py
```

The server will start at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Production Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Health & Status
- `GET /` - Root endpoint
- `GET /health` - Health check

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/logout` - User logout

### Users
- `GET /api/v1/users` - List all users
- `GET /api/v1/users/{id}` - Get user by ID
- `POST /api/v1/users` - Create new user
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user
- `POST /api/v1/users/{id}/avatar` - Upload user avatar

## Project Structure

```
{{name}}/
├── architecture/           # Architecture documentation & design
│   ├── architecture.drawio # Visual architecture diagram
│   └── README.md           # Architecture documentation
├── app/
│   ├── api/               # API endpoints
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── auth.py
│   ├── config/            # Configuration
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── core/              # Core functionality
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   └── exceptions.py
│   ├── models/            # Data models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/          # Business logic
│   │   ├── __init__.py
│   │   └── user_service.py
│   ├── utils/             # Utilities
│   │   ├── __init__.py
│   │   ├── constants.py
│   │   └── helpers.py
│   ├── db/                # Database (if configured)
│   └── main.py            # Application entry
├── logs/                  # Log files
├── uploads/               # Uploaded files
├── run.py                 # Application runner
├── .env                   # Environment variables
├── requirements.txt       # Dependencies
└── README.md              # This file
```

## Architecture

The `/architecture` folder contains design documentation:
- Open `architecture.drawio` with https://app.diagrams.net/ to design your system
- Document API flows, database schema, and system components
- Keep architecture docs updated as your project evolves

## Development

### Adding New Endpoints
1. Create a new router file in `app/api/`
2. Define your endpoints with appropriate models
3. Register the router in `app/api/__init__.py`

### Adding New Models
1. Create model classes in `app/models/`
2. Use Pydantic for validation
3. Separate base, create, update, and response models

### Adding Services
1. Create service classes in `app/services/`
2. Implement business logic
3. Use dependency injection where needed

### Database Integration
To add database support:
1. Choose PostgreSQL or MongoDB
2. Update `.env` with connection string
3. Add database models and migrations
4. Update services to use database

## Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

## Logging

Logs are stored in the `logs/` directory with automatic rotation:
- Max file size: 10MB
- Backup count: 5 files
- Format: timestamp - name - level - message

## Error Handling

Custom exception classes in `app/core/exceptions.py`:
- `ValidationError` - Validation errors
- `NotFoundError` - Resource not found
- `AuthenticationError` - Authentication errors
- `DatabaseError` - Database errors

## Configuration

All configuration is managed through:
1. `.env` file (environment variables)
2. `app/config/settings.py` (Pydantic settings)
3. `app/utils/constants.py` (constants)

## Security

- Change `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Configure proper CORS origins
- Use environment variables for sensitive data
- Implement proper authentication/authorization

## Deployment

### Docker
```bash
docker build -t {{name}}-api .
docker run -p 8000:8000 {{name}}-api
```

### Cloud Platforms
- **AWS**: Deploy to EC2, ECS, or Lambda
- **Google Cloud**: Deploy to Cloud Run or App Engine
- **Azure**: Deploy to App Service or Container Instances
- **Heroku**: Use Procfile for deployment

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
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/
.venv

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Logs
*.log
logs/

# Database
*.db
*.sqlite3
*.sqlite

# Uploads
uploads/
temp/

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# OS
.DS_Store
Thumbs.db
"""
}

# Template-specific features
FEATURES = {
    "Push Notifications": {
        "app/services/notification_service.py": """from typing import List
import httpx
import logging

logger = logging.getLogger(__name__)

class PushNotificationService:
    \"\"\"Push notification service for mobile apps\"\"\"
    
    def __init__(self, fcm_key: str = None):
        self.fcm_key = fcm_key or "your-fcm-key"
        self.fcm_url = "https://fcm.googleapis.com/fcm/send"

    async def send_notification(
        self,
        device_tokens: List[str],
        title: str,
        body: str,
        data: dict = None
    ):
        \"\"\"Send push notification to devices\"\"\"
        headers = {
            "Authorization": f"key={self.fcm_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "registration_ids": device_tokens,
            "notification": {
                "title": title,
                "body": body
            },
            "data": data or {}
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.fcm_url,
                json=payload,
                headers=headers
            )
            logger.info(f"Sent notification to {len(device_tokens)} devices")
            return response.json()

notification_service = PushNotificationService()
""",
        "requirements.txt": """fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
python-multipart==0.0.6
email-validator==2.1.0
httpx==0.25.2
"""
    },
    "Image Processing": {
        "app/services/image_service.py": """from PIL import Image
from io import BytesIO
from fastapi import UploadFile
import os
import logging

logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def process_image(file: UploadFile, max_size: tuple = (800, 800)):
    \"\"\"Process and resize image\"\"\"
    contents = await file.read()
    image = Image.open(BytesIO(contents))
    
    # Resize if needed
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    # Save processed image
    output_path = os.path.join(UPLOAD_DIR, file.filename)
    image.save(output_path, optimize=True, quality=85)
    
    logger.info(f"Processed image: {file.filename}")
    
    return {
        "filename": file.filename,
        "size": image.size,
        "format": image.format,
        "path": output_path
    }

async def create_thumbnail(file: UploadFile, size: tuple = (200, 200)):
    \"\"\"Create thumbnail from image\"\"\"
    contents = await file.read()
    image = Image.open(BytesIO(contents))
    
    image.thumbnail(size, Image.Resampling.LANCZOS)
    
    thumb_path = os.path.join(UPLOAD_DIR, f"thumb_{file.filename}")
    image.save(thumb_path, optimize=True, quality=75)
    
    logger.info(f"Created thumbnail: {file.filename}")
    return thumb_path
""",
        "requirements.txt": """fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
python-multipart==0.0.6
email-validator==2.1.0
Pillow==10.1.0
"""
    },
    "Rate Limiting": {
        "app/middleware/rate_limit.py": """from fastapi import HTTPException, Request
from collections import defaultdict
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    \"\"\"Rate limiting middleware\"\"\"
    
    def __init__(self, requests: int = 100, window: int = 60):
        self.requests = requests
        self.window = window
        self.clients = defaultdict(list)

    async def check_rate_limit(self, request: Request):
        \"\"\"Check if client has exceeded rate limit\"\"\"
        client_ip = request.client.host
        now = datetime.now()
        
        # Clean old requests
        self.clients[client_ip] = [
            req_time for req_time in self.clients[client_ip]
            if now - req_time < timedelta(seconds=self.window)
        ]
        
        # Check limit
        if len(self.clients[client_ip]) >= self.requests:
            logger.warning(f"Rate limit exceeded for {client_ip}")
            raise HTTPException(
                status_code=429,
                detail="Too many requests"
            )
        
        self.clients[client_ip].append(now)
        return True

rate_limiter = RateLimiter(requests=100, window=60)
"""
    },
    "File Storage": {
        "app/services/storage_service.py": """import os
import shutil
from fastapi import UploadFile
from typing import Optional
import uuid
import logging

logger = logging.getLogger(__name__)

STORAGE_DIR = "storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

class FileStorage:
    \"\"\"File storage service\"\"\"
    
    def __init__(self, base_dir: str = STORAGE_DIR):
        self.base_dir = base_dir

    async def save_file(
        self,
        file: UploadFile,
        subfolder: Optional[str] = None
    ) -> dict:
        \"\"\"Save file to storage\"\"\"
        # Generate unique filename
        file_id = str(uuid.uuid4())
        ext = os.path.splitext(file.filename)[1]
        filename = f"{file_id}{ext}"
        
        # Create subfolder if specified
        save_dir = self.base_dir
        if subfolder:
            save_dir = os.path.join(self.base_dir, subfolder)
            os.makedirs(save_dir, exist_ok=True)
        
        file_path = os.path.join(save_dir, filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Saved file: {file.filename} as {filename}")
        
        return {
            "file_id": file_id,
            "filename": file.filename,
            "stored_name": filename,
            "path": file_path,
            "size": os.path.getsize(file_path)
        }

    def delete_file(self, file_path: str) -> bool:
        \"\"\"Delete file from storage\"\"\"
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Deleted file: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            return False

storage = FileStorage()
"""
    }
}