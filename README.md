# CICDASSIGNMENT

This project consists of a FastAPI backend and a React frontend.

## Project Structure


## Prerequisites

- Python 3.10+
- Node.js 16+
- Docker (for containerized deployment)

## Running the Application Locally

### Backend (FastAPI)

1. Navigate to the backend directory:
   ```
   cd Application/Backend
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the FastAPI server:
   ```
   uvicorn app:app --reload
   ```

The backend will be available at `http://localhost:8000`.

### Frontend (React)

1. Navigate to the frontend directory:
   ```
   cd Application/Frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the React development server:
   ```
   npm start
   ```

The frontend will be available at `http://localhost:3000`.

## Running with Docker

To run the entire application using Docker:

1. Make sure Docker is installed and running on your machine.

2. Build the Docker image:
   ```
   docker build -t cicdassignment .
   ```

3. Run the Docker container:
   ```
   docker run -p 8000:8000 cicdassignment
   ```

The application will be available at `http://localhost:8000`.

## API Documentation

Once the backend is running, you can access the API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

### Backend Tests

To run backend tests:

```
cd Application/Backend
pytest
```

### Frontend Tests

To run frontend tests:

```
cd Application/Frontend
npm test
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
