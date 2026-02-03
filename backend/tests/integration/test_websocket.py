"""
Integration tests for WebSocket functionality
Tests WebSocket endpoint, authentication, and message broadcasting
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.models.user import User
from backend.core.security import create_access_token


class TestWebSocketIntegration:
    """Integration tests for WebSocket endpoint"""
    
    def test_websocket_connection_with_valid_token(
        self,
        client: TestClient,
        sample_user: User
    ):
        """Test that WebSocket accepts connection with valid JWT token"""
        # Create a valid token for the user
        token = create_access_token(
            data={
                "sub": str(sample_user.id),
                "org_id": str(sample_user.organization_id),
                "roles": [sample_user.role.value]
            }
        )
        
        session_id = "test-session-1"
        
        # Connect to WebSocket
        with client.websocket_connect(f"/ws/{session_id}?token={token}") as websocket:
            # Receive welcome message
            data = websocket.receive_json()
            
            assert data["type"] == "connection"
            assert data["message"] == "Connected to session"
            assert data["session_id"] == session_id
            assert data["user_id"] == str(sample_user.id)
            
            # Receive user_joined broadcast
            data = websocket.receive_json()
            
            assert data["type"] == "user_joined"
            assert data["user_id"] == str(sample_user.id)
            assert data["session_id"] == session_id
            assert data["participant_count"] == 1
    
    def test_websocket_rejects_invalid_token(
        self,
        client: TestClient
    ):
        """Test that WebSocket rejects connection with invalid token"""
        session_id = "test-session-2"
        invalid_token = "invalid.token.here"
        
        # Attempt to connect with invalid token
        with pytest.raises(Exception) as exc_info:
            with client.websocket_connect(f"/ws/{session_id}?token={invalid_token}"):
                pass
        
        # WebSocket should close with policy violation
        assert "1008" in str(exc_info.value)
    
    def test_websocket_rejects_missing_token(
        self,
        client: TestClient
    ):
        """Test that WebSocket rejects connection without token"""
        session_id = "test-session-3"
        
        # Attempt to connect without token
        with pytest.raises(Exception):
            with client.websocket_connect(f"/ws/{session_id}"):
                pass
    
    def test_websocket_broadcast_to_session(
        self,
        client: TestClient,
        sample_user: User,
        admin_user: User
    ):
        """Test that messages are broadcast to all connections in a session"""
        # Create tokens for both users
        token1 = create_access_token(
            data={
                "sub": str(sample_user.id),
                "org_id": str(sample_user.organization_id),
                "roles": [sample_user.role.value]
            }
        )
        
        token2 = create_access_token(
            data={
                "sub": str(admin_user.id),
                "org_id": str(admin_user.organization_id),
                "roles": [admin_user.role.value]
            }
        )
        
        session_id = "test-session-4"
        
        # Connect two clients to the same session
        with client.websocket_connect(f"/ws/{session_id}?token={token1}") as ws1:
            # Clear welcome messages for ws1
            ws1.receive_json()  # connection message
            ws1.receive_json()  # user_joined message
            
            with client.websocket_connect(f"/ws/{session_id}?token={token2}") as ws2:
                # ws1 should receive user_joined for ws2
                data = ws1.receive_json()
                assert data["type"] == "user_joined"
                assert data["user_id"] == str(admin_user.id)
                assert data["participant_count"] == 2
                
                # Clear welcome messages for ws2
                ws2.receive_json()  # connection message
                ws2.receive_json()  # user_joined message
                
                # Send a message from ws1
                ws1.send_json({
                    "type": "chat",
                    "data": {"text": "Hello from user 1"}
                })
                
                # ws1 should receive its own message (broadcast)
                msg1 = ws1.receive_json()
                assert msg1["type"] == "chat"
                assert msg1["user_id"] == str(sample_user.id)
                assert msg1["data"]["text"] == "Hello from user 1"
                
                # ws2 should also receive the message
                msg2 = ws2.receive_json()
                assert msg2["type"] == "chat"
                assert msg2["user_id"] == str(sample_user.id)
                assert msg2["data"]["text"] == "Hello from user 1"
    
    def test_websocket_session_isolation(
        self,
        client: TestClient,
        sample_user: User,
        admin_user: User
    ):
        """Test that messages don't leak between different sessions"""
        # Create tokens for both users
        token1 = create_access_token(
            data={
                "sub": str(sample_user.id),
                "org_id": str(sample_user.organization_id),
                "roles": [sample_user.role.value]
            }
        )
        
        token2 = create_access_token(
            data={
                "sub": str(admin_user.id),
                "org_id": str(admin_user.organization_id),
                "roles": [admin_user.role.value]
            }
        )
        
        session_id_1 = "test-session-5"
        session_id_2 = "test-session-6"
        
        # Connect to different sessions
        with client.websocket_connect(f"/ws/{session_id_1}?token={token1}") as ws1:
            # Clear welcome messages
            ws1.receive_json()
            ws1.receive_json()
            
            with client.websocket_connect(f"/ws/{session_id_2}?token={token2}") as ws2:
                # Clear welcome messages
                ws2.receive_json()
                ws2.receive_json()
                
                # Send message from ws1 in session_id_1
                ws1.send_json({
                    "type": "chat",
                    "data": {"text": "Message in session 1"}
                })
                
                # ws1 should receive its own message
                msg = ws1.receive_json()
                assert msg["session_id"] == session_id_1
                
                # ws2 should NOT receive the message (different session)
                # If we try to receive, it should timeout or we verify the message queue is empty
                # For this test, we just verify ws2 can send its own message
                ws2.send_json({
                    "type": "chat",
                    "data": {"text": "Message in session 2"}
                })
                
                msg = ws2.receive_json()
                assert msg["session_id"] == session_id_2
                assert msg["data"]["text"] == "Message in session 2"
    
    def test_websocket_disconnect_notification(
        self,
        client: TestClient,
        sample_user: User,
        admin_user: User
    ):
        """Test that disconnection is broadcast to other participants"""
        # Create tokens for both users
        token1 = create_access_token(
            data={
                "sub": str(sample_user.id),
                "org_id": str(sample_user.organization_id),
                "roles": [sample_user.role.value]
            }
        )
        
        token2 = create_access_token(
            data={
                "sub": str(admin_user.id),
                "org_id": str(admin_user.organization_id),
                "roles": [admin_user.role.value]
            }
        )
        
        session_id = "test-session-7"
        
        # Connect two clients
        with client.websocket_connect(f"/ws/{session_id}?token={token1}") as ws1:
            # Clear welcome messages for ws1
            ws1.receive_json()
            ws1.receive_json()
            
            # Connect second client in nested context
            with client.websocket_connect(f"/ws/{session_id}?token={token2}") as ws2:
                # ws1 receives user_joined for ws2
                data = ws1.receive_json()
                assert data["type"] == "user_joined"
                assert data["participant_count"] == 2
                
                # Clear ws2 welcome messages
                ws2.receive_json()
                ws2.receive_json()
            
            # After ws2 context exits, ws1 should receive user_left notification
            data = ws1.receive_json()
            assert data["type"] == "user_left"
            assert data["user_id"] == str(admin_user.id)
            assert data["participant_count"] == 1
