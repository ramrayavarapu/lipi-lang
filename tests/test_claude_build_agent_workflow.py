import unittest
from pathlib import Path


WORKFLOW_PATH = Path(__file__).resolve().parents[1] / '.github' / 'workflows' / 'claude-build-agent.yml'
DESIGN_BODY_LIMIT = 4000
TRUNCATED_TAG = '\n\n[truncated]'


class TestClaudeBuildAgentWorkflow(unittest.TestCase):
    def setUp(self):
        self.workflow = WORKFLOW_PATH.read_text(encoding='utf-8')

    def test_design_issue_body_is_capped_before_prompt(self):
        self.assertIn('Prepare bounded design issue body', self.workflow)
        self.assertIn('LIMIT = 4000', self.workflow)
        self.assertIn('TRUNCATED_TAG = "\\n\\n[truncated]"', self.workflow)
        self.assertIn('bounded_body = body if len(body) <= LIMIT else f"{body[:LIMIT]}{TRUNCATED_TAG}"', self.workflow)

    def test_truncation_output_format(self):
        over_limit_body = 'x' * (DESIGN_BODY_LIMIT + 10)
        bounded_body = (
            over_limit_body
            if len(over_limit_body) <= DESIGN_BODY_LIMIT
            else f"{over_limit_body[:DESIGN_BODY_LIMIT]}{TRUNCATED_TAG}"
        )

        self.assertEqual(DESIGN_BODY_LIMIT + len(TRUNCATED_TAG), len(bounded_body))
        self.assertTrue(bounded_body.endswith(TRUNCATED_TAG))

    def test_uses_bounded_design_body_in_claude_prompt(self):
        self.assertIn('--- DESIGN ---', self.workflow)
        self.assertIn('--- END DESIGN ---', self.workflow)
        design_block = self.workflow.split('--- DESIGN ---', 1)[1].split('--- END DESIGN ---', 1)[0]
        self.assertIn('${{ env.DESIGN_ISSUE_BODY }}', design_block)
        self.assertNotIn('${{ github.event.issue.body }}', design_block)
        self.assertIn('DESIGN_ISSUE_BODY<<__DESIGN_ISSUE_BODY_EOF__', self.workflow)


if __name__ == '__main__':
    unittest.main(verbosity=2)
