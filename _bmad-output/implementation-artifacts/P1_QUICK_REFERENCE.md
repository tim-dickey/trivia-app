# Quick Reference: Create P1 Issues

## 🚀 Quick Start

```bash
# Authenticate (one-time)
gh auth login

# Create all 5 P1 issues
python3 scripts/create-p1-issues.py
```

## 📋 What Gets Created

5 High Priority Issues from Code Review:

1. **[P1] Update Outdated Dependencies** (4h) - Security patches
2. **[P1] Add Frontend CI Workflow** (2h) - Quality validation  
3. **[P1] Expand CodeQL Analysis** (1h) - Python & TypeScript security
4. **[P1] Add Docker Compose Services** (3h) - Developer experience
5. **[P1] Add Security Headers** (2h) - Security hardening

**Total**: 12 hours (1.5 days)

## 🛠️ Three Ways to Create

### 1️⃣ Python Script (Recommended)
```bash
python3 scripts/create-p1-issues.py
```
✅ Tracks created issues  
✅ Prevents duplicates  
✅ Detailed output

### 2️⃣ Bash Script
```bash
./scripts/create-p1-issues.sh
```
✅ No Python needed  
✅ Colored output  
⚠️ No duplicate tracking

### 3️⃣ Manual Creation
Open: `_bmad-output/implementation-artifacts/P1_ISSUES_MANUAL_CREATION_GUIDE.md`

Copy-paste each issue into GitHub

## 📍 File Locations

- **Scripts**: `scripts/create-p1-issues.{py,sh}`
- **Source Data**: `_bmad-output/implementation-artifacts/code-review-issues-p1.json`
- **Manual Guide**: `_bmad-output/implementation-artifacts/P1_ISSUES_MANUAL_CREATION_GUIDE.md`
- **Task Summary**: `_bmad-output/implementation-artifacts/P1_ISSUES_TASK_SUMMARY.md`
- **Full Docs**: `scripts/README.md`

## ✅ Verification

After creation:
```bash
# View created issues
gh issue list --repo tim-dickey/trivia-app --label priority:high

# Or visit
https://github.com/tim-dickey/trivia-app/issues
```

## 🆘 Troubleshooting

### Not authenticated?
```bash
gh auth login
```

### Script not executable?
```bash
chmod +x scripts/create-p1-issues.sh
```

### Issues already exist?
Python script automatically skips them.

## 📚 More Info

- Full task summary: `_bmad-output/implementation-artifacts/P1_ISSUES_TASK_SUMMARY.md`
- All scripts documentation: `scripts/README.md`
- Issue creation guide: `ISSUE_CREATION_INSTRUCTIONS.md`
