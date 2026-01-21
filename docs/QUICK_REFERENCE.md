# Trivia App - Quick Reference Guide

A one-page reference for developers working on the Trivia App architecture.

---

## 🎯 Core Design Principles

| Principle | Implementation |
|-----------|-----------------|
| **Multi-Tenancy** | Row-level isolation via `organization_id` on all tables |
| **Real-Time** | WebSocket + Redis Pub/Sub for <1 second score updates |
| **Consistency** | Zustand + TanStack Query for coherent state across components |
| **Scalability** | Stateless FastAPI servers + managed container services |
| **Security** | JWT tokens + row-level filtering in FastAPI dependencies |

---

## 📝 Naming Conventions

### Backend (Python/SQL)

```python
# Functions & Variables: snake_case
def calculate_score(participant_id, question_id):
    total_score = 100
    return total_score

# Classes & Models: PascalCase
class Session(Base):
    organization_id: UUID
    
# Database: snake_case plural, indexed org_id
sessions table
├─ id (UUID, PK)
├─ organization_id (UUID, FK) ◄─ CRITICAL
├─ created_at (timestamp)
└─ status (enum)

# Indexes: idx_{table}_{column}
idx_sessions_organization_id
idx_questions_organization_id
idx_scores_organization_id

# Endpoints: plural, snake_case query params
GET    /api/v1/sessions
POST   /api/v1/questions?difficulty=hard
PUT    /api/v1/sessions/{id}/status
```

### Frontend (TypeScript/React)

```typescript
// Components: PascalCase (React convention)
export const SessionLeaderboard: React.FC = () => {}
export const QuestionDisplay: React.FC = () => {}

// Hooks: useCamelCase
const useSession = (sessionId: string) => {}
const useWebSocket = () => {}
const useScoring = () => {}

// Variables & Functions: camelCase
const currentScore = 150;
const handleAnswerSubmit = () => {}
const formatScore = (score: number) => {}

// Store: camelCase with 'Store' suffix
const sessionStore = create(...);
const scoringStore = create(...);
const authStore = create(...);

// API clients: camelCase
const sessionApi = { getSession, createSession, ... }
const scoreApi = { submitScore, getLeaderboard, ... }
```

### WebSocket Events

```
Naming: lowercase.dot.notation (namespace.entity.action)
Examples:
  session.score.updated
  session.participant.joined
  session.state.changed

Payload format:
{
  "event": "session.score.updated",
  "data": {
    "session_id": "uuid",
    "team_id": "uuid",
    "score": 150,
    "delta": 10,
    "v": 1,           ◄─ Version (for evolution)
    "ts": "ISO-8601"  ◄─ Timestamp
  }
}
```

---

## 🔄 Request/Response Formats

### REST API Success

```python
# Backend Response (FastAPI)
{
  "data": {
    "session_id": "123",
    "team_id": "team-1",
    "score": 150,
    "delta": 10
  }
}

# Backend Schema
class APIResponse(BaseModel):
    data: dict

class ScoreResponse(BaseModel):
    session_id: str
    score: int
    delta: int
```

### REST API Error

```python
# Backend Response
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "User not authorized for this organization"
  }
}

# Backend Schema
class ErrorResponse(BaseModel):
    error: dict
    error__: dict = Field(...)
        code: str
        message: str
```

### Frontend (TypeScript)

```typescript
// API Response type
type APIResponse<T> = {
  data?: T;
  error?: {
    code: string;
    message: string;
  };
};

// Usage
const response: APIResponse<Session> = await api.get("/sessions/123");
if (response.error) {
  toast.error(response.error.message);
} else {
  sessionStore.setSession(response.data!);
}
```

---

## 🏗️ Code Organization Patterns

### Backend: Feature-Oriented Modules

```
services/
├─ session_service.py          # Everything about sessions
├─ scoring_service.py          # Everything about scoring
├─ question_service.py         # Everything about questions
└─ ai_service.py               # Everything about AI

db/crud/
├─ session_crud.py             # Session DB operations
├─ score_crud.py               # Score DB operations
└─ question_crud.py            # Question DB operations

api/v1/endpoints/
├─ sessions.py                 # Session REST routes
├─ scores.py                   # Score REST routes
└─ questions.py                # Question REST routes

models/
├─ session.py                  # Session ORM model
├─ score.py                    # Score ORM model
└─ question.py                 # Question ORM model

schemas/
├─ session.py                  # Session validation schemas
├─ score.py                    # Score validation schemas
└─ responses.py                # Standard response schemas
```

### Frontend: Feature-Based Structure

```
components/
├─ Session/                    # Lightning Round components
│  ├─ SessionSetup.tsx         # Setup wizard
│  ├─ SessionView.tsx          # Main display
│  └─ SessionControls.tsx      # Facilitator controls
├─ Question/                   # Question components
│  ├─ QuestionDisplay.tsx      # Show question
│  ├─ QuestionOptions.tsx      # Show options
│  └─ QuestionFeedback.tsx     # Show feedback
├─ Scoring/                    # Scoring components
│  ├─ ScoreDisplay.tsx         # Show score
│  └─ ScoreDelta.tsx           # Animate delta
└─ Common/                     # Shared components
   ├─ Header.tsx
   ├─ Toast.tsx
   └─ ErrorBoundary.tsx

hooks/
├─ useSession.ts               # Session data fetching
├─ useWebSocket.ts             # WebSocket connection
├─ useScoring.ts               # Score calculations
└─ useAuth.ts                  # Authentication
```

---

## 🔐 Multi-Tenancy Enforcement

### Principle: Every Query Must Check org_id

```python
# ✅ CORRECT: org_id enforced in dependency
@app.get("/sessions")
async def get_sessions(
    current_user = Depends(get_current_user),  # org_id extracted
    db = Depends(get_db)
):
    sessions = db.query(Session).filter(
        Session.organization_id == current_user.org_id  # ◄─ REQUIRED
    )
    return sessions

# ❌ WRONG: No org_id check
@app.get("/sessions")
async def get_sessions(db = Depends(get_db)):
    sessions = db.query(Session).all()  # SECURITY BREACH
    return sessions

# ✅ CORRECT: Using dependency
def get_sessions_for_org(
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    return db.query(Session).filter(
        Session.organization_id == current_user.org_id
    )

@app.get("/sessions")
async def get_sessions(sessions = Depends(get_sessions_for_org)):
    return sessions
```

### Database Layer

```python
# All models inherit from Base with org_id
class Base:
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    organization_id: UUID = Field(...)  # ◄─ ALWAYS REQUIRED
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# All tables indexed on org_id
Index('idx_sessions_organization_id', 'organization_id')
Index('idx_questions_organization_id', 'organization_id')
Index('idx_scores_organization_id', 'organization_id')
```

---

## ⚡ Real-Time Scoring Flow

### Step-by-Step

```
1. Client submits answer
   POST /api/v1/scores {question_id, option}
   
2. Backend validates & calculates
   scoring_service.calculate_score()
   
3. Backend broadcasts
   realtime_service.broadcast()
   redis.publish("session:123:scores", {...})
   
4. WebSocket receives event
   useWebSocket hook receives
   
5. Frontend updates state
   scoringStore.updateScore(+10)
   
6. Component re-renders
   ScoreDisplay shows new score
   ScoreDelta animates "+10"
   
⏱️ Total: <1 second
```

### Frontend Code

```typescript
// hooks/useWebSocket.ts
const useWebSocket = (sessionId: string) => {
  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/sessions/${sessionId}`);
    
    ws.onmessage = (event) => {
      const { event: eventType, data } = JSON.parse(event.data);
      
      if (eventType === 'session.score.updated') {
        // Update Zustand store
        scoringStore.updateScore(data.team_id, data.score, data.delta);
      }
    };
    
    return () => ws.close();
  }, [sessionId]);
};

// components/Scoring/ScoreDisplay.tsx
const ScoreDisplay: React.FC = () => {
  const score = scoringStore((s) => s.currentScore);
  const delta = scoringStore((s) => s.lastDelta);
  
  return (
    <div>
      <span className="text-3xl font-bold">{score}</span>
      <ScoreDelta delta={delta} />
    </div>
  );
};
```

---

## 📊 Validation Strategy (4 Layers)

### Layer 1: Frontend Validation (Real-Time UX)

```typescript
// Input validation with user feedback
const validateEmail = (email: string): boolean => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
};

const LoginForm = () => {
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  
  const handleChange = (e) => {
    setEmail(e.target.value);
    if (!validateEmail(e.target.value)) {
      setError("Invalid email format");
    } else {
      setError("");
    }
  };
};
```

### Layer 2: Pydantic Validation (Contract)

```python
# Backend validation schemas
class UserIn(BaseModel):
    email: EmailStr  # ◄─ Built-in validation
    password: str
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('password must be at least 8 chars')
        return v

@app.post("/users/login")
async def login(user: UserIn):  # ◄─ Auto-validated
    # User.email already validated as EmailStr
    return {"token": create_jwt(user)}
```

### Layer 3: ORM Constraints (Model Level)

```python
# SQLAlchemy model constraints
class Session(Base):
    organization_id: UUID = Field(..., nullable=False)
    status: str = Field(..., nullable=False)
    
    __table_args__ = (
        # Column-level constraints
        CheckConstraint("status IN ('active', 'paused', 'ended')"),
        # Foreign key constraint
        ForeignKeyConstraint(['organization_id'], ['organizations.id']),
    )
```

### Layer 4: Database Constraints (Data Integrity)

```sql
-- Database-level enforcement (last resort)
ALTER TABLE sessions 
  ADD CONSTRAINT ck_session_status 
  CHECK (status IN ('active', 'paused', 'ended'));

ALTER TABLE sessions 
  ADD CONSTRAINT fk_session_org 
  FOREIGN KEY (organization_id) 
  REFERENCES organizations(id);

-- Index for performance
CREATE INDEX idx_sessions_organization_id 
  ON sessions(organization_id);
```

---

## 🚨 Error Handling

### Backend Pattern

```python
# Raise HTTPException for API errors
if not session:
    raise HTTPException(
        status_code=404,
        detail="Session not found"
    )

# Catch at middleware layer
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.detail.upper(),
                "message": exc.detail
            }
        }
    )
```

### Frontend Pattern

```typescript
// API error handling
const handleError = (error: APIError) => {
  const message = error.response?.data?.error?.message 
                  || "An error occurred";
  
  // Show user-friendly message
  toast.error(message);
  
  // Log for debugging
  console.error("API Error:", error.response?.data);
};

// Usage
try {
  const response = await api.post("/sessions", data);
  sessionStore.setSession(response.data);
} catch (error) {
  handleError(error);
}
```

---

## 📈 Performance Optimization

| Metric | Strategy |
|--------|----------|
| **API Latency** | Redis caching for queries, FastAPI async, connection pooling |
| **Score Updates** | Redis Pub/Sub (one publish → all clients in <1s) |
| **Mobile Load** | Vite code splitting, lazy loading, gzip compression |
| **DB Queries** | Indexes on org_id, query result caching, pagination |
| **Memory** | Pagination for large lists, stream responses for large uploads |

---

## 🧪 Testing Strategy

### Backend

```python
# tests/unit/test_scoring_service.py
def test_calculate_score_correct_answer():
    score = scoring_service.calculate_score(
        question_id="q1",
        selected_option="A",
        correct_option="A"
    )
    assert score == 100

# tests/integration/test_scores_endpoint.py
def test_post_score_broadcasts():
    with patch('redis.publish') as mock_publish:
        response = client.post("/api/v1/scores", json={...})
        mock_publish.assert_called_once()

# tests/e2e/test_session_flow.py
async def test_full_session_flow():
    # 1. Create session
    # 2. Join participant
    # 3. Submit answer
    # 4. Verify score broadcast
```

### Frontend

```typescript
// tests/components/Session.test.tsx
describe('SessionLeaderboard', () => {
  it('renders team scores', () => {
    const { getByText } = render(<SessionLeaderboard />);
    expect(getByText('Team 1: 150 pts')).toBeInTheDocument();
  });
});

// tests/hooks/useWebSocket.test.ts
it('connects to WebSocket on mount', () => {
  const { result } = renderHook(() => useWebSocket('session-123'));
  expect(result.current.connected).toBe(true);
});

// tests/e2e/session-flow.test.ts
test('submit answer and see score update', async () => {
  await page.fill('[name="option"]', 'A');
  await page.click('[name="submit"]');
  await expect(page.locator('[class="score"]')).toContainText('150');
});
```

---

## 📦 Deployment Checklist

- [ ] Environment variables configured (DB, Redis, JWT secret)
- [ ] Database migrations run (`alembic upgrade head`)
- [ ] Docker images built and pushed to registry
- [ ] Secrets stored in secrets manager (AWS Secrets Manager, GCP Secret Manager)
- [ ] API rate limiting configured
- [ ] HTTPS/TLS certificates installed
- [ ] Monitoring & logging set up (CloudWatch, Datadog)
- [ ] Backups configured (daily, 30-day retention)
- [ ] CORS configuration set for production domain
- [ ] Database connection pool sizing optimized
- [ ] Redis persistence enabled for Pub/Sub
- [ ] CI/CD pipeline tested end-to-end

---

## 🔗 Key Files to Know

| File | Purpose |
|------|---------|
| `backend/main.py` | FastAPI app entry point |
| `backend/core/config.py` | Configuration management |
| `backend/core/security.py` | JWT, encryption, hashing |
| `backend/api/v1/dependencies.py` | FastAPI dependency injection |
| `backend/services/scoring_service.py` | Score calculation |
| `frontend/store/scoringStore.ts` | Score state management |
| `frontend/hooks/useWebSocket.ts` | Real-time connection |
| `docs/ARCHITECTURE.md` | Complete architecture decisions |
| `docs/DIAGRAMS.md` | Architecture diagrams |
| `.github/workflows/ci.yml` | CI/CD pipeline |

---

## 💡 Tips & Tricks

### Debugging Multi-Tenancy Issues

```bash
# Check current user's org_id from JWT
jwt_payload=$(echo $JWT_TOKEN | base64 -d | jq)
echo $jwt_payload.org_id

# Query database for org_id
SELECT * FROM sessions WHERE organization_id = 'org-5';
```

### Testing Real-Time Scoring

```bash
# Terminal 1: Subscribe to Redis channel
redis-cli subscribe "session:123:scores"

# Terminal 2: Send test event
redis-cli publish "session:123:scores" '{"team_id":"t1","score":150}'

# Terminal 1: Observe message received
```

### Performance Profiling

```python
# Add timing to services
import time

def calculate_score(question_id):
    start = time.time()
    # ... calculation ...
    elapsed = time.time() - start
    logger.info(f"Score calculation took {elapsed:.3f}s")
    return score
```

---

## 📞 Common Questions

**Q: How do I add a new endpoint?**
A: Create in `api/v1/endpoints/`, add service in `services/`, add CRUD in `db/crud/`, add schema in `schemas/`, add test.

**Q: How do I ensure multi-tenancy?**
A: Always filter by `organization_id` in FastAPI dependencies before calling services/CRUD.

**Q: How do I test WebSocket?**
A: Use `python-socketio` test client or Playwright for browser-based E2E tests.

**Q: Why is my score not appearing in real-time?**
A: Check Redis Pub/Sub connection, verify WebSocket client is subscribed, check event format.

**Q: How do I scale to 10,000 concurrent users?**
A: Use multiple FastAPI instances behind load balancer, increase Redis memory, scale PostgreSQL with read replicas.

---

**Last Updated:** January 20, 2026  
**Architecture Status:** ✅ Complete & Validated  
**Implementation Status:** Ready to Begin
