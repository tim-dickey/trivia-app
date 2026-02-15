"""
Main FastAPI application entry point
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, status
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings
from backend.api.v1 import api_router
from backend.websocket.manager import manager
from backend.core.security import decode_token
from backend.core.security_middleware import SecurityHeadersMiddleware
import logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# Include API v1 router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "app": settings.APP_NAME}


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Trivia App API", "docs": f"{settings.API_V1_PREFIX}/docs"}


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket, session_id: str, token: str = Query(...)
):
    """
    WebSocket endpoint for real-time features

    Supports:
    - Real-time session updates
    - Live scoring
    - Participant tracking
    - Chat messages

    Authentication:
    - Requires valid JWT token passed as query parameter
    - Token must contain valid user_id and org_id

    Args:
        websocket: The WebSocket connection
        session_id: The session/room ID to join
        token: JWT authentication token (query parameter)

    Example:
        ws://localhost:8000/ws/my-session-id?token=your-jwt-token
    """
    # Authenticate the WebSocket connection
    payload = decode_token(token)
    if not payload:
        logger.warning("WebSocket connection rejected: Invalid token")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    user_id = payload.get("sub")
    org_id = payload.get("org_id")

    if not user_id or not org_id:
        logger.warning(
            "WebSocket connection rejected: Missing user_id or org_id in token"
        )
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # Accept connection and add to session
    await manager.connect(websocket, session_id)

    # Send welcome message
    await manager.send_personal_message(
        {
            "type": "connection",
            "message": "Connected to session",
            "session_id": session_id,
            "user_id": user_id,
        },
        websocket,
    )

    # Notify other participants
    await manager.broadcast_to_session(
        session_id,
        {
            "type": "user_joined",
            "user_id": user_id,
            "session_id": session_id,
            "participant_count": manager.get_session_connection_count(session_id),
        },
    )

    try:
        # Listen for messages from the client
        while True:
            data = await websocket.receive_json()

            # Process message based on type
            message_type = data.get("type", "message")

            # Broadcast the message to all session participants
            await manager.broadcast_to_session(
                session_id,
                {
                    "type": message_type,
                    "user_id": user_id,
                    "data": data.get("data"),
                    "session_id": session_id,
                },
            )

    except WebSocketDisconnect:
        # Handle disconnection
        manager.disconnect(websocket, session_id)

        # Notify other participants
        await manager.broadcast_to_session(
            session_id,
            {
                "type": "user_left",
                "user_id": user_id,
                "session_id": session_id,
                "participant_count": manager.get_session_connection_count(session_id),
            },
        )
        logger.info(f"User {user_id} disconnected from session {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error for user {user_id} in session {session_id}: {e}")
        manager.disconnect(websocket, session_id)
        try:
            await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        except Exception as close_error:
            # Connection may already be closed, log and continue
            logger.debug(
                f"Error closing WebSocket (may already be closed): {close_error}"
            )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=settings.DEBUG)
