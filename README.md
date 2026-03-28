# 🚀 DevCraft: AI-Powered Project Planner

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg?style=flat-square&logo=react&logoColor=black)](https://reactjs.org/)
[![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-4285F4.svg?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)

**DevCraft** is a high-performance, full-stack application that transforms your skills and interests into a comprehensive development roadmap. Powered by **Google Gemini**, it generates personalized project ideas and complete execution plans in seconds.

---

## ✨ Features

- 🎯 **Tailored Ideas**: Generates projects based on your specific tech stack and experience level.
- 📋 **Feature Breakdown**: Detailed core and nice-to-have feature lists with prioritization.
- 🛠️ **Smart Tech Stack**: Recommended libraries and tools specifically chosen for the project.
- 🗺️ **Phased Roadmap**: A step-by-step development guide from initialization to deployment.
- 📚 **Learning Path**: Curated resources to help you master the new technologies required.

---

## 🛠️ Tech Stack

| Layer         | Technology                  |
| :------------ | :-------------------------- |
| **Frontend**  | React, Vite, TailwindCSS    |
| **Backend**   | Python, FastAPI, SQLAlchemy |
| **Database**  | SQLite (Local)              |
| **AI Engine** | **Google Gemini**           |

---

## 🚀 Quick Start

### 1. Backend Setup

```bash
# Clone the repository
git clone https://github.com/Sarthakk404/DevCraft-AI-Powered-Project-Idea-Generator-Development-Planner.git
cd DevCraft

# Create and activate virtual environment
python -m venv venv

# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure Environment
# Create a .env file and add your Gemini API Key
echo "GEMINI_API_KEY=your_gemini_key_here" > .env
echo "GEMINI_MODEL=gemini-2.0-flash" >> .env

# Run the API
uvicorn app.main:app --reload
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## 📖 Usage

1.  Visit `http://localhost:5173`.
2.  Input your **Skills**, **Interests**, and **Experience Level**.
3.  Define your **Goal** and **Time Availability**.
4.  Hit **"Generate Project Plan"** and watch Gemini architect your next project in real-time.

---

## 🛡️ Troubleshooting

- **API Key Error**: Ensure `GEMINI_API_KEY` is set in your `.env` file.
- **Model Not Found**: The default is `gemini-2.0-flash`. Ensure your Google AI account has access to this model.
- **CORS Issues**: The backend defaults to allowing all origins (`*`) for local development.

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<p align="center">Made with ❤️ for Developers</p>
