from typing import Dict, List, Optional, BinaryIO
import base64
from datetime import datetime
from fastapi import HTTPException
import httpx
from microsoft.graph import GraphServiceClient
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

class DocumentService:
    def __init__(self, platform: str, credentials: Dict):
        """Initialize document service for specified platform"""
        self.platform = platform
        self.credentials = credentials
        self._init_client()

    def _init_client(self):
        """Initialize appropriate client based on platform"""
        try:
            if self.platform == "microsoft":
                self.client = GraphServiceClient(self.credentials)
            elif self.platform == "google":
                self.client = build('drive', 'v3', credentials=self.credentials)
            else:
                raise ValueError(f"Unsupported platform: {self.platform}")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize {self.platform} client: {str(e)}"
            )

    async def read_document(self, document_id: str) -> Dict:
        """Read document content from specified platform"""
        try:
            if self.platform == "microsoft":
                return await self._read_microsoft_document(document_id)
            elif self.platform == "google":
                return await self._read_google_document(document_id)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to read document: {str(e)}"
            )

    async def create_document(
        self,
        name: str,
        content: str,
        folder_id: Optional[str] = None
    ) -> Dict:
        """Create new document on specified platform"""
        try:
            if self.platform == "microsoft":
                return await self._create_microsoft_document(name, content, folder_id)
            elif self.platform == "google":
                return await self._create_google_document(name, content, folder_id)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create document: {str(e)}"
            )

    async def update_document(
        self,
        document_id: str,
        content: str
    ) -> Dict:
        """Update existing document on specified platform"""
        try:
            if self.platform == "microsoft":
                return await self._update_microsoft_document(document_id, content)
            elif self.platform == "google":
                return await self._update_google_document(document_id, content)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to update document: {str(e)}"
            )

    async def _read_microsoft_document(self, document_id: str) -> Dict:
        """Read document from Microsoft 365"""
        try:
            # Get the document content
            response = await self.client.drive.items[document_id].content.get()
            
            # Get document metadata
            metadata = await self.client.drive.items[document_id].get()
            
            return {
                "id": document_id,
                "name": metadata.name,
                "content": response.text(),
                "last_modified": metadata.last_modified_date_time,
                "created": metadata.created_date_time,
                "web_url": metadata.web_url
            }
        except Exception as e:
            raise Exception(f"Error reading Microsoft document: {str(e)}")

    async def _read_google_document(self, document_id: str) -> Dict:
        """Read document from Google Drive"""
        try:
            # Get document metadata
            file = self.client.files().get(fileId=document_id).execute()
            
            # Get document content
            content = self.client.files().export(
                fileId=document_id,
                mimeType='text/plain'
            ).execute()
            
            return {
                "id": document_id,
                "name": file['name'],
                "content": content.decode('utf-8'),
                "last_modified": file['modifiedTime'],
                "created": file['createdTime'],
                "web_url": file['webViewLink']
            }
        except Exception as e:
            raise Exception(f"Error reading Google document: {str(e)}")

    async def _create_microsoft_document(
        self,
        name: str,
        content: str,
        folder_id: Optional[str]
    ) -> Dict:
        """Create document in Microsoft 365"""
        try:
            document_data = {
                "name": name,
                "@microsoft.graph.conflictBehavior": "rename"
            }
            
            if folder_id:
                path = f"/drive/items/{folder_id}/children"
            else:
                path = "/drive/root/children"
            
            # Create empty document
            response = await self.client.post(
                path,
                json=document_data
            )
            
            # Update document content
            await self._update_microsoft_document(response['id'], content)
            
            return {
                "id": response['id'],
                "name": response['name'],
                "web_url": response['webUrl']
            }
        except Exception as e:
            raise Exception(f"Error creating Microsoft document: {str(e)}")

    async def _create_google_document(
        self,
        name: str,
        content: str,
        folder_id: Optional[str]
    ) -> Dict:
        """Create document in Google Drive"""
        try:
            file_metadata = {
                'name': name,
                'mimeType': 'application/vnd.google-apps.document'
            }
            
            if folder_id:
                file_metadata['parents'] = [folder_id]
            
            # Create document
            file = self.client.files().create(
                body=file_metadata,
                media_body=MediaIoBaseUpload(
                    io.BytesIO(content.encode()),
                    mimetype='text/plain'
                )
            ).execute()
            
            return {
                "id": file['id'],
                "name": file['name'],
                "web_url": file['webViewLink']
            }
        except Exception as e:
            raise Exception(f"Error creating Google document: {str(e)}")

    async def _update_microsoft_document(
        self,
        document_id: str,
        content: str
    ) -> Dict:
        """Update document in Microsoft 365"""
        try:
            # Update content
            await self.client.drive.items[document_id].content.put(
                content=content.encode()
            )
            
            # Get updated metadata
            metadata = await self.client.drive.items[document_id].get()
            
            return {
                "id": document_id,
                "name": metadata.name,
                "web_url": metadata.web_url,
                "last_modified": metadata.last_modified_date_time
            }
        except Exception as e:
            raise Exception(f"Error updating Microsoft document: {str(e)}")

    async def _update_google_document(
        self,
        document_id: str,
        content: str
    ) -> Dict:
        """Update document in Google Drive"""
        try:
            # Update content
            self.client.files().update(
                fileId=document_id,
                media_body=MediaIoBaseUpload(
                    io.BytesIO(content.encode()),
                    mimetype='text/plain'
                )
            ).execute()
            
            # Get updated metadata
            file = self.client.files().get(fileId=document_id).execute()
            
            return {
                "id": document_id,
                "name": file['name'],
                "web_url": file['webViewLink'],
                "last_modified": file['modifiedTime']
            }
        except Exception as e:
            raise Exception(f"Error updating Google document: {str(e)}")
