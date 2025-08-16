import json
import os
import uuid
from datetime import datetime
from typing import Dict, List


class SuggestionsStore:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.path = os.path.join(self.data_dir, "suggestions.json")

    def _load(self) -> List[Dict]:
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _save(self, items: List[Dict]):
        with open(self.path, "w") as f:
            json.dump(items, f, indent=2)

    def list(self) -> List[Dict]:
        return self._load()

    def add_many(self, items: List[Dict]):
        existing = self._load()
        for it in items:
            it.setdefault("id", str(uuid.uuid4()))
            it.setdefault("status", "proposed")
            it.setdefault("created_at", datetime.now().isoformat())
        existing.extend(items)
        self._save(existing)

    def update_status(self, item_id: str, status: str) -> bool:
        items = self._load()
        updated = False
        for it in items:
            if it.get("id") == item_id:
                it["status"] = status
                updated = True
                break
        if updated:
            self._save(items)
        return updated


