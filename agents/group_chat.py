import os
from typing import Dict, List, Optional, Union

from .crewai_orchestrator import CrewOrchestrator
from .elyx_agents import AgentOrchestrator
from .llm_router import LLMRouter


class GroupChatSystem:
    def __init__(self, use_crewai: bool = True):
        self.conversation_history: List[Dict] = []
        self.use_crewai = use_crewai
        if use_crewai:
            self.crew_orchestrator = CrewOrchestrator()
            self.agent_router = AgentOrchestrator()
        else:
            self.router = LLMRouter()

    def send_message(
        self,
        sender: str,
        message: str,
        context: Optional[Dict] = None,
    ) -> Union[List[Dict], None]:
        print(f"\n💬 {sender}: {message}")

        if sender == "Rohan":
            self.conversation_history.append({"sender": sender, "message": message})

            if self.use_crewai:
                # 1. Route message to get the right agent
                agent_name = self.agent_router.route_message(message, context)[0]

                # 2. Ask the selected agent
                response_text = self.crew_orchestrator.ask(agent_name, message, context)
                response = {"agent": agent_name, "message": response_text}
            else:
                response = self.router.route_message(message, context)

            if response:
                self.conversation_history.append(
                    {"sender": response["agent"], "message": response["message"]}
                )
                print(f"🤖 {response['agent']}: {response['message']}")
                return [
                    {"sender": sender, "message": message},
                    {"sender": response["agent"], "message": response["message"]},
                ]
            return [{"sender": sender, "message": message}]
        return None

    def get_conversation_history(self) -> List[Dict]:
        return self.conversation_history
