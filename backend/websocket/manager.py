"""
WebSocket connection manager for handling real-time connections
Manages multiple sessions with multiple connections per session
"""
from typing import Dict, List
from fastapi import WebSocket
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    Manages WebSocket connections for real-time features
    
    Supports:
    - Multiple sessions (e.g., different trivia games)
    - Multiple connections per session (multiple participants)
    - Broadcasting messages to all connections in a session
    """
    
    def __init__(self):
        # Maps session_id -> list of active WebSocket connections
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        """
        Accept a new WebSocket connection and add it to a session
        
        Args:
            websocket: The WebSocket connection to accept
            session_id: The session/room ID to join
        """
        await websocket.accept()
        
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        
        self.active_connections[session_id].append(websocket)
        logger.info(f"Client connected to session {session_id}. Total connections: {len(self.active_connections[session_id])}")
    
    def disconnect(self, websocket: WebSocket, session_id: str):
        """
        Remove a WebSocket connection from a session
        
        Args:
            websocket: The WebSocket connection to remove
            session_id: The session ID to remove from
        """
        if session_id in self.active_connections:
            if websocket in self.active_connections[session_id]:
                self.active_connections[session_id].remove(websocket)
                logger.info(f"Client disconnected from session {session_id}. Remaining connections: {len(self.active_connections[session_id])}")
                
                # Clean up empty session
                if not self.active_connections[session_id]:
                    del self.active_connections[session_id]
                    logger.info(f"Session {session_id} removed (no active connections)")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """
        Send a message to a specific WebSocket connection
        
        Args:
            message: The message to send (will be JSON serialized)
            websocket: The target WebSocket connection
        """
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
    
    async def broadcast_to_session(self, session_id: str, message: dict):
        """
        Broadcast a message to all connections in a session
        
        Args:
            session_id: The session ID to broadcast to
            message: The message to send (will be JSON serialized)
        """
        if session_id not in self.active_connections:
            logger.warning(f"Attempted to broadcast to non-existent session: {session_id}")
            return
        
        # Send to all connections, removing any that fail
        disconnected = []
        for connection in self.active_connections[session_id]:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to connection in session {session_id}: {e}")
                disconnected.append(connection)
        
        # Clean up failed connections
        for connection in disconnected:
            self.disconnect(connection, session_id)
    
    def get_session_connection_count(self, session_id: str) -> int:
        """
        Get the number of active connections in a session
        
        Args:
            session_id: The session ID to check
            
        Returns:
            Number of active connections (0 if session doesn't exist)
        """
        return len(self.active_connections.get(session_id, []))


# Global connection manager instance
manager = ConnectionManager()
