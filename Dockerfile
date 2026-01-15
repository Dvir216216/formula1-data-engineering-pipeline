# 1. Base Image: Use a lightweight Python version
FROM python:3.10-slim

# 2. Work Directory: Create a working directory inside the container
WORKDIR /app

# 3. Dependencies: Copy requirements file and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy Code: Copy the rest of the application code
# Note: This acts as a fallback if volumes are not used
COPY . .

# 5. Expose Port: Expose Streamlit's default port
EXPOSE 8501

# 6. Run Command: Start the Streamlit application
# 'server.address=0.0.0.0' is required to make it accessible from outside the container
CMD ["streamlit", "run", "src/dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]