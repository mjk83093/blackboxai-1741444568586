from typing import Dict, List, Optional
from fastapi import HTTPException
from microsoft.graph import GraphServiceClient
from googleapiclient.discovery import build
from datetime import datetime, timedelta

class TaskService:
    def __init__(self, platform: str, credentials: Dict):
        """Initialize task service for specified platform"""
        self.platform = platform
        self.credentials = credentials
        self._init_client()

    def _init_client(self):
        """Initialize appropriate client based on platform"""
        try:
            if self.platform == "microsoft":
                self.client = GraphServiceClient(self.credentials)
                self.calendar_client = self.client  # Same client for Microsoft
            elif self.platform == "google":
                self.client = build('tasks', 'v1', credentials=self.credentials)
                self.calendar_client = build('calendar', 'v3', credentials=self.credentials)
            else:
                raise ValueError(f"Unsupported platform: {self.platform}")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize {self.platform} client: {str(e)}"
            )

    async def create_task(
        self,
        title: str,
        description: Optional[str] = None,
        due_date: Optional[str] = None,
        list_id: Optional[str] = None
    ) -> Dict:
        """Create a new task"""
        try:
            if self.platform == "microsoft":
                return await self._create_microsoft_task(title, description, due_date, list_id)
            elif self.platform == "google":
                return await self._create_google_task(title, description, due_date, list_id)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create task: {str(e)}"
            )

    async def get_tasks(
        self,
        list_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Dict]:
        """Get tasks from specified list"""
        try:
            if self.platform == "microsoft":
                return await self._get_microsoft_tasks(list_id, status)
            elif self.platform == "google":
                return await self._get_google_tasks(list_id, status)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get tasks: {str(e)}"
            )

    async def create_event(
        self,
        title: str,
        start_time: str,
        end_time: str,
        description: Optional[str] = None,
        attendees: Optional[List[str]] = None,
        location: Optional[str] = None
    ) -> Dict:
        """Create a calendar event"""
        try:
            if self.platform == "microsoft":
                return await self._create_microsoft_event(
                    title, start_time, end_time, description, attendees, location
                )
            elif self.platform == "google":
                return await self._create_google_event(
                    title, start_time, end_time, description, attendees, location
                )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create event: {str(e)}"
            )

    async def _create_microsoft_task(
        self,
        title: str,
        description: Optional[str],
        due_date: Optional[str],
        list_id: Optional[str]
    ) -> Dict:
        """Create task in Microsoft To-Do"""
        try:
            task_data = {
                "title": title,
                "importance": "normal",
                "status": "notStarted"
            }
            
            if description:
                task_data["body"] = {
                    "content": description,
                    "contentType": "text"
                }
            
            if due_date:
                task_data["dueDateTime"] = {
                    "dateTime": due_date,
                    "timeZone": "UTC"
                }
            
            # Use default list if not specified
            if not list_id:
                lists = await self.client.me.todo.lists.get()
                list_id = lists.value[0].id
            
            response = await self.client.me.todo.lists[list_id].tasks.post(
                body=task_data
            )
            
            return {
                "id": response.id,
                "title": response.title,
                "status": response.status,
                "due_date": response.due_date_time.date_time if response.due_date_time else None
            }
        except Exception as e:
            raise Exception(f"Error creating Microsoft task: {str(e)}")

    async def _create_google_task(
        self,
        title: str,
        description: Optional[str],
        due_date: Optional[str],
        list_id: Optional[str]
    ) -> Dict:
        """Create task in Google Tasks"""
        try:
            task_data = {
                "title": title,
                "status": "needsAction"
            }
            
            if description:
                task_data["notes"] = description
            
            if due_date:
                task_data["due"] = due_date
            
            # Use default list if not specified
            if not list_id:
                lists = self.client.tasklists().list().execute()
                list_id = lists['items'][0]['id']
            
            response = self.client.tasks().insert(
                tasklist=list_id,
                body=task_data
            ).execute()
            
            return {
                "id": response['id'],
                "title": response['title'],
                "status": response['status'],
                "due_date": response.get('due')
            }
        except Exception as e:
            raise Exception(f"Error creating Google task: {str(e)}")

    async def _get_microsoft_tasks(
        self,
        list_id: Optional[str],
        status: Optional[str]
    ) -> List[Dict]:
        """Get tasks from Microsoft To-Do"""
        try:
            # Use default list if not specified
            if not list_id:
                lists = await self.client.me.todo.lists.get()
                list_id = lists.value[0].id
            
            # Build filter query
            filter_query = None
            if status:
                filter_query = f"status eq '{status}'"
            
            tasks = await self.client.me.todo.lists[list_id].tasks.get(
                params={"$filter": filter_query} if filter_query else None
            )
            
            return [{
                "id": task.id,
                "title": task.title,
                "status": task.status,
                "due_date": task.due_date_time.date_time if task.due_date_time else None,
                "importance": task.importance
            } for task in tasks.value]
        except Exception as e:
            raise Exception(f"Error getting Microsoft tasks: {str(e)}")

    async def _get_google_tasks(
        self,
        list_id: Optional[str],
        status: Optional[str]
    ) -> List[Dict]:
        """Get tasks from Google Tasks"""
        try:
            # Use default list if not specified
            if not list_id:
                lists = self.client.tasklists().list().execute()
                list_id = lists['items'][0]['id']
            
            # Get tasks
            tasks = self.client.tasks().list(
                tasklist=list_id,
                showCompleted=True
            ).execute()
            
            # Filter by status if specified
            task_list = tasks.get('items', [])
            if status:
                task_list = [
                    task for task in task_list
                    if task['status'].lower() == status.lower()
                ]
            
            return [{
                "id": task['id'],
                "title": task['title'],
                "status": task['status'],
                "due_date": task.get('due'),
                "notes": task.get('notes')
            } for task in task_list]
        except Exception as e:
            raise Exception(f"Error getting Google tasks: {str(e)}")

    async def _create_microsoft_event(
        self,
        title: str,
        start_time: str,
        end_time: str,
        description: Optional[str],
        attendees: Optional[List[str]],
        location: Optional[str]
    ) -> Dict:
        """Create event in Microsoft Calendar"""
        try:
            event_data = {
                "subject": title,
                "start": {
                    "dateTime": start_time,
                    "timeZone": "UTC"
                },
                "end": {
                    "dateTime": end_time,
                    "timeZone": "UTC"
                }
            }
            
            if description:
                event_data["body"] = {
                    "contentType": "HTML",
                    "content": description
                }
            
            if location:
                event_data["location"] = {
                    "displayName": location
                }
            
            if attendees:
                event_data["attendees"] = [
                    {
                        "emailAddress": {
                            "address": email
                        },
                        "type": "required"
                    } for email in attendees
                ]
            
            response = await self.calendar_client.me.events.post(
                body=event_data
            )
            
            return {
                "id": response.id,
                "title": response.subject,
                "start_time": response.start.date_time,
                "end_time": response.end.date_time,
                "web_link": response.web_link
            }
        except Exception as e:
            raise Exception(f"Error creating Microsoft event: {str(e)}")

    async def _create_google_event(
        self,
        title: str,
        start_time: str,
        end_time: str,
        description: Optional[str],
        attendees: Optional[List[str]],
        location: Optional[str]
    ) -> Dict:
        """Create event in Google Calendar"""
        try:
            event_data = {
                'summary': title,
                'start': {
                    'dateTime': start_time,
                    'timeZone': 'UTC'
                },
                'end': {
                    'dateTime': end_time,
                    'timeZone': 'UTC'
                }
            }
            
            if description:
                event_data['description'] = description
            
            if location:
                event_data['location'] = location
            
            if attendees:
                event_data['attendees'] = [
                    {'email': email} for email in attendees
                ]
            
            response = self.calendar_client.events().insert(
                calendarId='primary',
                body=event_data,
                sendUpdates='all'
            ).execute()
            
            return {
                "id": response['id'],
                "title": response['summary'],
                "start_time": response['start']['dateTime'],
                "end_time": response['end']['dateTime'],
                "html_link": response['htmlLink']
            }
        except Exception as e:
            raise Exception(f"Error creating Google event: {str(e)}")
