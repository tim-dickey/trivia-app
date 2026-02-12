# Security Headers Documentation

## Overview

The trivia app implements comprehensive security headers middleware to protect against common web vulnerabilities. All HTTP responses include security headers that enforce best practices for web application security.

## Implementation

The security headers are implemented through FastAPI middleware in `backend/core/security_middleware.py` and integrated into the application in `backend/main.py`.

## Security Headers

### 1. Strict-Transport-Security (HSTS)

**Header Value:** `max-age=31536000; includeSubDomains`

**Purpose:** Forces browsers to use HTTPS connections for all future requests to this domain.

**Protection Against:**
- Man-in-the-middle attacks
- Protocol downgrade attacks
- Cookie hijacking

**Details:**
- `max-age=31536000`: Valid for 1 year (31,536,000 seconds)
- `includeSubDomains`: Applies to all subdomains as well

**Browser Support:** All modern browsers

**Security Impact:** High - Prevents insecure HTTP connections

---

### 2. Content-Security-Policy (CSP)

**Header Value:**
```
default-src 'self'; 
script-src 'self' 'unsafe-inline'; 
style-src 'self' 'unsafe-inline'; 
img-src 'self' data: https:; 
font-src 'self' data:; 
connect-src 'self' ws: wss:;
```

**Purpose:** Restricts which resources can be loaded to prevent Cross-Site Scripting (XSS) attacks.

**Protection Against:**
- XSS (Cross-Site Scripting) attacks
- Data injection attacks
- Malicious script execution

**Policy Breakdown:**
- `default-src 'self'`: By default, only allow resources from the same origin
- `script-src 'self' 'unsafe-inline'`: Allow scripts from same origin and inline scripts (needed for modern JavaScript frameworks)
- `style-src 'self' 'unsafe-inline'`: Allow styles from same origin and inline styles
- `img-src 'self' data: https:`: Allow images from same origin, data URIs, and HTTPS sources
- `font-src 'self' data:`: Allow fonts from same origin and data URIs
- `connect-src 'self' ws: wss:`: Allow API connections to same origin and WebSocket connections (required for real-time features)

**Browser Support:** All modern browsers

**Security Impact:** Very High - Primary defense against XSS attacks

**Note:** The CSP policy is configured to work with the trivia app's architecture including WebSocket support for real-time features. Adjust as needed if adding third-party scripts or APIs.

---

### 3. X-Frame-Options

**Header Value:** `DENY`

**Purpose:** Prevents the application from being displayed in a frame, iframe, embed, or object tag.

**Protection Against:**
- Clickjacking attacks
- UI redress attacks
- Invisible iframe overlays

**Details:**
- `DENY`: The page cannot be displayed in a frame, regardless of the site attempting to do so

**Browser Support:** All browsers (legacy and modern)

**Security Impact:** High - Prevents clickjacking attacks

**Alternative Values:**
- `SAMEORIGIN`: Allow framing only from same origin (not used)
- `ALLOW-FROM uri`: Allow framing from specific URI (deprecated, not used)

---

### 4. X-Content-Type-Options

**Header Value:** `nosniff`

**Purpose:** Prevents browsers from MIME-sniffing a response away from the declared content-type.

**Protection Against:**
- MIME confusion attacks
- Content sniffing vulnerabilities
- Malicious file uploads being executed

**Details:**
- `nosniff`: Tells browsers to strictly follow the `Content-Type` header and not try to detect the content type

**Browser Support:** All modern browsers

**Security Impact:** Medium - Prevents certain types of content-based attacks

**Example Scenario:** Without this header, a browser might execute a file uploaded as `image.jpg` if it detects JavaScript content inside it. With `nosniff`, the browser respects the declared content type.

---

### 5. X-XSS-Protection

**Header Value:** `1; mode=block`

**Purpose:** Enables the browser's built-in XSS filter and instructs it to block the page if an attack is detected.

**Protection Against:**
- Reflected XSS attacks (legacy protection)

**Details:**
- `1`: Enable XSS filtering
- `mode=block`: Block the entire page rather than attempting to sanitize

**Browser Support:** Legacy browsers (modern browsers rely on CSP)

**Security Impact:** Low (for modern browsers) - CSP is the primary XSS defense

**Note:** This header is largely obsolete with modern browsers that rely on Content-Security-Policy for XSS protection. However, it provides defense-in-depth for older browsers.

---

## Testing Security Headers

### Automated Tests

Comprehensive test suite in `backend/tests/core/test_security_middleware.py` validates:
- All headers are present in all responses
- Header values are correct
- Headers don't break application functionality
- Headers are present on success, error, and authenticated endpoints

Run tests:
```bash
cd backend
pytest tests/core/test_security_middleware.py -v
```

### Manual Testing

Test headers using curl:
```bash
# Test health endpoint
curl -I http://localhost:8000/health

# Test API endpoint
curl -I http://localhost:8000/api/v1/auth/login

# All responses should include the 5 security headers
```

Test headers using browser DevTools:
1. Open the application in a browser
2. Open Developer Tools (F12)
3. Navigate to Network tab
4. Load any page
5. Click on a request and view Response Headers
6. Verify all 5 security headers are present

### Security Scanning

Use online security header scanners:
- [Security Headers](https://securityheaders.com/)
- [Mozilla Observatory](https://observatory.mozilla.org/)
- [Qualys SSL Labs](https://www.ssllabs.com/ssltest/)

These tools will analyze your security headers and provide a security rating.

---

## Maintenance and Updates

### When to Update CSP Policy

Update the CSP policy when:
- Adding third-party scripts (analytics, CDNs)
- Integrating external APIs
- Adding inline styles or scripts (try to avoid)
- Functionality breaks due to CSP restrictions

### CSP Policy Best Practices

1. **Remove 'unsafe-inline'**: Eliminate inline scripts/styles for better security
2. **Use nonce or hash**: For unavoidable inline scripts, use CSP nonces
3. **Monitor violations**: Set up CSP reporting to track policy violations
4. **Test thoroughly**: Changes to CSP can break functionality

### HSTS Considerations

- **Production Only**: HSTS should only be enabled in production with proper HTTPS setup
- **Certificate Issues**: Ensure SSL certificates are valid; HSTS will prevent access if HTTPS fails
- **Subdomain Impact**: `includeSubDomains` affects all subdomains
- **HSTS Preload**: Consider adding to the HSTS preload list for maximum protection

---

## Security Improvements

### Current Implementation: Good ✓

The current implementation provides strong protection against common web vulnerabilities.

### Future Enhancements (Optional):

1. **Permissions-Policy**: Control browser features (camera, microphone, geolocation)
2. **Referrer-Policy**: Control referrer information sent with requests
3. **CSP Reporting**: Add `report-uri` or `report-to` directives to monitor violations
4. **Subresource Integrity (SRI)**: Add integrity checks for external resources
5. **HSTS Preload**: Submit domain to HSTS preload list

---

## Troubleshooting

### Issue: CSP blocks WebSocket connections

**Solution:** Ensure `connect-src 'self' ws: wss:;` is in the CSP policy (already included).

### Issue: CSP blocks inline styles/scripts

**Solution:** 
1. Move inline code to external files (preferred)
2. Adjust CSP policy to allow specific inline code (less secure)
3. Use CSP nonces for specific inline code (recommended)

### Issue: Application cannot be embedded in iframe

**Explanation:** This is intentional. `X-Frame-Options: DENY` prevents clickjacking.

**Solution:** If legitimate iframe embedding is needed, consider:
1. Change to `X-Frame-Options: SAMEORIGIN` (allow same-origin framing)
2. Use CSP `frame-ancestors` directive for fine-grained control

### Issue: HSTS prevents access after SSL certificate expires

**Solution:** 
1. Fix the SSL certificate immediately
2. Users must wait for `max-age` to expire or clear HSTS settings
3. Ensure certificates are monitored and renewed before expiration

---

## Compliance

These security headers help meet compliance requirements for:
- **OWASP Top 10**: Protection against A03:2021 - Injection (XSS)
- **PCI DSS**: Requirement 6.5.7 (XSS prevention)
- **GDPR**: Security measures to protect user data
- **SOC 2**: Security controls for data protection
- **ISO 27001**: Information security best practices

---

## References

- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)
- [MDN Web Security](https://developer.mozilla.org/en-US/docs/Web/Security)
- [Content Security Policy Reference](https://content-security-policy.com/)
- [HTTP Strict Transport Security (HSTS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security)
- [Security Headers Best Practices](https://scotthelme.co.uk/hardening-your-http-response-headers/)

---

## Related Documentation

- [Multi-Tenancy Security](MULTI_TENANCY.md)
- [WebSocket Security](websocket-infrastructure.md)
- [CI/CD Security Scanning](CI_CD.md)
