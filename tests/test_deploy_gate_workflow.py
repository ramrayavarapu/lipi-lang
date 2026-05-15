import unittest
from pathlib import Path


WORKFLOW_PATH = Path(__file__).resolve().parents[1] / '.github' / 'workflows' / 'deploy-gate.yml'


class TestDeployGateWorkflow(unittest.TestCase):
    def setUp(self):
        self.workflow = WORKFLOW_PATH.read_text(encoding='utf-8')

    def test_resolves_pr_before_check_runs(self):
        self.assertIn("prs = gh_get_with_retry(f'/repos/{repo}/commits/{sha}/pulls')", self.workflow)
        self.assertIn("runs = gh_get_with_retry(f'/repos/{repo}/commits/{pr_sha}/check-runs')", self.workflow)
        self.assertNotIn("gh_get(f'/repos/{repo}/commits/{sha}/check-runs')", self.workflow)

    def test_direct_pushes_skip_the_gate(self):
        self.assertIn("if not prs:", self.workflow)
        self.assertIn("Skipping deploy gate (direct pushes bypass the PR review workflow by definition).", self.workflow)
        self.assertIn("sys.exit(0)", self.workflow)

    def test_failed_checks_message_includes_pr_number(self):
        self.assertIn("print(f'\\n🚫 Deploy gate FAILED — not all required checks passed on PR #{pr_number}.')", self.workflow)


if __name__ == '__main__':
    unittest.main(verbosity=2)
