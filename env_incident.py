from typing import Tuple, List, Dict
import random

from incidents import IncidentScenario, default_scenarios, ACTIONS
from llm_client import BaseLLMClient


class IncidentEnv:
    def __init__(self, llm_client: BaseLLMClient):
        self.llm_client = llm_client
        self.scenario_templates: List[IncidentScenario] = default_scenarios()
        self.current: IncidentScenario | None = None
        self.dialog_history: List[Dict[str, str]] = []
        self.last_state_text: str | None = None

    def reset(self) -> str:
        template = random.choice(self.scenario_templates)
        self.current = template.clone()
        self.dialog_history = []

        system_msg = {
            "role": "system",
            "content": (
                "You are a SOC incident simulator. You receive hidden incident state and an analyst action. "
                "Respond with what the analyst would observe: alerts, logs, user reports, and next hints. "
                "Keep responses concise: 3 to 6 sentences. Never reveal hidden fields like attacker_progress. "
                "If containment seems achieved, say it in natural SOC language. "
                "Avoid providing hacking instructions; focus on defense and incident response."
            ),
        }

        user_msg = {
            "role": "user",
            "content": (
                f"Incident description: {self.current.description}\n"
                f"Critical host: {self.current.critical_host}\n"
                "Start the scenario. Describe what the analyst initially sees in the SOC tools."
            ),
        }

        self.dialog_history = [system_msg, user_msg]
        text = self.llm_client.generate(self.dialog_history)
        self.dialog_history.append({"role": "assistant", "content": text})

        self.last_state_text = text
        return text

    def step(self, action: str) -> Tuple[str, float, bool]:
        if self.current is None:
            raise RuntimeError("Call reset() before step().")

        if action not in ACTIONS:
            raise ValueError(f"Unknown action: {action}")

        summary = self.current.apply_action(action)
        reward = self.current.compute_reward(summary)
        done = self.current.is_done(summary)

        internal_summary = (
            f"Internal incident summary (hidden from analyst):\n"
            f"- Name: {self.current.name}\n"
            f"- Attacker progress level: {summary['attacker_progress']}\n"
            f"- Contained: {summary['contained']}\n"
            f"- Resolved: {summary['resolved']}\n"
            f"- Last action: {summary['action']}\n"
            f"- Notes: {'; '.join(summary['notes'])}"
        )

        user_msg = {
            "role": "user",
            "content": (
                f"{internal_summary}\n\n"
                "Now describe what the analyst sees after this action in realistic SOC terms."
            ),
        }

        self.dialog_history.append(user_msg)
        text = self.llm_client.generate(self.dialog_history)
        self.dialog_history.append({"role": "assistant", "content": text})

        self.last_state_text = text
        return text, reward, done


def available_actions() -> List[str]:
    return ACTIONS
