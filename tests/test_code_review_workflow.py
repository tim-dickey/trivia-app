#!/usr/bin/env python3
"""
Comprehensive test suite for code review workflow

Tests cover:
- JSON schema validation
- Issue structure and content
- Priority categorization
- Effort estimation
- Acceptance criteria
- Cross-file consistency
"""

import json
import pytest
from pathlib import Path
from typing import Dict, List, Any


class CodeReviewValidator:
    """Validates code review JSON files against schema and rules"""
    
    def __init__(self, root_path: Path = None):
        self.root_path = root_path or Path(__file__).parent.parent
        self.artifacts_dir = self.root_path / "_bmad-output/implementation-artifacts"
    
    def load_json(self, filename: str) -> Dict:
        """Load JSON file"""
        filepath = self.artifacts_dir / filename
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def validate_file_structure(self, data: Dict, priority: str) -> List[str]:
        """Validate top-level file structure"""
        errors = []
        
        # Check required fields
        required = ['source', 'priority_level', 'priority_description', 'total_issues', 'issues']
        for field in required:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        # Check source format
        if 'source' in data:
            if not data['source'].startswith('Code Review '):
                errors.append(f"Invalid source format: {data['source']}")
        
        # Check priority level matches file
        if 'priority_level' in data and data['priority_level'] != priority:
            errors.append(f"Priority mismatch: expected {priority}, got {data['priority_level']}")
        
        # Check total_issues matches array length
        if 'issues' in data and 'total_issues' in data:
            if len(data['issues']) != data['total_issues']:
                errors.append(f"Total issues mismatch: expected {data['total_issues']}, got {len(data['issues'])}")
        
        return errors
    
    def validate_issue(self, issue: Dict, priority: str, issue_num: int, data: Dict) -> List[str]:
        """Validate individual issue"""
        errors = []
        
        # Required fields
        required = ['id', 'title', 'priority', 'labels', 'effort_hours', 'body']
        for field in required:
            if field not in issue:
                errors.append(f"Issue {issue_num}: Missing field '{field}'")
            elif not issue[field]:
                errors.append(f"Issue {issue_num}: Empty field '{field}'")
        
        # ID format
        if 'id' in issue:
            expected_id = f"{priority}-{issue_num}"
            if issue['id'] != expected_id:
                errors.append(f"Issue {issue_num}: ID mismatch. Expected {expected_id}, got {issue['id']}")
        
        # Title format
        if 'title' in issue:
            if not issue['title'].startswith('[P'):
                errors.append(f"Issue {issue_num}: Title missing [P#] prefix")
            expected_prefix = priority.split('-')[0]  # Extract P0, P1, etc.
            if not issue['title'].startswith(f"[{expected_prefix}]"): 
                errors.append(f"Issue {issue_num}: Title prefix doesn't match priority")
        
        # Priority value
        priority_mapping = {
            'P0': 'critical',
            'P1': 'high',
            'P2': 'medium',
            'P3': 'low'
        }
        if 'priority' in issue and 'priority_level' in data:
            priority_level = data.get('priority_level')
            if priority_level in priority_mapping:
                expected_priority = priority_mapping[priority_level]
                if issue['priority'] != expected_priority:
                    errors.append(f"Issue {issue_num}: Priority mismatch. Expected {expected_priority}, got {issue['priority']}")
        
        # Labels
        if 'labels' in issue:
            if len(issue['labels']) < 2:
                errors.append(f"Issue {issue_num}: At least 2 labels required")
            
            priority_labels = {
                'critical': 'priority:critical',
                'high': 'priority:high',
                'medium': 'priority:medium',
                'low': 'priority:low'
            }
            if 'priority' in issue:
                expected_label = priority_labels.get(issue['priority'])
                if expected_label and expected_label not in issue['labels']:
                    errors.append(f"Issue {issue_num}: Missing priority label {expected_label}")
        
        # Effort hours
        if 'effort_hours' in issue:
            effort = issue['effort_hours']
            if not isinstance(effort, (int, float)):
                errors.append(f"Issue {issue_num}: Effort must be a number")
            elif effort < 0.25 or effort > 40:
                errors.append(f"Issue {issue_num}: Effort must be between 0.25 and 40 hours")
        
        # Body content
        if 'body' in issue:
            body = issue['body']
            if len(body) < 150:
                errors.append(f"Issue {issue_num}: Body too short (min 150 chars)")
            
            required_sections = ['## Problem', '## Impact', '## Proposed Solution', '## Acceptance Criteria']
            for section in required_sections:
                if section not in body:
                    errors.append(f"Issue {issue_num}: Missing section '{section}'")
            
            # Check acceptance criteria has at least 2 items
            if '## Acceptance Criteria' in body:
                criteria_section = body.split('## Acceptance Criteria')[1]
                checkbox_count = criteria_section.count('- [ ]')
                if checkbox_count < 2:
                    errors.append(f"Issue {issue_num}: Minimum 2 acceptance criteria required")
        
        return errors


# Test Classes

class TestP0Issues:
    """Tests for P0 (Critical) issues"""
    
    def test_p0_file_exists(self):
        """Verify P0 JSON file exists"""
        filepath = Path(__file__).parent.parent / "_bmad-output/implementation-artifacts/code-review-issues-p0.json"
        assert filepath.exists(), "code-review-issues-p0.json not found"
    
    def test_p0_valid_json(self):
        """Verify P0 JSON is valid"""
        validator = CodeReviewValidator()
        data = validator.load_json('code-review-issues-p0.json')
        assert isinstance(data, dict)
        assert 'issues' in data
    
    def test_p0_file_structure(self):
        """Verify P0 file structure is correct"""
        validator = CodeReviewValidator()
        data = validator.load_json('code-review-issues-p0.json')
        errors = validator.validate_file_structure(data, 'P0')
        assert not errors, f"P0 file structure errors: {errors}"
    
    def test_p0_issues_valid(self):
        """Verify all P0 issues are valid"""
        validator = CodeReviewValidator()
        data = validator.load_json('code-review-issues-p0.json')
        issues = data.get('issues', [])
        
        assert len(issues) > 0, "P0 file has no issues"
        
        for idx, issue in enumerate(issues, 1):
            errors = validator.validate_issue(issue, 'P0', idx, data)
            assert not errors, f"P0 issue {idx} errors: {errors}"
    
    def test_p0_total_issues_count(self):
        """Verify P0 has correct number of issues"""
        validator = CodeReviewValidator()
        data = validator.load_json('code-review-issues-p0.json')
        assert len(data['issues']) == 5, "P0 should have 5 issues"


class TestP1Issues:
    """Tests for P1 (High) issues"""
    
    def test_p1_file_exists(self):
        """Verify P1 JSON file exists"""
        filepath = Path(__file__).parent.parent / "_bmad-output/implementation-artifacts/code-review-issues-p1.json"
        assert filepath.exists(), "code-review-issues-p1.json not found"
    
    def test_p1_valid_json(self):
        """Verify P1 JSON is valid"""
        validator = CodeReviewValidator()
        data = validator.load_json('code-review-issues-p1.json')
        assert isinstance(data, dict)
        assert 'issues' in data
    
    def test_p1_file_structure(self):
        """Verify P1 file structure is correct"""
        validator = CodeReviewValidator()
        data = validator.load_json('code-review-issues-p1.json')
        errors = validator.validate_file_structure(data, 'P1')
        assert not errors, f"P1 file structure errors: {errors}"
    
    def test_p1_issues_valid(self):
        """Verify all P1 issues are valid"""
        validator = CodeReviewValidator()
        data = validator.load_json('code-review-issues-p1.json')
        issues = data.get('issues', [])
        
        assert len(issues) > 0, "P1 file has no issues"
        
        for idx, issue in enumerate(issues, 1):
            errors = validator.validate_issue(issue, 'P1', idx, data)
            assert not errors, f"P1 issue {idx} errors: {errors}"


class TestP2Issues:
    """Tests for P2 (Medium) issues"""
    
    def test_p2_file_exists(self):
        """Verify P2 JSON file exists"""
        filepath = Path(__file__).parent.parent / "_bmad-output/implementation-artifacts/code-review-issues-p2.json"
        assert filepath.exists(), "code-review-issues-p2.json not found"
    
    def test_p2_valid_json(self):
        """Verify P2 JSON is valid"""
        validator = CodeReviewValidator()
        data = validator.load_json('code-review-issues-p2.json')
        assert isinstance(data, dict)
        assert 'issues' in data
    
    def test_p2_file_structure(self):
        """Verify P2 file structure is correct"""
        validator = CodeReviewValidator()
        data = validator.load_json('code-review-issues-p2.json')
        errors = validator.validate_file_structure(data, 'P2')
        assert not errors, f"P2 file structure errors: {errors}"


class TestCrossFileConsistency:
    """Tests for consistency across all files"""
    
    def test_no_duplicate_ids(self):
        """Verify no duplicate issue IDs across files"""
        validator = CodeReviewValidator()
        all_ids = set()
        
        for priority in ['P0', 'P1', 'P2', 'P3']:
            filename = f'code-review-issues-{priority.lower()}.json'
            try:
                data = validator.load_json(filename)
                for issue in data.get('issues', []):
                    issue_id = issue.get('id')
                    assert issue_id not in all_ids, f"Duplicate ID found: {issue_id}"
                    all_ids.add(issue_id)
            except FileNotFoundError:
                pass
    
    def test_sequential_numbering(self):
        """Verify sequential numbering within each priority"""
        validator = CodeReviewValidator()
        
        for priority in ['P0', 'P1', 'P2', 'P3']:
            filename = f'code-review-issues-{priority.lower()}.json'
            try:
                data = validator.load_json(filename)
                issues = sorted(data.get('issues', []), key=lambda x: int(x['id'].split('-')[1]))
                
                for idx, issue in enumerate(issues, 1):
                    expected_id = f"{priority}-{idx}"
                    actual_id = issue.get('id')
                    assert actual_id == expected_id, f"Non-sequential ID. Expected {expected_id}, got {actual_id}"
            except FileNotFoundError:
                pass


class TestAcceptanceCriteria:
    """Tests for acceptance criteria validation"""
    
    def test_acceptance_criteria_present(self):
        """Verify all issues have acceptance criteria"""
        validator = CodeReviewValidator()
        
        for priority in ['P0', 'P1', 'P2']:
            filename = f'code-review-issues-{priority.lower()}.json'
            data = validator.load_json(filename)
            
            for issue in data.get('issues', []):
                body = issue.get('body', '')
                assert '## Acceptance Criteria' in body, f"Issue {issue.get('id')} missing acceptance criteria"
                
                # Check for at least 2 criteria
                criteria_section = body.split('## Acceptance Criteria')[1]
                checkbox_count = criteria_section.count('- [ ]')
                assert checkbox_count >= 2, f"Issue {issue.get('id')} has {checkbox_count} criteria, need at least 2"
    
    def test_acceptance_criteria_format(self):
        """Verify acceptance criteria are properly formatted"""
        validator = CodeReviewValidator()
        
        for priority in ['P0', 'P1', 'P2']:
            filename = f'code-review-issues-{priority.lower()}.json'
            data = validator.load_json(filename)
            
            for issue in data.get('issues', []):
                body = issue.get('body', '')
                if '## Acceptance Criteria' in body:
                    criteria_section = body.split('## Acceptance Criteria')[1]
                    assert '- [ ]' in criteria_section, f"Issue {issue.get('id')} uses incorrect checkbox format"


class TestEffortEstimates:
    """Tests for effort estimate validation"""
    
    def test_reasonable_effort_ranges(self):
        """Verify effort estimates are within reasonable ranges"""
        validator = CodeReviewValidator()
        
        ranges = {
            'P0': (1, 16),
            'P1': (1, 8),
            'P2': (0.5, 3),
            'P3': (2, 8)
        }
        
        for priority, (min_hours, max_hours) in ranges.items():
            filename = f'code-review-issues-{priority.lower()}.json'
            try:
                data = validator.load_json(filename)
                
                for issue in data.get('issues', []):
                    effort = issue.get('effort_hours')
                    assert min_hours <= effort <= max_hours, (
                        f"Issue {issue.get('id')} effort {effort} outside range "
                        f"[{min_hours}, {max_hours}] for {priority}"
                    )
            except FileNotFoundError:
                pass


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
