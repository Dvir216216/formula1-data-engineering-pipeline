# 1. Base Image: Use Python 3.13 to match pyproject.toml
FROM python:3.13-slim

# 2. Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Work Directory
WORKDIR /app

# 4. Copy dependency files
COPY pyproject.toml uv.lock ./

# 5. Install dependencies using uv (creates a virtual environment inside the container)
RUN uv sync --frozen --no-cache

# 6. Copy the rest of the application code
COPY . .

# 7. Expose Port
EXPOSE 8501

# 8. Run Command using uv to run streamlit from the virtual environment
CMD ["uv", "run", "streamlit", "run", "src/dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]