# 🐎 Pony Express - Real-Time Chat Application

A modern, full-stack chat application built with FastAPI and React that enables users to create accounts, join chat rooms, and exchange messages in real-time.

## ✨ Features

- **User Authentication**: Secure user registration and login system
- **Chat Rooms**: Create and join multiple chat rooms
- **Real-Time Messaging**: Send and receive messages instantly
- **User Management**: Profile management and user discovery
- **Responsive Design**: Modern UI built with React and Tailwind CSS
- **RESTful API**: Well-documented API with automatic Swagger documentation

## 🛠️ Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **SQLModel** - Modern SQL database interactions with Python type hints
- **SQLAlchemy** - Database ORM and migrations
- **Uvicorn** - Lightning-fast ASGI server
- **Poetry** - Dependency management and packaging

### Frontend
- **React 18** - Modern React with hooks and functional components
- **React Router** - Client-side routing
- **React Query** - Server state management and caching
- **Tailwind CSS** - Utility-first CSS framework
- **Vite** - Fast build tool and development server

### Database
- **SQLite** (development) - Lightweight database for local development
- **PostgreSQL** (production ready) - Scalable relational database

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 16+
- Poetry (recommended) or pip

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd pony-express-code-sharingan
   ```

2. **Install Python dependencies**

   **Option A: Using Poetry (Recommended)**
   ```bash
   poetry install
   poetry shell
   ```

   **Option B: Using pip and venv**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Start the backend server**

   **With Poetry:**
   ```bash
   poetry run uvicorn backend.main:app --reload
   ```

   **With pip:**
   ```bash
   uvicorn backend.main:app --reload
   ```

4. **Access the API**
   - API Server: http://127.0.0.1:8000
   - Swagger Documentation: http://127.0.0.1:8000/docs
   - ReDoc Documentation: http://127.0.0.1:8000/redoc

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:5173

## 📁 Project Structure

```
pony-express-code-sharingan/
├── backend/
│   ├── routers/
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── users.py         # User management
│   │   └── chats.py         # Chat and messaging
│   ├── main.py              # FastAPI application entry point
│   ├── entities.py          # Database models and schemas
│   ├── database.py          # Database configuration
│   └── auth.py              # Authentication logic
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── context/         # React context providers
│   │   └── App.jsx          # Main application component
│   ├── package.json         # Frontend dependencies
│   └── vite.config.js       # Vite configuration
├── tests/                   # Test files
├── pyproject.toml           # Python project configuration
└── README.md
```

## 🔗 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user

### Users
- `GET /users` - List all users
- `GET /users/{user_id}` - Get user by ID
- `PUT /users/{user_id}` - Update user profile

### Chats
- `GET /chats` - List user's chats
- `POST /chats` - Create new chat room
- `GET /chats/{chat_id}` - Get chat details
- `POST /chats/{chat_id}/messages` - Send message
- `GET /chats/{chat_id}/messages` - Get chat messages
- `POST /chats/{chat_id}/users` - Add user to chat

## 🧪 Development

### Running Tests
```bash
# Backend tests
poetry run pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality
```bash
# Linting
cd frontend
npm run lint

# Type checking (if TypeScript)
npm run type-check
```

### Database Operations
The database is automatically created when the server starts. To reset the database during development, simply delete the SQLite file and restart the server.

## 🐳 Docker Support (Future Enhancement)
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 📊 Database Schema

The application uses a relational database with the following main entities:

- **Users**: Store user account information
- **Chats**: Chat room information and metadata
- **Messages**: Individual messages within chats
- **UserChatLinks**: Many-to-many relationship between users and chats

## 🔐 Security Features

- Password hashing using secure algorithms
- JWT token-based authentication
- CORS configuration for cross-origin requests
- Input validation and sanitization
- SQL injection protection through ORM

## 🚧 Future Enhancements

- [ ] Real-time messaging with WebSockets
- [ ] File and image sharing
- [ ] Message reactions and threading
- [ ] Push notifications
- [ ] Docker containerization
- [ ] Production deployment guides
- [ ] Message encryption
- [ ] User presence indicators

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

Your Name - [your.email@example.com]

## 🙏 Acknowledgments

- FastAPI team for the excellent framework
- React team for the powerful frontend library
- The open-source community for the amazing tools and libraries