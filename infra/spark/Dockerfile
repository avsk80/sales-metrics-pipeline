FROM apache/spark:3.5.1

USER root

# Install python + pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip curl && \
    rm -rf /var/lib/apt/lists/*

# Install python deps
COPY requirements.txt /opt/spark/requirements.txt
RUN pip3 install --no-cache-dir -r /opt/spark/requirements.txt

# Optional: make "python" exist (some tooling expects it)
RUN ln -sf /usr/bin/python3 /usr/bin/python

# Spark defaults can be mounted via volume (recommended), so no COPY needed here
USER 185
