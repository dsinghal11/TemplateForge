"""Templates package initialization"""

from .react_web import BASE_TEMPLATE as REACT_BASE
from .nodejs_app import BASE_TEMPLATE as NODEJS_BASE
from .fastapi_core import BASE_TEMPLATE as FASTAPI_BASE, FEATURES as FASTAPI_FEATURES
from .mobile_backend import BASE_TEMPLATE as MOBILE_BASE, FEATURES as MOBILE_FEATURES
from .desktop_app import BASE_TEMPLATE as DESKTOP_BASE, FEATURES as DESKTOP_FEATURES


TEMPLATES = {
    "React Web Dashboard": REACT_BASE,
    "Node.js Application": NODEJS_BASE,
    "FastAPI Core Service": FASTAPI_BASE,
    "Mobile App Backend": MOBILE_BASE,
    "Desktop Application": DESKTOP_BASE,
}

FEATURES = {
    "FastAPI Core Service": FASTAPI_FEATURES,
    "Mobile App Backend": MOBILE_FEATURES,
    "Desktop Application": DESKTOP_FEATURES,
}