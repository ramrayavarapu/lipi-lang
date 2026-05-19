import unittest
from pathlib import Path


WORKFLOW_PATH = Path(__file__).resolve().parents[1] / '.github' / 'workflows' / 'claude-build-agent.yml'


class TestClaudeBuildAgentWorkflow(unittest.TestCase):
    def setUp(self):
        self.workflow = WORKFLOW_PATH.read_text(encoding='utf-8')

    def test_design_issue_body_is_capped_before_prompt(self):
        self.assertIn('Prepare bounded design issue body', self.workflow)
        self.assertIn('LIMIT = 4000', self.workflow)
        self.assertIn('TRUNCATED_TAG = "\\n\\n[truncated]"', self.workflow)
        self.assertIn('bounded_body = body if len(body) <= LIMIT else f"{body[:LIMIT]}{TRUNCATED_TAG}"', self.workflow)

    def test_uses_bounded_design_body_in_claude_prompt(self):
        self.assertIn('${{ env.DESIGN_ISSUE_BODY }}', self.workflow)
        self.assertNotIn('${{ github.event.issue.body }}', self.workflow)
        self.assertIn('DESIGN_ISSUE_BODY<<__LIPI_DESIGN_ISSUE_BODY_EOF__', self.workflow)


if __name__ == '__main__':
    unittest.main(verbosity=2)
