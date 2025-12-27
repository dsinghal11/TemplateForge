BASE_TEMPLATE = {
    "app/__init__.py": "",
    "app/main.py": """from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from app.api import router

app = FastAPI(
    title="{{name}} Mobile Backend",
    description="Mobile backend service",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "service": "{{name}} Mobile Backend",
        "status": "running"
    }

@app.get("/api/v1/ping")
def ping():
    return {"pong": True}

@app.post("/api/v1/upload")
async def upload_file(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file.size
    }
""",
    "app/api.py": """from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

class User(BaseModel):
    id: int = None
    username: str
    email: str

users_db = []

@router.get("/users", response_model=List[User])
def get_users():
    return users_db

@router.post("/users", response_model=User)
def create_user(user: User):
    user.id = len(users_db) + 1
    users_db.append(user)
    return user

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")
""",
    "requirements.txt": """fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0
python-multipart==0.0.6
""",
    ".env": """DEBUG=True
HOST=0.0.0.0
PORT=8000
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
    "README.md": """# {{name}} Mobile Backend

Backend service for mobile applications.

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
python run.py
```

## API Endpoints

- GET /api/v1/ping - Health check
- GET /api/v1/users - List all users
- POST /api/v1/users - Create a new user
- GET /api/v1/users/{id} - Get user by ID
- POST /api/v1/upload - Upload a file
""",
    ".gitignore": """__pycache__/
*.py[cod]
.env
.venv
venv/
uploads/
"""
}

FEATURES = {
    "Push Notifications": {
        "app/notifications.py": """from typing import List
import httpx

class PushNotificationService:
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
            return response.json()

notification_service = PushNotificationService()
""",
        "requirements.txt": """fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0
python-multipart==0.0.6
httpx==0.25.2
"""
    },
    "Image Processing": {
        "app/image_handler.py": """from PIL import Image
from io import BytesIO
from fastapi import UploadFile
import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def process_image(file: UploadFile, max_size: tuple = (800, 800)):
    contents = await file.read()
    image = Image.open(BytesIO(contents))
    
    # Resize if needed
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    # Save processed image
    output_path = os.path.join(UPLOAD_DIR, file.filename)
    image.save(output_path, optimize=True, quality=85)
    
    return {
        "filename": file.filename,
        "size": image.size,
        "format": image.format,
        "path": output_path
    }

async def create_thumbnail(file: UploadFile, size: tuple = (200, 200)):
    contents = await file.read()
    image = Image.open(BytesIO(contents))
    
    image.thumbnail(size, Image.Resampling.LANCZOS)
    
    thumb_path = os.path.join(UPLOAD_DIR, f"thumb_{file.filename}")
    image.save(thumb_path, optimize=True, quality=75)
    
    return thumb_path
""",
        "requirements.txt": """fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0
python-multipart==0.0.6
Pillow==10.1.0
"""
    },
    "Rate Limiting": {
        "app/rate_limit.py": """from fastapi import HTTPException, Request
from collections import defaultdict
from datetime import datetime, timedelta
import asyncio

class RateLimiter:
    def __init__(self, requests: int = 100, window: int = 60):
        self.requests = requests
        self.window = window
        self.clients = defaultdict(list)

    async def check_rate_limit(self, request: Request):
        client_ip = request.client.host
        now = datetime.now()
        
        # Clean old requests
        self.clients[client_ip] = [
            req_time for req_time in self.clients[client_ip]
            if now - req_time < timedelta(seconds=self.window)
        ]
        
        # Check limit
        if len(self.clients[client_ip]) >= self.requests:
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
        "app/storage.py": """import os
import shutil
from fastapi import UploadFile
from typing import Optional
import uuid

STORAGE_DIR = "storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

class FileStorage:
    def __init__(self, base_dir: str = STORAGE_DIR):
        self.base_dir = base_dir

    async def save_file(
        self,
        file: UploadFile,
        subfolder: Optional[str] = None
    ) -> dict:
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
        
        return {
            "file_id": file_id,
            "filename": file.filename,
            "stored_name": filename,
            "path": file_path,
            "size": os.path.getsize(file_path)
        }

    def delete_file(self, file_path: str) -> bool:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception:
            return False

storage = FileStorage()
"""
    }
}