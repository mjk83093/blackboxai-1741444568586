from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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

# Static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

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

# Root route - serve the login page
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

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

# [Rest of the routes remain the same...]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, ssl_keyfile="key.pem", ssl_certfile="cert.pem")
