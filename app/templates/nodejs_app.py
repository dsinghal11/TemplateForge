"""Node.js Application Template with API Integration Features"""

BASE_TEMPLATE = {
    "package.json": """{
  "name": "{{name}}",
  "version": "1.0.0",
  "description": "Node.js application with Express",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js",
    "dev": "nodemon src/index.js",
    "test": "jest"
  },
  "keywords": ["nodejs", "express", "api"],
  "author": "",
  "license": "MIT",
  "dependencies": {
    "express": "^4.18.2",
    "dotenv": "^16.3.1",
    "cors": "^2.8.5"
  },
  "devDependencies": {
    "nodemon": "^3.0.1",
    "jest": "^29.7.0"
  }
}""",
    "src/index.js": """const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const { APP_CONFIG } = require('./utils/constants');

dotenv.config();

const app = express();

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Basic routes
app.get('/', (req, res) => {
  res.json({
    message: `Welcome to ${APP_CONFIG.NAME}`,
    version: APP_CONFIG.VERSION,
    status: 'running'
  });
});

app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: 'Internal Server Error',
    message: err.message
  });
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Environment: ${APP_CONFIG.ENVIRONMENT}`);
});
""",
    ".env.example": """# Application
NODE_ENV=development
PORT=3000

# AI Configuration
AI_MODEL=gpt-4
ENABLE_AI=true
AI_MAX_TOKENS=2000
AI_TEMPERATURE=0.7

# API Configuration
API_TIMEOUT=30000
""",
    ".env": """# Application
NODE_ENV=development
PORT=3000

# AI Configuration
AI_MODEL=gpt-4
ENABLE_AI=true
AI_MAX_TOKENS=2000
AI_TEMPERATURE=0.7

# API Configuration
API_TIMEOUT=30000
""",
    "README.md": """# {{name}}

Node.js application built with Express.js

## Features

- Express.js framework
- CORS enabled
- Environment configuration
- Core AI utilities
- Error handling middleware
- Development mode with nodemon

## Installation

```bash
npm install
```

## Running

### Development
```bash
npm run dev
```

### Production
```bash
npm start
```

## API Endpoints

- `GET /` - Welcome endpoint
- `GET /health` - Health check

## Project Structure

```
{{name}}/
├── src/
│   ├── architecture/    # Empty folders for organized code
│   ├── utils/          # Utilities and constants
│   └── index.js        # Entry point
├── .env                # Environment variables
├── package.json        # Dependencies
└── README.md           # Documentation
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

- `NODE_ENV` - Environment (development/production)
- `PORT` - Server port
- `AI_MODEL` - AI model to use
- `ENABLE_AI` - Enable/disable AI features

## Development

Add your routes, controllers, and business logic in the appropriate folders in `src/architecture/`.

## License

MIT
""",
    ".gitignore": """# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Environment
.env
.env.local
.env.*.local

# Logs
logs/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Build
dist/
build/
.cache/

# Testing
coverage/
.nyc_output/
"""
}

# Node.js Template-Specific Features
FEATURES = {
    "API Integration": {
        "src/routes/api.js": """const express = require('express');
const router = express.Router();

// Sample API routes
router.get('/items', (req, res) => {
  res.json({
    items: [],
    count: 0
  });
});

router.post('/items', (req, res) => {
  const item = req.body;
  res.status(201).json({
    item,
    created: true
  });
});

router.get('/items/:id', (req, res) => {
  const { id } = req.params;
  res.json({
    id,
    name: 'Sample Item'
  });
});

router.put('/items/:id', (req, res) => {
  const { id } = req.params;
  const updates = req.body;
  res.json({
    id,
    updated: true,
    ...updates
  });
});

router.delete('/items/:id', (req, res) => {
  const { id } = req.params;
  res.json({
    id,
    deleted: true
  });
});

module.exports = router;
""",
        "src/middlewares/validation.js": """/**
 * Validation middleware
 */

const validateItem = (req, res, next) => {
  const { name } = req.body;
  
  if (!name || name.trim().length === 0) {
    return res.status(400).json({
      error: 'VALIDATION_ERROR',
      message: 'Name is required'
    });
  }
  
  next();
};

const validateId = (req, res, next) => {
  const { id } = req.params;
  
  if (!id || isNaN(id)) {
    return res.status(400).json({
      error: 'VALIDATION_ERROR',
      message: 'Invalid ID'
    });
  }
  
  next();
};

module.exports = {
  validateItem,
  validateId
};
""",
        "src/middlewares/auth.js": """/**
 * Authentication middleware
 */

const authenticate = (req, res, next) => {
  const authHeader = req.headers.authorization;
  
  if (!authHeader) {
    return res.status(401).json({
      error: 'AUTHENTICATION_ERROR',
      message: 'No authorization header'
    });
  }
  
  // Add your authentication logic here
  // For example: JWT verification
  
  next();
};

const authorize = (roles = []) => {
  return (req, res, next) => {
    // Add your authorization logic here
    next();
  };
};

module.exports = {
  authenticate,
  authorize
};
""",
        "src/controllers/itemController.js": """/**
 * Item controller
 */

// In-memory storage (replace with database)
let items = [];
let nextId = 1;

const getItems = (req, res) => {
  res.json({
    items,
    count: items.length
  });
};

const getItem = (req, res) => {
  const { id } = req.params;
  const item = items.find(i => i.id === parseInt(id));
  
  if (!item) {
    return res.status(404).json({
      error: 'NOT_FOUND',
      message: 'Item not found'
    });
  }
  
  res.json(item);
};

const createItem = (req, res) => {
  const { name, description } = req.body;
  
  const item = {
    id: nextId++,
    name,
    description,
    createdAt: new Date().toISOString()
  };
  
  items.push(item);
  
  res.status(201).json(item);
};

const updateItem = (req, res) => {
  const { id } = req.params;
  const { name, description } = req.body;
  
  const index = items.findIndex(i => i.id === parseInt(id));
  
  if (index === -1) {
    return res.status(404).json({
      error: 'NOT_FOUND',
      message: 'Item not found'
    });
  }
  
  items[index] = {
    ...items[index],
    name,
    description,
    updatedAt: new Date().toISOString()
  };
  
  res.json(items[index]);
};

const deleteItem = (req, res) => {
  const { id } = req.params;
  const index = items.findIndex(i => i.id === parseInt(id));
  
  if (index === -1) {
    return res.status(404).json({
      error: 'NOT_FOUND',
      message: 'Item not found'
    });
  }
  
  items.splice(index, 1);
  
  res.json({
    message: 'Item deleted successfully',
    id: parseInt(id)
  });
};

module.exports = {
  getItems,
  getItem,
  createItem,
  updateItem,
  deleteItem
};
""",
        "src/services/itemService.js": """/**
 * Item service - Business logic layer
 */

class ItemService {
  constructor() {
    this.items = [];
    this.nextId = 1;
  }

  findAll() {
    return this.items;
  }

  findById(id) {
    return this.items.find(item => item.id === id);
  }

  create(data) {
    const item = {
      id: this.nextId++,
      ...data,
      createdAt: new Date().toISOString()
    };
    
    this.items.push(item);
    return item;
  }

  update(id, data) {
    const index = this.items.findIndex(item => item.id === id);
    
    if (index === -1) {
      return null;
    }
    
    this.items[index] = {
      ...this.items[index],
      ...data,
      updatedAt: new Date().toISOString()
    };
    
    return this.items[index];
  }

  delete(id) {
    const index = this.items.findIndex(item => item.id === id);
    
    if (index === -1) {
      return false;
    }
    
    this.items.splice(index, 1);
    return true;
  }
}

module.exports = new ItemService();
""",
        "src/index.js": """const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const { APP_CONFIG } = require('./utils/constants');
const apiRoutes = require('./routes/api');

dotenv.config();

const app = express();

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Request logging
app.use((req, res, next) => {
  console.log(`${req.method} ${req.path}`);
  next();
});

// Basic routes
app.get('/', (req, res) => {
  res.json({
    message: `Welcome to ${APP_CONFIG.NAME}`,
    version: APP_CONFIG.VERSION,
    status: 'running',
    endpoints: {
      health: '/health',
      api: '/api'
    }
  });
});

app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy',
    timestamp: new Date().toISOString()
  });
});

// API routes
app.use('/api', apiRoutes);

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'NOT_FOUND',
    message: 'Route not found'
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: 'INTERNAL_ERROR',
    message: err.message
  });
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
  console.log(`📦 Environment: ${APP_CONFIG.ENVIRONMENT}`);
  console.log(`🔗 API: http://localhost:${PORT}/api`);
});
""",
        "package.json": """{
  "name": "{{name}}",
  "version": "1.0.0",
  "description": "Node.js application with Express and API integration",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js",
    "dev": "nodemon src/index.js",
    "test": "jest"
  },
  "keywords": ["nodejs", "express", "api", "rest"],
  "author": "",
  "license": "MIT",
  "dependencies": {
    "express": "^4.18.2",
    "dotenv": "^16.3.1",
    "cors": "^2.8.5"
  },
  "devDependencies": {
    "nodemon": "^3.0.1",
    "jest": "^29.7.0"
  }
}"""
    },
    "WebSocket": {
        "src/websocket/server.js": """/**
 * WebSocket server implementation
 */

const WebSocket = require('ws');

class WebSocketServer {
  constructor(server) {
    this.wss = new WebSocket.Server({ server });
    this.clients = new Set();
    
    this.initialize();
  }

  initialize() {
    this.wss.on('connection', (ws) => {
      console.log('New WebSocket connection');
      this.clients.add(ws);

      ws.on('message', (message) => {
        console.log('Received:', message.toString());
        this.broadcast(message.toString());
      });

      ws.on('close', () => {
        console.log('WebSocket connection closed');
        this.clients.delete(ws);
      });

      ws.send(JSON.stringify({ type: 'connection', message: 'Connected to WebSocket server' }));
    });
  }

  broadcast(message) {
    this.clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(message);
      }
    });
  }
}

module.exports = WebSocketServer;
""",
        "package.json": """{
  "name": "{{name}}",
  "version": "1.0.0",
  "description": "Node.js application with Express and WebSocket",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js",
    "dev": "nodemon src/index.js",
    "test": "jest"
  },
  "keywords": ["nodejs", "express", "websocket"],
  "author": "",
  "license": "MIT",
  "dependencies": {
    "express": "^4.18.2",
    "dotenv": "^16.3.1",
    "cors": "^2.8.5",
    "ws": "^8.14.2"
  },
  "devDependencies": {
    "nodemon": "^3.0.1",
    "jest": "^29.7.0"
  }
}"""
    }
}