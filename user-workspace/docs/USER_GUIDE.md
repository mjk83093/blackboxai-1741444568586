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

4. **Access the Application**
- Open `https://localhost:8443` in your browser
- You may see a security warning about the self-signed certificate
- Click "Advanced" and proceed to the website
- You'll see the Work Production AI Agent login page

### Security Notes
- The application uses HTTPS for secure communication
- All traffic is encrypted using SSL/TLS
- HTTP requests on port 8080 are automatically redirected to HTTPS (8443)
- In production, replace the self-signed certificates with valid SSL certificates

### Authentication Options

1. **Google Sign-In**
- Click "Sign in with Google"
- Select your Google account
- Grant the necessary permissions

2. **Microsoft Sign-In**
- Click "Sign in with Microsoft"
- Enter your Microsoft credentials
- Grant the necessary permissions

## Features

### 1. Document Processing
- Upload and analyze documents
- Extract key information
- Generate summaries

### 2. Email Management
- AI-assisted email drafting
- Smart categorization
- Template management

### 3. Task Automation
- Create and manage tasks
- AI-powered prioritization
- Deadline management

## Troubleshooting

### Common Issues

1. **Certificate Warning**
   - This is normal in development environment
   - Click "Advanced" > "Proceed to localhost"
   - For production, use a valid SSL certificate

2. **Can't Access the Application?**
   - Ensure Docker containers are running: `docker-compose ps`
   - Check logs: `docker-compose logs`
   - Verify you're using HTTPS and port 8443
   - Make sure ports 8080 and 8443 are not in use

3. **SSL/HTTPS Issues**
   - Ensure nginx container is running
   - Check nginx logs: `docker-compose logs nginx`
   - Verify SSL certificate paths
   - Make sure you're using the correct port (8443)

### Container Management

1. **View container status**
```bash
docker-compose ps
```

2. **Check logs**
```bash
# All containers
docker-compose logs

# Specific container
docker-compose logs nginx
docker-compose logs api
```

3. **Restart containers**
```bash
docker-compose restart
```

### Need Help?
- Check the container logs
- Review documentation
- Contact support

## Stopping the Application
```bash
docker-compose down
```

## Production Deployment
For production deployment:
1. Replace self-signed certificates with valid SSL certificates
2. Update domain names in nginx configuration
3. Configure proper security measures
4. Set up monitoring and logging
5. Consider using standard ports (80/443) with proper permissions
