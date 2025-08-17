import random
from typing import Dict, List

from data.persistence import PersistenceManager
from agents.group_chat import GroupChatSystem


class JourneyOrchestrator:
    def __init__(self):
        self.persistence = PersistenceManager()
        self.chat_system = GroupChatSystem()
        self.current_state = self.persistence.load_journey_state()

    def simulate_week(self, week: int, user_message: Optional[str] = None) -> Dict:
        print(f"=== Simulating Week {week} ===")

        events = self.generate_weekly_events(week)

        if user_message:
            user_messages = [user_message]
        else:
            user_messages = self.generate_user_messages(week, events)

        weekly_conversations: List[Dict] = []
        for message in user_messages:
            context = {"week": week, "events": events}
            conversation = self.chat_system.send_message("Rohan", message, context)
            if conversation:
                weekly_conversations.extend(conversation)

        report = self.generate_weekly_report(week, events, weekly_conversations)

        self.persistence.save_weekly_report(week, report)
        self.persistence.save_conversation_history(self.chat_system.conversation_history)

        return report

    def generate_weekly_events(self, week: int) -> List[str]:
        events: List[str] = []
        if week == 1:
            events.append("onboarding_complete")
            events.append("initial_blood_test_high_sugar")
        elif week in [12, 24, 34]:
            events.append("quarterly_diagnostic_test")
        elif week == 10:
            events.append("leg_injury_reported")
        elif week % 4 == 0:
            events.append("business_travel")
        elif week % 2 == 0:
            events.append("exercise_plan_update")
        return events

    def generate_user_messages(self, week: int, events: List[str]) -> List[str]:
        messages: List[str] = []
        num_messages = random.randint(3, 5)
        for _ in range(num_messages):
            if "leg_injury_reported" in events:
                messages.append("I twisted my leg at the hotel gym - it's painful and swollen. What should I do?")
            elif "business_travel" in events:
                messages.append("I'm traveling to Singapore next week. How should I adjust my plan?")
            elif "quarterly_diagnostic_test" in events:
                messages.append("Just got my test results back. Can we review them together?")
            else:
                curiosity_messages = [
                    "I read about CGM devices. Should I get one for better blood sugar monitoring?",
                    "What's the latest research on intermittent fasting for diabetes?",
                    "How does sleep quality affect blood sugar levels?",
                    "Can stress really impact my A1C levels?",
                    "What supplements should I consider for better metabolic health?",
                ]
                messages.append(random.choice(curiosity_messages))
        return messages

    def generate_weekly_report(self, week: int, events: List[str], conversations: List[Dict]) -> Dict:
        adherence = random.choice([0.3, 0.5, 0.7, 0.8])
        blood_sugar_improvement = max(0, (week - 1) * 2)
        return {
            "week": week,
            "events": events,
            "conversations_count": len(conversations),
            "adherence_rate": adherence,
            "health_metrics": {
                "blood_sugar_avg": max(120, 180 - blood_sugar_improvement),
                "a1c": max(5.5, 6.2 - (week * 0.02)),
                "weight": 75 - (week * 0.1) if week > 4 else 75,
            },
            "agent_actions": {
                "doctor_hours": random.randint(8, 15),
                "coach_hours": random.randint(10, 20),
            },
            "recommendations": self.extract_recommendations(conversations),
        }

    def extract_recommendations(self, conversations: List[Dict]) -> List[str]:
        recommendations: List[str] = []
        for conv in conversations:
            if conv.get("sender") != "Rohan" and "recommend" in conv.get("message", "").lower():
                recommendations.append(f"{conv['sender']}: {conv['message'][:100]}...")
        return recommendations

    def run_full_journey(self):
        for week in range(1, 35):
            report = self.simulate_week(week)
            print(f"Week {week} completed - Adherence: {report['adherence_rate']:.1%}")
        print("8-month journey simulation completed!")


