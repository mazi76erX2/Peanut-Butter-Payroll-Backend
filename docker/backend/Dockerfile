# Use a slim Python 3.12 base image
FROM python:3.12.7-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update
RUN apt-get install libpq-dev -y

# Install Pipenv
RUN python3 -m ensurepip --upgrade
RUN pip install pipenv

# Copy Pipenv files and lock file (if using)
COPY Pipfile Pipfile.lock ./

# Install dependencies using Pipenv
RUN pipenv install --system --dev

# Copy your application code
COPY . .

# Set the entrypoint command
EXPOSE 8000

# Default command
CMD ["bash", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --app-dir backend --port 8000 --reload"]