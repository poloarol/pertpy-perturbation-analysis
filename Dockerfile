FROM python:3.11-slim

# --------------------------------------------------
# System dependencies
# --------------------------------------------------

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libhdf5-dev \
    libopenblas-dev \
    liblapack-dev \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*


# --------------------------------------------------
# Python configuration
# --------------------------------------------------

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /workspace


# --------------------------------------------------
# Install Python dependencies
# --------------------------------------------------

COPY ./requirements.txt .

RUN pip install -r ./requirements.txt


# --------------------------------------------------
# Default command
# --------------------------------------------------

CMD ["snakemake", "--cores", "1"]