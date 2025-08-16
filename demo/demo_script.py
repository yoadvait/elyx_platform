import time
import sys
import os

# Ensure project root is on sys.path when running this file directly
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from simulation.journey_orchestrator import JourneyOrchestrator


def run_demo():
    print("🎬 Starting Elyx Healthcare Demo")
    orchestrator = JourneyOrchestrator()

    demo_scenarios = [
        {"week": 1, "description": "Onboarding with high blood sugar"},
        {"week": 10, "description": "Leg injury event injection"},
        {"week": 12, "description": "Improved blood sugar results"},
        {"week": 24, "description": "Full recovery milestone"},
    ]

    for scenario in demo_scenarios:
        print(f"\n📍 Week {scenario['week']}: {scenario['description']}")
        report = orchestrator.simulate_week(scenario["week"])
        print(f"✅ Adherence: {report['adherence_rate']:.1%}")
        print(f"🩺 Agent Actions: {report['agent_actions']}")
        time.sleep(1)

    print("\n🎉 Demo completed!")


if __name__ == "__main__":
    run_demo()


