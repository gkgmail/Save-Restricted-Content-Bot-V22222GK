FROM python:3.10-slim-bookworm

# Environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    ffmpeg \
    bash \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Work directory
WORKDIR /app

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip wheel \
    && pip install --no-cache-dir -r requirements.txt

# App source
COPY . .

# Port (Koyeb / webhook use case)
EXPOSE 8000

# Start bot (ONLY ONE PROCESS)
CMD ["python3", "-m", "devgagan"]
