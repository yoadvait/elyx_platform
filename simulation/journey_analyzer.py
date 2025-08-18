from typing import List, Dict, Any

class JourneyAnalyzer:
    def analyze(self, conversation_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyzes the conversation history and returns a structured journey summary.
        This is a mock implementation.
        """

        summary = {
            "total_episodes": 8,
            "key_milestones": [
                "Onboarded and set up Whoop device.",
                "Identified correlation between late-night coffee and poor sleep.",
                "Successfully managed jetlag during USA trip.",
                "Recovered from stomach ache and identified potential food sensitivity.",
                "Managed high-stress period with breathing exercises.",
                "Addressed high blood pressure with lifestyle changes.",
                "Resolved back ache by changing mattress.",
                "Improved glucose control with diet plan.",
            ],
            "overall_progress": "Rohan has made significant progress in understanding and managing his health. He has learned to correlate his lifestyle choices with his health metrics and has proactively sought solutions to his health challenges."
        }

        return summary
