from collections import defaultdict
from typing import Tuple, Dict, List
import random


def encode_state(text: str) -> Tuple[bool, bool, bool, bool]:
    """
    Coarse features from the LLM text. (No ML, just basic signals.)
    """
    t = text.lower()
    mentions_ransom = ("ransom" in t) or ("encryption" in t) or ("encrypt" in t)
    mentions_account = ("login" in t) or ("credentials" in t) or ("account" in t)
    mentions_network = ("network" in t) or ("traffic" in t) or ("beacon" in t) or ("c2" in t)
    mentions_contained = ("contained" in t) or ("isolated" in t) or ("blocked" in t) or ("mitigated" in t)
    return (mentions_ransom, mentions_account, mentions_network, mentions_contained)


class QLearningAgent:
    def __init__(
        self,
        actions: List[str],
        alpha: float = 0.15,
        gamma: float = 0.95,
        epsilon: float = 0.3,
    ):
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.Q: Dict[Tuple, Dict[str, float]] = defaultdict(
            lambda: {a: 0.0 for a in self.actions}
        )

    def choose_action(self, state_id: Tuple) -> str:
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        action_values = self.Q[state_id]
        return max(action_values, key=action_values.get)

    def update(self, state_id: Tuple, action: str, reward: float, next_state_id: Tuple) -> None:
        best_next = max(self.Q[next_state_id].values())
        old_value = self.Q[state_id][action]
        self.Q[state_id][action] = old_value + self.alpha * (reward + self.gamma * best_next - old_value)
