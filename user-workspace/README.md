# Work Production AI Agent

An AI-powered assistant that integrates with Microsoft 365 and Google Workspace to help users with document processing, email automation, and task management using the Model Context Protocol (MCP).

## Features

- 🔐 **Secure Authentication**
  - OAuth 2.0 integration with Microsoft and Google
  - Role-Based Access Control (RBAC)
  - JWT token-based session management

- 🤖 **AI Processing with MCP**
  - Context-aware automation
  - Intelligent document and email processing
  - Multi-step workflow support

- 📄 **Document Management**
  - Read, create, and edit documents across platforms
  - Document format conversion
  - AI-powered content generation

- 📧 **Email Automation**
  - Smart email processing and categorization
  - Automated response generation
  - Calendar integration for scheduling

- ✅ **Task Management**
  - Cross-platform task creation and tracking
  - Project status reporting
  - Automated workflow management

## Prerequisites

- Python 3.8+
- Microsoft 365 Developer Account
- Google Cloud Project with enabled APIs
- OpenAI API Key

## Installation

1. Clone the repository:
\`\`\`bash
git clone https://github.com/yourusername/work-production-ai.git
cd work-production-ai
\`\`\`

2. Install dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. Create a .env file with your configuration:
\`\`\`env
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

# Security Settings
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
\`\`\`

## Usage

1. Start the server:
\`\`\`bash
python -m uvicorn app.main:app --reload
\`\`\`

2. Access the API documentation at http://localhost:8000/docs

3. Authenticate with either Microsoft or Google:
   - Navigate to /auth/microsoft or /auth/google
   - Complete the OAuth flow
   - Use the returned access token for subsequent requests

## API Endpoints

### Authentication
- GET `/auth/microsoft` - Get Microsoft OAuth URL
- GET `/auth/google` - Get Google OAuth URL
- POST `/auth/microsoft/callback` - Handle Microsoft OAuth callback
- POST `/auth/google/callback` - Handle Google OAuth callback

### AI Processing
- POST `/ai/process` - Process user request through AI

### Documents
- POST `/documents/create` - Create new document
- GET `/documents/{document_id}` - Read document content

### Emails
- POST `/emails/send` - Send email
- GET `/emails` - Read emails from folder

### Tasks
- POST `/tasks/create` - Create new task
- GET `/tasks` - Get tasks from list
- POST `/calendar/events/create` - Create calendar event

## Security

- All endpoints require authentication via JWT tokens
- OAuth 2.0 flow for secure platform access
- RBAC implementation for user permissions
- Data encryption in transit and at rest

## Development

### Project Structure
\`\`\`
work-production-ai/
├── app/
│   ├── auth/
│   │   ├── microsoft.py
│   │   └── google.py
│   ├── ai/
│   │   └── mcp.py
│   ├── services/
│   │   ├── document_service.py
│   │   ├── email_service.py
│   │   └── task_service.py
│   └── main.py
├── config.py
├── requirements.txt
└── README.md
\`\`\`

### Adding New Features

1. Create new service modules in `app/services/`
2. Implement new routes in `app/main.py`
3. Update authentication if needed in `app/auth/`
4. Add new AI capabilities in `app/ai/mcp.py`

## Testing

Run tests using pytest:
\`\`\`bash
pytest
\`\`\`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
