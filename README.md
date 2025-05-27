# Task-Management-System
[Check out Live Site Here !](https://task-management-system-nf38e2b3z.vercel.app/)


A modern, full-featured task management application built with Python Flask and SQLite. This project demonstrates complete CRUD operations with an excellent responsive web interface.

## Features

### Core Functionality
- **Create Tasks** - Add new tasks with title, description, priority, and due date
- **Read Tasks** - View all tasks in a beautiful dashboard with statistics
- **Update Tasks** - Edit task details and update status in real-time
- **Delete Tasks** - Remove tasks with confirmation prompts

### Advanced Features
- **Dashboard Statistics** - Real-time counters for pending, in-progress, and completed tasks
- **Smart Filtering** - Filter tasks by status and priority
- **Modern UI/UX** - Responsive design with smooth animations and transitions
- **Real-time Updates** - AJAX-powered status updates without page refresh
- **Mobile Responsive** - Works perfectly on all device sizes
- **Priority System** - Visual priority indicators (High, Medium, Low)
- **Due Date Management** - Track and display task deadlines
- **Data Persistence** - SQLite database for reliable data storage
- **Flash Notifications** - User-friendly success/error messages
- **Keyboard Shortcuts** - Ctrl+N for new task, Escape to go back

## Technology Stack

### Backend
- **Python 3.8+** - Core programming language
- **Flask 2.3.3** - Web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Lightweight database

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with Grid and Flexbox
- **JavaScript (ES6+)** - Interactive functionality
- **Font Awesome** - Beautiful icons

## Project Structure

```
task-management-system/
├── app.py             
├── init_db.py            
├── requirements.txt      
├── README.md            
├── tasks.db             
├── templates/         
│   ├── base.html        
│   ├── index.html     
│   ├── create.html      
│   └── edit.html      
└── static/              
    ├── css/
    │   └── style.css    
    └── js/
        └── script.js   
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone or Download
```bash
git clone https://github.com/BHARATHKUMARREDDY2004/Task-Management-System
cd task-management-system

```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database
```bash
python init_db.py
```

### Step 5: Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage Guide

### Creating Tasks
1. Click "New Task" in the navigation or use Ctrl+N
2. Fill in the task details:
   - **Title** (required) - Brief description of the task
   - **Description** (optional) - Detailed information
   - **Priority** - High, Medium, or Low
   - **Due Date** (optional) - When the task should be completed
3. Click "Create Task" to save

### Managing Tasks
- **View Dashboard** - See all tasks with statistics
- **Filter Tasks** - Use dropdown filters for status and priority
- **Update Status** - Change task status directly from the dashboard
- **Edit Tasks** - Click the edit button to modify task details
- **Delete Tasks** - Click delete button (with confirmation)

### Dashboard Features
- **Statistics Cards** - Quick overview of task counts by status
- **Real-time Filtering** - Instantly filter tasks without page reload
- **Status Updates** - Change task status with immediate visual feedback
- **Responsive Grid** - Tasks automatically arrange based on screen size

## API Endpoints

The application also provides REST API endpoints:

- `GET /api/tasks` - Get all tasks
- `GET /api/tasks/<id>` - Get specific task
- `PUT /api/tasks/<id>/status` - Update task status

## Database Schema

### Task Model
```python
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')
    priority = db.Column(db.String(10), default='medium')
    due_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
```


## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
||What is error in it,
