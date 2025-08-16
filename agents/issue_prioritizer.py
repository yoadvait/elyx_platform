from __future__ import annotations

from typing import Dict, Optional

from .base_agent import BaseAgent


class IssuePrioritizer:
    """LLM-backed prioritizer with keyword fallbacks.

    Returns: {"priority": "low|medium|high|critical", "time_window": "6-24h|3-5d|3-6m|..."}
    """

    def __init__(self):
        self.agent = BaseAgent(
            name="IssuePrioritizer",
            role="Triage",
            system_prompt=(
                """
You prioritize member issues by urgency and expected resolution/recovery timeline.
Output STRICT JSON: {"priority": "low|medium|high|critical", "time_window": "<number>-<number><h|d|w|m>"}
Guidance examples:
- headache: priority=medium-high, time_window=6-24h
- leg fracture: priority=high, time_window=3-6m
- stomach ache: priority=medium, time_window=12-24h
- viral fever: priority=high, time_window=3-5d
Fallback to reasonable defaults if uncertain.
                """
            ),
        )

    def prioritize(self, title: str, details: str, context: Optional[Dict] = None) -> Dict[str, str]:
        try:
            messages = [
                {"role": "system", "content": self.agent.system_prompt},
                {"role": "user", "content": f"Title: {title}\nDetails: {details}\nContext: {context or {}}\nReturn STRICT JSON only."},
            ]
            raw = self.agent.call_openrouter(messages)
            import json, re
            try:
                data = json.loads(raw)
            except Exception:
                m = re.search(r"\{[\s\S]*\}", raw)
                data = json.loads(m.group(0)) if m else {}
            pr = str(data.get("priority", "medium")).lower()
            tw = str(data.get("time_window", "24-72h"))
            return {"priority": pr, "time_window": tw}
        except Exception:
            # Keyword fallback
            lower = f"{title} {details}".lower()
            if any(k in lower for k in ["fracture", "broken bone"]):
                return {"priority": "high", "time_window": "3-6m"}
            if any(k in lower for k in ["viral", "fever", "flu"]):
                return {"priority": "high", "time_window": "3-5d"}
            if any(k in lower for k in ["headache", "migraine"]):
                return {"priority": "medium-high", "time_window": "6-24h"}
            if any(k in lower for k in ["stomach", "abdominal", "ache"]):
                return {"priority": "medium", "time_window": "12-24h"}
            # Default
            return {"priority": "medium", "time_window": "24-72h"}


