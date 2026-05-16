import unittest
from pathlib import Path


WORKFLOW_PATH = Path(__file__).resolve().parents[1] / '.github' / 'workflows' / 'design-agent.yml'


class TestDesignAgentWorkflow(unittest.TestCase):
    def setUp(self):
        self.workflow = WORKFLOW_PATH.read_text(encoding='utf-8')

    def test_design_agent_uses_github_script_v8(self):
        self.assertIn('uses: actions/github-script@v8', self.workflow)
        self.assertNotIn('uses: actions/github-script@v7', self.workflow)


if __name__ == '__main__':
    unittest.main(verbosity=2)
