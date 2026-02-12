"""
Unit tests for lib modules

Tests for:
- config.py
- issue_validator.py
- issue_tracker.py
- github_client.py (partial - auth tests only)
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path to import lib
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.config import Config
from lib.issue_validator import (
    validate_issue,
    normalize_priority,
    get_priority_labels,
    validate_priority,
    merge_labels,
    PRIORITY_LABELS
)
from lib.issue_tracker import IssueTracker


class TestConfig(unittest.TestCase):
    """Tests for Config class"""
    
    def test_config_initialization(self):
        """Test that Config initializes with default values"""
        config = Config()
        self.assertIsNotNone(config.repo)
        self.assertIsInstance(config.base_dir, Path)
        self.assertIsInstance(config.issues_dir, Path)
        self.assertIsInstance(config.scripts_dir, Path)
    
    def test_parse_git_url_ssh(self):
        """Test parsing SSH git URL"""
        config = Config()
        url = "git@github.com:owner/repo.git"
        result = config.parse_git_url(url)
        self.assertEqual(result, "owner/repo")
    
    def test_parse_git_url_https(self):
        """Test parsing HTTPS git URL"""
        config = Config()
        url = "https://github.com/owner/repo.git"
        result = config.parse_git_url(url)
        self.assertEqual(result, "owner/repo")
    
    def test_parse_git_url_https_no_git(self):
        """Test parsing HTTPS URL without .git"""
        config = Config()
        url = "https://github.com/owner/repo"
        result = config.parse_git_url(url)
        self.assertEqual(result, "owner/repo")
    
    def test_parse_git_url_invalid(self):
        """Test parsing invalid URL returns None"""
        config = Config()
        url = "invalid-url"
        result = config.parse_git_url(url)
        self.assertIsNone(result)
    
    def test_get_repo_name_from_env(self):
        """Test repo name from environment variable"""
        with patch.dict(os.environ, {"GITHUB_REPOSITORY": "test/repo"}):
            config = Config()
            self.assertEqual(config.repo, "test/repo")
    
    def test_get_issue_file(self):
        """Test getting issue file path"""
        config = Config()
        p1_file = config.get_issue_file("p1")
        self.assertEqual(p1_file.name, "code-review-issues-p1.json")
    
    def test_get_issues_log_file(self):
        """Test getting issues log file path"""
        config = Config()
        log_file = config.get_issues_log_file()
        self.assertEqual(log_file.name, "issues-log.json")
    
    def test_get_tracking_file(self):
        """Test getting tracking file path"""
        config = Config()
        tracking_file = config.get_tracking_file()
        self.assertEqual(tracking_file.name, "issues-tracking.json")
    
    def test_config_repr(self):
        """Test Config string representation"""
        config = Config()
        repr_str = repr(config)
        self.assertIn("Config", repr_str)
        self.assertIn("repo", repr_str)


class TestIssueValidator(unittest.TestCase):
    """Tests for issue_validator module"""
    
    def test_validate_issue_valid(self):
        """Test validation of valid issue"""
        issue = {
            "title": "Test Issue",
            "body": "Test body",
            "labels": ["bug"],
            "priority": "high"
        }
        is_valid, error = validate_issue(issue)
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_validate_issue_missing_field(self):
        """Test validation fails for missing field"""
        issue = {
            "title": "Test Issue",
            "body": "Test body",
            "labels": ["bug"]
            # Missing priority
        }
        is_valid, error = validate_issue(issue)
        self.assertFalse(is_valid)
        self.assertIn("Missing required field", error)
    
    def test_validate_issue_empty_field(self):
        """Test validation fails for empty field"""
        issue = {
            "title": "",
            "body": "Test body",
            "labels": ["bug"],
            "priority": "high"
        }
        is_valid, error = validate_issue(issue)
        self.assertFalse(is_valid)
        self.assertIn("Empty required field", error)
    
    def test_validate_issue_invalid_priority(self):
        """Test validation fails for invalid priority"""
        issue = {
            "title": "Test Issue",
            "body": "Test body",
            "labels": ["bug"],
            "priority": "invalid"
        }
        is_valid, error = validate_issue(issue)
        self.assertFalse(is_valid)
        self.assertIn("Invalid priority", error)
    
    def test_validate_issue_labels_not_list(self):
        """Test validation fails when labels is not a list"""
        issue = {
            "title": "Test Issue",
            "body": "Test body",
            "labels": "bug",  # Should be a list
            "priority": "high"
        }
        is_valid, error = validate_issue(issue)
        self.assertFalse(is_valid)
        self.assertIn("Labels must be a list", error)
    
    def test_normalize_priority_alias(self):
        """Test normalizing priority alias"""
        self.assertEqual(normalize_priority("p0"), "critical")
        self.assertEqual(normalize_priority("p1"), "high")
        self.assertEqual(normalize_priority("p2"), "medium")
        self.assertEqual(normalize_priority("p3"), "low")
    
    def test_normalize_priority_standard(self):
        """Test normalizing standard priority"""
        self.assertEqual(normalize_priority("critical"), "critical")
        self.assertEqual(normalize_priority("high"), "high")
        self.assertEqual(normalize_priority("medium"), "medium")
        self.assertEqual(normalize_priority("low"), "low")
    
    def test_normalize_priority_case_insensitive(self):
        """Test priority normalization is case insensitive"""
        self.assertEqual(normalize_priority("P1"), "high")
        self.assertEqual(normalize_priority("HIGH"), "high")
    
    def test_get_priority_labels(self):
        """Test getting priority labels"""
        labels = get_priority_labels("p1")
        self.assertEqual(labels, ["priority:high"])
        
        labels = get_priority_labels("critical")
        self.assertEqual(labels, ["priority:critical"])
    
    def test_validate_priority_valid(self):
        """Test validate_priority with valid priorities"""
        self.assertTrue(validate_priority("p0"))
        self.assertTrue(validate_priority("high"))
        self.assertTrue(validate_priority("critical"))
    
    def test_validate_priority_invalid(self):
        """Test validate_priority with invalid priority"""
        self.assertFalse(validate_priority("invalid"))
        self.assertFalse(validate_priority("p5"))
    
    def test_merge_labels(self):
        """Test merging issue labels with priority labels"""
        issue_labels = ["bug", "frontend"]
        priority = "high"
        merged = merge_labels(issue_labels, priority)
        
        self.assertIn("bug", merged)
        self.assertIn("frontend", merged)
        self.assertIn("priority:high", merged)
    
    def test_merge_labels_no_duplicates(self):
        """Test merge_labels removes duplicates"""
        issue_labels = ["bug", "priority:high"]
        priority = "high"
        merged = merge_labels(issue_labels, priority)
        
        # Should only have one "priority:high"
        self.assertEqual(merged.count("priority:high"), 1)
    
    def test_priority_labels_constant(self):
        """Test PRIORITY_LABELS constant"""
        self.assertIn("critical", PRIORITY_LABELS)
        self.assertIn("high", PRIORITY_LABELS)
        self.assertIn("medium", PRIORITY_LABELS)
        self.assertIn("low", PRIORITY_LABELS)


class TestIssueTracker(unittest.TestCase):
    """Tests for IssueTracker class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.tracking_file = Path(self.temp_dir) / "test-tracking.json"
    
    def tearDown(self):
        """Clean up test files"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_tracker_initialization_new_file(self):
        """Test tracker initialization with non-existent file"""
        tracker = IssueTracker(self.tracking_file)
        self.assertIsInstance(tracker.data, dict)
        self.assertEqual(tracker.data["version"], "2.0")
        self.assertEqual(tracker.data["summary"]["total_issues"], 0)
    
    def test_tracker_save_and_load(self):
        """Test saving and loading tracker data"""
        tracker = IssueTracker(self.tracking_file)
        tracker.mark_created("TEST-1", 123, "high", "test")
        tracker.save()
        
        # Load from file
        tracker2 = IssueTracker(self.tracking_file)
        self.assertTrue(tracker2.is_created("TEST-1"))
        self.assertEqual(tracker2.get_github_number("TEST-1"), 123)
    
    def test_is_created(self):
        """Test checking if issue is created"""
        tracker = IssueTracker(self.tracking_file)
        self.assertFalse(tracker.is_created("TEST-1"))
        
        tracker.mark_created("TEST-1", 123)
        self.assertTrue(tracker.is_created("TEST-1"))
    
    def test_mark_created(self):
        """Test marking issue as created"""
        tracker = IssueTracker(self.tracking_file)
        tracker.mark_created("TEST-1", 123, "high", "test")
        
        issue = tracker.get_issue("TEST-1")
        self.assertIsNotNone(issue)
        self.assertEqual(issue["github_issue_number"], 123)
        self.assertEqual(issue["status"], "open")
        self.assertEqual(issue["priority"], "high")
        self.assertEqual(issue["source"], "test")
    
    def test_get_issue(self):
        """Test getting issue data"""
        tracker = IssueTracker(self.tracking_file)
        tracker.mark_created("TEST-1", 123)
        
        issue = tracker.get_issue("TEST-1")
        self.assertIsNotNone(issue)
        self.assertEqual(issue["github_issue_number"], 123)
        
        # Non-existent issue
        issue2 = tracker.get_issue("TEST-999")
        self.assertIsNone(issue2)
    
    def test_get_github_number(self):
        """Test getting GitHub issue number"""
        tracker = IssueTracker(self.tracking_file)
        tracker.mark_created("TEST-1", 123)
        
        num = tracker.get_github_number("TEST-1")
        self.assertEqual(num, 123)
        
        # Non-existent issue
        num2 = tracker.get_github_number("TEST-999")
        self.assertIsNone(num2)
    
    def test_get_all_issues(self):
        """Test getting all issues"""
        tracker = IssueTracker(self.tracking_file)
        tracker.mark_created("TEST-1", 123)
        tracker.mark_created("TEST-2", 124)
        
        all_issues = tracker.get_all_issues()
        self.assertEqual(len(all_issues), 2)
        self.assertIn("TEST-1", all_issues)
        self.assertIn("TEST-2", all_issues)
    
    def test_get_created_issues(self):
        """Test getting created issues list"""
        tracker = IssueTracker(self.tracking_file)
        tracker.mark_created("TEST-1", 123, "high")
        tracker.mark_created("TEST-2", 124, "low")
        
        created = tracker.get_created_issues()
        self.assertEqual(len(created), 2)
        self.assertTrue(any(i["issue_id"] == "TEST-1" for i in created))
    
    def test_get_summary(self):
        """Test getting summary statistics"""
        tracker = IssueTracker(self.tracking_file)
        tracker.mark_created("TEST-1", 123, "high")
        tracker.mark_created("TEST-2", 124, "critical")
        
        summary = tracker.get_summary()
        self.assertEqual(summary["total_issues"], 2)
        self.assertEqual(summary["created"], 2)
        self.assertEqual(summary["by_priority"]["high"], 1)
        self.assertEqual(summary["by_priority"]["critical"], 1)
    
    def test_merge_from_legacy(self):
        """Test merging from legacy tracking file"""
        # Create legacy tracking file
        legacy_file = Path(self.temp_dir) / "legacy.json"
        legacy_data = {
            "issues": [
                {"id": "LEG-1", "github_issue_number": 100, "priority": "high"},
                {"id": "LEG-2", "github_issue_number": 101, "priority": "low"}
            ]
        }
        with open(legacy_file, 'w') as f:
            json.dump(legacy_data, f)
        
        # Merge into new tracker
        tracker = IssueTracker(self.tracking_file)
        count = tracker.merge_from_legacy(legacy_file, "legacy")
        
        self.assertEqual(count, 2)
        self.assertTrue(tracker.is_created("LEG-1"))
        self.assertTrue(tracker.is_created("LEG-2"))
        self.assertEqual(tracker.get_github_number("LEG-1"), 100)
    
    def test_tracker_repr(self):
        """Test IssueTracker string representation"""
        tracker = IssueTracker(self.tracking_file)
        repr_str = repr(tracker)
        self.assertIn("IssueTracker", repr_str)
        self.assertIn("total=", repr_str)


class TestGitHubClient(unittest.TestCase):
    """Tests for GitHubClient class (auth checks only)"""
    
    @patch('subprocess.run')
    def test_check_auth_success(self, mock_run):
        """Test successful auth check"""
        mock_run.return_value = MagicMock(returncode=0)
        
        # Import here to use mocked subprocess
        from lib.github_client import GitHubClient
        
        # Create client (will call _check_auth in __init__)
        try:
            client = GitHubClient("test/repo")
            # If we get here, auth check passed
            self.assertEqual(client.repo, "test/repo")
        except RuntimeError:
            self.fail("GitHubClient raised RuntimeError unexpectedly")
    
    @patch('subprocess.run')
    def test_check_auth_method(self, mock_run):
        """Test check_auth method returns bool"""
        from lib.github_client import GitHubClient
        
        # Mock successful auth first for __init__
        mock_run.return_value = MagicMock(returncode=0)
        client = GitHubClient("test/repo")
        
        # Test check_auth method
        result = client.check_auth()
        self.assertTrue(result)
        
        # Test failed auth
        mock_run.return_value = MagicMock(returncode=1)
        result = client.check_auth()
        self.assertFalse(result)


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
