from typing import Dict, List
from simulation.journey_orchestrator import JourneyOrchestrator
from simulation.decision_tree_planner import DecisionTreePlanner
from simulation.xml_parser import XMLEpisodeParser

class CompleteJourney:
    def __init__(self, num_months: int = 8):
        self.num_weeks = num_months * 4
        self.orchestrator = JourneyOrchestrator()
        self.planner = DecisionTreePlanner()
        self.parser = XMLEpisodeParser('episodes.xml')
        self.episodes = self.parser.parse_episodes()

    def run(self) -> Dict:
        """
        Runs the complete journey simulation using the episodes from episodes.xml.
        """
        print(f"🚀 Starting Complete Journey Simulation for {self.num_weeks} weeks...")

        journey_data = []

        for episode in self.episodes:
            print(f"--- Starting Episode: {episode['name']} ---")
            for message in episode['messages']:
                # This is a simplified simulation of the back-and-forth conversation
                # A more complex implementation would handle the interactive flow
                user_message = message['text']
                print(f"--- Rohan says: '{user_message}' ---")

                weekly_report = self.orchestrator.simulate_week(1, user_message) # a mock week

                next_action = self.planner.get_next_action(weekly_report)
                if next_action:
                    weekly_report["suggested_action"] = next_action
                    print(f"🧠 Planner suggestion: {next_action}")

                journey_data.append(weekly_report)

            print(f"--- Finished Episode: {episode['name']} ---")


        print("🎉 Complete Journey Simulation finished!")

        return {
            "conversation_history": self.orchestrator.chat_system.get_conversation_history(),
            "journey_data": journey_data,
        }
