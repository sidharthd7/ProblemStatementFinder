# Problem Statement Finder

A powerful tool designed to help hackathon participants and project mentors match teams with the most suitable problem statements based on their skills and experience.

## 🎯 Use Cases

### For Hackathon Participants
- **Smart Team Matching**: Automatically match teams with problem statements that align with their technical expertise
- **Skill-Based Distribution**: Ensure fair distribution of challenges based on team capabilities
- **Efficient Resource Allocation**: Reduce manual effort in team-problem matching process

### For Project Mentors
- **Skill Gap Analysis**: Identify areas where teams need additional support or training
- **Personalized Recommendations**: Provide tailored guidance based on team capabilities

## ⚙️ Technologies Used

### Frontend
- **React.js**: Modern UI development
- **Tailwind CSS**: Responsive and beautiful styling
- **React Router**: Navigation and routing
- **Axios**: API communication

### Backend
- **FastAPI**: High-performance API framework
- **Cohere AI**: Natural language processing for skill analysis (Vector Embeddings and Content generation)
- **SQLAlchemy**: Database ORM
- **PostgreSQL**: Relational database
- **Alembic**: Database migrations

## 📁 Project Structure

project/
├── backend/
│   ├── alembic/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   ├── utils/
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx

## 🚀 Features

- **Team Management**
  - Create and manage teams
  - Add team members with their skills

- **Problem Statement Analysis**
  - Upload problem statements
  - Automatic skill requirement extraction
  - Difficulty level assessment

- **Smart Matching**
  - AI-powered team-problem matching
  - Skill gap analysis
  - Personalized recommendations

- **User Interface**
  - Clean and intuitive design
  - Real-time updates

## 📸 Project Snapshots

### Authentication 
![Login and Signup](/frontend/src/assets/Login.png)  

### Home Page
![Home Page](/frontend/src/assets/Home.png)

### Team Management and Creation
![Teams Dashboard](/frontend/src/assets/Team.png)
![Teams Creation](/frontend/src/assets/TeamCreation.png)

### Results Display
![Results](/frontend/src/assets/HomePagewResults.png)

## 🛠️ Setup and Installation

### Prerequisites
- Node.js (v14 or higher)
- Python (v3.8 or higher)
- PostgreSQL
- Cohere AI API key

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Backend Setup
```bash
cd backend
python -m venv venv
source venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## 🔧 Environment Variables

Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
COHERE_API_KEY=your_cohere_api_key
```
