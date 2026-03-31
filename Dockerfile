# Use Python 3.10 for OpenEnv compatibility
FROM python:3.10-slim

# Set up a new user named "user" with user ID 1000 (HF requirement)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Copy dependency files first for faster building
COPY --chown=user pyproject.toml ./ 
# Install core dependencies
RUN pip install --no-cache-dir fastapi uvicorn requests pydantic openai

# Copy the rest of your validated code
COPY --chown=user . /app

# Hugging Face Spaces MUST listen on port 7860
EXPOSE 7860

# Launch Uvicorn pointing to your root app.py
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
