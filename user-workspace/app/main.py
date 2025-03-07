from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Optional
import jwt
from datetime import datetime, timedelta

from config import settings
from app.auth.microsoft import MicrosoftAuth
from app.auth.google import GoogleAuth
from app.ai.mcp import ModelContextProtocol
from app.services.document_service import DocumentService
from app.services.email_service import EmailService
from app.services.task_service import TaskService

app = FastAPI(title="Work Production AI Agent")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
microsoft_auth = MicrosoftAuth()
google_auth = GoogleAuth()
mcp = ModelContextProtocol()

# JWT token handling
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

async def get_current_user(request: Request) -> Dict:
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authentication")
    
    try:
        token = token.split(" ")[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Authentication routes
@app.get("/auth/microsoft")
async def microsoft_auth_url():
    """Get Microsoft OAuth URL"""
    return {"url": microsoft_auth.get_auth_url()}

@app.get("/auth/google")
async def google_auth_url():
    """Get Google OAuth URL"""
    return {"url": google_auth.get_auth_url()}

@app.post("/auth/microsoft/callback")
async def microsoft_callback(code: str):
    """Handle Microsoft OAuth callback"""
    try:
        token_info = await microsoft_auth.get_token(code)
        access_token = create_access_token({
            "platform": "microsoft",
            "token_info": token_info
        })
        return {"access_token": access_token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/google/callback")
async def google_callback(code: str):
    """Handle Google OAuth callback"""
    try:
        token_info = await google_auth.get_token(code)
        access_token = create_access_token({
            "platform": "google",
            "token_info": token_info
        })
        return {"access_token": access_token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# AI Assistant routes
@app.post("/ai/process")
async def process_request(
    request: Dict,
    current_user: Dict = Depends(get_current_user)
):
    """Process user request through AI"""
    try:
        platform = current_user["platform"]
        token_info = current_user["token_info"]
        
        response = await mcp.process_request(
            user_id=token_info["id"],
            request=request["text"],
            platform=platform,
            additional_context=request.get("context")
        )
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Document routes
@app.post("/documents/create")
async def create_document(
    request: Dict,
    current_user: Dict = Depends(get_current_user)
):
    """Create new document"""
    try:
        service = DocumentService(
            platform=current_user["platform"],
            credentials=current_user["token_info"]
        )
        
        return await service.create_document(
            name=request["name"],
            content=request["content"],
            folder_id=request.get("folder_id")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents/{document_id}")
async def read_document(
    document_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Read document content"""
    try:
        service = DocumentService(
            platform=current_user["platform"],
            credentials=current_user["token_info"]
        )
        
        return await service.read_document(document_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Email routes
@app.post("/emails/send")
async def send_email(
    request: Dict,
    current_user: Dict = Depends(get_current_user)
):
    """Send email"""
    try:
        service = EmailService(
            platform=current_user["platform"],
            credentials=current_user["token_info"]
        )
        
        return await service.send_email(
            to=request["to"],
            subject=request["subject"],
            body=request["body"],
            cc=request.get("cc"),
            bcc=request.get("bcc")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/emails")
async def read_emails(
    folder: str = "inbox",
    limit: int = 10,
    query: Optional[str] = None,
    current_user: Dict = Depends(get_current_user)
):
    """Read emails from folder"""
    try:
        service = EmailService(
            platform=current_user["platform"],
            credentials=current_user["token_info"]
        )
        
        return await service.read_emails(folder, limit, query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Task routes
@app.post("/tasks/create")
async def create_task(
    request: Dict,
    current_user: Dict = Depends(get_current_user)
):
    """Create new task"""
    try:
        service = TaskService(
            platform=current_user["platform"],
            credentials=current_user["token_info"]
        )
        
        return await service.create_task(
            title=request["title"],
            description=request.get("description"),
            due_date=request.get("due_date"),
            list_id=request.get("list_id")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks")
async def get_tasks(
    list_id: Optional[str] = None,
    status: Optional[str] = None,
    current_user: Dict = Depends(get_current_user)
):
    """Get tasks from list"""
    try:
        service = TaskService(
            platform=current_user["platform"],
            credentials=current_user["token_info"]
        )
        
        return await service.get_tasks(list_id, status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/calendar/events/create")
async def create_event(
    request: Dict,
    current_user: Dict = Depends(get_current_user)
):
    """Create calendar event"""
    try:
        service = TaskService(
            platform=current_user["platform"],
            credentials=current_user["token_info"]
        )
        
        return await service.create_event(
            title=request["title"],
            start_time=request["start_time"],
            end_time=request["end_time"],
            description=request.get("description"),
            attendees=request.get("attendees"),
            location=request.get("location")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Error handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
