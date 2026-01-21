FROM python:3.11-slim

WORKDIR /backend

# Copy requirements first for cache efficiency
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend application code
COPY src ./src

# Expose the port expected by HF Spaces (7860)
EXPOSE 7860

# Run the application
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "7860"]
