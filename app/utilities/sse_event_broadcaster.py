"""
SSE Event Broadcaster

Server-Sent Events broadcaster for real-time updates.
"""

import asyncio
from typing import Dict, Set, Any, Optional
from uuid import UUID
import json

from app.telemetries.logger import logger


class SSEEventBroadcaster:
    """
    Manages Server-Sent Events broadcasting
    """
    
    def __init__(self):
        """Initialize broadcaster"""
        self.clients: Dict[str, Set[asyncio.Queue]] = {}
        logger.info("SSEEventBroadcaster initialized")
    
    def subscribe(self, channel: str) -> asyncio.Queue:
        """
        Subscribe to a channel
        
        Args:
            channel: Channel name
            
        Returns:
            Queue for receiving events
        """
        queue = asyncio.Queue()
        
        if channel not in self.clients:
            self.clients[channel] = set()
        
        self.clients[channel].add(queue)
        logger.info(f"Client subscribed to channel: {channel}")
        
        return queue
    
    def unsubscribe(self, channel: str, queue: asyncio.Queue) -> None:
        """
        Unsubscribe from a channel
        
        Args:
            channel: Channel name
            queue: Queue to remove
        """
        if channel in self.clients:
            self.clients[channel].discard(queue)
            
            # Clean up empty channels
            if not self.clients[channel]:
                del self.clients[channel]
            
            logger.info(f"Client unsubscribed from channel: {channel}")
    
    async def broadcast(self, channel: str, event: Dict[str, Any]) -> int:
        """
        Broadcast event to all subscribers of a channel
        
        Args:
            channel: Channel name
            event: Event data
            
        Returns:
            Number of clients that received the event
        """
        if channel not in self.clients:
            logger.debug(f"No clients subscribed to channel: {channel}")
            return 0
        
        event_data = json.dumps(event)
        sent_count = 0
        dead_queues = set()
        
        for queue in self.clients[channel]:
            try:
                await queue.put(event_data)
                sent_count += 1
            except Exception as e:
                logger.warning(f"Failed to send to queue: {e}")
                dead_queues.add(queue)
        
        # Clean up dead queues
        for queue in dead_queues:
            self.clients[channel].discard(queue)
        
        logger.debug(f"Broadcast event to {sent_count} clients on channel: {channel}")
        
        return sent_count
    
    async def broadcast_to_all(self, event: Dict[str, Any]) -> int:
        """
        Broadcast event to all channels
        
        Args:
            event: Event data
            
        Returns:
            Total number of clients that received the event
        """
        total_sent = 0
        
        for channel in list(self.clients.keys()):
            sent = await self.broadcast(channel, event)
            total_sent += sent
        
        logger.info(f"Broadcast event to {total_sent} clients across all channels")
        
        return total_sent
    
    def get_subscriber_count(self, channel: Optional[str] = None) -> int:
        """
        Get subscriber count
        
        Args:
            channel: Specific channel or None for total
            
        Returns:
            Number of subscribers
        """
        if channel:
            return len(self.clients.get(channel, set()))
        
        return sum(len(queues) for queues in self.clients.values())
    
    def get_channels(self) -> list[str]:
        """
        Get list of active channels
        
        Returns:
            List of channel names
        """
        return list(self.clients.keys())


# Global broadcaster instance
_broadcaster: Optional[SSEEventBroadcaster] = None


def get_broadcaster() -> SSEEventBroadcaster:
    """
    Get global broadcaster instance
    
    Returns:
        SSEEventBroadcaster instance
    """
    global _broadcaster
    
    if _broadcaster is None:
        _broadcaster = SSEEventBroadcaster()
    
    return _broadcaster
