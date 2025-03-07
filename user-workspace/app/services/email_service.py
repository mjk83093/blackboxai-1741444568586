from typing import Dict, List, Optional
from fastapi import HTTPException
from microsoft.graph import GraphServiceClient
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class EmailService:
    def __init__(self, platform: str, credentials: Dict):
        """Initialize email service for specified platform"""
        self.platform = platform
        self.credentials = credentials
        self._init_client()

    def _init_client(self):
        """Initialize appropriate client based on platform"""
        try:
            if self.platform == "microsoft":
                self.client = GraphServiceClient(self.credentials)
            elif self.platform == "google":
                self.client = build('gmail', 'v1', credentials=self.credentials)
            else:
                raise ValueError(f"Unsupported platform: {self.platform}")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize {self.platform} client: {str(e)}"
            )

    async def read_emails(
        self,
        folder: str = "inbox",
        limit: int = 10,
        query: Optional[str] = None
    ) -> List[Dict]:
        """Read emails from specified folder"""
        try:
            if self.platform == "microsoft":
                return await self._read_microsoft_emails(folder, limit, query)
            elif self.platform == "google":
                return await self._read_google_emails(folder, limit, query)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to read emails: {str(e)}"
            )

    async def send_email(
        self,
        to: List[str],
        subject: str,
        body: str,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> Dict:
        """Send email through specified platform"""
        try:
            if self.platform == "microsoft":
                return await self._send_microsoft_email(to, subject, body, cc, bcc)
            elif self.platform == "google":
                return await self._send_google_email(to, subject, body, cc, bcc)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to send email: {str(e)}"
            )

    async def _read_microsoft_emails(
        self,
        folder: str,
        limit: int,
        query: Optional[str]
    ) -> List[Dict]:
        """Read emails from Microsoft 365"""
        try:
            # Build filter query if provided
            filter_query = f"search('{query}')" if query else None
            
            # Get messages
            messages = await self.client.me.mail_folders[folder].messages.get(
                params={
                    "$top": limit,
                    "$orderby": "receivedDateTime desc",
                    "$filter": filter_query
                }
            )
            
            return [{
                "id": msg.id,
                "subject": msg.subject,
                "from": msg.from_.email_address.address,
                "received": msg.received_date_time,
                "body": msg.body.content,
                "is_read": msg.is_read
            } for msg in messages.value]
        except Exception as e:
            raise Exception(f"Error reading Microsoft emails: {str(e)}")

    async def _read_google_emails(
        self,
        folder: str,
        limit: int,
        query: Optional[str]
    ) -> List[Dict]:
        """Read emails from Gmail"""
        try:
            # Build query string
            q = f"in:{folder}"
            if query:
                q += f" {query}"
            
            # Get message list
            messages = self.client.users().messages().list(
                userId='me',
                q=q,
                maxResults=limit
            ).execute()
            
            emails = []
            for msg in messages.get('messages', []):
                # Get full message details
                email = self.client.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='full'
                ).execute()
                
                # Extract headers
                headers = email['payload']['headers']
                subject = next(h['value'] for h in headers if h['name'] == 'Subject')
                from_email = next(h['value'] for h in headers if h['name'] == 'From')
                
                # Get body
                if 'parts' in email['payload']:
                    body = base64.urlsafe_b64decode(
                        email['payload']['parts'][0]['body']['data']
                    ).decode()
                else:
                    body = base64.urlsafe_b64decode(
                        email['payload']['body']['data']
                    ).decode()
                
                emails.append({
                    "id": email['id'],
                    "subject": subject,
                    "from": from_email,
                    "received": datetime.fromtimestamp(
                        int(email['internalDate'])/1000
                    ).isoformat(),
                    "body": body,
                    "is_read": 'UNREAD' not in email['labelIds']
                })
            
            return emails
        except Exception as e:
            raise Exception(f"Error reading Gmail emails: {str(e)}")

    async def _send_microsoft_email(
        self,
        to: List[str],
        subject: str,
        body: str,
        cc: Optional[List[str]],
        bcc: Optional[List[str]]
    ) -> Dict:
        """Send email through Microsoft 365"""
        try:
            message = {
                "subject": subject,
                "body": {
                    "contentType": "HTML",
                    "content": body
                },
                "toRecipients": [
                    {"emailAddress": {"address": email}} for email in to
                ]
            }
            
            if cc:
                message["ccRecipients"] = [
                    {"emailAddress": {"address": email}} for email in cc
                ]
            
            if bcc:
                message["bccRecipients"] = [
                    {"emailAddress": {"address": email}} for email in bcc
                ]
            
            response = await self.client.me.send_mail.post(
                body={"message": message}
            )
            
            return {"status": "sent", "message_id": response.id}
        except Exception as e:
            raise Exception(f"Error sending Microsoft email: {str(e)}")

    async def _send_google_email(
        self,
        to: List[str],
        subject: str,
        body: str,
        cc: Optional[List[str]],
        bcc: Optional[List[str]]
    ) -> Dict:
        """Send email through Gmail"""
        try:
            message = MIMEMultipart()
            message['to'] = ', '.join(to)
            message['subject'] = subject
            
            if cc:
                message['cc'] = ', '.join(cc)
            if bcc:
                message['bcc'] = ', '.join(bcc)
            
            message.attach(MIMEText(body, 'html'))
            
            # Encode the message
            raw = base64.urlsafe_b64encode(
                message.as_bytes()
            ).decode()
            
            # Send the email
            sent_message = self.client.users().messages().send(
                userId='me',
                body={'raw': raw}
            ).execute()
            
            return {
                "status": "sent",
                "message_id": sent_message['id']
            }
        except Exception as e:
            raise Exception(f"Error sending Gmail email: {str(e)}")
