from __future__ import annotations

import json
from typing import Dict, List, Optional

from .base_agent import BaseAgent


class PlanExtractor:
    """LLM-backed extractor to identify suggestions/plans/recommendations in an agent reply."""

    def __init__(self):
        self.agent = BaseAgent(
            name="PlanExtractor",
            role="Summarizer",
            system_prompt=(
                """
You extract actionable suggestions/plans from an AGENT reply.
Output STRICT JSON with shape:
{
  "suggestions": [
    {"title": str, "details": str, "category": str}
  ]
}
Rules:
- Summarize concrete actions only (meals/supplements/exercises/tests/logistics, etc.).
- categories: "medical", "nutrition", "physio", "logistics", "performance", "other".
- Keep titles <= 80 chars; details <= 300 chars.
"""
            ),
        )

    def build_messages(self, agent_name: str, reply: str, context: Optional[Dict] = None) -> List[Dict[str, str]]:
        u = {
            "role": "user",
            "content": (
                f"Agent: {agent_name}\nReply: {reply}\n\n"
                f"Context: {json.dumps(context) if context else '{}'}\n\n"
                "Extract suggestions now."
            ),
        }
        return [
            {"role": "system", "content": self.agent.system_prompt},
            u,
        ]

    def extract(self, agent_name: str, reply: str, context: Optional[Dict] = None) -> List[Dict]:
        msgs = self.build_messages(agent_name, reply, context)
        raw = self.agent.call_openrouter(msgs)
        try:
            data = json.loads(raw)
        except Exception:
            import re

            m = re.search(r"\{[\s\S]*\}", raw)
            if not m:
                return []
            try:
                data = json.loads(m.group(0))
            except Exception:
                return []
        items = data.get("suggestions")
        if not isinstance(items, list):
            return []
        out: List[Dict] = []
        for s in items:
            if not isinstance(s, dict):
                continue
            title = str(s.get("title", "")).strip()
            details = str(s.get("details", "")).strip()
            category = (str(s.get("category", "other")).strip() or "other")[:40]
            if not title:
                continue
            out.append({"title": title[:200], "details": details[:600], "category": category})
        return out


