"""
Unit Tests for ScoutEdge CLI Interface
"""

import sys
import os
import unittest
from io import StringIO
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from scoutedge.cli.main import main as cli_main


class TestScoutEdgeCLI(unittest.TestCase):
    def test_cli_version_command(self):
        with patch("sys.argv", ["scoutedge", "version"]):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                cli_main()
                output = fake_out.getvalue()
                self.assertIn("ScoutEdge Sports Intelligence Infrastructure", output)

    def test_cli_eval_demo_command(self):
        with patch("sys.argv", ["scoutedge", "eval", "--demo"]):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                cli_main()
                output = fake_out.getvalue()
                self.assertIn("SCOUTEDGE ATHLETE EVALUATION REPORT", output)
                self.assertIn("SE-R™ Rating", output)
                self.assertIn("RECOMMENDATION", output)

    def test_cli_benchmark_command(self):
        with patch("sys.argv", ["scoutedge", "benchmark", "--count", "20"]):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                cli_main()
                output = fake_out.getvalue()
                self.assertIn("SCOUTEDGE PIPELINE BENCHMARK REPORT", output)
                self.assertIn("Throughput Speed", output)


if __name__ == "__main__":
    unittest.main()
