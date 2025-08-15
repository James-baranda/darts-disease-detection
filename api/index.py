from flask import Flask, render_template, request, send_from_directory
import os
import sys

# Add the parent directory to the Python path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the main app from the parent directory
from app import app

# This is required for Vercel
if __name__ == "__main__":
    app.run()
