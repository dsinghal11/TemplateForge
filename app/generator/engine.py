"""
Project generation engine - UPDATED VERSION
"""
from pathlib import Path
import shutil
import logging

logger = logging.getLogger(__name__)


def merge_requirements(base_req: str, feature_req: str) -> str:
    """Merge two requirements.txt contents, avoiding duplicates"""
    base_lines = set(line.strip() for line in base_req.split('\n') if line.strip())
    feature_lines = set(line.strip() for line in feature_req.split('\n') if line.strip())

    all_requirements = base_lines | feature_lines
    return '\n'.join(sorted(all_requirements)) + '\n'


def generate_project(template: str, name: str, output_dir: Path, config: dict):
    """
    Generate a project with the specified template

    Args:
        template: Template name (e.g., "React Web Dashboard")
        name: Project name
        output_dir: Output directory path
        config: Configuration dictionary with settings
    """
    from app.templates import TEMPLATES

    # Get the appropriate template module
    if "React" in template:
        from app.templates.react_web import BASE_TEMPLATE
        template_files = BASE_TEMPLATE.copy()
        base_dir = "src"
    elif "Node.js" in template:
        from app.templates.nodejs_app import BASE_TEMPLATE, FEATURES as NODE_FEATURES
        template_files = BASE_TEMPLATE.copy()
        base_dir = "src"

        # Add Node.js template features
        for feature_name in config.get("features", []):
            if feature_name in NODE_FEATURES:
                feature_files = NODE_FEATURES[feature_name]
                for file_path, content in feature_files.items():
                    template_files[file_path] = content
                logger.info(f"Adding Node.js feature: {feature_name}")

    elif "Desktop" in template:
        from app.templates.desktop_app import BASE_TEMPLATE, FEATURES as DESKTOP_FEATURES
        template_files = BASE_TEMPLATE.copy()
        base_dir = "app"

        # Add Desktop template features
        for feature_name in config.get("features", []):
            if feature_name in DESKTOP_FEATURES:
                feature_files = DESKTOP_FEATURES[feature_name]
                for file_path, content in feature_files.items():
                    if file_path == "requirements.txt":
                        template_files[file_path] = merge_requirements(
                            template_files.get(file_path, ""),
                            content
                        )
                    else:
                        template_files[file_path] = content
                logger.info(f"Adding Desktop feature: {feature_name}")

    elif "FastAPI" in template:
        from app.templates.fastapi_core import BASE_TEMPLATE, FEATURES as FASTAPI_FEATURES
        template_files = BASE_TEMPLATE.copy()
        base_dir = "app"

        # Add FastAPI template features
        for feature_name in config.get("features", []):
            if feature_name in FASTAPI_FEATURES:
                feature_files = FASTAPI_FEATURES[feature_name]
                for file_path, content in feature_files.items():
                    if file_path == "requirements.txt":
                        template_files[file_path] = merge_requirements(
                            template_files.get(file_path, ""),
                            content
                        )
                    else:
                        template_files[file_path] = content
                logger.info(f"Adding FastAPI feature: {feature_name}")

    elif "Mobile" in template:
        from app.templates.mobile_backend import BASE_TEMPLATE, FEATURES as MOBILE_FEATURES
        template_files = BASE_TEMPLATE.copy()
        base_dir = "app"

        # Add Mobile template features
        for feature_name in config.get("features", []):
            if feature_name in MOBILE_FEATURES:
                feature_files = MOBILE_FEATURES[feature_name]
                for file_path, content in feature_files.items():
                    if file_path == "requirements.txt":
                        template_files[file_path] = merge_requirements(
                            template_files.get(file_path, ""),
                            content
                        )
                    else:
                        template_files[file_path] = content
                logger.info(f"Adding Mobile feature: {feature_name}")
    else:
        from app.templates.python_core import BASE_TEMPLATE
        template_files = BASE_TEMPLATE.copy()
        base_dir = "app"

    project_path = output_dir / name

    # Remove existing directory if it exists
    if project_path.exists():
        shutil.rmtree(project_path)

    # Create project directory
    project_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"Creating project: {name}")

    # Add architecture folder at project root level (always included)
    create_architecture_folder(project_path, template)

    # Add logger if enabled (for Python projects)
    if config.get("enable_logger", True) and "React" not in template and "Node.js" not in template:
        add_logger(project_path, base_dir)

    # Add exception handler if enabled
    if config.get("enable_exception_handler", True):
        add_exception_handler(project_path, template, base_dir)

    # Add database configuration if selected (for Python projects)
    if config.get("database_type") and "React" not in template and "Node.js" not in template:
        add_database_config(project_path, config["database_type"], template_files, base_dir)

    # Write all template files
    for file_path, content in template_files.items():
        full_path = project_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        # Replace placeholders
        content = content.replace("{{name}}", name)

        full_path.write_text(content)
        logger.info(f"Created: {file_path}")

    # Initialize git repository if enabled
    if config.get("git_init", True):
        init_git_repo(project_path)

    # Create SETUP.md
    create_setup_md(project_path, template, config)

    logger.info(f"Project '{name}' generated successfully!")


def create_architecture_folder(project_path: Path, template: str):
    """Create architecture folder at project root with empty .drawio file"""
    arch_path = project_path / "architecture"
    arch_path.mkdir(parents=True, exist_ok=True)

    # Create empty .drawio file
    (arch_path / "architecture.drawio").write_text("""<mxfile host="app.diagrams.net" modified="2024-01-01T00:00:00.000Z" agent="5.0" version="22.0.0" etag="" type="device">
  <diagram name="Architecture" id="architecture">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>""")

    # Create README in architecture folder
    (arch_path / "README.md").write_text("""# Architecture

This folder contains architecture design documents for your project.

## Files

- **architecture.drawio**: Draw.io diagram file for visual architecture documentation

## Usage

1. Open `architecture.drawio` with draw.io (https://app.diagrams.net/) to design your system architecture
2. Document your component relationships, data flows, and system design
3. Keep this documentation up to date as your project evolves

## Best Practices

- Use the .drawio file to visualize your system architecture
- Include component diagrams, data flow diagrams, and deployment diagrams
- Update the architecture documentation whenever you make significant structural changes
""")


def add_logger(project_path: Path, base_dir: str):
    """Add logging configuration in core directory"""
    logger_path = project_path / base_dir / "core"
    logger_path.mkdir(parents=True, exist_ok=True)

    (logger_path / "__init__.py").write_text('"""Core functionality"""')

    (logger_path / "logger.py").write_text("""\"\"\"
Logging configuration with file rotation
\"\"\"
import logging
import os
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
""")


def add_exception_handler(project_path: Path, template: str, base_dir: str):
    """Add exception handling"""
    if "React" in template or "Node.js" in template:
        # React and Node.js don't need Python exception handler
        return
    else:
        # Add Python exception handler in core directory
        exceptions_path = project_path / base_dir / "core" / "exceptions.py"
        exceptions_path.parent.mkdir(parents=True, exist_ok=True)

        exceptions_path.write_text("""\"\"\"
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
""")


def add_database_config(project_path: Path, db_type: str, template_files: dict, base_dir: str):
    """Add database configuration in db directory"""
    if db_type == "postgresql":
        template_files[".env"] = """# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Application
APP_NAME={{name}}
DEBUG=True
SECRET_KEY=change-me-in-production
"""

        template_files[f"{base_dir}/db/database.py"] = """\"\"\"
PostgreSQL database configuration
\"\"\"
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/dbname")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    \"\"\"Get database session\"\"\"
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""
        template_files[f"{base_dir}/db/__init__.py"] = '"""Database package"""'

    elif db_type == "mongodb":
        template_files[".env"] = """# Database Configuration
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB={{name}}

# Application
APP_NAME={{name}}
DEBUG=True
SECRET_KEY=change-me-in-production
"""

        template_files[f"{base_dir}/db/database.py"] = """\"\"\"
MongoDB database configuration
\"\"\"
import os
from pymongo import MongoClient
from typing import Optional

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "{{name}}")

client: Optional[MongoClient] = None


def get_database():
    \"\"\"Get MongoDB database instance\"\"\"
    global client
    if client is None:
        client = MongoClient(MONGODB_URL)
    return client[MONGODB_DB]


def close_database():
    \"\"\"Close database connection\"\"\"
    global client
    if client:
        client.close()
        client = None
"""
        template_files[f"{base_dir}/db/__init__.py"] = '"""Database package"""'


def init_git_repo(project_path: Path):
    """Initialize git repository"""
    try:
        import subprocess
        subprocess.run(["git", "init"], cwd=project_path, check=True, capture_output=True)
        subprocess.run(["git", "add", "."], cwd=project_path, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit"],
            cwd=project_path,
            check=True,
            capture_output=True
        )
        logger.info("Git repository initialized")
    except Exception as e:
        logger.warning(f"Could not initialize git repository: {e}")


def create_setup_md(project_path: Path, template: str, config: dict):
    """Create SETUP.md with instructions"""
    content = f"""# Setup Instructions

## Project: {project_path.name}
## Template: {template}

### Quick Start

"""

    if "React" in template:
        content += """#### 1. Install Dependencies
```bash
npm install
```

#### 2. Environment Setup (Optional)
Create `.env` file:
```bash
REACT_APP_API_URL=http://localhost:8000
```

#### 3. Run Development Server
```bash
npm start
```

The application will open at [http://localhost:3000](http://localhost:3000)

#### 4. Build for Production
```bash
npm run build
```

### Features Included

- ✅ React 18 with TypeScript
- ✅ Modern component structure
- ✅ Responsive design
- ✅ Architecture folder at project root with .drawio file

"""
    elif "Node.js" in template:
        content += """#### 1. Install Dependencies
```bash
npm install
```

#### 2. Environment Setup
Create `.env` file:
```bash
NODE_ENV=development
PORT=3000
```

#### 3. Run Development Server
```bash
npm run dev
```

The server will start at [http://localhost:3000](http://localhost:3000)

#### 4. Run Production Server
```bash
npm start
```

### Features Included

- ✅ Express.js framework
- ✅ TypeScript/JavaScript support
- ✅ Environment configuration
- ✅ Error handling middleware
- ✅ Architecture folder at project root with .drawio file

"""
        if "API Integration" in config.get("features", []):
            content += """#### Additional Features
- ✅ Advanced API Integration
- ✅ RESTful endpoints
- ✅ Request validation

"""

    elif "Desktop" in template:
        content += """#### 1. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Environment Setup
Create `.env` file:
```bash
APP_NAME={{name}}
```

#### 4. Run Desktop Application
```bash
python run.py
```

"""
        if "API Integration" in config.get("features", []):
            content += """#### 5. Run API Server (Optional)
In a separate terminal:
```bash
python run_api.py
```

API will be available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Welcome endpoint**: http://localhost:8000/welcome
- **Health check**: http://localhost:8000/health

"""

        content += """### Features Included

- ✅ Architecture folder at project root with .drawio file
"""
        if config.get("enable_logger"):
            content += "- ✅ Logger (file rotation)\n"
        if config.get("enable_exception_handler"):
            content += "- ✅ Exception Handler\n"
        if "API Integration" in config.get("features", []):
            content += "- ✅ API Integration with FastAPI\n"

    else:
        # Python projects
        content += """#### 1. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Environment Setup
Create `.env` file with your configuration

#### 4. Run Application
```bash
python run.py
```

### Features Included

- ✅ Architecture folder at project root with .drawio file
"""

    if config.get("database_type"):
        content += f"- ✅ Database: {config['database_type'].upper()}\n"

    content += """
### Architecture

The `/architecture` folder at the project root contains:
- Empty subfolders for organizing your code
- `architecture.drawio` file for visual documentation
- Open the .drawio file with https://app.diagrams.net/ to design your system

### Project Structure

Refer to README.md for detailed project structure.

### Next Steps

1. Configure environment variables in `.env`
2. Design your architecture in `architecture/architecture.drawio`
3. Organize your code in the architecture subfolders
4. Add your business logic
5. Test thoroughly
6. Deploy to production

### Support

For issues or questions, refer to the documentation or create an issue.
"""

    (project_path / "SETUP.md").write_text(content)