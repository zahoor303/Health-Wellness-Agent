"""
Streaming utilities for real-time responses
"""
import asyncio
from typing import Dict, Any, AsyncIterator
from datetime import datetime

class StreamingResponse:
    """Simple streaming response utility"""
    
    def __init__(self):
        self.is_streaming = False
    
    async def stream_text(self, text: str, chunk_size: int = 50, delay: float = 0.05) -> AsyncIterator[str]:
        """Stream text in chunks"""
        self.is_streaming = True
        
        try:
            for i in range(0, len(text), chunk_size):
                chunk = text[i:i + chunk_size]
                yield chunk
                await asyncio.sleep(delay)
        finally:
            self.is_streaming = False
    
    async def stream_response(self, data: Dict[str, Any], delay: float = 0.1) -> AsyncIterator[Dict[str, Any]]:
        """Stream response data"""
        self.is_streaming = True
        
        try:
            # Processing stage
            yield {
                "type": "processing",
                "message": "Processing your request...",
                "timestamp": datetime.now().isoformat()
            }
            
            await asyncio.sleep(delay)
            
            # Response stage
            yield {
                "type": "response",
                "data": data,
                "timestamp": datetime.now().isoformat()
            }
            
        finally:
            self.is_streaming = False

# Global streaming manager
streaming_manager = StreamingResponse()