from __future__ import annotations

import json
from typing import Dict, List, Optional

from .base_agent import BaseAgent


class IssueExtractor:
    """LLM-backed extractor to identify problems/issues/doubts from a user message.

    Returns structured JSON safe for storage.
    """

    def __init__(self):
        self.agent = BaseAgent(
            name="IssueExtractor",
            role="Classifier",
            system_prompt=(
                """
You are a concise classifier that extracts PROBLEMS/ISSUES/DOUBTS from a user's message.
Output STRICT JSON with shape:
{
  "issues": [
    {"title": str, "details": str, "category": str, "severity": "low|medium|high"}
  ]
}
Rules:
- If none found, return {"issues": []}.
- categories to prefer: "medical", "nutrition", "physio", "logistics", "performance", "other".
- Keep titles short (<=80 chars). Details <= 240 chars.
"""
            ),
        )

    def build_messages(self, message: str, context: Optional[Dict] = None) -> List[Dict[str, str]]:
        u = {
            "role": "user",
            "content": (
                f"User message: {message}\n\n"
                f"Context: {json.dumps(context) if context else '{}'}\n\n"
                "Extract issues now."
            ),
        }
        return [
            {"role": "system", "content": self.agent.system_prompt},
            u,
        ]

    def extract(self, message: str, context: Optional[Dict] = None) -> List[Dict]:
        msgs = self.build_messages(message, context)
        raw = self.agent.call_openrouter(msgs)
        try:
            data = json.loads(raw)
        except Exception:
            # attempt to find object
            import re

            m = re.search(r"\{[\s\S]*\}", raw)
            if not m:
                return []
            try:
                data = json.loads(m.group(0))
            except Exception:
                return []
        issues = data.get("issues")
        if not isinstance(issues, list):
            return []
        cleaned: List[Dict] = []
        for it in issues:
            if not isinstance(it, dict):
                continue
            title = str(it.get("title", "")).strip()
            details = str(it.get("details", "")).strip()
            category = str(it.get("category", "other")).strip() or "other"
            severity = str(it.get("severity", "medium")).strip().lower()
            if not title:
                continue
            if severity not in {"low", "medium", "high"}:
                severity = "medium"
            cleaned.append(
                {
                    "title": title[:200],
                    "details": details[:500],
                    "category": category[:40],
                    "severity": severity,
                }
            )
        return cleaned


