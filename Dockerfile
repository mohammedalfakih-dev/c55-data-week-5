# Task 4: Write a cache-friendly Dockerfile.
#
# Requirements (in order):
# 1. Use python:3.11-slim as the base image.
# 2. Copy requirements.txt BEFORE copying source code.
# 3. Install dependencies from requirements.txt.
# 4. Copy src/ into the image.
# 5. Set the CMD to run the pipeline: python -m src.pipeline
#
# Replace each TODO comment with the correct Dockerfile instruction.

# TODO: set the base image
FROM python:3.11-slim

WORKDIR /app

# TODO: copy requirements.txt (before source — this keeps the install layer cached)
COPY requirements.txt .
# TODO: install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# TODO: copy source code
COPY src/ src/
# TODO: set the command that runs when the container starts
CMD ["python", "-m", "src.pipeline"]
