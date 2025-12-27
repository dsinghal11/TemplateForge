"""FastAPI Core Service Template with Features"""

BASE_TEMPLATE = {
    "app/__init__.py": "",
    "app/main.py": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router
from app.utils.constants import APP_NAME, VERSION

app = FastAPI(
    title=APP_NAME,
    description="Core service built with FastAPI",
    version=VERSION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {
        "service": APP_NAME,
        "status": "running",
        "version": VERSION
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
""",
    "app/api.py": """from fastapi import APIRouter

router = APIRouter()

@router.get("/items")
def get_items():
    return {"items": []}

@router.post("/items")
def create_item(item: dict):
    return {"item": item, "created": True}
""",
    "requirements.txt": """fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0
""",
    ".env": """# Application
APP_NAME={{name}}
DEBUG=True
HOST=0.0.0.0
PORT=8000

# AI Configuration
AI_MODEL=gpt-4
ENABLE_AI=True
AI_MAX_TOKENS=2000
AI_TEMPERATURE=0.7
""",
    "run.py": """import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )
""",
    "README.md": """# {{name}}

FastAPI Core Service with AI capabilities

## Features

- ⚡ FastAPI framework
- 🤖 Core AI utilities built-in
- 📚 Automatic API documentation
- 🔄 Hot reload in development
- 🔐 CORS enabled
- ⚙️ Environment configuration

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
```

## Running

```bash
python run.py
```

## API Documentation

Visit http://localhost:8000/docs for interactive API documentation (Swagger UI).
Visit http://localhost:8000/redoc for alternative documentation (ReDoc).

## Project Structure

```
{{name}}/
├── app/
│   ├── architecture/    # Empty folders for organized code
│   ├── utils/          # Core utilities & AI helpers
│   ├── main.py         # FastAPI application
│   └── api.py          # API routes
├── .env                # Environment variables
├── requirements.txt    # Dependencies
└── run.py             # Application runner
```

## Core AI Features

This template includes:
- AI helper utilities in `app/utils/ai_helper.py`
- Configuration constants in `app/utils/constants.py`
- Ready for AI integration (OpenAI, Anthropic, etc.)

## Environment Variables

Configure in `.env`:
- `APP_NAME` - Application name
- `DEBUG` - Debug mode
- `AI_MODEL` - AI model to use
- `ENABLE_AI` - Enable/disable AI features

## API Endpoints

- `GET /` - Service info
- `GET /health` - Health check
- `GET /api/items` - Get all items
- `POST /api/items` - Create item

## Development

Add your routes, models, and business logic in the appropriate folders in `app/architecture/`.
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
"""
}

FEATURES = {
    "PostgreSQL Database": {
        "app/database/__init__.py": "",
        "app/database/config.py": """\"\"\"PostgreSQL database configuration\"\"\"
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/dbname")

engine = create_engine(DATABASE_URL)
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
        "app/models.py": """from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database.config import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
""",
        ".env": """# Application
APP_NAME={{name}}
DEBUG=True
HOST=0.0.0.0
PORT=8000

# AI Configuration
AI_MODEL=gpt-4
ENABLE_AI=True

# PostgreSQL Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
DB_HOST=localhost
DB_PORT=5432
DB_NAME=dbname
DB_USER=user
DB_PASSWORD=password
""",
        "requirements.txt": """fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0
psycopg2-binary>=2.9.0
sqlalchemy>=2.0.0
"""
    },
    "MongoDB Database": {
        "app/database/__init__.py": "",
        "app/database/config.py": """\"\"\"MongoDB database configuration\"\"\"
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "dbname")

# Async client for FastAPI
async_client = AsyncIOMotorClient(MONGODB_URI)
async_db = async_client[DB_NAME]

# Sync client for scripts
sync_client = MongoClient(MONGODB_URI)
sync_db = sync_client[DB_NAME]


def get_database():
    \"\"\"Get database instance\"\"\"
    return async_db


def get_collection(collection_name: str):
    \"\"\"Get collection\"\"\"
    return async_db[collection_name]
""",
        ".env": """# Application
APP_NAME={{name}}
DEBUG=True
HOST=0.0.0.0
PORT=8000

# AI Configuration
AI_MODEL=gpt-4
ENABLE_AI=True

# MongoDB Database Configuration
MONGODB_URI=mongodb://localhost:27017
DB_NAME=dbname
""",
        "requirements.txt": """fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0
motor>=3.3.0
pymongo>=4.6.0
"""
    },
    "Authentication": {
        "app/auth.py": """from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
""",
        "requirements.txt": """fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
"""
    },
    "WebSocket": {
        "app/websocket.py": """from fastapi import WebSocket, WebSocketDisconnect
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()
""",
        "app/main.py": """from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.api import router
from app.websocket import manager
from app.utils.constants import APP_NAME, VERSION

app = FastAPI(
    title=APP_NAME,
    description="Core service built with FastAPI",
    version=VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {
        "service": APP_NAME,
        "status": "running",
        "version": VERSION
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
"""
    },
    "Caching": {
        "app/cache.py": """from functools import wraps
from typing import Any, Callable
import json
import hashlib

cache_store = {}

def cache_key(*args, **kwargs) -> str:
    key_data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True)
    return hashlib.md5(key_data.encode()).hexdigest()

def cached(expire_seconds: int = 300):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            key = f"{func.__name__}:{cache_key(*args, **kwargs)}"
            
            if key in cache_store:
                return cache_store[key]
            
            result = await func(*args, **kwargs)
            cache_store[key] = result
            return result
        
        return wrapper
    return decorator
""",
        "requirements.txt": """fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0
redis==5.0.1
"""
    }
}