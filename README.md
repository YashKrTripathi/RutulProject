# 🎬 YouTube Thumbnail Board

A web application for managing and organizing YouTube thumbnail collections with scoring and categorization.

## 📋 Project Structure

```
thumbnail_board_project/
├── backend/
│   ├── app.py              # Flask REST API
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── streamlit_app.py    # Streamlit UI
│   └── README.txt
├── docker-compose.yml     # Docker multi-container setup
├── Dockerfile            # Docker image definition
├── Procfile             # Heroku deployment config
└── .gitignore          # Git ignore rules
```

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone/Navigate to project**
```bash
cd thumbnail_board_project
```

2. **Install dependencies**
```bash
pip install -r backend/requirements.txt
```

3. **Start Flask Backend** (Terminal 1)
```bash
cd backend
python app.py
```
Backend runs at: `http://localhost:5000`

4. **Start Streamlit Frontend** (Terminal 2)
```bash
cd frontend
streamlit run streamlit_app.py
```
Frontend runs at: `http://localhost:8501`

## 🐳 Docker Setup

### Build & Run with Docker Compose
```bash
docker-compose up --build
```

Access:
- Streamlit: `http://localhost:8501`
- Flask API: `http://localhost:5000`

### Manual Docker Build
```bash
docker build -t thumbnail-board .
docker run -p 8501:8501 -p 5000:5000 thumbnail-board
```

## 📤 Deployment

### Option 1: Streamlit Cloud (Recommended)

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/thumbnail_board_project
git push -u origin main
```

2. **Deploy on Streamlit Cloud**
   - Go to [streamlit.io/cloud](https://streamlit.io/cloud)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file to `frontend/streamlit_app.py`
   - Deploy

### Option 2: Heroku

1. **Install Heroku CLI**
```bash
# On Windows
choco install heroku-cli

# Or download from https://devcenter.heroku.com/articles/heroku-cli
```

2. **Deploy**
```bash
heroku login
heroku create your-app-name
git push heroku main
heroku open
```

### Option 3: Railway.app

1. Go to [railway.app](https://railway.app)
2. Create new project → Deploy from GitHub
3. Connect your repository
4. Set root directory if needed
5. Deploy

### Option 4: Docker + Any Cloud Provider

Push Docker image to:
- **Docker Hub**: `docker push yourusername/thumbnail-board`
- **AWS ECR**
- **Google Cloud Run**
- **Azure Container Registry**

## 📚 API Endpoints

### Boards
- `POST /boards` - Create board
- `GET /boards` - List all boards

### Thumbnails
- `POST /boards/<id>/thumbnails` - Add thumbnail to board
- `GET /boards/<id>/thumbnails` - Get all thumbnails in board
- `PUT /thumbnails/<id>` - Update thumbnail
- `DELETE /thumbnails/<id>` - Delete thumbnail

## ✨ Features

- ✅ Create and manage thumbnail boards
- ✅ Add YouTube URLs (auto-fetch thumbnails)
- ✅ Score and categorize thumbnails
- ✅ Filter by category and score
- ✅ Sort by score or date added
- ✅ Add notes to thumbnails
- ✅ Responsive UI

## 🔧 Environment Variables

Create `.env` file (optional):
```
FLASK_ENV=production
API_BASE_URL=http://localhost:5000
```

## 📝 Development Notes

- Backend runs on port **5000**
- Frontend runs on port **8501**
- SQLite database: `backend/thumbnails.db`
- No authentication currently - add if deploying publicly

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

MIT License - feel free to use this project however you'd like.
