# Step 1: Base Image
FROM python:3.10

# Step 2: Working Directory
WORKDIR /app

# Step 3: System Dependencies (for psycopg2)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Step 4: Install Python Dependencies
# We copy requirements from the backend folder
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy Application Code
# We need both backend (code) and frontend (templates)
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Step 6: Expose Port
EXPOSE 5000

# Step 7: Command to run the app
# Use -u (unbuffered) so logs show up immediately
CMD ["python", "-u", "backend/app.py"]