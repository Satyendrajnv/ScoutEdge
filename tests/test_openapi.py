"""
Unit Tests for ScoutEdge OpenAPI Specification and Swagger UI Endpoint
"""

import sys
import os
import json
import unittest
import threading
from urllib.request import urlopen

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from scoutedge.api.server import create_scoutedge_app
from scoutedge.api.openapi import get_openapi_spec_dict, get_swagger_ui_html


class TestOpenAPISpec(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = create_scoutedge_app(host="127.0.0.1", port=0)
        cls.port = cls.server.server_address[1]
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_openapi_dict_structure(self):
        spec = get_openapi_spec_dict()
        self.assertEqual(spec["openapi"], "3.0.3")
        self.assertIn("info", spec)
        self.assertIn("/api/v1/evaluate", spec["paths"])
        self.assertIn("/api/v1/health", spec["paths"])

    def test_swagger_ui_html_structure(self):
        html = get_swagger_ui_html()
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("SwaggerUIBundle", html)
        self.assertIn("/api/v1/openapi.json", html)

    def test_openapi_json_endpoint(self):
        url = f"{self.base_url}/api/v1/openapi.json"
        with urlopen(url) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode("utf-8"))
            self.assertEqual(data["openapi"], "3.0.3")
            self.assertIn("info", data)

    def test_swagger_docs_endpoint(self):
        url = f"{self.base_url}/api/v1/docs"
        with urlopen(url) as response:
            self.assertEqual(response.status, 200)
            html = response.read().decode("utf-8")
            self.assertIn("SwaggerUIBundle", html)


if __name__ == "__main__":
    unittest.main()
