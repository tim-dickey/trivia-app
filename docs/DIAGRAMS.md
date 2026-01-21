# Trivia App - Architecture Diagrams

This document contains detailed diagrams visualizing the Trivia App architecture and data flows.

---

## 1. System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         TRIVIA APP PLATFORM                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌──────────────────────┐   ┌──────────────────┐   ┌─────────────────┐ │
│  │   WEB BROWSER UI     │   │  SLACK BOT       │   │  TEAMS BOT      │ │
│  │  (React + Vite)      │   │  (Thin Client)   │   │  (Thin Client)  │ │
│  │  (WebSocket client)  │   │                  │   │                 │ │
│  └──────────┬───────────┘   └────────┬─────────┘   └────────┬────────┘ │
│             │                        │                      │            │
│             │ REST + WebSocket       │ REST                 │ REST       │
│             │                        │                      │            │
│             └────────────────────────┼──────────────────────┘            │
│                                      │                                   │
│                     ┌────────────────▼──────────────┐                   │
│                     │   FASTAPI BACKEND             │                   │
│                     │  (Python async server)        │                   │
│                     │                               │                   │
│                     │  ├─ API Endpoints (/v1)      │                   │
│                     │  ├─ WebSocket Gateway        │                   │
│                     │  ├─ Session Management       │                   │
│                     │  ├─ Scoring Engine           │                   │
│                     │  ├─ AI Integration Layer     │                   │
│                     │  └─ Background Tasks         │                   │
│                     └────────┬─────────┬────────────┘                   │
│                              │         │                                │
│            ┌─────────────────┼─────────┼─────────────────┐             │
│            │                 │         │                 │             │
│            ▼                 ▼         ▼                 ▼             │
│     ┌──────────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐    │
│     │ PostgreSQL   │  │  Redis   │  │  Redis   │  │  Celery    │    │
│     │  Database    │  │  Cache   │  │ Pub/Sub  │  │  Task      │    │
│     │              │  │          │  │          │  │  Queue     │    │
│     │ ✓ Row-level  │  │ ✓ Query  │  │ ✓ Cross- │  │ ✓ Async    │    │
│     │ isolation    │  │ results  │  │ instance │  │ scoring    │    │
│     │ (org_id)     │  │ (1hr TTL)│  │ broadcast│  │ analytics  │    │
│     └──────────────┘  └──────────┘  └──────────┘  └────────────┘    │
│                                                                        │
│     ┌────────────────────────────────────────────────────────────┐   │
│     │              EXTERNAL INTEGRATIONS                         │   │
│     │                                                            │   │
│     │  ├─ OpenAI API (ChatGPT)                                 │   │
│     │  ├─ Anthropic API (Claude)                              │   │
│     │  ├─ Azure OpenAI (Enterprise)                           │   │
│     │  ├─ Slack API (Notifications)                           │   │
│     │  ├─ Teams API (Notifications)                           │   │
│     │  └─ SendGrid (Email)                                    │   │
│     └────────────────────────────────────────────────────────────┘   │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Real-Time Scoring Data Flow

```
                    PARTICIPANT CLIENT
                    (Browser/Mobile)
                            │
                            │ 1. Submit Answer
                            │    {question_id, selected_option}
                            │
                            ▼
                    ┌──────────────────┐
                    │  FastAPI Backend │
                    │  POST /scores    │
                    └────────┬─────────┘
                             │
                     ┌───────┴───────┐
                     │               │
                     ▼               ▼
          ┌─────────────────┐  ┌───────────────┐
          │  Validate       │  │  Extract JWT  │
          │  answer &       │  │  verify org   │
          │  question       │  │  + access     │
          └────────┬────────┘  └───────────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ scoring_service  │
          │ .calculate_score()  
          │                  │
          │ • Check if       │
          │   correct        │
          │ • Apply bonus    │
          │   multipliers    │
          │ • Detect streaks │
          │ • Update DB      │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ realtime_service │
          │ .broadcast()     │
          │                  │
          │ Publish to Redis:│
          │ Channel:         │
          │  session:123:    │
          │  scores          │
          │                  │
          │ Payload:         │
          │ {                │
          │  session_id,     │
          │  team_id,        │
          │  score: 150,     │
          │  delta: +10,     │
          │  v: 1,  (version)│
          │  ts: "2026-01..."│
          │ }                │
          └────────┬─────────┘
                   │
    ┌──────────────┴──────────────┐
    │                             │
    ▼                             ▼
┌─────────────────┐         ┌──────────────┐
│ PARTICIPANT 1   │         │ PARTICIPANT 2│
│  (Still in      │         │  (Also in    │
│   session)      │         │   session)   │
│                 │         │              │
│ ◀─ WebSocket ───┼─────────┼──ReceiveEvent
│   connection    │         │              │
│   stays open    │         │              │
│                 │         └──────┬───────┘
└────────┬────────┘                │
         │                         │
         ▼                         ▼
    Frontend:             Frontend:
    1. Zustand store      1. Zustand store
       updated               updated
    2. Score +10          2. Score +10
       animation          3. "Participant 1
    3. Delta shows           scored 10 points!"
       "+10"              4. Leaderboard
                             refreshed

    ⏱️ Total latency: <1 second from answer submission
       to all clients seeing the update
```

---

## 3. Multi-Tenancy & Row-Level Isolation

```
                       INCOMING REQUEST
                   (with JWT auth token)
                            │
                            ▼
                    ┌────────────────────┐
                    │  JWT Token         │
                    │  ─────────────────  │
                    │  sub: user_42      │
                    │  org_id: 5         │ ◄── CRITICAL
                    │  roles: [admin]    │
                    │  iat: 1674...      │
                    └────────┬───────────┘
                             │
                    ┌────────▼─────────┐
                    │ get_current_user │
                    │ (FastAPI Depends)│
                    └────────┬─────────┘
                             │ Extract org_id
                             ▼
                    ┌────────────────────┐
                    │ Query: Get Sessions│
                    │                    │
                    │ SELECT * FROM      │
                    │  sessions          │
                    │ WHERE              │
                    │  organization_id   │
                    │  = 5               │ ◄── FILTER APPLIED
                    │  AND               │     BEFORE DATABASE
                    │  user_id = 42      │
                    └────────┬───────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
     ┌─────────┐        ┌─────────┐       ┌─────────┐
     │Org 5    │        │Org 12   │       │Org 8    │
     │Sessions │        │Sessions │       │Sessions │
     │VISIBLE  │        │HIDDEN   │       │HIDDEN   │
     │✓✓✓✓     │        │✗✗✗✗     │       │✗✗✗✗     │
     └─────────┘        └─────────┘       └─────────┘

    KEY PRINCIPLES:
    ✓ Isolation enforced at APPLICATION layer (before DB)
    ✓ Every table has organization_id column + index
    ✓ Every query automatically filtered by org_id
    ✓ Impossible for user to see data from other orgs
    ✓ Even if WHERE clause fails, data is still isolated
```

---

## 4. Component Communication Patterns

```
                        CLIENT (Browser)
                              │
                ┌─────────────┼─────────────┐
                │             │             │
              REST         WebSocket      REST
             (CRUD)       (Real-time)    (Integrations)
                │             │             │
                ▼             ▼             ▼
        ┌─────────────────────────────────────┐
        │     FastAPI Application             │
        │  (Single Python process)            │
        └──────────┬────────────────────┬─────┘
                   │                    │
         ┌─────────▼─────┐     ┌────────▼────────┐
         │ API Endpoints │     │  WebSocket      │
         │               │     │  Handlers       │
         │ POST /scores  │     │                 │
         │ GET /sessions │     │ /ws/sessions/   │
         │ ...           │     │ {session_id}    │
         └────────┬──────┘     └────────┬────────┘
                  │                     │
         ┌────────▼──────────┐   ┌──────▼──────────┐
         │ services/         │   │ services/       │
         │ scoring_service   │   │ realtime_service│
         │ session_service   │   │                 │
         │ question_service  │   │ (Broadcast logic)
         │ ...               │   │                 │
         └────────┬──────────┘   └──────┬──────────┘
                  │                     │
         ┌────────▼──────────┐   ┌──────▼──────────┐
         │ db/crud/          │   │ integrations/   │
         │                   │   │ redis_pubsub.py │
         │ • session_crud.py │   │                 │
         │ • score_crud.py   │   │ PUBLISH to:     │
         │ • ...             │   │ session:123:    │
         │                   │   │ scores          │
         └────────┬──────────┘   └──────┬──────────┘
                  │                     │
         ┌────────▼──────────┐   ┌──────▼──────────┐
         │  PostgreSQL DB    │   │   Redis Pub/Sub │
         │  (Row-level       │   │   (Broadcast)   │
         │   isolation)      │   │                 │
         └───────────────────┘   └─────────────────┘
                                        │
                                   ┌────▼────┐
                                   │ ALL      │
                                   │ Connected
                                   │ Clients  │
                                   │ Receive  │
                                   │ Event    │
                                   └──────────┘

PATTERN:
• REST: Services call CRUD → Database (one request/response cycle)
• WebSocket: Handler publishes to Redis → All subscribed clients
• Pub/Sub: Cross-instance broadcasting (one FastAPI instance can reach all clients)
```

---

## 5. Authentication & Authorization Flow

```
                            LOGIN REQUEST
                     {email, password}
                              │
                              ▼
                    ┌──────────────────────┐
                    │ POST /users/login    │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼──────────┐
                    │ 1. Validate input   │
                    │ 2. Hash password    │
                    │    with bcrypt      │
                    │ 3. Compare to DB    │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Password matches?   │
                    └──┬─────────────────┬┘
                     YES               NO
                       │                 │
                       ▼                 ▼
            ┌──────────────────┐  ┌─────────────────┐
            │ Create JWT       │  │ Return 401      │
            │ Token            │  │ Unauthorized    │
            │                  │  └─────────────────┘
            │ Token format:    │
            │ {                │
            │  sub: user_42    │
            │  org_id: 5       │
            │  roles: [admin]  │
            │  email: u@ex.com │
            │  iat: 1674...    │
            │  exp: 1674...+1h │
            │ }                │
            └────────┬─────────┘
                     │
                     ▼
            ┌──────────────────┐
            │ Return token to  │
            │ client           │
            └────────┬─────────┘
                     │
           ┌─────────┴──────────┐
           │                    │
           ▼                    ▼
    ACCESS TOKEN          REFRESH TOKEN
    (15 min)              (7 days)
    Sent in               Stored in
    Authorization        HTTP-only
    header               cookie
         │                    │
         ▼                    ▼
    ┌──────────────────────────────────┐
    │  SUBSEQUENT REQUESTS              │
    │                                   │
    │  GET /api/v1/sessions             │
    │  Authorization: Bearer {token}    │
    │  Cookie: {refresh_token}          │
    └───────────┬──────────────────────┘
                │
      ┌─────────▼─────────┐
      │ verify_token()    │
      │ (FastAPI Depends) │
      └────┬──────────┬───┘
         VALID    EXPIRED
           │         │
           ▼         ▼
        Continue  ┌──────────────────┐
        Request  │ Refresh token     │
                 │ still valid?      │
                 └────┬──────────┬───┘
                    YES        NO
                     │         │
                     ▼         ▼
                  Issue    Return 401
                  new      Redirect
                  token    login
```

---

## 6. Feature: Lightning Round Implementation

```
┌──────────────────────────────────────────────────────────────────────┐
│                    LIGHTNING ROUND FEATURE                            │
└──────────────────────────────────────────────────────────────────────┘

FLOW:

1. Setup Phase
   ├─ SessionSetup.tsx (frontend component)
   ├─ User selects "Lightning Round"
   ├─ Specify duration (5-15 min)
   ├─ Specify # of questions
   └─ POST /api/v1/sessions
        {event_type: "lightning_round", duration: 10, question_count: 20}

2. Load Questions Phase
   ├─ Backend: question_service.get_random_questions()
   ├─ Query: SELECT * FROM questions 
          WHERE organization_id = 5 
          ORDER BY RANDOM() 
          LIMIT 20
   ├─ Cache in Redis (5 min TTL)
   └─ Return to frontend

3. Display Question Phase
   ├─ QuestionDisplay.tsx renders question + options
   ├─ QuestionTimer.tsx shows countdown (typically 30-60 sec)
   ├─ Participant selects answer
   └─ Optional: useWebSocket hook listens for other participants' scores

4. Score Submission Phase
   ├─ Participant clicks "Submit Answer"
   ├─ Frontend: Optimistic UI update (local score += points)
   ├─ POST /api/v1/scores
        {session_id, question_id, selected_option}
   │
   ├─ Backend: scoring_service.calculate_score()
   │  ├─ Is answer correct? (look up correct_option)
   │  ├─ Calculate base points (100)
   │  ├─ Apply time bonus (faster = more points)
   │  ├─ Apply multiplier (streak bonus)
   │  ├─ Store in database
   │  └─ Create score delta event
   │
   ├─ Broadcast: realtime_service.broadcast()
   │  ├─ Publish to Redis: session:123:scores
   │  ├─ Payload: {session_id, team_id, score: 150, delta: +10, v:1, ts}
   │  └─ All connected clients receive via WebSocket
   │
   ├─ Frontend clients receive event
   │  ├─ Update Zustand scoringStore
   │  ├─ ScoreDelta.tsx animates "+10"
   │  ├─ Leaderboard refreshes
   │  └─ Toast: "Great job! +10 points!"
   │
   └─ Response: {data: {score: 150, feedback: "..."}}

5. Feedback Phase
   ├─ question_service.get_educational_feedback(question_id)
   ├─ Check Redis cache (1 hour TTL)
   ├─ If not cached:
   │  ├─ Call ai_service (route to configured provider)
   │  ├─ ai_service calls OpenAI/Anthropic/Azure based on config
   │  ├─ Cache response in Redis
   │  └─ Return to frontend
   ├─ QuestionFeedback.tsx displays AI-generated feedback
   └─ Participant learns from mistake

6. Next Question Phase
   ├─ Timer expires OR participant clicks "Next"
   ├─ Load next question from pre-loaded cache
   ├─ SessionLeaderboard.tsx shows live scores
   ├─ Repeat phases 3-5
   └─ Continue until all questions answered or time expires

7. Session End Phase
   ├─ Final leaderboard displayed
   ├─ Background tasks triggered (Celery):
   │  ├─ Aggregate session stats
   │  ├─ Send notifications (Slack/Teams)
   │  ├─ Update analytics
   │  └─ Award participation streaks
   └─ Option to start new session or return to dashboard

COMPONENT TREE:
  SessionView
  ├─ SessionLeaderboard (TanStack Query: GET /scores)
  ├─ QuestionDisplay
  │  ├─ QuestionOptions (Radio buttons)
  │  ├─ QuestionTimer (Countdown)
  │  └─ QuestionFeedback (AI-generated)
  ├─ ScoreDisplay (Zustand + animation)
  │  ├─ ScoreDelta ("+10" animation)
  │  └─ StreakBadge ("5-session streak!")
  └─ SessionControls (Facilitator only)
     ├─ Pause/Resume
     ├─ End Session
     └─ Skip Question

DATABASE TABLES:
  ✓ sessions (event_type = "lightning_round")
  ✓ session_participants (tracking all participants)
  ✓ questions (pre-loaded lightning questions)
  ✓ question_options (answer choices)
  ✓ participant_answers (audit trail: which participant answered what)
  ✓ scores (final scores + deltas)
  ✓ participant_scores (per-participant scores)

REDIS CHANNELS:
  • session:123:scores (broadcast score updates)
  • session:123:join (broadcast when participant joins)
  • session:123:state (broadcast state changes: started, paused, ended)

PERFORMANCE:
  ✓ Questions pre-loaded in Redis (instant delivery)
  ✓ Score calculation <100ms (in-process)
  ✓ Broadcast to all clients <1s (Redis Pub/Sub)
  ✓ Mobile load time <2s (Vite optimization)
```

---

## 7. Enterprise AI Model Selection Feature

```
┌──────────────────────────────────────────────────────────────────────┐
│          ENTERPRISE AI MODEL SELECTION FEATURE                        │
│          (Tier-based routing to different AI providers)              │
└──────────────────────────────────────────────────────────────────────┘

TIER-BASED ROUTING:

Free Tier
  └─► Fixed: Microsoft Copilot
      (No choice for facilitator)
      Feedback quality: Good
      Cost: Free

Premium Tier
  └─► Organization-selected default
      (Admin sets org default, facilitator cannot change)
      Options: GPT-4, Claude, Copilot
      Feedback quality: Good
      Cost: Monthly subscription

Enterprise Tier
  └─► Facilitator choice per session
      (Dropdown to select model for this session)
      Options: GPT-5.1-Codex-Max, Claude 3 Opus, Azure OpenAI, Custom
      Feedback quality: Excellent
      Cost: Enterprise contract


IMPLEMENTATION:

1. Database Schema
   ┌─────────────────────────────────┐
   │ ai_model_configs table          │
   ├─────────────────────────────────┤
   │ id                              │
   │ organization_id (org_5)         │
   │ tier ("enterprise")             │
   │ provider ("gpt-5.1-codex-max")  │
   │ api_key (AES-256 encrypted)     │
   │ is_active (true)                │
   │ created_at                      │
   │ updated_at                      │
   └─────────────────────────────────┘

2. Admin Configuration (UIAdminPanel)
   ┌─────────────────────────────────┐
   │ AIModelConfig.tsx (Admin UI)    │
   │                                 │
   │ Org: Acme Corp                  │
   │ Tier: Enterprise                │
   │                                 │
   │ Available Models:               │
   │ [✓] GPT-5.1-Codex-Max          │
   │ [✓] Claude 3 Opus              │
   │ [✓] Azure OpenAI               │
   │ [ ] Custom Provider            │
   │                                 │
   │ Default Model: GPT-5.1-Codex    │
   │                                 │
   │ API Keys:                       │
   │ GPT Key: ••••••••••• [Change]   │
   │ Claude Key: ••••••••• [Change]  │
   │                                 │
   │ [Save Configuration]            │
   └─────────────────────────────────┘

3. Facilitator Selection (Session Setup)
   ┌──────────────────────────────────┐
   │ SessionSetup.tsx (Free/Premium)  │
   │ AI Model: [Microsoft Copilot ✓] │
   │ (disabled - no choice)           │
   └──────────────────────────────────┘

   ┌──────────────────────────────────┐
   │ SessionSetup.tsx (Enterprise)    │
   │ AI Model: [Select ▼]             │
   │ ├─ GPT-5.1-Codex-Max             │
   │ ├─ Claude 3 Opus                 │
   │ └─ Azure OpenAI                  │
   │ [Session Start]                  │
   └──────────────────────────────────┘

4. API Layer Routing
   ┌───────────────────────────────────────────┐
   │ POST /api/v1/questions/{id}/feedback      │
   │ {session_id, selected_model?}             │
   └──────────────────┬────────────────────────┘
                      │
            ┌─────────▼──────────┐
            │ api/endpoints/     │
            │ questions.py       │
            │                    │
            │ 1. Get session     │
            │ 2. Get user tier   │
            │ 3. Verify model    │
            │    selection       │
            │ 4. Call ai_service │
            └─────────┬──────────┘
                      │
            ┌─────────▼──────────────┐
            │ services/ai_service.py │
            │                        │
            │ Route based on:        │
            │ - Tier                 │
            │ - Selected model       │
            │ - API keys             │
            └──┬──────────┬──────┬───┘
               │          │      │
               ▼          ▼      ▼
         ┌─────────┐ ┌────────┐ ┌──────┐
         │ OpenAI  │ │Anthropic│ │Azure │
         │ API     │ │ API    │ │OpenAI│
         │         │ │        │ │ API  │
         │ GPT-5.1 │ │Claude  │ │GPT-4 │
         └─────────┘ └────────┘ └──────┘
                │
                ▼
         ┌──────────────┐
         │ Response     │
         │ {            │
         │  feedback:   │
         │  "The      │
         │   answer..." │
         │ }            │
         └──────────────┘

5. Caching Strategy
   ┌─────────────────────────────┐
   │ Redis Cache (1 hour TTL)    │
   │                             │
   │ Key Format:                 │
   │ ai_feedback:{q_id}:{model}  │
   │                             │
   │ Example:                    │
   │ ai_feedback:42:gpt-5.1      │
   │ → {feedback: "..."}         │
   │                             │
   │ Benefit:                    │
   │ ✓ Same question, same model │
   │   → use cached feedback     │
   │ ✓ Different model selected  │
   │   → call API again          │
   └─────────────────────────────┘

SECURITY:
  ✓ API keys stored encrypted (AES-256)
  ✓ Only org admins can change config
  ✓ Tier verified server-side (not client)
  ✓ API calls made server-to-server (no client exposure)
  ✓ Rate limiting per organization
  ✓ Audit log: which model used for which session
```

---

## 8. Backend Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│                  FASTAPI APPLICATION                    │
└─────────────────────────────────────────────────────────┘

LAYER 1: HTTP & WebSocket Entry Points
┌─────────────────────────────────────────────────────────┐
│ api/v1/endpoints/                                       │
│ ├─ sessions.py      → GET/POST /sessions/              │
│ ├─ questions.py     → GET/POST /questions/             │
│ ├─ scores.py        → GET/POST /scores/                │
│ ├─ users.py         → GET/POST /users/                 │
│ └─ ai_models.py     → GET/POST /ai_models/config       │
│                                                         │
│ websocket/router.py → GET /ws/sessions/{id}            │
└─────────────────────────────────────────────────────────┘
              ↓ (Validates request + extracts org_id)

LAYER 2: Validation & Authorization
┌─────────────────────────────────────────────────────────┐
│ api/v1/dependencies.py                                  │
│ ├─ get_current_user()     → Verify JWT                 │
│ ├─ verify_org_access()    → Check org_id matches       │
│ ├─ verify_session_access()→ User in session?           │
│ └─ verify_admin()         → Is user admin?             │
│                                                         │
│ schemas/ (Pydantic models)                              │
│ ├─ SessionIn              → Validate input schema      │
│ ├─ SessionOut             → Response schema            │
│ └─ ErrorResponse          → Standard error format      │
└─────────────────────────────────────────────────────────┘
              ↓ (Calls business logic services)

LAYER 3: Business Logic
┌─────────────────────────────────────────────────────────┐
│ services/                                               │
│ ├─ session_service.py     → Session orchestration      │
│ ├─ scoring_service.py     → Score calculation          │
│ ├─ question_service.py    → Question management        │
│ ├─ ai_service.py          → AI provider routing        │
│ ├─ realtime_service.py    → WebSocket broadcasts       │
│ ├─ slack_service.py       → Slack notifications        │
│ └─ teams_service.py       → Teams notifications        │
│                                                         │
│ Example: scoring_service.calculate_score()             │
│ ├─ Verify question correctness                         │
│ ├─ Apply scoring multipliers                           │
│ ├─ Detect participation streaks                        │
│ ├─ Call realtime_service to broadcast                  │
│ └─ Return score + delta                                │
└─────────────────────────────────────────────────────────┘
              ↓ (Calls data access layer)

LAYER 4: Data Access (CRUD)
┌─────────────────────────────────────────────────────────┐
│ db/crud/                                                │
│ ├─ session_crud.py    → create_session, get_session    │
│ ├─ score_crud.py      → create_score, get_leaderboard  │
│ ├─ question_crud.py   → get_questions                  │
│ └─ common_crud.py     → Base CRUD patterns             │
│                                                         │
│ ALL queries filtered by organization_id:               │
│ SELECT * FROM sessions                                 │
│ WHERE organization_id = current_user.org_id            │
│                                                         │
│ models/                                                 │
│ ├─ base.py            → BaseModel (id, org_id, ts)    │
│ ├─ session.py         → Session ORM model              │
│ ├─ question.py        → Question ORM model             │
│ └─ score.py           → Score ORM model                │
└─────────────────────────────────────────────────────────┘
              ↓ (Executes SQL queries)

LAYER 5: Database & Cache
┌─────────────────────────────────────────────────────────┐
│ PostgreSQL                    │ Redis                   │
│ ├─ sessions table            │ ├─ Query cache        │
│ ├─ questions table           │ ├─ Session state      │
│ ├─ scores table              │ ├─ AI feedback (1h)   │
│ ├─ users table               │ └─ Pub/Sub channels  │
│ ├─ organizations table       │                       │
│ └─ ai_model_configs table    │ Celery tasks          │
│   (ALL with organization_id) │ ├─ Score aggregation │
│                              │ ├─ Notifications     │
│   Indexes:                   │ └─ Analytics          │
│   ├─ idx_sessions_org_id    │                       │
│   ├─ idx_questions_org_id   │                       │
│   └─ idx_scores_org_id      │                       │
└─────────────────────────────────────────────────────────┘

CONTROL FLOW EXAMPLE:

Client: POST /api/v1/scores {question_id: 5, option: B}
                                    │
                    ┌───────────────▼──────────────┐
                    │ endpoints/scores.py          │
                    │ @app.post("/scores")         │
                    └───────────────┬──────────────┘
                                    │
                ┌───────────────────┴──────────────┐
                │                                  │
                ▼                                  ▼
        ┌──────────────┐                ┌─────────────────┐
        │ Pydantic     │                │ get_current_user│
        │ validation   │                │ (from JWT)      │
        │ (schema)     │                │ org_id: 5       │
        └──────┬───────┘                └─────────┬───────┘
               │                                  │
               └──────────────┬───────────────────┘
                              │
                ┌─────────────▼────────────┐
                │ scoring_service.py       │
                │ .calculate_score()       │
                │                          │
                │ 1. Validate session      │
                │ 2. Get question          │
                │ 3. Check if correct      │
                │ 4. Apply multipliers     │
                │ 5. Create score record   │
                └─────────────┬────────────┘
                              │
                ┌─────────────▼────────────┐
                │ score_crud.py            │
                │ .create_score()          │
                │                          │
                │ INSERT INTO scores       │
                │ WHERE org_id = 5         │
                └─────────────┬────────────┘
                              │
                ┌─────────────▼────────────┐
                │ PostgreSQL               │
                │ +1 record inserted       │
                └─────────────┬────────────┘
                              │
                ┌─────────────▼────────────┐
                │ realtime_service.py      │
                │ .broadcast()             │
                │                          │
                │ PUBLISH to Redis:        │
                │ session:123:scores       │
                └─────────────┬────────────┘
                              │
                ┌─────────────▼────────────┐
                │ Redis Pub/Sub            │
                │ → All subscribers get    │
                │   {score: 150, delta:10} │
                └─────────────┬────────────┘
                              │
                ┌─────────────▼────────────┐
                │ WebSocket manager        │
                │ → Send to all clients    │
                │ → Frontend updates       │
                │ → Animate score change   │
                └──────────────────────────┘
```

---

## 9. Frontend State Management

```
┌──────────────────────────────────────────────────────────┐
│       ZUSTAND STATE MANAGEMENT ARCHITECTURE              │
└──────────────────────────────────────────────────────────┘

store/authStore.ts
├─ user (current user object)
├─ tokens (access + refresh)
├─ permissions (user roles)
├─ setUser() → Update user
├─ logout() → Clear state
└─ isAuthenticated() → Check if logged in

store/sessionStore.ts
├─ currentSession (session object)
├─ participants (list of participants)
├─ sessionStatus (active/paused/ended)
├─ setSession() → Load session
├─ addParticipant() → Join participant
└─ endSession() → Session ended

store/scoringStore.ts
├─ localScores (Map<team_id, score>)
├─ scoreDeltas (Map<team_id, delta>)
├─ streaks (participation streaks)
├─ updateLocalScore() → Optimistic update
├─ confirmScore() → Server confirmation
├─ revertScore() → Error handling
└─ animateScore() → Visual animation

store/uiStore.ts
├─ sidebarOpen (boolean)
├─ theme (light/dark)
├─ notifications (toast queue)
├─ toggleSidebar() → Open/close
├─ addNotification() → Toast message
└─ removeNotification() → Dismiss toast


DATA FLOW EXAMPLE (Score Update):

1. User submits answer
   └─► QuestionOptions.tsx
       └─► scoringStore.updateLocalScore(+10)  ◄─ Optimistic
           (Zustand state updated immediately)

2. API Call
   └─► scoreApi.ts
       └─► POST /api/v1/scores
           └─► Backend calculates

3. WebSocket Event (Real-Time)
   └─► websocketService receives event
       └─► Publish to Zustand
           └─► scoringStore.confirmScore(response.score)

4. Component Re-render (Automatic)
   └─► ScoreDisplay.tsx watches scoringStore
       └─► When store updates:
           ├─► Show score change
           ├─► Animate delta
           └─► Update leaderboard


INTEGRATION WITH TANSTACK QUERY:

useSession Hook:
├─ const { data: session, isLoading, error } = useQuery({
│   queryKey: ['session', sessionId],
│   queryFn: () => sessionApi.getSession(sessionId),
│   refetchInterval: 5000  // Refetch every 5s
│ })
└─ TanStack Query = Server state
   Zustand = Local state

Example:
├─ TanStack Query (server-sourced):
│  ├─ Session details (persistent)
│  ├─ Leaderboard (cached 30s)
│  └─ Participants list
│
└─ Zustand (local/real-time):
   ├─ My local score (before server confirmation)
   ├─ Animations (showing delta)
   └─ UI state (sidebar open/close)

```

---

## Summary

These diagrams help visualize:

1. **System Architecture** - Overall component layout and integration
2. **Real-Time Flow** - How scoring updates reach all clients in <1 second
3. **Multi-Tenancy** - Row-level isolation enforcement
4. **Communication Patterns** - REST vs WebSocket vs Pub/Sub
5. **Authentication** - JWT token flow and refresh mechanisms
6. **Feature Implementation** - End-to-end flow for Lightning Round
7. **Enterprise AI** - Tier-based model routing
8. **Backend Layers** - Separation of concerns and data flow
9. **Frontend State** - Zustand stores and TanStack Query integration

Use these as reference when implementing features and reviewing PRs.
