from typing import Dict, List
from simulation.journey_orchestrator import JourneyOrchestrator
from simulation.decision_tree_planner import DecisionTreePlanner
from simulation.xml_parser import XMLEpisodeParser
from simulation.journey_analyzer import JourneyAnalyzer

class CompleteJourney:
    def __init__(self, xml_content: str, num_months: int = 8):
        self.num_weeks = num_months * 4
        self.orchestrator = JourneyOrchestrator()
        self.planner = DecisionTreePlanner()
        self.parser = XMLEpisodeParser(xml_content)
        self.episodes = self.parser.parse_episodes()
        self.analyzer = JourneyAnalyzer()

    def run(self) -> Dict:
        """
        Runs the complete journey simulation for 242 days.
        """
        print(f"🚀 Starting Complete Journey Simulation for 242 days...")

        from datetime import datetime, timedelta

        start_date = datetime.now()

        journey_data = []

        # Create a flat list of messages with their timing
        scheduled_messages = []
        for episode in self.episodes:
            for message in episode['messages']:
                day = int(message['day'])
                # This is a simplified mapping of episode to day
                # A more robust solution would parse the episode name
                import re
                match = re.search(r'Month (\d+)', episode['name'])
                if match:
                    month = int(match.group(1))
                    day += (month - 1) * 30

                scheduled_messages.append({"day": day, "text": message['text']})

        for day in range(1, 243):
            user_message = "Just checking in."
            for msg in scheduled_messages:
                if msg['day'] == day:
                    user_message = msg['text']
                    break

            print(f"--- Day {day}: Rohan says: '{user_message}' ---")

            current_date = start_date + timedelta(days=day-1)
            message_time = current_date.strftime("%H:%M:%S")
            message_date = current_date.strftime("%Y-%m-%d")

            weekly_report = self.orchestrator.simulate_week(day // 7 + 1, user_message)

            # Add timestamp to conversation history
            for conv in self.orchestrator.chat_system.conversation_history:
                if 'date' not in conv:
                    conv['date'] = message_date
                    conv['time'] = message_time

            next_action = self.planner.get_next_action(weekly_report)
            if next_action:
                weekly_report["suggested_action"] = next_action
                print(f"🧠 Planner suggestion: {next_action}")

            journey_data.append(weekly_report)

        print("🎉 Complete Journey Simulation finished!")

        # Analyze the journey
        journey_summary = self.analyzer.analyze(self.orchestrator.chat_system.get_conversation_history())

        return {
            "conversation_history": self.orchestrator.chat_system.get_conversation_history(),
            "journey_data": journey_data,
            "journey_summary": journey_summary,
        }
