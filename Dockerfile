# Base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app files
COPY . .

# Expose the port Streamlit will run on
EXPOSE 8501

# Streamlit specific configuration to avoid asking runtime questions
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Run the app
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
