# Installation Instructions for Work Production AI Agent

Follow these steps to set up the Work Production AI Agent on your local machine or server.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher**
- **Docker** (for containerization)
- **Docker Compose** (for managing multi-container applications)
- **Git** (for version control)
- **AWS CLI** (if deploying to AWS)

## Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/work-production-ai.git
cd work-production-ai
```

## Step 2: Set Up a Virtual Environment

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

## Step 3: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Step 4: Configure Environment Variables

Create a `.env` file based on the provided `.env.example`:

```bash
cp .env.example .env
```

Edit the `.env` file to include your credentials for Microsoft, Google, and OpenAI:

```env
# Application Settings
DEBUG=False

# Microsoft OAuth Settings
MS_CLIENT_ID=your_microsoft_client_id
MS_CLIENT_SECRET=your_microsoft_client_secret
MS_TENANT_ID=your_microsoft_tenant_id
MS_REDIRECT_URI=http://localhost:8000/auth/microsoft/callback

# Google OAuth Settings
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

# OpenAI Settings
OPENAI_API_KEY=your_openai_api_key

# Database Settings
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/workproduction

# Redis Settings
REDIS_URL=redis://localhost:6379/0
```

## Step 5: Set Up Database and Redis

If you are using Docker, you can start PostgreSQL and Redis services with Docker Compose:

```bash
docker-compose up -d db redis
```

Wait for the services to be ready before proceeding.

## Step 6: Initialize the Database

Run the following command to create the necessary database tables:

```bash
python -c "
from app.main import app
from app.models import Base
from app.database import engine
Base.metadata.create_all(bind=engine)
"
```

## Step 7: Start the Development Server

Run the FastAPI application:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Access the application at `http://localhost:8000/docs` for the API documentation.

## Step 8: Running Tests

To run the test suite, use:

```bash
pytest
```

## Step 9: Deployment

For production deployment, use the provided deployment scripts:

```bash
./scripts/deploy.sh
```

## Additional Resources

- [API Documentation](docs/API_REFERENCE.md)
- [Contribution Guidelines](docs/CONTRIBUTING.md)
- [Security Policies](docs/SECURITY.md)

## Troubleshooting

If you encounter issues during installation, please check the following:

- Ensure all prerequisites are installed correctly.
- Verify that your environment variables are set up properly.
- Check the logs for any error messages.

For further assistance, feel free to open an issue in the repository.

Thank you for setting up the Work Production AI Agent! 🚀
