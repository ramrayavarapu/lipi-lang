import unittest
from pathlib import Path


WORKFLOW_PATH = Path(__file__).resolve().parents[1] / '.github' / 'workflows' / 'design-agent.yml'


class TestDesignAgentWorkflow(unittest.TestCase):
    def setUp(self):
        self.workflow = WORKFLOW_PATH.read_text(encoding='utf-8')

    def test_design_agent_uses_github_script_v8(self):
        self.assertIn('uses: actions/github-script@v8', self.workflow)
        self.assertNotIn('uses: actions/github-script@v7', self.workflow)

    def test_design_agent_triggers_on_pull_request_open(self):
        self.assertIn('pull_request:', self.workflow)
        self.assertIn('types: [opened]', self.workflow)
        self.assertIn("github.event_name == 'pull_request'", self.workflow)

    def test_design_agent_posts_comment_for_pull_requests(self):
        self.assertIn("context.eventName === 'pull_request'", self.workflow)
        self.assertIn('Design Proposal comment posted to PR', self.workflow)
        self.assertIn('Source: Pull Request #${pr.number}', self.workflow)


if __name__ == '__main__':
    unittest.main(verbosity=2)
