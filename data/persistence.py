import json
import os
from typing import List, Dict


class PersistenceManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def save_conversation_history(self, history: List[Dict]):
        filename = os.path.join(self.data_dir, "conversation_history.json")
        with open(filename, "w") as f:
            json.dump(history, f, indent=2)

    def load_conversation_history(self) -> List[Dict]:
        filename = os.path.join(self.data_dir, "conversation_history.json")
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_journey_state(self, state: Dict):
        filename = os.path.join(self.data_dir, "journey_state.json")
        with open(filename, "w") as f:
            json.dump(state, f, indent=2)

    def load_journey_state(self) -> Dict:
        filename = os.path.join(self.data_dir, "journey_state.json")
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"current_week": 1, "total_weeks": 34}

    def save_weekly_report(self, week: int, report: Dict):
        filename = os.path.join(self.data_dir, f"week_{week:02d}_report.json")
        with open(filename, "w") as f:
            json.dump(report, f, indent=2)


