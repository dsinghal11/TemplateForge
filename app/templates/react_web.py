"""React Web Dashboard Template with TypeScript - UPDATED"""

BASE_TEMPLATE = {
    "package.json": """{
  "name": "{{name}}",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "typescript": "^4.9.5",
    "web-vitals": "^2.1.4",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@types/node": "^18.0.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}""",
    "tsconfig.json": """{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "jsx": "react-jsx",
    "module": "ESNext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "allowJs": true,
    "noEmit": true,
    "isolatedModules": true,
    "esModuleInterop": true,
    "strict": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "allowSyntheticDefaultImports": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": "src"
  },
  "include": ["src"]
}""",
    "public/index.html": """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="{{name}} - Modern React Dashboard" />
    <title>{{name}}</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>""",
    "src/index.tsx": """import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);""",
    "src/App.tsx": """import React from 'react';
import './App.css';

const App: React.FC = () => {
  const appName = process.env.REACT_APP_NAME || '{{name}}';
  const appVersion = '1.0.0';
  const environment = process.env.NODE_ENV || 'development';

  return (
    <div className="App">
      <header className="App-header">
        <h1>{appName} Dashboard</h1>
        <p>Welcome to your new React TypeScript dashboard!</p>
        <div className="info">
          <p>Version: {appVersion}</p>
          <p>Environment: {environment}</p>
        </div>
      </header>
    </div>
  );
};

export default App;""",
    "src/App.css": """.App {
  text-align: center;
}

.App-header {
  background-color: #282c34;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: calc(10px + 2vmin);
  color: white;
}

.App-header h1 {
  margin-bottom: 1rem;
}

.App-header p {
  font-size: 1.2rem;
  color: #61dafb;
}

.info {
  margin-top: 2rem;
  padding: 1rem;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
}

.info p {
  font-size: 0.9rem;
  color: #ffffff;
  margin: 0.5rem 0;
}""",
    "src/index.css": """* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}""",
    "src/react-app-env.d.ts": """/// <reference types="react-scripts" />""",
    ".env.example": """# Application
REACT_APP_NAME={{name}}
REACT_APP_API_URL=http://localhost:8000
""",
    ".env": """# Application
REACT_APP_NAME={{name}}
REACT_APP_API_URL=http://localhost:8000
""",
    "README.md": """# {{name}}

A modern React TypeScript dashboard application with production-ready setup.

## Features

- ⚛️ React 18 with TypeScript
- 🎨 Modern CSS styling
- 🔧 Configured ESLint and TypeScript
- 📦 Production build optimization
- 🔄 Hot reload development server
- 📐 Architecture folder at project root with .drawio file for design

## Getting Started

### Install Dependencies
```bash
npm install
```

### Development Server
```bash
npm start
```
Opens [http://localhost:3000](http://localhost:3000)

### Build for Production
```bash
npm build
```

### Run Tests
```bash
npm test
```

## Project Structure

```
{{name}}/
├── architecture/          # Architecture documentation & design
│   ├── architecture.drawio  # Visual architecture diagram
│   ├── components/       # Component architecture
│   ├── hooks/            # Custom hooks
│   ├── contexts/         # React contexts
│   ├── services/         # API services
│   ├── pages/            # Page components
│   ├── assets/           # Static assets
│   ├── styles/           # Global styles
│   ├── types/            # TypeScript types
│   └── utils/            # Utility functions
├── public/
│   └── index.html
├── src/
│   ├── App.tsx           # Main app component
│   ├── App.css           # App styles
│   └── index.tsx         # Entry point
├── .env                  # Environment variables
├── package.json
└── tsconfig.json
```

## Architecture

Use the `/architecture` folder at project root to:
1. Design your system with `architecture.drawio` (open with https://app.diagrams.net/)
2. Organize code files in architecture subfolders
3. Document your component structure

## Available Scripts

- `npm start` - Run development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm eject` - Eject from Create React App (irreversible)

## TypeScript

This project uses TypeScript for type safety. All `.tsx` and `.ts` files are type-checked.

## Environment Variables

Configure your app in `.env`:
```
REACT_APP_NAME=your-app-name
REACT_APP_API_URL=http://localhost:8000
```

## Learn More

- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/)
- [Create React App Documentation](https://create-react-app.dev/)
""",
    ".gitignore": """# Dependencies
node_modules/
.pnp
.pnp.js

# Testing
coverage/

# Production
build/
dist/

# Environment
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*
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

# Misc
.cache/
temp/
tmp/
"""
}