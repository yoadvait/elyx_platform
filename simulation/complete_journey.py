from typing import Dict, List
from simulation.journey_orchestrator import JourneyOrchestrator
from simulation.decision_tree_planner import DecisionTreePlanner

class CompleteJourney:
    def __init__(self, messages: List[str], num_months: int = 8):
        self.messages = messages
        self.num_weeks = num_months * 4
        self.orchestrator = JourneyOrchestrator()
        self.planner = DecisionTreePlanner()

    def run(self) -> Dict:
        """
        Runs the complete journey simulation using the provided messages.
        """
        print(f"🚀 Starting Complete Journey Simulation for {self.num_weeks} weeks...")

        journey_data = []

        for week in range(1, self.num_weeks + 1):
            # Use a message for the week if available
            if self.messages:
                user_message = self.messages.pop(0)
            else:
                user_message = "Just checking in for the week."

            print(f"--- Week {week}: Rohan says: '{user_message}' ---")

            weekly_report = self.orchestrator.simulate_week(week, user_message)

            # Use the planner to get the next action

            next_action = self.planner.get_next_action(weekly_report)
            if next_action:
                weekly_report["suggested_action"] = next_action
                print(f"🧠 Planner suggestion: {next_action}")

            journey_data.append(weekly_report)

            print(f"✅ Week {week} completed.")

        print("🎉 Complete Journey Simulation finished!")

        return {
            "conversation_history": self.orchestrator.chat_system.get_conversation_history(),
            "journey_data": journey_data,
        }
