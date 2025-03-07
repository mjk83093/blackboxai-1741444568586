from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from fastapi import HTTPException
from typing import Dict, Optional
import json
from config import settings

class GoogleAuth:
    def __init__(self):
        self.client_config = {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI]
            }
        }
        
        self.scopes = [
            'https://www.googleapis.com/auth/gmail.modify',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/tasks'
        ]

    def get_auth_url(self) -> str:
        """Generate Google OAuth authorization URL"""
        try:
            flow = Flow.from_client_config(
                self.client_config,
                scopes=self.scopes,
                redirect_uri=settings.GOOGLE_REDIRECT_URI
            )
            
            auth_url, _ = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                prompt='consent'
            )
            
            return auth_url
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate Google auth URL: {str(e)}"
            )

    async def get_token(self, auth_code: str) -> Dict:
        """Exchange authorization code for access token"""
        try:
            flow = Flow.from_client_config(
                self.client_config,
                scopes=self.scopes,
                redirect_uri=settings.GOOGLE_REDIRECT_URI
            )
            
            flow.fetch_token(code=auth_code)
            credentials = flow.credentials
            
            return {
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get Google token: {str(e)}"
            )

    async def refresh_token(self, token_info: Dict) -> Optional[Dict]:
        """Refresh the access token using refresh token"""
        try:
            credentials = Credentials(
                token=token_info.get('token'),
                refresh_token=token_info.get('refresh_token'),
                token_uri=token_info.get('token_uri'),
                client_id=token_info.get('client_id'),
                client_secret=token_info.get('client_secret'),
                scopes=token_info.get('scopes')
            )
            
            if credentials.expired:
                credentials.refresh(Request())
                
                return {
                    'token': credentials.token,
                    'refresh_token': credentials.refresh_token,
                    'token_uri': credentials.token_uri,
                    'client_id': credentials.client_id,
                    'client_secret': credentials.client_secret,
                    'scopes': credentials.scopes
                }
            
            return token_info
        except Exception:
            return None
