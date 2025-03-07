from typing import Dict, List, Optional, Any
from pydantic import BaseModel
from datetime import datetime
import openai
from config import settings

class Context(BaseModel):
    """Context model for maintaining conversation state and user preferences"""
    user_id: str
    platform: str  # 'microsoft' or 'google'
    conversation_history: List[Dict[str, str]] = []
    current_task: Optional[Dict[str, Any]] = None
    last_interaction: datetime = datetime.now()
    preferences: Dict[str, Any] = {}

class ModelContextProtocol:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.contexts: Dict[str, Context] = {}

    def create_context(self, user_id: str, platform: str) -> Context:
        """Create a new context for a user"""
        context = Context(user_id=user_id, platform=platform)
        self.contexts[user_id] = context
        return context

    def get_context(self, user_id: str) -> Optional[Context]:
        """Retrieve existing context for a user"""
        return self.contexts.get(user_id)

    async def process_request(
        self,
        user_id: str,
        request: str,
        platform: str,
        additional_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process user request with context awareness"""
        # Get or create context
        context = self.get_context(user_id) or self.create_context(user_id, platform)
        
        # Update context with new information
        if additional_context:
            context.preferences.update(additional_context)
        
        # Prepare conversation history
        messages = [
            {"role": "system", "content": self._get_system_prompt(context)},
            *context.conversation_history,
            {"role": "user", "content": request}
        ]
        
        try:
            # Get AI response
            response = await self._get_ai_response(messages)
            
            # Update conversation history
            context.conversation_history.append({"role": "user", "content": request})
            context.conversation_history.append({"role": "assistant", "content": response})
            
            # Trim conversation history if too long
            if len(context.conversation_history) > 10:
                context.conversation_history = context.conversation_history[-10:]
            
            # Update last interaction time
            context.last_interaction = datetime.now()
            
            return {
                "response": response,
                "context": context.dict()
            }
        except Exception as e:
            return {
                "error": str(e),
                "context": context.dict()
            }

    def _get_system_prompt(self, context: Context) -> str:
        """Generate system prompt based on context"""
        platform_specific = {
            "microsoft": "You are an AI assistant integrated with Microsoft 365.",
            "google": "You are an AI assistant integrated with Google Workspace."
        }
        
        base_prompt = f"""
        {platform_specific[context.platform]}
        You help users with document processing, email automation, and task management.
        
        User Preferences:
        {context.preferences}
        
        Current Task:
        {context.current_task}
        
        Please provide clear, concise responses and always maintain context of the conversation.
        """
        
        return base_prompt.strip()

    async def _get_ai_response(self, messages: List[Dict[str, str]]) -> str:
        """Get response from OpenAI API"""
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Failed to get AI response: {str(e)}")

    def update_task(self, user_id: str, task: Dict[str, Any]) -> None:
        """Update current task in context"""
        if context := self.get_context(user_id):
            context.current_task = task

    def clear_context(self, user_id: str) -> None:
        """Clear context for a user"""
        if user_id in self.contexts:
            del self.contexts[user_id]
