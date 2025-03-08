# Work Production AI Agent - Quick Start Guide

## Getting Started

### Prerequisites
- Docker and Docker Compose installed on your system
- API keys for the services you want to use

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

3. **Start the application**
```bash
docker-compose up -d
```

The application will be available at `http://localhost:8000`

## Basic Usage

### Authentication
- Click "Sign in with Google" or "Sign in with Microsoft"
- Follow the authentication prompts
- Once authenticated, you'll be redirected to the dashboard

### Main Features

1. **Document Processing**
   - Upload documents using the upload button
   - View processed results in the dashboard
   - Download or share results as needed

2. **Email Management**
   - Connect your email account
   - Use AI to draft and analyze emails
   - Manage email templates

3. **Task Automation**
   - Create new tasks
   - Let AI help prioritize and organize
   - Track progress in the dashboard

## Troubleshooting

### Common Issues

1. **Can't start the application?**
   - Ensure Docker is running
   - Check if ports 8000 is available
   - Verify your API keys in `.env`

2. **Authentication issues?**
   - Ensure your API keys are correct
   - Check your internet connection
   - Try clearing your browser cache

### Need Help?
- Check the logs: `docker-compose logs`
- Visit our documentation
- Contact support

## Stopping the Application
```bash
docker-compose down
