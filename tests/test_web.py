"""
Unit Tests for ScoutEdge Glassmorphic Web Dashboard Interface
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


class TestWebDashboard(unittest.TestCase):
    def setUp(self):
        self.web_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../web"))

    def test_web_files_exist(self):
        html_path = os.path.join(self.web_dir, "index.html")
        css_path = os.path.join(self.web_dir, "styles.css")
        js_path = os.path.join(self.web_dir, "app.js")

        self.assertTrue(os.path.exists(html_path), "index.html must exist")
        self.assertTrue(os.path.exists(css_path), "styles.css must exist")
        self.assertTrue(os.path.exists(js_path), "app.js must exist")

    def test_html_content_structure(self):
        html_path = os.path.join(self.web_dir, "index.html")
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("ScoutEdge Live™", content)
        self.assertIn("SE-R™ Rating Engine", content)
        self.assertIn("PGI™ Growth Index", content)
        self.assertIn("EdgeCare™ Readiness", content)
        self.assertIn("Financial Valuation & Contract Efficiency", content)

    def test_css_glassmorphism(self):
        css_path = os.path.join(self.web_dir, "styles.css")
        with open(css_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("backdrop-filter: blur", content)
        self.assertIn("--cyan", content)
        self.assertIn("--emerald", content)


if __name__ == "__main__":
    unittest.main()
