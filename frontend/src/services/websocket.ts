/**
 * WebSocket service for real-time features
 * Handles connection management, message handling, and event subscriptions
 */

export type MessageType = 
  | 'connection'
  | 'user_joined'
  | 'user_left'
  | 'message'
  | 'score_update'
  | 'session_update'
  | 'chat';

export interface WebSocketMessage {
  type: MessageType;
  user_id?: string;
  session_id?: string;
  data?: any;
  message?: string;
  participant_count?: number;
}

export type MessageHandler = (message: WebSocketMessage) => void;

export class WebSocketService {
  private ws: WebSocket | null = null;
  private url: string;
  private token: string;
  private sessionId: string;
  private reconnectAttempts: number = 0;
  private maxReconnectAttempts: number = 5;
  private reconnectDelay: number = 1000; // Start with 1 second
  private messageHandlers: Map<MessageType | 'all', Set<MessageHandler>> = new Map();
  private isIntentionalClose: boolean = false;

  constructor(baseUrl?: string) {
    // Auto-detect protocol based on current page protocol
    // Uses wss:// for HTTPS pages, ws:// for HTTP (development)
    if (!baseUrl) {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const host = window.location.hostname;
      const port = process.env.NODE_ENV === 'production' ? '' : ':8000';
      this.url = `${protocol}//${host}${port}`;
    } else {
      this.url = baseUrl;
    }
    this.token = '';
    this.sessionId = '';
  }

  /**
   * Connect to a WebSocket session
   * @param sessionId - The session ID to join
   * @param token - JWT authentication token
   * 
   * Security Note: Token is passed via query parameter due to WebSocket API limitations.
   * While this exposes the token in URLs, it's a common pattern for WebSocket auth.
   * Mitigation: Use short-lived tokens, HTTPS/WSS in production, and don't log URLs server-side.
   */
  connect(sessionId: string, token: string): void {
    this.sessionId = sessionId;
    this.token = token;
    this.isIntentionalClose = false;
    this.createConnection();
  }

  /**
   * Create and configure the WebSocket connection
   * 
   * Security Note: Tokens in query params are a known WebSocket limitation.
   * The WebSocket API doesn't support custom headers in browsers.
   * This is industry-standard practice for WebSocket authentication.
   */
  private createConnection(): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      console.warn('WebSocket already connected');
      return;
    }

    const wsUrl = `${this.url}/ws/${this.sessionId}?token=${this.token}`;
    this.ws = new WebSocket(wsUrl);

    this.ws.onopen = this.handleOpen.bind(this);
    this.ws.onmessage = this.handleMessage.bind(this);
    this.ws.onerror = this.handleError.bind(this);
    this.ws.onclose = this.handleClose.bind(this);
  }

  /**
   * Handle WebSocket connection opened
   */
  private handleOpen(event: Event): void {
    console.log('WebSocket connected to session:', this.sessionId);
    this.reconnectAttempts = 0;
    this.reconnectDelay = 1000;
  }

  /**
   * Handle incoming WebSocket messages
   */
  private handleMessage(event: MessageEvent): void {
    try {
      const message: WebSocketMessage = JSON.parse(event.data);
      
      // Call type-specific handlers
      const typeHandlers = this.messageHandlers.get(message.type);
      if (typeHandlers) {
        typeHandlers.forEach(handler => handler(message));
      }

      // Call generic handlers
      const allHandlers = this.messageHandlers.get('all');
      if (allHandlers) {
        allHandlers.forEach(handler => handler(message));
      }
    } catch (error) {
      console.error('Error parsing WebSocket message:', error);
    }
  }

  /**
   * Handle WebSocket errors
   */
  private handleError(event: Event): void {
    console.error('WebSocket error:', event);
  }

  /**
   * Handle WebSocket connection closed
   */
  private handleClose(event: CloseEvent): void {
    console.log('WebSocket disconnected:', event.code, event.reason);
    
    // Attempt to reconnect if not an intentional close
    if (!this.isIntentionalClose && this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
      
      setTimeout(() => {
        this.createConnection();
      }, this.reconnectDelay);
      
      // Exponential backoff
      this.reconnectDelay = Math.min(this.reconnectDelay * 2, 30000); // Max 30 seconds
    } else if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
    }
  }

  /**
   * Send a message through the WebSocket
   * @param type - Message type
   * @param data - Message data
   */
  send(type: MessageType, data?: any): void {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      console.error('WebSocket is not connected');
      return;
    }

    const message = {
      type,
      data
    };

    this.ws.send(JSON.stringify(message));
  }

  /**
   * Subscribe to messages of a specific type
   * @param type - Message type to listen for, or 'all' for all messages
   * @param handler - Callback function to handle messages
   * @returns Unsubscribe function
   */
  on(type: MessageType | 'all', handler: MessageHandler): () => void {
    if (!this.messageHandlers.has(type)) {
      this.messageHandlers.set(type, new Set());
    }
    
    this.messageHandlers.get(type)!.add(handler);

    // Return unsubscribe function
    return () => {
      const handlers = this.messageHandlers.get(type);
      if (handlers) {
        handlers.delete(handler);
      }
    };
  }

  /**
   * Remove a message handler
   * @param type - Message type
   * @param handler - Handler to remove
   */
  off(type: MessageType | 'all', handler: MessageHandler): void {
    const handlers = this.messageHandlers.get(type);
    if (handlers) {
      handlers.delete(handler);
    }
  }

  /**
   * Disconnect from the WebSocket
   */
  disconnect(): void {
    this.isIntentionalClose = true;
    
    if (this.ws) {
      this.ws.close(1000, 'Client initiated disconnect');
      this.ws = null;
    }
    
    this.messageHandlers.clear();
  }

  /**
   * Get current connection state
   */
  get isConnected(): boolean {
    return this.ws !== null && this.ws.readyState === WebSocket.OPEN;
  }

  /**
   * Get current session ID
   */
  get currentSessionId(): string {
    return this.sessionId;
  }
}

// Export a singleton instance for convenience
export const websocketService = new WebSocketService();
