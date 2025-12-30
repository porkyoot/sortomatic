FROM python:3.11-alpine

# Install build and runtime dependencies
RUN apk add --no-cache \
    build-base \
    chromaprint-dev \
    gcc \
    musl-dev \
    libffi-dev \
    zlib-dev \
    jpeg-dev \
    git

# Install NiceTheme directly from git
RUN pip install --no-cache-dir git+https://github.com/porkyoot/nicetheme
# Copy dependency files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

# Copy the rest
COPY . .

# Install the project in editable mode
RUN pip install -e .

EXPOSE 8080

# Use /data for persistence
VOLUME /data

CMD ["sortomatic", "gui", "/data"]
