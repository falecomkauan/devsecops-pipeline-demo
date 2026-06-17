# Intentionally insecure Dockerfile, for IaC/config scanners (Trivy, Checkov)
# to flag. Each issue is annotated with the fix.

# ISSUE: using a floating/old base tag instead of a pinned digest.
# Fix: pin to a digest, e.g. python:3.12-slim@sha256:<digest>
FROM python:3.9

# ISSUE: running as root (no USER directive).
# Fix: create and switch to a non-root user.

WORKDIR /app

COPY app/requirements.txt .
RUN pip install -r requirements.txt

COPY app/ .

# ISSUE: secret passed via ENV at build time (ends up in image layers).
# Fix: use build secrets / runtime secrets manager, never bake secrets in.
ENV API_KEY="EXAMPLE_FAKE_API_KEY_PLACEHOLDER_1234"

# ISSUE: container listens on all interfaces with no health check.
EXPOSE 5000

# ISSUE: no USER set, so this runs as root.
CMD ["python", "vulnerable_example.py"]
