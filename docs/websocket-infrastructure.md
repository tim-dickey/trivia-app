# WebSocket Infrastructure Documentation

## Overview

The trivia app includes WebSocket infrastructure for real-time features such as:
- Live scoring updates
- Real-time participant tracking
- Session state synchronization
- Chat messages
- Participant join/leave notifications

## Architecture

### Backend Components

#### Connection Manager (`backend/websocket/manager.py`)
The `ConnectionManager` class handles all WebSocket connections:
- Maintains active connections organized by session ID
- Provides connection lifecycle management (connect/disconnect)
- Broadcasts messages to all participants in a session
- Automatically cleans up disconnected clients

#### WebSocket Endpoint (`backend/main.py`)
The `/ws/{session_id}` endpoint provides:
- JWT-based authentication via query parameter
- Automatic connection acceptance
- Message routing and broadcasting
- Error handling and graceful disconnection

### Frontend Component

#### WebSocket Service (`frontend/src/services/websocket.ts`)
The `WebSocketService` class provides:
- Connection management with automatic reconnection
- Type-safe message handling
- Event subscription system
- Graceful error handling

## Usage Examples

### Backend: Broadcasting Messages

```python
from backend.websocket.manager import manager

# Broadcast to all participants in a session
await manager.broadcast_to_session(
    session_id="trivia-session-123",
    message={
        "type": "score_update",
        "data": {
            "team": "Team A",
            "score": 150
        }
    }
)
```

### Frontend: Connecting to WebSocket

```typescript
import { websocketService } from '@/services/websocket';

// Connect to a session
const token = 'your-jwt-token';
const sessionId = 'trivia-session-123';

websocketService.connect(sessionId, token);

// Subscribe to score updates
const unsubscribe = websocketService.on('score_update', (message) => {
  console.log('Score updated:', message.data);
});

// Send a message
websocketService.send('chat', { text: 'Hello everyone!' });

// Clean up
unsubscribe();
websocketService.disconnect();
```

### React Hook Example

```typescript
import { useEffect } from 'react';
import { websocketService } from '@/services/websocket';

function useWebSocket(sessionId: string, token: string) {
  useEffect(() => {
    websocketService.connect(sessionId, token);
    
    return () => {
      websocketService.disconnect();
    };
  }, [sessionId, token]);
}

function TriviaSession({ sessionId, token }) {
  useWebSocket(sessionId, token);
  
  useEffect(() => {
    const unsubscribe = websocketService.on('user_joined', (message) => {
      console.log('User joined:', message.user_id);
    });
    
    return unsubscribe;
  }, []);
  
  // Component code...
}
```

## Message Types

### System Messages (Backend → Frontend)

#### `connection`
Sent when a client successfully connects.
```json
{
  "type": "connection",
  "message": "Connected to session",
  "session_id": "session-123",
  "user_id": "user-456"
}
```

#### `user_joined`
Broadcast when a new participant joins the session.
```json
{
  "type": "user_joined",
  "user_id": "user-456",
  "session_id": "session-123",
  "participant_count": 5
}
```

#### `user_left`
Broadcast when a participant disconnects.
```json
{
  "type": "user_left",
  "user_id": "user-456",
  "session_id": "session-123",
  "participant_count": 4
}
```

### Application Messages (Bidirectional)

#### `chat`
Chat messages between participants.
```json
{
  "type": "chat",
  "user_id": "user-456",
  "data": {
    "text": "Great answer!"
  }
}
```

#### `score_update`
Live scoring updates.
```json
{
  "type": "score_update",
  "data": {
    "team": "Team A",
    "score": 150,
    "question_id": "q-789"
  }
}
```

#### `session_update`
Session state changes (question transitions, timer updates, etc.).
```json
{
  "type": "session_update",
  "data": {
    "state": "question_active",
    "question_number": 5,
    "time_remaining": 30
  }
}
```

## Authentication

WebSocket connections require JWT authentication:

1. Client obtains JWT token via `/api/v1/auth/login`
2. Client connects to WebSocket with token as query parameter:
   ```
   ws://localhost:8000/ws/{session_id}?token={jwt_token}
   ```
3. Server validates token and extracts user/organization information
4. Connection is accepted or rejected based on authentication

### Security Considerations

- Tokens are validated on every connection
- Invalid/expired tokens result in immediate connection rejection (1008 Policy Violation)
- Organization ID is extracted from token for multi-tenant isolation
- WebSocket messages are not persisted (ephemeral communication only)

## Connection Lifecycle

### Connection Flow
1. Client initiates WebSocket connection with JWT token
2. Server validates authentication
3. Server accepts connection and adds to session
4. Welcome message sent to client
5. Join notification broadcast to all session participants

### Disconnection Flow
1. Client disconnects (intentional or network issue)
2. Server detects disconnection
3. Connection removed from session
4. Leave notification broadcast to remaining participants
5. Empty sessions are automatically cleaned up

### Reconnection
The frontend WebSocket service includes automatic reconnection:
- Exponential backoff (1s, 2s, 4s, 8s, 16s, 30s max)
- Maximum 5 reconnection attempts
- Configurable via `maxReconnectAttempts` and `reconnectDelay`

## Testing

### Integration Tests
Comprehensive integration tests are located in `backend/tests/integration/test_websocket.py`:

```bash
# Run WebSocket tests
cd backend
export DATABASE_URL="sqlite:///./test_trivia.db"
python3 -m pytest tests/integration/test_websocket.py -v
```

Test coverage includes:
- ✅ Connection with valid token
- ✅ Rejection of invalid tokens
- ✅ Rejection of missing tokens
- ✅ Message broadcasting to all participants
- ✅ Session isolation (messages don't leak between sessions)
- ✅ Disconnect notifications

### Manual Testing with `wscat`

```bash
# Install wscat
npm install -g wscat

# Get a JWT token first (via API)
TOKEN="your-jwt-token-here"

# Connect to WebSocket
wscat -c "ws://localhost:8000/ws/test-session?token=$TOKEN"

# Send messages (JSON format)
{"type": "chat", "data": {"text": "Hello!"}}
```

## Performance Considerations

### Scaling
- Each session maintains its own list of connections
- No shared state between sessions (horizontal scaling friendly)
- Consider Redis Pub/Sub for multi-instance deployments

### Resource Management
- Connections are automatically cleaned up on disconnect
- Empty sessions are removed from memory
- Failed broadcasts remove stale connections

### Recommended Limits
- **Max connections per session**: 100 (configurable)
- **Message size limit**: 64KB (WebSocket default)
- **Reconnection attempts**: 5 (configurable in frontend service)

## Future Enhancements

Planned features for WebSocket infrastructure:

1. **Redis Pub/Sub Integration**
   - Distribute messages across multiple backend instances
   - Share session state across instances
   - Enable horizontal scaling

2. **Message Persistence**
   - Store chat history in database
   - Replay messages for reconnected clients
   - Message delivery guarantees

3. **Rate Limiting**
   - Prevent message spam
   - Per-user message rate limits
   - DDoS protection

4. **Binary Message Support**
   - Image sharing in chat
   - File transfers
   - Voice messages

5. **WebSocket Compression**
   - Reduce bandwidth usage
   - Improve performance on slow connections

## Troubleshooting

### Connection Refused
- Verify server is running on port 8000
- Check CORS settings in backend configuration
- Ensure WebSocket URL uses `ws://` (not `wss://`) for local development

### Authentication Failures
- Verify JWT token is valid and not expired
- Check token includes `sub` (user_id) and `org_id` claims
- Ensure token is passed as query parameter: `?token=...`

### Messages Not Received
- Check session_id matches between sender and receiver
- Verify WebSocket connection is in OPEN state
- Check browser console for errors
- Ensure message handlers are registered before sending

### Disconnection Issues
- Network timeouts: Check firewall/proxy settings
- Server restarts: Frontend will auto-reconnect
- Token expiration: Obtain new token and reconnect

## API Reference

### Backend

#### `ConnectionManager.connect(websocket, session_id)`
Accept a new WebSocket connection and add to session.

#### `ConnectionManager.disconnect(websocket, session_id)`
Remove a WebSocket connection from session.

#### `ConnectionManager.broadcast_to_session(session_id, message)`
Send a message to all connections in a session.

#### `ConnectionManager.send_personal_message(message, websocket)`
Send a message to a specific connection.

#### `ConnectionManager.get_session_connection_count(session_id)`
Get the number of active connections in a session.

### Frontend

#### `WebSocketService.connect(sessionId, token)`
Connect to a WebSocket session with authentication.

#### `WebSocketService.disconnect()`
Disconnect from the current session.

#### `WebSocketService.send(type, data)`
Send a message through the WebSocket.

#### `WebSocketService.on(type, handler)`
Subscribe to messages of a specific type. Returns unsubscribe function.

#### `WebSocketService.off(type, handler)`
Remove a message handler.

#### Properties
- `isConnected`: Boolean indicating connection state
- `currentSessionId`: Current session ID (or empty string)
