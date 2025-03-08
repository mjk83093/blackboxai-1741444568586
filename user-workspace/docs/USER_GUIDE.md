# Work Production AI Agent - Quick Start Guide

## Getting Started

### Prerequisites
- Docker and Docker Compose installed on your system
- API keys for the services you want to use
- SSL certificate (for secure HTTPS connection)

### Quick Setup

1. **Clone the repository and navigate to it**
```bash
git clone <repository-url>
cd work-production-ai
```

2. **Set up your environment variables**
- Copy `.env.example` to `.env`
```bash
cp .env.example .env
```
- Add your API keys to `.env`:
```env
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
DEEPEEK_API_KEY=your-deepseek-key
```

3. **Start the application with SSL**
```bash
docker-compose up -d
```

The application will be available at `https://localhost:8000`

## Basic Usage

### Authentication
- Access the application via HTTPS
- Click "Sign in with Google" or "Sign in with Microsoft"
- Follow the authentication prompts
- Once authenticated, you'll be redirected to the dashboard

### Main Features

1. **Document Processing**
   - Upload documents using the upload button
   - View processed results in the dashboard

2. **Email Management**
   - Connect your email account
   - Use AI to draft and analyze emails

3. **Task Automation**
   - Create and manage tasks
   - AI-assisted prioritization

## Troubleshooting

### Common Issues

1. **SSL Certificate Error?**
   - Ensure you're using HTTPS
   - Accept the self-signed certificate in development
   - For production, use a valid SSL certificate

2. **Can't access the application?**
   - Verify Docker containers are running: `docker-compose ps`
   - Check logs: `docker-compose logs`
   - Ensure you're using HTTPS, not HTTP

### Need Help?
- Check the logs: `docker-compose logs`
- Visit our documentation
- Contact support

## Stopping the Application
```bash
docker-compose down
