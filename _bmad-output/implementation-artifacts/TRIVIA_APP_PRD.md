# Product Requirements Document (PRD)
## Trivia App - Corporate Training Engagement Platform

**Version:** 1.0  
**Date:** January 19, 2026  
**Author:** Tim_D (Product Vision), Mary (Business Analyst Facilitation)  
**Status:** Ready for Development  

---

## 1. Executive Summary

### Product Vision

Trivia App is a Python-based engagement platform that solves corporate training's critical "cold start" problem by transforming disengaged training events into energizing, connected learning moments that drive talent retention, productivity, and organizational competitive advantage.

### Problem Statement

Organizations invest heavily in training but face persistent participant disengagement. People arrive physically but remain mentally absent—scrolling phones, thinking about work—resulting in:
- **Wasted training ROI** - Poor knowledge retention and skill transfer
- **Lost connection opportunities** - Training events should build team bonds but often feel solitary
- **Culture misalignment** - Training fails to reinforce organizational values
- **Talent risk** - Lack of visible investment in development drives turnover

### Solution Overview

A strategic trivia engagement tool that:
- **Facilitates cognitive transition** from work mode to learning mode
- **Creates low-stakes team competition** that builds rapport and psychological safety
- **Generates shared learning experiences** that become part of organizational culture
- **Provides persistent engagement** between formal events through mobile and chat integrations
- **Demonstrates ROI through analytics** showing training impact on knowledge retention and team cohesion

### Success Definition

MVP success = validated product/market fit demonstrating that trivia-based engagement meaningfully improves training event experience and organizational learning outcomes, with clear path to sustainable revenue model.

---

## 2. Product Positioning & Messaging

### Target Market (MVP Phase)

**Primary:** Mid-to-large enterprises (500-5000 employees) with mature training/HR functions
- L&D departments seeking engagement solutions
- Corporate training facilitators managing regular events
- HR teams responsible for onboarding and culture building

**Secondary (Phase 2+):**
- Educational institutions
- Professional certification bodies
- Client success/customer education teams

### Key Differentiators

1. **Corporate-First Design** - Purpose-built for corporate training context (not education gamification)
2. **Team Connection Focus** - Emphasizes rapport building, not just individual achievement
3. **Psychological Safety** - Designed to reduce training anxiety through team-based, low-stakes competition
4. **Engagement Science** - Grounded in habit formation (fitness app patterns), flow state (gaming), and adult learning principles
5. **Community Model** - Open-source question banks + community curation creates sustainable content growth
6. **Multiple Engagement Modes** - Live events + persistent coffee-break participation + async prep

### Value Proposition

**For Training Facilitators:**
- Deploy training events in <2 minutes
- Dramatically increase participant engagement and presence
- Get data on knowledge retention
- Reduce training anxiety through proven engagement mechanics

**For Participants:**
- Engaging alternative to boring training
- Build team connections through healthy competition
- Safe way to learn from peers
- Visible progress tracking and achievement

**For Organizations:**
- Demonstrate investment in employee development
- Improve training ROI through better retention and skill transfer
- Build culture alignment and shared organizational values
- Strategic talent retention tool (more cost-effective than hiring)

---

## 3. User Personas & Scenarios

### Persona 1: Training Facilitator (Laura)

**Background:** L&D professional, 8 years experience, moderate technical skill

**Goals:**
- Make training events engaging and memorable
- Measure what people actually learned
- Reduce time spent on administrative training setup
- See evidence of training ROI to justify program investment

**Pain Points:**
- Complex training software requires certification
- Participants mentally checked out (scrolling phones)
- Can't easily tell if training actually stuck
- Justifying training budget to finance becomes harder each year

**Scenarios:**
- Laura needs to run all-hands training next week for 150 people across two sites (50 in-person, 100 virtual)
- Laura wants to supplement her compliance training with engagement activities
- Laura needs to show her director that training actually improves team knowledge

### Persona 2: Team Member (Marcus)

**Background:** Software engineer, moderate interest in learning, prefers practical approaches

**Goals:**
- Learn what I need without wasting time
- Have fun with my teammates
- Feel like the company invests in my growth
- Understand how training connects to my career

**Pain Points:**
- Training feels like mandatory compliance, not real development
- Competitive testing makes me anxious
- Generic corporate training doesn't feel relevant
- No feedback on what I actually learned

**Scenarios:**
- Marcus gets invited to morning product training with his team
- Marcus sees a "coffee break trivia" challenge posted in Slack during the day
- Marcus wants to review product knowledge before a client meeting

### Persona 3: HR Leader (James)

**Background:** VP of HR, strategic focus, executive visibility

**Goals:**
- Improve training ROI and demonstrate impact
- Build culture and organizational alignment
- Reduce turnover through visible development investment
- Make training a competitive advantage in hiring

**Pain Points:**
- Training attendance doesn't correlate with actual skill development
- Hard to measure culture impact of training events
- Can't differentiate training effectiveness across programs
- Competitors using better engagement tools

**Scenarios:**
- James needs data showing training improves retention and performance
- James wants to pilot new training approach with key departments
- James is evaluating training platforms for enterprise adoption

---

## 4. Functional Requirements

### Feature Category 1: Core Facilitation

#### Feature 1.1: Lightning Round Opening Trivia

**Purpose:** Enable facilitators to launch engaging ice-breaker trivia that transitions participants from work mode to learning mode

**User Stories:**

**US-1.1.1:** As a facilitator, I can create a 3-5 question lightning round in less than 2 minutes so that training events start with energy and engagement.

**Acceptance Criteria:**
- [ ] Facilitator can launch new session with pre-built template in <2 minutes
- [ ] Template includes prompt to select question category (industry knowledge, company culture, professional backgrounds)
- [ ] Facilitator can quickly form teams (auto-assign or manual)
- [ ] Team size options: 3-5 people per team
- [ ] Session duration countdown visible (5-7 minutes)
- [ ] Questions display clearly on central screen (supports screen sharing)
- [ ] Participants answer on mobile devices simultaneously
- [ ] Real-time answer submission with clear "question locked" state
- [ ] Team scores update live during session

**US-1.1.2:** As a participant, I can quickly answer opening trivia questions on my mobile device so that I feel welcomed into the training moment.

**Acceptance Criteria:**
- [ ] Mobile interface loads within 2 seconds
- [ ] Question text readable on any device size
- [ ] Multiple choice options clearly clickable on mobile
- [ ] Answer submission requires single click/tap
- [ ] Clear visual feedback when answer submitted (button state change)
- [ ] Countdown timer visible for question window
- [ ] Team score visible after question closes

**US-1.1.3:** As a facilitator, I can see which teams are winning in real-time so that I can maintain momentum and celebrate progress.

**Acceptance Criteria:**
- [ ] Live scoreboard displays team names and scores
- [ ] Updates in real-time as answers come in
- [ ] Scoreboard visible on screen facilitator controls
- [ ] Final scores clearly announced at end of round
- [ ] Option to announce winning team or keep scores private

---

#### Feature 1.2: Post-Session Knowledge Check Trivia

**Purpose:** Assess knowledge retention through trivia that feels like continued gameplay rather than formal testing

**User Stories:**

**US-1.2.1:** As a facilitator, I can add a knowledge check at the end of training to assess what people actually learned.

**Acceptance Criteria:**
- [ ] Facilitator can configure post-session trivia from training event setup
- [ ] Select 8-10 questions from training content bank
- [ ] Add 1-2 "gotcha" questions designed to test application/synthesis
- [ ] Set difficulty (basic recall vs. application vs. synthesis)
- [ ] Configure scoring (all-or-nothing vs. partial credit)
- [ ] Set time limit per question (default 30-60 seconds)
- [ ] Decide if results public or private

**US-1.2.2:** As a participant, I can see immediate feedback on my answers to understand what I learned.

**Acceptance Criteria:**
- [ ] After answering, show: correct answer, explanation, why other options wrong
- [ ] For incorrect answers: highlight common misconceptions
- [ ] Explain correct concept briefly (1-2 sentences)
- [ ] No delay in feedback (instant gratification)
- [ ] Visual indicator: green for correct, red for incorrect
- [ ] Educational tone (not punitive)

**US-1.2.3:** As a facilitator, I can see which topics the group struggled with so I know what to reinforce.

**Acceptance Criteria:**
- [ ] Report shows questions answered correctly vs. incorrectly
- [ ] Identifies topics with <70% correct rate
- [ ] Shows individual and team performance
- [ ] Exportable results for further analysis
- [ ] Comparison to previous similar trainings (trending)

---

### Feature Category 2: Integration & Persistence

#### Feature 2.1: Video Conferencing Integration (Shallow/Mobile-First)

**Purpose:** Enable hybrid training where virtual and in-person participants compete fairly

**Technical Approach:** Web app on mobile devices (not deep SDK integration)

**User Stories:**

**US-2.1.1:** As an in-person participant, I can answer trivia on my phone while seeing questions displayed on the screen, just like remote participants.

**Acceptance Criteria:**
- [ ] Facilitator shares screen showing current question (simple design)
- [ ] Participants access web URL (unique session code) on phones
- [ ] All participants see same question displayed on screen simultaneously
- [ ] Participants answer on phones, scores update in real-time on screen
- [ ] No lag between screen and phone updates (sub-1 second latency)
- [ ] Works without Zoom/Teams/WebEx app integration (browser-based)

**US-2.1.2:** As a remote participant, I have the same experience as in-person participants.

**Acceptance Criteria:**
- [ ] Same mobile interface as in-person participants
- [ ] Same scoring and real-time updates
- [ ] Facilitator can see hybrid team scores
- [ ] No technical barriers for remote users

**US-2.1.3:** As a facilitator, I can manage hybrid sessions with minimal complexity.

**Acceptance Criteria:**
- [ ] Single session accommodates both in-person and remote
- [ ] Scoring treats all participants equally (no hybrid advantage)
- [ ] Can manually manage participant assignment to teams
- [ ] Clear instructions for sharing screen + phone participation

---

#### Feature 2.2: Coffee Break Trivia (Chat Bot Integration)

**Purpose:** Enable persistent trivia engagement outside formal events through team chat platforms

**Integration:** Slack and Microsoft Teams (initial support)

**User Stories:**

**US-2.2.1:** As a team member, I can answer daily trivia challenges in Slack without leaving my workflow.

**Acceptance Criteria:**
- [ ] Bot responds to `/trivia` command to start challenge
- [ ] Question posts in channel or via DM (configurable)
- [ ] Multiple choice options clearly formatted
- [ ] Participants reply with their answer in thread
- [ ] Bot accepts emoji reactions or text responses
- [ ] 24-hour window to answer (async participation)
- [ ] No scoring pressure (answers not public)

**US-2.2.2:** As a facilitator, I can schedule trivia to drop into team channels automatically.

**Acceptance Criteria:**
- [ ] Configure daily/weekly question drops
- [ ] Select question categories (company culture, compliance, product knowledge, etc.)
- [ ] Target specific channels or teams
- [ ] Preview questions before scheduling
- [ ] Pause/resume schedules as needed

**US-2.2.3:** As a team, we see coffee break trivia as part of our learning culture, not corporate compliance.

**Acceptance Criteria:**
- [ ] Questions feel relevant and interesting
- [ ] Mix of reinforcement (training-related) + culture (company knowledge)
- [ ] Tone is playful, not mandatory
- [ ] No leaderboards (psychological safety)
- [ ] Optional participation (never forced)

---

### Feature Category 3: Engagement & Motivation

#### Feature 3.1: Streak Tracking

**Purpose:** Create habit formation through visible participation progress

**User Stories:**

**US-3.1.1:** As a participant, I can see my participation streak and feel motivated to maintain it.

**Acceptance Criteria:**
- [ ] Visible streak counter: "Current Streak: 15 days"
- [ ] Streak increments for any trivia participation (formal events + coffee break)
- [ ] Resets if >24 hours without participation
- [ ] Displayed on personal dashboard
- [ ] Optional sharing to team chat
- [ ] Milestone celebrations at 7, 14, 30, 60 day marks

**US-3.1.2:** As a facilitator, I can see team participation streaks to understand engagement patterns.

**Acceptance Criteria:**
- [ ] Team dashboard shows individual streaks
- [ ] Can identify highly engaged vs. lapsed participants
- [ ] Streak data exportable for HR analytics

---

#### Feature 3.2: AI-Powered Knowledge Gap Analysis

**Purpose:** Provide personalized recommendations based on team learning profile

**MVP Implementation:** Rule-based logic (evolve to ML in v2+)

**User Stories:**

**US-3.2.1:** As a team, we receive trivia recommendations based on what we've struggled with.

**Acceptance Criteria:**
- [ ] System identifies topics with <70% correct rate
- [ ] Recommends follow-up challenges for low-performing areas
- [ ] Format: "Your team mastered Compliance! Try these Ethics scenarios?"
- [ ] Recommendations appear in chat bot or dashboard
- [ ] Teams can accept/decline recommendations
- [ ] Optional (never forced)

**US-3.2.2:** As a facilitator, I can see which topics my team should focus on.

**Acceptance Criteria:**
- [ ] Dashboard shows knowledge gap analysis
- [ ] Visual display of topic mastery levels
- [ ] Can manually add recommendations
- [ ] Export gap analysis for curriculum planning

---

#### Feature 3.3: Time-Limited Challenges (FOMO Mechanics)

**Purpose:** Create urgency and recurring engagement moments

**User Stories:**

**US-3.3.1:** As a team, we know about special time-limited challenges and feel motivated to participate.

**Acceptance Criteria:**
- [ ] "Flash Challenge" posted with clear deadline (24-48 hours)
- [ ] Clear messaging: "This challenge expires Sunday midnight!"
- [ ] Distinct from always-on coffee break trivia
- [ ] Special branding/notification to highlight urgency
- [ ] Weekly or bi-weekly cadence
- [ ] Themed challenges (Product Knowledge Week, Compliance Challenge, etc.)

**US-3.3.2:** As a facilitator, I can launch special challenges to drive engagement spikes.

**Acceptance Criteria:**
- [ ] Simple interface to schedule time-limited challenges
- [ ] Set duration, questions, difficulty
- [ ] Pre-built challenge templates for common themes
- [ ] Manual launch or scheduled deployment
- [ ] Analytics on participation in time-limited challenges

---

#### Feature 3.4: Progress Tracking Over Time

**Purpose:** Provide evidence of training ROI and learning growth

**User Stories:**

**US-3.4.1:** As an organization, I can see that training improves knowledge retention over time.

**Acceptance Criteria:**
- [ ] Historical dashboard showing learning trajectories
- [ ] Visualize question performance trends (did scores improve after training?)
- [ ] Track topics trending up vs. down
- [ ] Compare same questions asked at different times
- [ ] Team-level aggregation
- [ ] Show learning velocity: how quickly topics mastered

**US-3.4.2:** As an individual, I can see my learning progress.

**Acceptance Criteria:**
- [ ] Personal dashboard shows questions attempted over time
- [ ] Score improvement visible (5 weeks ago: 60%, now: 85%)
- [ ] Topics mastered vs. still developing
- [ ] Motivational messaging on progress

**US-3.4.3:** As a trainer, I can prove training effectiveness to executives.

**Acceptance Criteria:**
- [ ] Export report showing pre/post training scores
- [ ] Compare trainings (Onboarding v1 vs. v2 - which more effective?)
- [ ] ROI messaging: "This cohort shows 30% knowledge improvement"
- [ ] Executive summary for leadership presentations

---

### Feature Category 4: User Experience & Friction Reduction

#### Feature 4.1: Frictionless Onboarding

**Purpose:** Enable non-technical facilitators to deploy in <2 minutes

**User Stories:**

**US-4.1.1:** As a trainer with minimal tech skills, I can create and launch a trivia session in under 2 minutes.

**Acceptance Criteria:**
- [ ] Landing page: "Create New Session" button (prominent)
- [ ] Three-step wizard: (1) Name event, (2) Select questions, (3) Add teams
- [ ] Each step takes <30 seconds
- [ ] Pre-built templates for common events (All-Hands, Onboarding, Department Training)
- [ ] Template selection auto-populates questions
- [ ] Option to customize or use defaults
- [ ] "Launch Now" button deploys session immediately
- [ ] Share link auto-generated for participants
- [ ] Success confirmation with clear next steps

**US-4.1.2:** As a facilitator, I can use pre-built question banks without creating custom questions.

**Acceptance Criteria:**
- [ ] Company provides curated question libraries (company culture, values, products)
- [ ] Department libraries available
- [ ] One-click selection of question bank
- [ ] No need to write/import questions for MVP
- [ ] Simple UI for adding custom questions (future iteration)

**US-4.1.3:** As a participant, I receive clear instructions on how to join and participate.

**Acceptance Criteria:**
- [ ] Session link clear and simple (trivia.app/join/ABC123)
- [ ] Mobile page auto-detects device
- [ ] Single input field: "Enter team name"
- [ ] Join button immediately enters session
- [ ] Waiting screen shows: "Waiting for facilitator to start"
- [ ] No confusing options or settings

---

#### Feature 4.2: Real-Time Educational Feedback

**Purpose:** Transform assessment into teaching moment through immediate, rich feedback

**User Stories:**

**US-4.2.1:** As a participant, I immediately understand why my answer was right or wrong.

**Acceptance Criteria:**
- [ ] After question closes, show results screen with:
  - Correct answer clearly highlighted
  - Brief explanation (1-2 sentences) of correct concept
  - If wrong: common misconceptions explained
  - Visual indicator (green checkmark for correct, red X for wrong)
- [ ] Feedback screen visible for 5 seconds before next question
- [ ] Facilitator can extend pause time if discussing
- [ ] Tone is educational, not judgmental

**US-4.2.2:** As a facilitator, I can verbally discuss answers while feedback displays.

**Acceptance Criteria:**
- [ ] Pause button to freeze feedback screen
- [ ] Facilitator can extend time for Q&A
- [ ] Resume button to move to next question
- [ ] Audio/visual synced (no lag)

---

### Feature Category 5: Extended Use Cases

#### Feature 5.1: New Hire Onboarding Module

**Purpose:** Integrate trivia into onboarding process to accelerate learning and peer bonding

**User Stories:**

**US-5.1.1:** As a new hire, I learn company culture and values through engaging trivia with my onboarding cohort.

**Acceptance Criteria:**
- [ ] Dedicated "Onboarding Learning Path" available
- [ ] Trivia topics: company culture, values, products, team structures, policies
- [ ] Cohort-based competition (new hires together)
- [ ] Multiple sessions over first week
- [ ] Progress toward "First Week Knowledge" badge
- [ ] Results feed into onboarding manager dashboard

**US-5.1.2:** As an onboarding manager, I can track new hire learning progress.

**Acceptance Criteria:**
- [ ] Dashboard showing onboarding cohort trivia performance
- [ ] Identify struggling new hires for additional support
- [ ] Track retention correlations (engaged onboarders → longer tenure?)

---

#### Feature 5.2: Client/Partner Education Platform (Future - Post-MVP)

**Purpose:** Enable enterprise customers to train their teams on products

**Note:** Deferred to Phase 2+ (white-label licensing)

**High-level Concept:**
- White-label interface for customer success teams
- Embed trivia into customer training portals
- Custom question banks for customer-specific content
- New revenue stream: customer education licensing

---

#### Feature 5.3: Event Sponsorship/Conference Mode (Future - Post-MVP)

**Purpose:** Deploy at conferences and trade shows for brand engagement and lead generation

**Note:** Deferred to Phase 2+ (event/sponsorship tier)

**High-level Concept:**
- Branded booth trivia experiences
- Attendee competitions with prizes
- Lead capture (email for trivia leaderboard)
- Measurable engagement metrics for marketing

---

### Feature Category 6: Leadership Model Reversals

#### Feature 6.1: Peer-Led Session Mode

**Purpose:** Empower any team member to launch sessions without facilitator training

**User Stories:**

**US-6.1.1:** As a team member (not official trainer), I can launch a trivia session for my team.

**Acceptance Criteria:**
- [ ] Same simple 3-step wizard as facilitator
- [ ] No special permissions required
- [ ] Pre-built templates available
- [ ] Can be launched spontaneously during team meetings
- [ ] Results tracked in team dashboard
- [ ] Enables grassroots adoption

**US-6.1.2:** As an organization, I can see peer-led sessions in analytics.

**Acceptance Criteria:**
- [ ] Distinguish facilitator-led vs. peer-led sessions
- [ ] Track adoption across organization
- [ ] Identify high-engagement teams driving adoption

---

#### Feature 6.2: Async-Before-Sync Workflow

**Purpose:** Enable solo practice before team competitions

**User Stories:**

**US-6.2.1:** As a team member, I can practice alone before team competition.

**Acceptance Criteria:**
- [ ] "Practice Mode" available for any question bank
- [ ] Solo participant answers questions
- [ ] Receives immediate feedback
- [ ] No scoring or competition pressure
- [ ] Results optional (can stay private)
- [ ] Prepares individuals for team sessions

**US-6.2.2:** As a team, we compare practice results before live competition.

**Acceptance Criteria:**
- [ ] Team dashboard shows who practiced
- [ ] Compare individual scores (private, not public leaderboard)
- [ ] Discuss results before live session
- [ ] Builds collective confidence

---

#### Feature 6.3: Observer Mode

**Purpose:** Enable low-pressure participation for anxious or new participants

**User Stories:**

**US-6.3.1:** As a participant concerned about competition, I can observe first before competing.

**Acceptance Criteria:**
- [ ] "Watch Mode" option when joining session
- [ ] See all questions and answers as they're revealed
- [ ] See team scores (no pressure)
- [ ] Can transition to active participation mid-session
- [ ] Reduces performance anxiety

**US-6.3.2:** As a facilitator, I can encourage observers to participate.

**Acceptance Criteria:**
- [ ] Visible indicator of observers
- [ ] Facilitator can invite observers to join
- [ ] Warm welcome messaging for observers
- [ ] Psychological safety maintained

---

#### Feature 6.4: Enterprise AI Model Selection

**Purpose:** Enable enterprise organizations to customize AI model selection for events while maintaining security and governance at other tiers

**User Stories:**

**US-6.4.1:** As an enterprise facilitator, I can select from approved AI models when creating trivia events.

**Acceptance Criteria:**
- [ ] Enterprise tier only: model selection available
- [ ] Dropdown showing available models (default: Microsoft Copilot or organization-selected model)
- [ ] Model selection appears in session setup wizard
- [ ] Selected model used for generating explanations, hints, and feedback
- [ ] Selection persists as organization default (can be overridden per-event)
- [ ] Clear labeling: "GPT-5.1-Codex-Max" vs. other available options
- [ ] Feature locked/hidden for free and premium tiers (shows selected org model only)

**US-6.4.2:** As an enterprise admin, I can set default AI model and approved models for all facilitators.

**Acceptance Criteria:**
- [ ] Admin console: "AI Model Configuration" section
- [ ] Set organization-wide default model
- [ ] Whitelist approved models available to facilitators
- [ ] Audit log: track which facilitators use which models
- [ ] Can restrict to single model or allow facilitator choice
- [ ] Default: Microsoft Copilot (fallback for all orgs not configured)
- [ ] Alternative: API call to organization's preferred model provider
- [ ] Configuration tied to organization profile (not user)

**US-6.4.3:** As the product, I route model requests appropriately based on subscription tier.

**Acceptance Criteria:**
- [ ] Free tier: locked to Microsoft Copilot (no selection)
- [ ] Premium tier: locked to organization-selected default model (no selection)
- [ ] Enterprise tier: facilitators can select from approved models per event
- [ ] API layer: transparent model routing based on tier and org config
- [ ] Fallback to Microsoft Copilot if model unavailable
- [ ] Error handling: graceful degradation if selected model fails

**US-6.4.4:** As an organization, I can integrate with my preferred AI API provider.

**Acceptance Criteria:**
- [ ] Admin console: "AI Provider Integration" section
- [ ] Configure API keys securely (encrypted at rest, httpOnly storage)
- [ ] Support for multiple providers: OpenAI, Anthropic, Azure OpenAI, etc.
- [ ] Test connection: validate API credentials before saving
- [ ] Usage tracking: see API call volume per model per org
- [ ] Cost allocation: understand spend by model and session
- [ ] Failover: automatically fall back to Microsoft Copilot on auth failure
- [ ] Documentation: clear setup guide for each provider

---

## 5. Non-Functional Requirements

### Performance Requirements

| Requirement | Target | Notes |
|-------------|--------|-------|
| Mobile app load time | <2 seconds | First paint on 4G network |
| Answer submission latency | <500ms | Acceptable for real-time gameplay |
| Score update latency | <1 second | Real-time feel for facilitator display |
| Concurrent participants | 5000+ per event | Support large company-wide events |
| Availability | 99.5% uptime | Corporate SLA expectation |
| Database query response | <100ms | Responsive experience |

### Security Requirements

- [ ] HTTPS/TLS encryption for all data in transit
- [ ] Password hashing (bcrypt or equivalent)
- [ ] Rate limiting on API endpoints (prevent abuse)
- [ ] SQL injection prevention (parameterized queries)
- [ ] CSRF protection for forms
- [ ] Input validation on all user inputs
- [ ] Secure session management (httpOnly cookies)
- [ ] Data encryption at rest (MVP: application-level, post-MVP: DB-level)
- [ ] GDPR compliance (data export, deletion)
- [ ] SOC 2 audit readiness (post-MVP)

### Scalability Requirements

- [ ] Horizontal scaling: stateless app servers
- [ ] Database: connection pooling, read replicas for analytics
- [ ] Static assets: CDN delivery
- [ ] Real-time: WebSocket scalability (Redis Pub/Sub or similar)
- [ ] Load testing: simulate 5000 concurrent users
- [ ] Auto-scaling: infrastructure auto-scales with load

### Accessibility Requirements

- [ ] WCAG 2.1 AA compliance
- [ ] Mobile-first responsive design
- [ ] Touch targets minimum 48x48px
- [ ] Color contrast ratio 4.5:1 for text
- [ ] Keyboard navigation support
- [ ] Screen reader compatible
- [ ] No flashing content >3Hz

### Browser & Device Support

- [ ] Chrome (latest 2 versions)
- [ ] Safari (latest 2 versions)
- [ ] Firefox (latest 2 versions)
- [ ] Mobile Safari iOS 12+
- [ ] Chrome Mobile Android 9+
- [ ] Responsive design: 320px - 1920px
- [ ] Touch-optimized mobile experience

---

## 6. Technical Architecture

### Technology Stack (Python-Based)

**Backend:**
- Framework: FastAPI (modern, async-native, excellent for real-time)
- Runtime: Python 3.10+
- Task queue: Celery (async tasks, background jobs)
- Real-time: WebSockets via FastAPI
- Message queue: Redis (PubSub for real-time scoring)

**Frontend:**
- Framework: React or Vue.js (lightweight, mobile-optimized)
- HTTP Client: Axios or Fetch API
- Real-time: WebSocket client
- Responsive design: Tailwind CSS or Bootstrap
- Mobile-first approach

**Database:**
- Primary: PostgreSQL 13+ (relational data)
- Cache: Redis (real-time scoring, sessions)
- Analytics: Consider PostGIS or separate analytics DB (future)

**Deployment:**
- Container: Docker
- Orchestration: Kubernetes or simplified container service (AWS ECS, Google Cloud Run)
- CI/CD: GitHub Actions or GitLab CI
- Infrastructure: AWS, Google Cloud, or Azure

**Third-Party Integrations:**
- Slack API: @slack/bolt-js or python-slack-sdk
- Microsoft Teams: BotFramework SDK
- Authentication: Optional (Auth0, Okta for enterprise SSO - post-MVP)

### Architecture Diagram (High-Level)

```
┌─────────────────────────────────────────────────────┐
│                  Web Browser / Mobile App            │
│  (React/Vue frontend - responsive, mobile-first)    │
└──────────────────┬──────────────────────────────────┘
                   │
    HTTP + WebSocket (Real-time scoring)
                   │
┌──────────────────▼──────────────────────────────────┐
│           FastAPI Backend (Python)                   │
│  - REST API endpoints                               │
│  - WebSocket handlers for real-time updates         │
│  - Session management                               │
│  - Authentication/Authorization                     │
└──────┬──────────────────────────────────────────────┘
       │
       ├─────────────────────────────────────────────┐
       │                                              │
       ▼                                              ▼
┌──────────────────┐                        ┌──────────────────┐
│   PostgreSQL DB  │ Redis Cache/Sessions   │ Redis PubSub     │
│   - Users        │ - Session data         │ (Real-time       │
│   - Questions    │ - Streaks              │  scoring         │
│   - Teams        │ - User prefs           │  updates)        │
│   - Results      │                        │                  │
└──────────────────┘                        └──────────────────┘
       │
       └─────────────────────────────────────────────┐
                                                      │
                                        ┌─────────────▼──────────────┐
                                        │ External Integrations      │
                                        │ - Slack Bot                │
                                        │ - Teams Bot                │
                                        │ - Analytics (future)       │
                                        └────────────────────────────┘
```

### Database Schema (MVP)

```sql
-- Users table
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  password_hash VARCHAR(255),
  organization_id UUID REFERENCES organizations(id),
  role ENUM('facilitator', 'participant', 'admin'),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Organizations table
CREATE TABLE organizations (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  slug VARCHAR(255) UNIQUE NOT NULL,
  plan ENUM('free', 'premium', 'white_label'),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Sessions table (individual trivia events)
CREATE TABLE sessions (
  id UUID PRIMARY KEY,
  organization_id UUID REFERENCES organizations(id),
  facilitator_id UUID REFERENCES users(id),
  name VARCHAR(255) NOT NULL,
  status ENUM('setup', 'active', 'completed') DEFAULT 'setup',
  event_type ENUM('opening', 'assessment', 'coffee_break', 'challenge') DEFAULT 'opening',
  question_bank_id UUID REFERENCES question_banks(id),
  started_at TIMESTAMP,
  ended_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Teams table
CREATE TABLE teams (
  id UUID PRIMARY KEY,
  session_id UUID REFERENCES sessions(id),
  name VARCHAR(255) NOT NULL,
  score INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Participants table (join table for users + teams)
CREATE TABLE participants (
  id UUID PRIMARY KEY,
  team_id UUID REFERENCES teams(id),
  user_id UUID REFERENCES users(id),
  score INT DEFAULT 0,
  streak INT DEFAULT 0,
  last_participation_date DATE,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Questions table
CREATE TABLE questions (
  id UUID PRIMARY KEY,
  question_bank_id UUID REFERENCES question_banks(id),
  question_text TEXT NOT NULL,
  question_type ENUM('multiple_choice') DEFAULT 'multiple_choice',
  correct_answer VARCHAR(255) NOT NULL,
  explanation TEXT,
  difficulty ENUM('easy', 'normal', 'hard') DEFAULT 'normal',
  topic VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Answer options table (for multiple choice)
CREATE TABLE answer_options (
  id UUID PRIMARY KEY,
  question_id UUID REFERENCES questions(id),
  option_text VARCHAR(255) NOT NULL,
  is_correct BOOLEAN DEFAULT FALSE,
  display_order INT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Question banks (curated sets of questions)
CREATE TABLE question_banks (
  id UUID PRIMARY KEY,
  organization_id UUID REFERENCES organizations(id),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  category ENUM('onboarding', 'compliance', 'product', 'culture', 'custom'),
  is_public BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Session results table
CREATE TABLE session_results (
  id UUID PRIMARY KEY,
  session_id UUID REFERENCES sessions(id),
  participant_id UUID REFERENCES participants(id),
  question_id UUID REFERENCES questions(id),
  answer_given VARCHAR(255),
  is_correct BOOLEAN,
  response_time_ms INT,
  answered_at TIMESTAMP DEFAULT NOW()
);
```

### API Endpoints (MVP - REST)

```
Auth & Sessions
  POST   /api/v1/auth/register
  POST   /api/v1/auth/login
  POST   /api/v1/auth/logout
  GET    /api/v1/auth/me

Sessions
  POST   /api/v1/sessions                 # Create new session
  GET    /api/v1/sessions/{id}            # Get session details
  PUT    /api/v1/sessions/{id}            # Update session
  DELETE /api/v1/sessions/{id}            # Delete session
  POST   /api/v1/sessions/{id}/start      # Start trivia
  POST   /api/v1/sessions/{id}/end        # End trivia

Teams
  POST   /api/v1/sessions/{id}/teams      # Create team
  GET    /api/v1/sessions/{id}/teams      # List teams
  PUT    /api/v1/sessions/{id}/teams/{id} # Update team

Participants
  POST   /api/v1/teams/{id}/join          # User joins team
  POST   /api/v1/teams/{id}/leave         # User leaves team

Questions
  GET    /api/v1/sessions/{id}/next-question  # Get next question
  POST   /api/v1/sessions/{id}/answer         # Submit answer

Results
  GET    /api/v1/sessions/{id}/results    # Session results
  GET    /api/v1/users/{id}/history       # User learning history

Real-time (WebSocket)
  /ws/sessions/{id}  # Real-time updates during session
    - question_started
    - answer_submitted
    - question_ended
    - session_ended
    - score_updated
```

### Real-Time Architecture (WebSocket)

```javascript
// Client connects to WebSocket
const ws = new WebSocket('ws://api.trivia.app/ws/sessions/{sessionId}');

// Receives real-time events:
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  switch(data.type) {
    case 'question_started':
      // Display new question to all participants
      displayQuestion(data.question);
      break;
    case 'answer_submitted':
      // Update participant count, animate answer
      updateParticipantProgress(data.answered_count);
      break;
    case 'question_ended':
      // Show results
      showResults(data.results);
      break;
    case 'score_updated':
      // Update team scoreboard
      updateScoreboard(data.scores);
      break;
  }
};
```

---

## 7. Data Model & Analytics

### Key Metrics Tracked

**Learning Outcomes:**
- Questions answered correctly/incorrectly (by topic)
- Knowledge gaps identified (topics <70% correct)
- Learning improvement over time (trending)
- Retention metrics (same questions asked weeks later)

**Engagement Metrics:**
- Participation rate (% of participants actively engaged)
- Session duration and intensity
- Streak consistency (habit formation)
- Repeat session frequency

**Business Metrics:**
- Free tier → Premium conversion rate
- Session frequency per organization
- User retention curves
- Feature adoption rates

**Organizational Impact:**
- Training ROI (knowledge improvement vs. investment)
- Team connection perception (survey correlation)
- Culture alignment metrics
- Retention correlation (do trivia participants stay longer?)

---

## 8. Integration Requirements

### Slack Bot Integration

**MVP Scope:**
- `/trivia` command to start coffee break challenge
- Auto-scheduled daily question drops
- DM-based response collection
- Private responses (no public leaderboards)

**Technical Approach:**
- Use python-slack-sdk
- Slash command handling via webhook
- Event subscription for message reactions
- Scheduled jobs for daily drops (Celery + APScheduler)

### Microsoft Teams Bot Integration

**MVP Scope:**
- Similar to Slack
- Teams connector for bot deployment
- Adaptive cards for question display

**Technical Approach:**
- Use botframework-connector SDK
- Teams manifest configuration
- Card rendering for Q&A display

### Video Conferencing Integration (Shallow)

**MVP Scope:**
- No deep SDK integration
- Web URL shared with participants
- Screen sharing by facilitator
- Mobile browsers for participants

**Technical Approach:**
- Simple HTTPS web app
- Responsive mobile interface
- No native app integration needed

---

## 9. Success Metrics & KPIs

### MVP Success Criteria (Phase 1: 0-3 months)

**Product Validation:**
- [X] Core trivia gameplay works smoothly
- [X] Mobile interface responsive and intuitive
- [X] <2 minute setup time for facilitators
- [X] Real-time scoring/updates feel responsive
- [X] Integration with Slack/Teams functional

**User Adoption:**
- [ ] 100+ organizations signed up (free tier)
- [ ] 1000+ active participants
- [ ] 500+ sessions created
- [ ] 20% week-over-week growth

**Business Viability:**
- [ ] 10-15% free → premium conversion rate
- [ ] 3-5 white-label customers (pilot)
- [ ] $10K+ MRR (premium + white-label combined)
- [ ] NPS >40 (net promoter score)

**Engagement Quality:**
- [ ] Average session participation >80%
- [ ] User retention day 7: >60%
- [ ] User retention day 30: >40%
- [ ] Session frequency: >2x per week for engaged orgs

---

## 10. Release Plan & Timeline

### Phase 1: MVP Launch (Months 1-3)

**Month 1: Foundation**
- Authentication system
- Basic question bank + data model
- Session creation wizard
- Team management
- Real-time WebSocket infrastructure

**Month 2: Core Features**
- Lightning round opening trivia
- Knowledge check assessment
- Mobile interface optimization
- Slack bot integration
- Real-time score updates

**Month 3: Polish & Analytics**
- Frictionless onboarding refinement
- Educational feedback display
- Basic analytics dashboard
- Performance optimization
- Launch to beta users (50-100 orgs)

**Deliverable:** MVP ready for public launch

### Phase 2: Market Fit Validation (Months 4-6)

**Month 4: Expansion Features**
- Coffee break trivia improvements
- Streak tracking
- AI gap analysis (rule-based)
- Time-limited challenges
- Video conferencing integration

**Month 5: Monetization**
- Premium tier analytics dashboard
- Pricing implementation
- White-label tier setup
- Payment processing (Stripe)

**Month 6: Enterprise Readiness**
- Performance optimization for large events (1000+ participants)
- Advanced admin features
- Enhanced security/compliance
- White-label customer onboarding

**Deliverable:** Product/market fit validated, sustainable revenue flowing

### Phase 3+: Scale & Expansion (Months 7+)

**See Backlog section (Section 12) for prioritized features**

---

## 11. Assumptions & Dependencies

### Assumptions

1. **Adoption Assumption:** Corporate L&D departments will adopt gamified training if friction removed (MVP validates this)
2. **Engagement Assumption:** Team-based competition without leaderboards maintains psychological safety while driving engagement
3. **Revenue Assumption:** Organizations will pay for advanced analytics + white-label capabilities
4. **Market Assumption:** Mid-to-large enterprises have budget for training enhancement tools
5. **Community Assumption:** Open-source question bank model can sustain high-quality content

### Dependencies

- Cloud infrastructure (AWS/GCP/Azure) for hosting and scaling
- Python 3.10+ runtime
- PostgreSQL database service
- Redis for caching and real-time
- Slack/Teams API availability
- Third-party payment processor (Stripe for white-label)

---

## 12. Backlog for Future Iterations

### Phase 2+ Feature Backlog (Prioritized)

**Tier 1: High Priority (Months 4-6)**
1. Coffee break trivia improvements
2. Streak tracking (habit formation)
3. Knowledge gap analysis (AI recommendations)
4. Time-limited challenges
5. Progress tracking dashboard
6. New hire onboarding module
7. Enterprise AI Model Selection (GPT-5.1-Codex-Max and provider integration)

**Tier 2: Medium Priority (Months 7-9)**
1. Video conferencing deep integration (Zoom, Teams native)
2. Multiple question types (true/false, short answer, ranking)
3. Advanced admin dashboards
4. Role-based permissions
5. Competency mapping framework
6. Peer learning/mentorship
7. Micro-credentialing and badges
8. AI Model cost optimization and usage analytics

**Tier 3: Lower Priority (Months 10+)**
1. Streaming service personalization patterns
2. Seasonal content and battle pass mechanics
3. Episodic question releases
4. Community features and social proof
5. Interview assessment tool
6. LMS integrations
7. Performance management integration

---

## 13. Success Stories & Use Cases

### Use Case 1: All-Hands Training Event

**Scenario:** Laura (L&D Manager) needs to train 200 people (150 in-person, 50 remote) on new product features

**Before Trivia App:**
- 30% of participants mentally checked out
- Unknown how many people actually learned
- Post-event: "Did anyone learn anything?" No data

**With Trivia App:**
- Laura sets up session in 2 minutes using "product training" template
- Lightning round to energize everyone (people actually paying attention)
- Post-training: knowledge check shows 85% mastery
- Analytics show 3 teams with gaps → can follow up with targeted training
- Executive report: "Training improved product knowledge 30% vs. last quarter"

**Outcome:** Training ROI proven, budget approved for next quarter

---

### Use Case 2: New Hire Onboarding

**Scenario:** Marcus starts at company, goes through 3-day onboarding

**Before Trivia App:**
- Day 1: PowerPoint about company values (boring, doesn't stick)
- Meeting teammates, but no shared learning moments
- Unsure what he actually learned
- Takes 2-3 months to fully understand company

**With Trivia App:**
- Day 1 afternoon: Marcus joins onboarding cohort trivia
- Learns about culture, values, products through competition with 4 other new hires
- Immediate bonding with cohort through shared experience
- Gets feedback: "You're strong on product knowledge, review compliance policies"
- Day 2-3: Coffee break trivia keeps reinforcing what he learned
- After first week: Manager sees Marcus scored high on culture/values → faster integration

**Outcome:** Faster onboarding, new hire cohort bonding, data-driven follow-up

---

### Use Case 3: Compliance Training

**Scenario:** Organization needs annual compliance certification

**Before Trivia App:**
- Mandatory boring training (people do it to check box)
- No engagement, no retention
- Next year: same mistakes, same training needed

**With Trivia App:**
- Compliance training delivered as engaging trivia
- Coffee break challenges keep compliance top-of-mind
- Post-training: knowledge check proves understanding
- Quarterly "compliance refresh" challenge keeps skills fresh
- Next year: renewal training shows 40% higher scores than year before

**Outcome:** Real learning instead of compliance theater

---

## 14. Appendix: Glossary

| Term | Definition |
|------|-----------|
| **Facilitator** | Person leading training event (trainer, L&D, team leader) |
| **Participant** | Person taking trivia in event |
| **Team** | Group of 3-5 participants competing together |
| **Session** | Individual trivia event (with unique questions, teams, scoring) |
| **Question Bank** | Curated set of related questions (e.g., "Product Knowledge") |
| **Knowledge Gap** | Topic where team showed <70% correct rate |
| **Streak** | Consecutive days/weeks of trivia participation |
| **Flash Challenge** | Time-limited trivia (24-48 hour window) creating urgency |
| **White-Label** | Branded interface for enterprise customers |
| **Coffee Break Trivia** | Async trivia integrated into Slack/Teams for daily engagement |
| **Observer Mode** | Low-pressure viewing of trivia without competitive scoring |
| **Enterprise Tier** | Premium subscription with model selection and governance features |
| **AI Model Selection** | Enterprise feature allowing facilitators to choose from approved AI models |
| **Model Provider Integration** | Enterprise feature for connecting to custom AI API providers (OpenAI, Anthropic, etc.) |
| **Microsoft Copilot** | Default AI model used across free and standard tiers |

---

## 15. Sign-Off

**Product Vision Owner:** Tim_D  
**Business Analyst:** Mary  
**Status:** Ready for Development  
**Approval Required From:** Engineering Lead, CTO  

---

**Version History:**

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-19 | Initial PRD from product design brief |

---

**Document Control:**

- Owner: Tim_D (Product)
- Last Updated: 2026-01-19
- Review Cycle: Quarterly or as major changes occur
- Distribution: Development team, Product stakeholders

