from datetime import datetime, date
import os

def init_database():
    """Initialize the database with sample data"""
    # Import here to avoid circular imports
    from app import app, db, Task
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if we already have data
        if Task.query.first():
            print("Database already has data. Skipping initialization.")
            return
        
        # Create sample tasks
        sample_tasks = [
            Task(
                title="Setup Development Environment",
                description="Install Python, Flask, and set up the project structure",
                status="completed",
                priority="high",
                due_date=date(2024, 1, 15)
            ),
            Task(
                title="Design Database Schema",
                description="Create the database models for the task management system",
                status="completed",
                priority="high",
                due_date=date(2024, 1, 20)
            ),
            Task(
                title="Implement CRUD Operations",
                description="Build Create, Read, Update, Delete functionality for tasks",
                status="in_progress",
                priority="high",
                due_date=date(2024, 1, 25)
            ),
            Task(
                title="Create Web Interface",
                description="Design and implement the user interface with HTML, CSS, and JavaScript",
                status="in_progress",
                priority="medium",
                due_date=date(2024, 1, 30)
            ),
            Task(
                title="Add User Authentication",
                description="Implement user login and registration functionality",
                status="pending",
                priority="medium",
                due_date=date(2024, 2, 5)
            ),
            Task(
                title="Write Documentation",
                description="Create comprehensive documentation for the project",
                status="pending",
                priority="low",
                due_date=date(2024, 2, 10)
            ),
            Task(
                title="Deploy to Production",
                description="Set up production environment and deploy the application",
                status="pending",
                priority="high",
                due_date=date(2024, 2, 15)
            )
        ]
        
        # Add sample tasks to database
        for task in sample_tasks:
            db.session.add(task)
        
        try:
            db.session.commit()
            print("Database initialized with sample data successfully!")
        except Exception as e:
            print(f"Error initializing database: {e}")
            db.session.rollback()

if __name__ == '__main__':
    init_database()
