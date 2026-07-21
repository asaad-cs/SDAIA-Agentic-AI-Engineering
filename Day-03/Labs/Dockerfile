# Step 1 — start from the official slim Python image
# "slim" is ~120 MB vs ~1 GB for the full image.
# We pin 3.12 (not "latest") so the image is reproducible:
# "latest" changes under you and breaks builds six months from now.
FROM python:3.12-slim

# Step 6 — create a non-root user before anything else.
# If a prompt-injected payload ever achieves code execution, it runs
# as "agent" (no write access to the host) not as root.
RUN useradd --create-home agent

WORKDIR /app

# Step 2 — copy requirements.txt FIRST, then install.
# Docker caches each layer. Because requirements.txt changes far less
# often than your code, the pip layer will be reused on every code
# edit — rebuilds drop from ~60 s to ~2 s.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 2 — copy the code, renamed to app.py inside the image.
# The container is a product; its internal filenames shouldn't depend
# on what the file was called in class.
COPY lab_prototype_to_enterprise.py app.py

# Step 4b — persistent report storage.
# REPORTS_DIR is already read by save_report() in the code.
# We create /reports before the VOLUME declaration so the directory
# exists in the image layer with the correct ownership.
ENV REPORTS_DIR=/reports
RUN mkdir /reports && chown agent /reports
VOLUME /reports

# Step 5 — default to the Stage 5 API server.
# Pass -e LAB_STAGE=3 (or any other stage) at run time to override.
ENV LAB_STAGE=5
EXPOSE 8000

# Step 6 — drop to the non-root user before the process starts.
USER agent

# Step 6 — health check so orchestrators (Kubernetes, ECS) know when
# the container is ready and can restart it if /health stops responding.
# python:3.12-slim has no curl/wget, so we use Python's built-in urllib.
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["python", "app.py", "serve"]
