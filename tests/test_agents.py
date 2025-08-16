import os
import unittest

os.environ.setdefault("USE_MOCK_RESPONSES", "1")

from agents.elyx_agents import RubyAgent, DrWarrenAgent  # noqa: E402


class TestAgents(unittest.TestCase):
    def setUp(self):
        self.ruby = RubyAgent()
        self.dr_warren = DrWarrenAgent()

    def test_ruby_scheduling_response(self):
        message = "Can you schedule my blood test?"
        response = self.ruby.respond(message)
        self.assertTrue(len(response) > 0)

    def test_dr_warren_medical_response(self):
        message = "My blood sugar is high"
        response = self.dr_warren.respond(message)
        self.assertTrue(len(response) > 0)


if __name__ == "__main__":
    unittest.main()


