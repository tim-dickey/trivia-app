# UI/UX Specifications
## Trivia App - Corporate Training Engagement Platform

**Version:** 1.0  
**Date:** January 19, 2026  
**Status:** Ready for Design & Development  

---

## 1. Design Philosophy & Principles

### Core Principles

**1. Frictionless Experience**
- Every action should require minimal clicks/taps
- Clear call-to-action buttons
- Progressive disclosure (advanced options hidden until needed)
- Mobile-first responsive design

**2. Psychological Safety**
- Avoid competitive anxiety through aggressive leaderboards
- Celebratory feedback (not punitive)
- Color coding: green for success, neutral for attempts
- No public shaming or exposure

**3. Clarity Over Cleverness**
- Simple language, no jargon
- Visual hierarchy clear (headers, buttons, spacing)
- Status always clear (what's happening, what's next)
- Error messages helpful, not technical

**4. Mobile-First**
- Optimized for 320px - 1920px width
- Touch targets minimum 48x48px
- Finger-friendly spacing
- Fast loading (<2 seconds)

**5. Accessibility**
- WCAG 2.1 AA compliance
- Color contrast 4.5:1 minimum
- Keyboard navigation support
- Screen reader compatible

---

## 2. Design System

### Color Palette

**Primary Colors:**
- **Primary Blue:** `#0066FF` (CTAs, key actions)
- **Success Green:** `#00B34D` (correct answers, completion)
- **Warning Orange:** `#FF9500` (time limits, urgency)
- **Neutral Gray:** `#F5F5F5` (backgrounds)
- **Dark Gray:** `#333333` (text)

**Semantic Colors:**
- **Correct Answer:** `#00B34D` (green) with checkmark
- **Incorrect Answer:** `#E74C3C` (red) with X
- **Neutral Attempt:** `#95A5A6` (gray) with dash
- **Active/Hover:** Darker shade of primary blue

### Typography

**Font Family:** Inter or Open Sans (system font fallback)

**Font Sizes:**
- H1 (Page Title): 32px, bold, line-height 1.2
- H2 (Section Title): 24px, bold, line-height 1.3
- H3 (Subsection): 18px, semi-bold, line-height 1.4
- Body Text: 16px, regular, line-height 1.5
- Small Text: 14px, regular, line-height 1.4
- Button Text: 16px, semi-bold
- Question Text: 18px, regular, line-height 1.6

### Spacing Scale

- **xs:** 4px
- **sm:** 8px
- **md:** 16px
- **lg:** 24px
- **xl:** 32px
- **2xl:** 48px

### Components

**Buttons:**
- **Primary Button:** Blue background, white text, rounded corners (8px)
- **Secondary Button:** Blue outline, blue text, rounded corners (8px)
- **Danger Button:** Red background, white text (for destructive actions)
- **Disabled Button:** Gray background, gray text, 50% opacity
- **Size:** 44px height minimum for mobile touch targets

**Cards:**
- White background, subtle shadow (0 2px 8px rgba(0,0,0,0.1))
- Rounded corners (8px)
- Padding: 16px-24px
- Hover effect: shadow elevation

**Input Fields:**
- 44px minimum height
- Blue border on focus
- 12px padding
- Clear label above
- Error state: red border + error message

**Badge:**
- Padding: 4px 12px
- Border radius: 12px
- Font size: 12px
- Background: light gray, text: dark gray

---

## 3. Key User Flows

### Flow 1: Facilitator - Create & Launch Session (MVP Focus)

**Goal:** Enable facilitator to create and launch session in <2 minutes

```
Start
  ↓
Landing Page
  ↓
"Create New Session" CTA
  ↓
Step 1: Session Details
  ├─ Name: "All-Hands Product Training"
  ├─ Event Type: "Training Event" (dropdown)
  ├─ Select Template: "Lightning Round" / "Assessment" / "Custom"
  ↓
Step 2: Questions
  ├─ Show pre-built questions from selected template
  ├─ Option to use default or customize
  ├─ Quick preview of questions
  ↓
Step 3: Teams
  ├─ Number of teams: slider (1-20)
  ├─ Auto-assign participants or manual entry
  ├─ Can skip for now
  ↓
Review & Launch
  ├─ Preview session summary
  ├─ Generate share link
  ├─ "Launch Now" button
  ↓
Session Active
  ├─ Display questions on screen
  ├─ Show live scoring
  ├─ Manage question progression
  ↓
End
```

**Wireframe - Session Creation Wizard:**

```
┌─────────────────────────────────────────────┐
│ Trivia App - Create Session                 │
├─────────────────────────────────────────────┤
│                                             │
│ Step 1 of 3: Session Details               │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    │
│                                             │
│ Session Name *                              │
│ ┌────────────────────────────────────────┐ │
│ │ All-Hands Product Training             │ │
│ └────────────────────────────────────────┘ │
│                                             │
│ Event Type *                                │
│ ┌────────────────────────────────────────┐ │
│ │ Training Event              ⌄           │ │
│ └────────────────────────────────────────┘ │
│                                             │
│ Select Template                             │
│ ┌─────────────┐ ┌──────────────┐ ┌───────┐│
│ │ 🎯 Opening  │ │ ✓ Assessment │ │Custom ││
│ │  Trivia     │ │               │ │       ││
│ └─────────────┘ └──────────────┘ └───────┘│
│                                             │
│                  ┌──────────┬────────────┐  │
│                  │ < Back   │ Next  >   │  │
│                  └──────────┴────────────┘  │
│                                             │
└─────────────────────────────────────────────┘
```

---

### Flow 2: Participant - Join & Answer (Mobile-Optimized)

**Goal:** Participant quickly joins and answers trivia with minimal friction

```
Receive Link (Slack/Email)
  ↓
Click Link → Mobile Browser
  ↓
Join Screen
  ├─ Session name displayed
  ├─ "Enter Team Name" input
  ├─ "Join Now" button
  ↓
Waiting Screen
  ├─ "Waiting for facilitator to start..."
  ├─ Your Team: [Team Name]
  ├─ Team Members: [List]
  ↓
Question Display
  ├─ Question text (large, readable)
  ├─ Timer countdown (30-60 seconds)
  ├─ 4 answer options (single tap each)
  ↓
Answer Submitted
  ├─ Visual feedback: "Submitted!"
  ├─ Brief animation
  ├─ Wait for results
  ↓
Results Screen
  ├─ Correct answer highlighted
  ├─ Your answer highlighted
  ├─ Explanation of answer
  ├─ Current team score
  ↓
Next Question or Session End
  ↓
End
```

**Wireframe - Mobile Question Screen:**

```
┌─────────────────────────────┐
│ Trivia App                  │
├─────────────────────────────┤
│                             │
│ All-Hands Training      ⏱️ 45│
│                             │
├─────────────────────────────┤
│                             │
│ What is our company's core │
│ value?                      │
│                             │
├─────────────────────────────┤
│                             │
│ ☐ Innovation & Speed       │
│                             │
│ ☐ Customer Excellence      │
│                             │
│ ☐ Integrity & Trust        │
│                             │
│ ☐ Growth & Learning        │
│                             │
├─────────────────────────────┤
│ Your Team: Engineering      │
│ Team Score: 280 pts        │
│                             │
└─────────────────────────────┘
```

---

### Flow 3: Facilitator - Monitor Live Session

**Goal:** Facilitator controls session progression and monitors engagement

```
Session Started
  ↓
Facilitator Dashboard
  ├─ Current question displayed
  ├─ Live team scoreboard
  ├─ Participant progress bar (how many answered)
  ├─ Question timer
  ↓
Control Options
  ├─ Extend time on current question
  ├─ Skip question
  ├─ Move to next question
  ├─ End session early
  ↓
Between Questions
  ├─ Show results/explanation
  ├─ Display updated scores
  ├─ Facilitator can discuss
  ↓
Session End
  ├─ Final scores
  ├─ Winning team celebration
  ├─ Generate results link
  ↓
End
```

**Wireframe - Facilitator Control Screen:**

```
┌──────────────────────────────────────────────────┐
│ Trivia Facilitator - Control Panel               │
├──────────────────────────────────────────────────┤
│                                                  │
│ Current Question: 3 of 10          ⏱️ 45 seconds │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    │
│                                                  │
│ "What is our product roadmap for Q2?"           │
│                                                  │
│ Participants Answered: ██████░░░░░░ 65%         │
│                                                  │
│ TEAM SCOREBOARD:                                │
│ ┌────────────────────────────────────────────┐ │
│ │ 🥇 Engineering  ████████  420 pts  ✓ Ready │ │
│ │ 🥈 Marketing    ████░░░░  320 pts  ✓ Ready │ │
│ │ 🥉 Sales        ███░░░░░  280 pts  ✓ Ready │ │
│ └────────────────────────────────────────────┘ │
│                                                  │
│ ┌──────────────┬─────────────┬────────────────┐ │
│ │ ⏸️ Pause     │ ⏭️ Next Q   │ 🎬 End Session │ │
│ └──────────────┴─────────────┴────────────────┘ │
│                                                  │
│ Share Link: trivia.app/join/ABC123             │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 4. Page/Screen Specifications

### Screen 1: Landing Page (Unauthenticated User)

**Purpose:** Clear value prop, drive signup or login

**Key Elements:**
- Hero headline: "Make Training Unforgettable"
- Subheading: "Engage your team with trivia that builds culture"
- CTA buttons: "Get Started" (primary), "Learn More" (secondary)
- Social proof: "Join 1000+ organizations"
- Feature highlights (3 icons + text):
  - ⚡ Set up in 2 minutes
  - 🎯 Increase engagement 80%
  - 📊 Measure training ROI

**Layout:**
- Hero section (60vh): background image or gradient
- Features section (40vh): 3-column grid
- CTA section: "Ready to try?"
- Footer: links, social, support

---

### Screen 2: Dashboard - Authenticated Facilitator

**Purpose:** Overview of sessions, quick access to create new

**Key Elements:**
- Welcome message: "Welcome, Laura"
- Quick action: "Create New Session" (large primary button)
- Recent sessions list:
  - Session name, date, participant count, status (completed/upcoming)
  - Quick actions: "View Results", "Duplicate", "Delete"
- Analytics summary:
  - Total sessions created
  - Total participants
  - Average engagement rate
  - Top topics trained

**Layout:**
- Header with user profile
- Main content: Recent sessions + quick actions
- Sidebar (collapsible on mobile): Navigation
- Analytics cards below

---

### Screen 3: Session Setup - Create New Session

**Three-Step Wizard (as described in Flow 1)**

**Step 1: Session Details**
- Input: Session name (text field)
- Dropdown: Event type (opening, assessment, challenge, custom)
- Template selection (visual cards with preview)

**Step 2: Questions**
- Show pre-built questions from template
- Preview cards for first 3 questions
- Option: "Customize" → expands to full question editor
- Option: "Use defaults" → proceeds to next step

**Step 3: Teams**
- Input: Number of teams (slider 1-20)
- Option: Auto-assign or manual
- Display: Preview of team assignments
- Can skip and auto-assign later

**Review:**
- Summary of session configuration
- "Launch Now" button (primary, large)
- "Edit" links to go back to any step
- Copy session link automatically generated

---

### Screen 4: Live Session - Facilitator View

**Purpose:** Control session, monitor engagement, display to audience

**Key Elements:**
- Large question display (readable from 30ft away on screen)
- Team scoreboard with real-time updates
- Participant progress indicator ("65% have answered")
- Timer countdown (large, red when <10 seconds)
- Control buttons: Pause, Next Question, End Session
- Share link prominently displayed

**Layout:**
- Question (60% of screen): Large text, readable
- Scoreboard (30% of screen): Team names + scores
- Controls (10% of screen): Buttons for progression

---

### Screen 5: Live Session - Participant View (Mobile)

**Purpose:** Simple, distraction-free trivia answering

**Key Elements:**
- Question (large, clear)
- Answer options (4 buttons, single tap)
- Timer (visible but not dominant)
- Current team score (small, bottom)
- Session name (top)

**Layout:**
- Minimal chrome, maximum question visibility
- Vertical stack: Session info → Question → Answers → Team score
- No navigation, no distractions
- Touch-optimized spacing

---

### Screen 6: Results Screen - Post-Question

**Purpose:** Educate and maintain momentum

**Key Elements:**
- Correct answer highlighted (green)
- User's answer highlighted (their selection shown)
- Explanation (1-2 sentences)
- Common misconceptions (if relevant)
- Updated team score
- "Next Question" auto-advances after 5 seconds

**Layout:**
- Correct answer at top (largest)
- User's answer below (smaller)
- Explanation in body text
- Auto-advance or "Next" button

---

### Screen 7: Session Results - Post-Session

**Purpose:** Celebrate, show learning data, enable next steps

**Key Elements:**
- 🏆 Winning team announcement (celebratory)
- Final scores (visual chart)
- Knowledge check data (% correct by topic)
- Export results (PDF or CSV)
- Share results (link to share)
- "Create Another Session" CTA
- "View Analytics" link

**Layout:**
- Header: "Session Complete! 🎉"
- Large winning team display
- Scores visualization (bar chart or table)
- Data insights (topics mastered, gaps identified)
- Action buttons below

---

### Screen 8: Analytics Dashboard

**Purpose:** Show training impact and knowledge trends

**Key Elements:**
- Date range selector
- Tabs: Overview, Topics, Teams, Individuals
- Overview tab:
  - Total sessions created (metric card)
  - Total participants (metric card)
  - Average engagement (metric card)
  - Knowledge improvement trend (line chart)
- Topics tab:
  - Topic mastery (bar chart)
  - Knowledge gaps (<70% correct)
  - Recommended follow-up topics
- Teams tab:
  - Team performance comparison
  - Engagement leaderboard (non-public)
- Individuals tab:
  - Streak tracking
  - Learning history

**Layout:**
- Header: "Analytics"
- Tabs for different views
- Cards and charts in grid layout
- Exportable data (CSV, PDF)

---

### Screen 9: Slack Bot - Coffee Break Trivia

**Purpose:** Send engaging trivia question to Slack channel

**Message Format:**

```
:brain: Daily Trivia Challenge

Which of these is our company value?

:radio_button: Innovation & Speed
:radio_button: Customer First
:radio_button: Integrity & Trust
:radio_button: Growth Mindset

Reply with your answer (A, B, C, or D)!

Expires in 24 hours
```

**UX Flow:**
1. User reacts with emoji (A, B, C, D)
2. Bot DMs confirmation + whether correct
3. Feedback: "Correct! ✅" or "Try again! 🤔"
4. Optional: Show explanation in thread

---

## 5. Mobile Responsive Design

### Breakpoints

- **Mobile:** 320px - 640px
  - Single column layout
  - Touch-optimized buttons (48px minimum)
  - Full-width content
  
- **Tablet:** 640px - 1024px
  - Two-column grid where appropriate
  - Horizontal scrolling for charts
  
- **Desktop:** 1024px - 1920px
  - Multi-column layouts
  - Sidebar navigation
  - Larger charts and data tables

### Mobile-Specific Design Decisions

1. **Question Display:**
   - Large text (18px minimum)
   - Single-column layout
   - Answer buttons full width (44px height)
   - No horizontal scrolling

2. **Navigation:**
   - Bottom tab bar for main navigation (mobile convention)
   - Hamburger menu for secondary options
   - Breadcrumbs for depth orientation

3. **Forms:**
   - One input per line
   - Dropdown instead of complex selections
   - Clear error messages inline

4. **Performance:**
   - Lazy load images
   - Minimize animations on mobile
   - Reduce data transfer
   - Cache static assets

---

## 6. Accessibility Specifications

### Color Contrast

- All text on background: 4.5:1 minimum contrast ratio
- Use WCAG Contrast Checker to verify
- Never rely on color alone (pair with icons, text)

### Keyboard Navigation

- All interactive elements focusable with Tab key
- Focus state clearly visible (outline or highlight)
- Enter/Space to activate buttons
- Arrow keys for option selection
- Escape to close modals

### Screen Reader Support

- Semantic HTML (buttons, links, headings, labels)
- ARIA labels for icons
- Form labels associated with inputs
- Image alt text where relevant
- Skip navigation link at top

### Motor Skills

- 48x48px minimum touch targets
- Click targets not adjacent (minimum 8px spacing)
- Avoid hover-only interactions
- Double-click not required
- Allow text selection

### Visual Accessibility

- Font size minimum 14px (body), 16px (interactive)
- 1.5x line height minimum
- No flashing content >3Hz
- Avoid auto-playing video/sound

---

## 7. Animation & Interaction Design

### Animation Guidelines

**Principles:**
- Animations serve a purpose (feedback, guidance)
- Keep duration short (200-300ms)
- Use easing functions for natural feel
- Don't animate on older devices

**Specific Animations:**

1. **Answer Submission:**
   - Button feedback: color change + slight scale (100ms)
   - Checkmark appears (200ms)
   - Brief pulse effect (200ms)

2. **Score Update:**
   - Number increments smoothly (500ms)
   - Accompanied by brief sound (optional)
   - Cell highlights briefly (green) (300ms)

3. **Question Transition:**
   - Fade out current question (200ms)
   - Fade in next question (200ms)
   - Slight slide-down effect (add dynamism)

4. **Modal Entrance:**
   - Scale from center (200ms)
   - Fade in (200ms)
   - Backdrop darkens simultaneously

### Microinteractions

- Button hover state: color deepens
- Input field focus: border becomes blue
- Error message appears: shake animation (feedback)
- Loading state: pulsing skeleton screen

---

## 8. Dark Mode (Future - Post-MVP)

**Note:** Deferred to v2+

**Considerations for Future:**
- Invert color palette while maintaining contrast
- Alternative images for dark mode
- Reduced brightness animations

---

## 9. Localization & Internationalization (Future - Post-MVP)

**Note:** Deferred to v2+

**MVP Scope:** English only

**Future Scope:**
- Support for major languages (Spanish, French, German, Japanese)
- Right-to-left language support
- Date/time locale formatting
- Currency localization

---

## 10. Component Library Specifications

### Reusable Components

**1. Button Component**
```jsx
<Button 
  variant="primary" | "secondary" | "danger"
  size="sm" | "md" | "lg"
  disabled={boolean}
  onClick={handler}
>
  Click Me
</Button>
```

**2. Input Component**
```jsx
<Input 
  type="text" | "email" | "number"
  label="Label Text"
  placeholder="Placeholder"
  error={errorMessage}
  required={boolean}
  value={state}
  onChange={handler}
/>
```

**3. Card Component**
```jsx
<Card title="Card Title" subtitle="Subtitle">
  Card content here
</Card>
```

**4. Progress Bar**
```jsx
<ProgressBar 
  percentage={65}
  label="Answered: 65%"
/>
```

**5. ScoreBoard**
```jsx
<ScoreBoard 
  teams={[
    { name: "Engineering", score: 420 },
    { name: "Marketing", score: 320 }
  ]}
/>
```

**6. Timer**
```jsx
<Timer 
  seconds={45}
  onComplete={handler}
  variant="normal" | "warning" | "danger"
/>
```

---

## 11. Performance Targets

### Load Times

- First Contentful Paint (FCP): <1 second
- Largest Contentful Paint (LCP): <2 seconds
- Cumulative Layout Shift (CLS): <0.1
- First Input Delay (FID): <100ms

### Optimization Strategies

- Lazy load images and components
- Minify CSS/JS
- Compress assets
- Cache static files in browser
- Use CDN for media
- Code splitting by route

---

## 12. Design Handoff

### Deliverables for Development

1. **Figma/Design File**
   - All screens and components
   - Responsive breakpoints
   - Interactive prototypes (key flows)
   - Exported assets (SVG icons, PNG images)

2. **Design Tokens/Variables**
   - Color values (hex, RGB, HSL)
   - Typography scales
   - Spacing units
   - Shadow definitions
   - Border radius values

3. **Component Specs**
   - Padding/margin for each component
   - Font sizes and weights
   - Color states (normal, hover, active, disabled)
   - Animation/transition details

4. **Responsive Specs**
   - Layouts for each breakpoint
   - Font size adjustments
   - Touch target sizes
   - Spacing adjustments

---

## 13. Testing & Validation

### User Testing Plan

**Phase 1: Facilitator Usability Testing**
- Task: Create session in <2 minutes
- Task: Launch and monitor live session
- Observe: Where do they struggle?
- Success: 80% complete both tasks without help

**Phase 2: Participant Mobile Testing**
- Task: Join session on phone
- Task: Answer 5 questions correctly
- Observe: Confusion points, clarity issues
- Success: 95% answer correctly formatted

**Phase 3: Accessibility Testing**
- Test with screen reader
- Keyboard-only navigation
- Color contrast checker
- Success: WCAG 2.1 AA compliance

### A/B Testing (Post-MVP)

- CTA button placement/color
- Question display formats
- Scoreboard prominence
- Timer display styles

---

## 14. Design System Evolution

### Version Control

- Version 1.0: MVP launch (January 2026)
- Quarterly reviews for updates
- Feature releases may introduce new components

### Feedback Loop

- User testing → Design refinements
- Analytics → Identify friction points
- Performance → Optimize critical paths
- Accessibility → Expand support

---

## Appendix: Screen Size References

```
iPhone SE:        375 x 667px
iPhone 12/13:     390 x 844px
iPhone 14 Pro:    430 x 932px
Samsung Galaxy S21: 360 x 800px
iPad (10.2"):     810 x 1080px
iPad Pro (12.9"): 1024 x 1366px
Desktop:          1920 x 1080px
```

---

## Design Sign-Off

**Design Owner:** [Design Lead Name]  
**Product Owner:** Tim_D  
**Status:** Ready for Implementation  
**Last Updated:** 2026-01-19  

