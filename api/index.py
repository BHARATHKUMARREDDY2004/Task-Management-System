from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import sys

# Add the parent directory to sys.path to ensure imports work correctly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import app from app.py
from app import app as flask_app

# This is the entry point for Vercel
app = flask_app

# If this file is run directly, start the development server
if __name__ == "__main__":
    app.run(debug=True)
