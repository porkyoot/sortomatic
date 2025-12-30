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

# Clone NiceTheme and install it
RUN git clone https://github.com/porkyoot/nicetheme /deps/NiceTheme
RUN pip install -e /deps/NiceTheme

WORKDIR /app

# Copy dependency files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest
COPY . .

# Install the project in editable mode
RUN pip install -e .

EXPOSE 8080

# Use /data for persistence
VOLUME /data

CMD ["sortomatic", "gui", "/data"]
