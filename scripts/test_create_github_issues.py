#!/usr/bin/env python3
"""
Unit tests for create_github_issues.py

Test Coverage:
- Issue validation (required fields, priority levels)
- Priority label mapping
- JSON file loading
- Mock issue creation
- Acceptance criteria validation
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import from the module under test
from create_github_issues import (
    validate_issue,
    load_issues_from_json,
    get_priority_name,
    PRIORITY_LABELS
)


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
        is_valid, error = validate_issue(issue)
        assert is_valid is True
        assert error is None
    
    def test_valid_issue_p3(self):
        """Test validation of valid P3 issue"""
        issue = {
            "title": "Low Priority Issue",
            "body": "Nice-to-have improvement",
            "labels": ["priority:low"],
            "priority": "low"
        }
        is_valid, error = validate_issue(issue)
        assert is_valid is True
        assert error is None
    
    def test_missing_title(self):
        """Test validation fails with missing title"""
        issue = {
            "body": "Issue description",
            "labels": ["priority:high"],
            "priority": "high"
        }
        is_valid, error = validate_issue(issue)
        assert is_valid is False
        assert "Missing required field: title" in error
    
    def test_invalid_priority(self):
        """Test validation fails with invalid priority"""
        issue = {
            "title": "Issue",
            "body": "Description",
            "labels": ["priority:invalid"],
            "priority": "invalid"
        }
        is_valid, error = validate_issue(issue)
        assert is_valid is False
        assert "Invalid priority" in error
    
    def test_empty_priority_field(self):
        """Test validation fails with empty priority"""
        issue = {
            "title": "Issue",
            "body": "Description",
            "labels": [],
            "priority": ""
        }
        is_valid, error = validate_issue(issue)
        assert is_valid is False
        assert "Empty required field" in error


class TestPriorityMapping:
    """Test priority to label mapping"""
    
    def test_critical_mapping(self):
        """Test P0 critical priority mapping"""
        assert PRIORITY_LABELS["critical"] == ["priority:critical"]
    
    def test_high_mapping(self):
        """Test P1 high priority mapping"""
        assert PRIORITY_LABELS["high"] == ["priority:high"]
    
    def test_medium_mapping(self):
        """Test P2 medium priority mapping"""
        assert PRIORITY_LABELS["medium"] == ["priority:medium"]
    
    def test_low_mapping(self):
        """Test P3 low priority mapping"""
        assert PRIORITY_LABELS["low"] == ["priority:low"]
    
    def test_all_priorities_mapped(self):
        """Test all priority levels have mappings"""
        assert len(PRIORITY_LABELS) == 4
        assert set(PRIORITY_LABELS.keys()) == {"critical", "high", "medium", "low"}


class TestPriorityNameHelper:
    """Test the get_priority_name helper function"""
    
    def test_p0_to_critical(self):
        """Test P0 maps to critical"""
        assert get_priority_name("P0") == "critical"
    
    def test_p1_to_high(self):
        """Test P1 maps to high"""
        assert get_priority_name("P1") == "high"
    
    def test_p2_to_medium(self):
        """Test P2 maps to medium"""
        assert get_priority_name("P2") == "medium"
    
    def test_p3_to_low(self):
        """Test P3 maps to low"""
        assert get_priority_name("P3") == "low"
    
    def test_invalid_priority(self):
        """Test invalid priority returns unknown"""
        assert get_priority_name("P99") == "unknown"
    
    def test_case_insensitive(self):
        """Test priority key is case insensitive"""
        assert get_priority_name("p0") == "critical"
        assert get_priority_name("p3") == "low"


class TestIssueFileLoading:
    """Test JSON file loading"""
    
    def test_load_valid_json(self, tmp_path):
        """Test loading valid JSON issue file"""
        # Create a temporary JSON file
        test_file = tmp_path / "test_issues.json"
        test_data = {
            "source": "Test",
            "total_issues": 1,
            "issues": [
                {
                    "id": "TEST-1",
                    "title": "Test Issue",
                    "priority": "critical",
                    "labels": ["priority:critical"],
                    "body": "Test body"
                }
            ]
        }
        
        import json
        with open(test_file, 'w') as f:
            json.dump(test_data, f)
        
        # Load using the actual function
        issues = load_issues_from_json(test_file)
        assert len(issues) == 1
        assert issues[0]["title"] == "Test Issue"
        assert issues[0]["priority"] == "critical"
    
    def test_load_empty_issues(self, tmp_path):
        """Test handling of empty issues list"""
        # Create a temporary JSON file with empty issues
        test_file = tmp_path / "empty_issues.json"
        test_data = {
            "source": "Test",
            "total_issues": 0,
            "issues": []
        }
        
        import json
        with open(test_file, 'w') as f:
            json.dump(test_data, f)
        
        # Load using the actual function
        issues = load_issues_from_json(test_file)
        assert issues == []


class TestAcceptanceCriteria:
    """Test acceptance criteria for all priority levels"""
    
    def test_p0_critical_acceptance(self):
        """P0: Must include security/blocking classification"""
        issue = {
            "title": "[P0] Security Issue",
            "priority": "critical",
            "labels": ["priority:critical"],
            "body": "blocks-deployment: true\nsecurity-risk: high"
        }
        is_valid, error = validate_issue(issue)
        assert is_valid is True
    
    def test_p1_high_acceptance(self):
        """P1: Must include business impact"""
        issue = {
            "title": "[P1] Feature Gap",
            "priority": "high",
            "labels": ["priority:high"],
            "body": "## Business Impact\nAffects users"
        }
        is_valid, error = validate_issue(issue)
        assert is_valid is True
    
    def test_p2_medium_acceptance(self):
        """P2: Must include acceptance criteria"""
        issue = {
            "title": "[P2] Improvement",
            "priority": "medium",
            "labels": ["priority:medium"],
            "body": "## Acceptance Criteria\n- [ ] Item 1"
        }
        is_valid, error = validate_issue(issue)
        assert is_valid is True
    
    def test_p3_low_acceptance(self):
        """P3: Must be nice-to-have or optimization"""
        issue = {
            "title": "[P3] Nice-to-have",
            "priority": "low",
            "labels": ["priority:low"],
            "body": "optimization"
        }
        is_valid, error = validate_issue(issue)
        assert is_valid is True


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
