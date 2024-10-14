# Backend (FastAPI) - Stage 1
FROM python:3.10-slim as backend

WORKDIR /app

# Copy backend requirements and install dependencies
COPY Application/Backend/requirements.txt ./Backend/
RUN pip install --no-cache-dir -r Backend/requirements.txt

# Copy backend source code
COPY Application/Backend ./Backend

# Frontend (React) - Stage 2
FROM node:16-alpine as frontend

WORKDIR /app/Frontend

# Copy frontend dependencies and install
COPY Application/Frontend/package.json Application/Frontend/package-lock.json ./
RUN npm install

# Copy frontend source code
COPY Application/Frontend ./

# Build the frontend
RUN npm run build

# Final Stage
FROM python:3.10-slim

WORKDIR /app

# Copy backend files
COPY --from=backend /app/Backend ./Backend

# Copy frontend build files
COPY --from=frontend /app/Frontend/build ./Frontend/build

# Install backend dependencies
RUN pip install --no-cache-dir -r Backend/requirements.txt

# Create a non-root user and switch to it
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Expose backend port
EXPOSE 8000

# Use an environment variable for the port
ENV PORT=8000

# Command to run the FastAPI app
CMD ["sh", "-c", "cd Backend && uvicorn app:app --host 0.0.0.0 --port $PORT"]
