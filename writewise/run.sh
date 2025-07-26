#!/bin/bash

# Use the Python from virtual environment
PYTHON_CMD="/Users/gsaravanan/gsdev/aicourse-week4/.venv/bin/python"

# Start the FastAPI backend
echo "Starting FastAPI backend..."
cd backend
$PYTHON_CMD -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a moment for the backend to start
echo "Waiting for backend to start..."
sleep 3

# Start the Streamlit frontend
echo "Starting Streamlit frontend..."
cd ../frontend
$PYTHON_CMD -m streamlit run app.py

# Clean up processes when script is terminated
cleanup() {
    echo "Shutting down services..."
    kill $BACKEND_PID
    exit 0
}

# Register the cleanup function for SIGINT and SIGTERM signals
trap cleanup SIGINT SIGTERM

# Keep script running
wait
