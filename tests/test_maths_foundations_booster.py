import unittest
from pathlib import Path


APP_DIR = Path(__file__).resolve().parents[1] / 'maths-foundations-booster'


class TestMathsFoundationsBooster(unittest.TestCase):
    def test_app_files_exist(self):
        self.assertTrue((APP_DIR / 'index.html').exists())
        self.assertTrue((APP_DIR / 'app.js').exists())
        self.assertTrue((APP_DIR / 'styles.css').exists())
        self.assertTrue((APP_DIR / 'README.md').exists())

    def test_index_includes_required_sections(self):
        content = (APP_DIR / 'index.html').read_text(encoding='utf-8')
        self.assertIn('id="auth-section"', content)
        self.assertIn('id="dashboard-section"', content)
        self.assertIn('id="activity-section"', content)
        self.assertIn('id="exercise-section"', content)

    def test_app_js_has_data_flow_functions(self):
        content = (APP_DIR / 'app.js').read_text(encoding='utf-8')
        self.assertIn('function registerUser()', content)
        self.assertIn('function loginUser()', content)
        self.assertIn('function startActivity()', content)
        self.assertIn('function submitAnswer()', content)


if __name__ == '__main__':
    unittest.main(verbosity=2)
