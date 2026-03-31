FROM python:3.10-slim

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock* ./
# Note: If 'pip install .' fails, use: RUN pip install fastapi uvicorn requests pydantic openai
RUN pip install .

# Copy the rest of the code
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# FIXED: Removed 'server.' because app.py is in the root folder
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]