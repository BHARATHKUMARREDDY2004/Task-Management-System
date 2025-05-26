from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import sqlite3
import re
import html
import importlib.util
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

# Configure database
# For Vercel, we'll use a temporary in-memory database for demo purposes
# In a real app, you would use a managed database service
is_vercel = 'VERCEL' in os.environ
if is_vercel:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    print("Running on Vercel with in-memory database")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    print("Running locally with file database")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed
    priority = db.Column(db.String(10), default='medium')  # low, medium, high
    due_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Routes
@app.route('/')
def index():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template('index.html', tasks=tasks)

@app.route('/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        due_date = request.form['due_date']
        
        if not title:
            flash('Title is required!', 'error')
            return redirect(url_for('create_task'))
        
        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=datetime.strptime(due_date, '%Y-%m-%d').date() if due_date else None
        )
        
        try:
            db.session.add(task)
            db.session.commit()
            flash('Task created successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash('Error creating task!', 'error')
            db.session.rollback()
    
    return render_template('create.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    task = Task.query.get_or_404(id)
    
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        task.status = request.form['status']
        task.priority = request.form['priority']
        due_date = request.form['due_date']
        task.due_date = datetime.strptime(due_date, '%Y-%m-%d').date() if due_date else None
        task.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('Task updated successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash('Error updating task!', 'error')
            db.session.rollback()
    
    return render_template('edit.html', task=task)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    
    try:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!', 'success')
    except Exception as e:
        flash('Error deleting task!', 'error')
        db.session.rollback()
    
    return redirect(url_for('index'))

@app.route('/api/tasks')
def api_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@app.route('/api/tasks/<int:id>')
def api_task(id):
    task = Task.query.get_or_404(id)
    return jsonify(task.to_dict())

@app.route('/api/tasks/<int:id>/status', methods=['PUT'])
def update_task_status(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    
    if 'status' in data:
        task.status = data['status']
        task.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(task.to_dict())
    
    return jsonify({'error': 'Status is required'}), 400

@app.route('/raw-data')
def view_raw_data():
    tasks = Task.query.all()
    return render_template('raw_data.html', tasks=tasks, query=None, results=None, columns=None, error=None)

@app.route('/execute-query', methods=['POST'])
def execute_query():
    query = request.form.get('query', '')
    tasks = Task.query.all()  # Always get tasks for the default table view
    
    # Security check: Only allow SELECT statements
    if not query.strip().lower().startswith('select'):
        return render_template('raw_data.html', 
                              tasks=tasks,
                              query=query,
                              error="Only SELECT queries are allowed for security reasons.",
                              results=None,
                              columns=None)
    
    # Sanitize the query to prevent SQL injection
    # This is a basic check and not comprehensive
    if re.search(r'(;[\s]*(drop|delete|update|insert|alter|create|replace))', query.lower(), re.DOTALL):
        return render_template('raw_data.html',
                              tasks=tasks,
                              query=query,
                              error="Query contains prohibited statements.",
                              results=None,
                              columns=None)
    
    # Execute the query
    try:
        # Use the appropriate database path based on environment
        is_vercel = 'VERCEL' in os.environ
        if is_vercel:
            # For Vercel, we need to use the in-memory database
            conn = sqlite3.connect(':memory:')
        else:
            # For local development, use the file database
            db_path = os.path.join(app.root_path, 'instance', 'tasks.db')
            conn = sqlite3.connect(db_path)
        
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Adding a timeout to prevent long-running queries
        cursor.execute("PRAGMA query_timeout = 5000")  # 5 second timeout
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Get column names
        columns = [description[0] for description in cursor.description]
        
        # Convert results to list of lists for easier templating
        results_list = []
        for row in results:
            row_list = []
            for value in row:
                # Handle special cases like datetime objects
                if isinstance(value, datetime):
                    row_list.append(value.strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    row_list.append(value)
            results_list.append(row_list)
        
        conn.close()
        
        return render_template('raw_data.html', 
                              tasks=tasks,
                              query=query,
                              results=results_list,
                              columns=columns,
                              error=None)
    
    except Exception as e:
        return render_template('raw_data.html', 
                              tasks=tasks,
                              query=query,
                              error=f"Error executing query: {str(e)}",
                              results=None,
                              columns=None)

def initialize_database_if_empty():
    with app.app_context():
        db.create_all()
        # Check if database is empty
        if Task.query.first() is None:
            try:
                # Import init_database function from init_db.py
                spec = importlib.util.spec_from_file_location(
                    "init_db", 
                    os.path.join(os.path.dirname(os.path.abspath(__file__)), "init_db.py")
                )
                init_db_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(init_db_module)
                
                # Call the init_database function
                init_db_module.init_database()
                print("Database initialized with sample data!")
            except Exception as e:
                print(f"Error initializing database: {e}")

# Initialize the database (especially important for Vercel's in-memory database)
with app.app_context():
    db.create_all()
    # Check if the database is empty
    if Task.query.first() is None:
        try:
            # Import and call init_database if not on Vercel
            if not ('VERCEL' in os.environ):
                from init_db import init_database
                init_database()
            else:
                # Create some sample data for Vercel demo
                from datetime import date
                sample_tasks = [
                    Task(
                        title="Setup Development Environment",
                        description="Install Python, Flask, and set up the project structure",
                        status="completed",
                        priority="high",
                        due_date=date(2025, 1, 15)
                    ),
                    Task(
                        title="Design Database Schema",
                        description="Create the database models for the task management system",
                        status="completed",
                        priority="high",
                        due_date=date(2025, 1, 20)
                    ),
                    Task(
                        title="Implement CRUD Operations",
                        description="Build Create, Read, Update, Delete functionality for tasks",
                        status="in_progress",
                        priority="high",
                        due_date=date(2025, 1, 25)
                    )
                ]
                for task in sample_tasks:
                    db.session.add(task)
                db.session.commit()
                print("Vercel database initialized with sample data")
        except Exception as e:
            print(f"Error initializing database: {e}")

if __name__ == '__main__':
    app.run(debug=True)
