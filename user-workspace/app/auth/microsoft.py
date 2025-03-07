from msal import ConfidentialClientApplication
from fastapi import HTTPException
from typing import Dict, Optional
from config import settings

class MicrosoftAuth:
    def __init__(self):
        self.client = ConfidentialClientApplication(
            client_id=settings.MS_CLIENT_ID,
            client_credential=settings.MS_CLIENT_SECRET,
            authority=f"https://login.microsoftonline.com/{settings.MS_TENANT_ID}"
        )
        
        self.scopes = [
            'User.Read',
            'Mail.Read',
            'Mail.Send',
            'Files.ReadWrite',
            'Tasks.ReadWrite',
            'Calendars.ReadWrite'
        ]

    def get_auth_url(self) -> str:
        """Generate Microsoft OAuth authorization URL"""
        auth_url = self.client.get_authorization_request_url(
            scopes=self.scopes,
            redirect_uri=settings.MS_REDIRECT_URI,
            state="microsoft"
        )
        return auth_url

    async def get_token(self, auth_code: str) -> Dict:
        """Exchange authorization code for access token"""
        try:
            result = self.client.acquire_token_by_authorization_code(
                code=auth_code,
                scopes=self.scopes,
                redirect_uri=settings.MS_REDIRECT_URI
            )
            
            if "error" in result:
                raise HTTPException(
                    status_code=400,
                    detail=f"Error getting token: {result.get('error_description')}"
                )
                
            return result
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get Microsoft token: {str(e)}"
            )

    async def refresh_token(self, refresh_token: str) -> Optional[Dict]:
        """Refresh the access token using refresh token"""
        try:
            result = self.client.acquire_token_by_refresh_token(
                refresh_token=refresh_token,
                scopes=self.scopes
            )
            
            if "error" in result:
                return None
                
            return result
        except Exception:
            return None
