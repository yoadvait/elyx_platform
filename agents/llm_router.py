from __future__ import annotations

import json
import re
from typing import Dict, List, Optional, Tuple

from .base_agent import BaseAgent
from .elyx_agents import (
    RubyAgent,
    DrWarrenAgent,
    AdvikAgent,
    CarlaAgent,
    RachelAgent,
    NeelAgent,
)


class LLMRouter:
    """LLM-based router that decides which agents should reply based on message meaning.

    Returns a minimal set of relevant agents; avoids hard-coded keyword rules.
    """

    def __init__(self):
        # Build registry with agent role/system prompts for routing context
        self.agent_descriptions: Dict[str, str] = {
            "Ruby": RubyAgent().system_prompt,
            "Dr. Warren": DrWarrenAgent().system_prompt,
            "Advik": AdvikAgent().system_prompt,
            "Carla": CarlaAgent().system_prompt,
            "Rachel": RachelAgent().system_prompt,
            "Neel": NeelAgent().system_prompt,
        }

        self.router = BaseAgent(
            name="Router",
            role="Orchestrator",
            system_prompt=(
                """
You are an expert router for a multi-agent healthcare team. Your goal is to select the SINGLE most relevant agent,
unless the message clearly spans multiple domains. Choose the smallest set (usually 1).

Team (roles & voices):
- Ruby (Concierge / Orchestrator): default agent, logistics, coordination, scheduling, reminders, follow-ups. Voice: empathetic, organized, proactive.
- Dr. Warren (Medical Strategist): lab results, medical records, diagnostics, medical direction. Voice: authoritative, precise, scientific.
- Advik (Performance Scientist): wearable data (Whoop, Oura), sleep, recovery, HRV, stress, cardiovascular training. Voice: analytical, data-driven.
- Carla (Nutritionist): nutrition plans, food logs, CGM data, supplements, fuel pillar. Voice: practical, educational, behavioral change.
- Rachel (Physiotherapist): movement, strength training, mobility, injury rehab, exercise programming. Voice: direct, form & function focused.
- Neel (Concierge Lead): escalations, strategic reviews, value framing, long-term goals. Voice: strategic, reassuring, big-picture.

Rules: Do NOT include Ruby unless the user is asking for scheduling/coordination/logistics.
Output STRICT JSON only: {"agents": ["Name", ...]} with valid names from the list above.
"""
            ),
        )

    def _build_route_prompt(self, message: str, context: Optional[Dict] = None) -> List[Dict[str, str]]:
        descriptions = "\n".join([f"- {k}: {v}" for k, v in self.agent_descriptions.items()])
        route_instructions = (
            f"Agents:\n{descriptions}\n\n"
            f"User Message: {message}\n"
            f"Context: {json.dumps(context) if context else '{}'}\n\n"
            "Return STRICT JSON only."
        )
        return [
            {"role": "system", "content": self.router.system_prompt},
            {"role": "user", "content": route_instructions},
        ]

    def _extract_json(self, text: str) -> Dict:
        # Try direct JSON
        try:
            return json.loads(text)
        except Exception:
            pass
        # Try to find first JSON object in text
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                return {}
        return {}

    _cache: Dict[Tuple[str, str], List[str]] = {}

    def route(self, message: str, context: Optional[Dict] = None, max_agents: int = 2) -> List[str]:
        cache_key = (message.strip(), json.dumps(context or {}, sort_keys=True))
        if cache_key in self._cache:
            return self._cache[cache_key][:max_agents]

        msgs = self._build_route_prompt(message, context)
        raw = self.router.call_openrouter(msgs)
        data = self._extract_json(raw)
        agents = data.get("agents") if isinstance(data, dict) else None
        result: List[str]
        if isinstance(agents, list):
            valid = [a for a in agents if a in self.agent_descriptions]
            seen = set()
            ordered: List[str] = []
            for a in valid:
                if a not in seen:
                    seen.add(a)
                    ordered.append(a)
            result = ordered[:max_agents]
        else:
            # Conservative fallback: no agent selected; let Ruby route only if explicitly logistics
            result = []

        # Tiny LRU: cap cache size to 128 entries
        if len(self._cache) > 128:
            self._cache.pop(next(iter(self._cache)))
        self._cache[cache_key] = result
        return result


