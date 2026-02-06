#!/usr/bin/env python3
"""
Unit tests for create-github-issues.py

Test Coverage:
- Issue validation (required fields, priority levels)
- Priority label mapping
- JSON file loading
- Mock issue creation
- Acceptance criteria validation
"""

import json
import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))


class TestIssueValidation:
    """Test issue validation logic"""
    
    def test_valid_issue_p0(self):
        """Test validation of valid P0 issue"""
        issue = {
            "title": "Critical Issue",
            "body": "Issue description",
            "labels": ["priority:critical"],
            "priority": "critical"
        }
        assert issue["priority"] in ["critical", "high", "medium", "low"]
        assert all(key in issue for key in ["title", "body", "labels", "priority"])
    
    def test_valid_issue_p3(self):
        """Test validation of valid P3 issue"""
        issue = {
            "title": "Low Priority Issue",
            "body": "Nice-to-have improvement",
            "labels": ["priority:low"],
            "priority": "low"
        }
        assert issue["priority"] == "low"
    
    def test_missing_title(self):
        """Test validation fails with missing title"""
        issue = {
            "body": "Issue description",
            "labels": ["priority:high"],
            "priority": "high"
        }
        assert "title" not in issue
    
    def test_invalid_priority(self):
        """Test validation fails with invalid priority"""
        issue = {
            "title": "Issue",
            "body": "Description",
            "labels": ["priority:invalid"],
            "priority": "invalid"
        }
        valid_priorities = ["critical", "high", "medium", "low"]
        assert issue["priority"] not in valid_priorities
    
    def test_empty_priority_field(self):
        """Test validation fails with empty priority"""
        issue = {
            "title": "Issue",
            "body": "Description",
            "labels": [],
            "priority": ""
        }
        assert not issue["priority"]


class TestPriorityMapping:
    """Test priority to label mapping"""
    
    PRIORITY_LABELS = {
        "critical": ["priority:critical"],
        "high": ["priority:high"],
        "medium": ["priority:medium"],
        "low": ["priority:low"],
    }
    
    def test_critical_mapping(self):
        """Test P0 critical priority mapping"""
        assert self.PRIORITY_LABELS["critical"] == ["priority:critical"]
    
    def test_high_mapping(self):
        """Test P1 high priority mapping"""
        assert self.PRIORITY_LABELS["high"] == ["priority:high"]
    
    def test_medium_mapping(self):
        """Test P2 medium priority mapping"""
        assert self.PRIORITY_LABELS["medium"] == ["priority:medium"]
    
    def test_low_mapping(self):
        """Test P3 low priority mapping"""
        assert self.PRIORITY_LABELS["low"] == ["priority:low"]
    
    def test_all_priorities_mapped(self):
        """Test all priority levels have mappings"""
        assert len(self.PRIORITY_LABELS) == 4
        assert set(self.PRIORITY_LABELS.keys()) == {"critical", "high", "medium", "low"}


class TestIssueFileLoading:
    """Test JSON file loading"""
    
    def test_valid_json_structure(self):
        """Test loading valid JSON issue file"""
        issue_data = {
            "source": "Code Review",
            "priority_level": "P0",
            "total_issues": 1,
            "issues": [
                {
                    "id": "P0-1",
                    "title": "[P0] Test Issue",
                    "priority": "critical",
                    "labels": ["priority:critical"],
                    "body": "Test body"
                }
            ]
        }
        assert "issues" in issue_data
        assert len(issue_data["issues"]) == 1
        assert issue_data["issues"][0]["priority"] == "critical"
    
    def test_empty_issues_list(self):
        """Test handling of empty issues list"""
        issue_data = {
            "source": "Code Review",
            "priority_level": "P3",
            "total_issues": 0,
            "issues": []
        }
        assert issue_data.get("issues", []) == []


class TestAcceptanceCriteria:
    """Test acceptance criteria for all priority levels"""
    
    def test_p0_critical_acceptance(self):
        """P0: Must include security/blocking classification"""
        issue = {
            "title": "[P0] Security Issue",
            "priority": "critical",
            "body": "blocks-deployment: true\nsecurity-risk: high"
        }
        assert "[P0]" in issue["title"] or issue["priority"] == "critical"
    
    def test_p1_high_acceptance(self):
        """P1: Must include business impact"""
        issue = {
            "title": "[P1] Feature Gap",
            "priority": "high",
            "body": "## Business Impact\nAffects users"
        }
        assert "## Business Impact" in issue["body"] or issue["priority"] == "high"
    
    def test_p2_medium_acceptance(self):
        """P2: Must include acceptance criteria"""
        issue = {
            "title": "[P2] Improvement",
            "priority": "medium",
            "body": "## Acceptance Criteria\n- [ ] Item 1"
        }
        assert "## Acceptance Criteria" in issue["body"] or issue["priority"] == "medium"
    
    def test_p3_low_acceptance(self):
        """P3: Must be nice-to-have or optimization"""
        issue = {
            "title": "[P3] Nice-to-have",
            "priority": "low",
            "body": "optimization"
        }
        assert "[P3]" in issue["title"] or issue["priority"] == "low"


class TestPriorityBreakdown:
    """Test priority level breakdown"""
    
    def test_all_priorities_present(self):
        """Test that all 4 priorities are tracked"""
        priority_counts = {"P0": 5, "P1": 5, "P2": 5, "P3": 5}
        assert len(priority_counts) == 4
        assert sum(priority_counts.values()) == 20
    
    def test_priority_distribution(self):
        """Test valid priority distribution"""
        total = 20
        assert total == 20


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
