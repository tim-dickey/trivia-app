"""
Security Headers Middleware for FastAPI

This middleware adds security headers to all HTTP responses to protect against
common web vulnerabilities including XSS, clickjacking, and MIME sniffing attacks.

Security Headers Implemented:
- Strict-Transport-Security (HSTS): Forces HTTPS connections
- Content-Security-Policy (CSP): Prevents XSS by restricting resource loading
- X-Frame-Options: Prevents clickjacking attacks
- X-Content-Type-Options: Prevents MIME sniffing attacks
- X-XSS-Protection: Legacy XSS protection for older browsers
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware that adds security headers to all HTTP responses.
    
    This middleware should be added to the FastAPI application to ensure
    all responses include appropriate security headers that protect against
    common web vulnerabilities.
    
    Example:
        app = FastAPI()
        app.add_middleware(SecurityHeadersMiddleware)
    """
    
    def __init__(self, app: ASGIApp):
        """
        Initialize the security headers middleware.
        
        Args:
            app: The ASGI application
        """
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        """
        Process the request and add security headers to the response.
        
        Args:
            request: The incoming HTTP request
            call_next: The next middleware or route handler
            
        Returns:
            Response with security headers added
        """
        response = await call_next(request)
        
        # HSTS - HTTP Strict Transport Security
        # Forces browsers to use HTTPS for all future connections to this domain
        # max-age=31536000: Valid for 1 year (in seconds)
        # includeSubDomains: Apply to all subdomains as well
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # CSP - Content Security Policy
        # Restricts which resources can be loaded to prevent XSS attacks
        # default-src 'self': Only allow resources from same origin by default
        # script-src 'self' 'unsafe-inline': Allow scripts from same origin and inline scripts (needed for some frameworks)
        # style-src 'self' 'unsafe-inline': Allow styles from same origin and inline styles
        # img-src 'self' data: https:: Allow images from same origin, data URIs, and HTTPS
        # font-src 'self' data:: Allow fonts from same origin and data URIs
        # connect-src 'self' ws: wss:: Allow connections to same origin and WebSocket connections
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' ws: wss:;"
        )
        
        # X-Frame-Options - Clickjacking Protection
        # DENY: Prevent the page from being displayed in a frame/iframe
        # This protects against clickjacking attacks where malicious sites
        # embed your app in an invisible iframe to trick users
        response.headers["X-Frame-Options"] = "DENY"
        
        # X-Content-Type-Options - MIME Sniffing Protection
        # nosniff: Prevents browsers from MIME-sniffing responses away from the declared content-type
        # This prevents browsers from interpreting files as a different MIME type than declared
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # X-XSS-Protection - Legacy XSS Protection
        # 1; mode=block: Enable XSS filtering and block the page if attack is detected
        # Note: This is a legacy header for older browsers. Modern browsers use CSP instead.
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        return response
