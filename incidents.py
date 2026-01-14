from dataclasses import dataclass, field
from typing import List, Dict
# Define possible actions
ACTIONS = [
    "view_alert_details",
    "check_endpoint_logs",
    "check_auth_logs",
    "isolate_host",
    "block_ip",
    "reset_user_password",
    "escalate",
    "close_incident",
]

# Define incident scenarios
@dataclass
class IncidentScenario:
    name: str
    description: str
    critical_host: str
    attacker_goal: str
    max_steps: int = 10

    step_count: int = 0
    contained: bool = False
    resolved: bool = False
    attacker_progress: int = 0
    history: List[Dict] = field(default_factory=list)

    def clone(self) -> "IncidentScenario":
        return IncidentScenario(
            name=self.name,
            description=self.description,
            critical_host=self.critical_host,
            attacker_goal=self.attacker_goal,
            max_steps=self.max_steps,
        )

    def apply_action(self, action: str) -> Dict:
        self.step_count += 1
        notes: List[str] = []

        # Attacker progresses unless contained/resolved
        if not self.contained and not self.resolved:
            self.attacker_progress += 1

        if action == "view_alert_details":
            notes.append("Analyst reviewed SIEM alert metadata and timestamps.")

        elif action == "check_endpoint_logs":
            notes.append("Endpoint logs were reviewed for suspicious processes and file activity.")
            if self.name == "ransomware_workstation":
                notes.append("Multiple file renames and encryption-like writes detected after opening an email attachment.")

        elif action == "check_auth_logs":
            notes.append("Authentication logs were reviewed for anomalous logins.")
            if self.name == "compromised_user_account":
                notes.append("Burst of failed logins followed by a success from an unusual geo-location and new device.")

        elif action == "isolate_host":
            if self.name == "ransomware_workstation":
                self.contained = True
                notes.append("Workstation isolated from network. Lateral movement risk reduced.")
            else:
                notes.append("Host isolated. Impact depends on whether the incident is endpoint-driven.")

        elif action == "block_ip":
            notes.append("Firewall rule added to block suspicious IP / domain.")
            if self.name == "c2_beaconing":
                self.contained = True
                notes.append("Outbound beaconing stops after block rule applied.")

        elif action == "reset_user_password":
            if self.name == "compromised_user_account":
                self.contained = True
                notes.append("Password reset and sessions revoked. Malicious access likely cut off.")
            else:
                notes.append("Password reset performed, but incident may not be identity-related.")

        elif action == "escalate":
            notes.append("Escalated to Tier 2 / IR team with collected evidence and timeline.")

        elif action == "close_incident":
            if self.contained and self.attacker_progress < 5:
                self.resolved = True
                notes.append("Incident closed after containment and basic remediation steps.")
            else:
                # premature close worsens the situation
                notes.append("Incident closed without clear containment. Residual risk remains.")
                self.attacker_progress += 2

        attacker_success = self.attacker_progress >= 7 and not self.contained

        self.history.append(
            {
                "step": self.step_count,
                "action": action,
                "attacker_progress": self.attacker_progress,
                "contained": self.contained,
                "resolved": self.resolved,
                "attacker_success": attacker_success,
            }
        )

        return {
            "step": self.step_count,
            "action": action,
            "attacker_progress": self.attacker_progress,
            "contained": self.contained,
            "resolved": self.resolved,
            "attacker_success": attacker_success,
            "notes": notes,
        }

    def compute_reward(self, summary: Dict) -> float:
        reward = 0.0

        # Step cost to encourage efficiency
        reward -= 0.5

        # Containment bonus
        if summary["contained"]:
            reward += 5.0

        # Proper resolution bonus
        if self.resolved and summary["attacker_progress"] < 7:
            reward += 15.0

        # Premature closure penalty
        if summary["action"] == "close_incident" and not self.resolved:
            reward -= 5.0

        # Attacker wins penalty
        if summary["attacker_success"]:
            reward -= 20.0

        return reward

    def is_done(self, summary: Dict) -> bool:
        if summary["attacker_success"]:
            return True
        if self.resolved:
            return True
        if self.step_count >= self.max_steps:
            return True
        return False


def default_scenarios() -> List[IncidentScenario]:
    return [
        IncidentScenario(
            name="ransomware_workstation",
            description=(
                "Endpoint security raised an alert for suspicious encryption activity "
                "on a finance department workstation."
            ),
            critical_host="FINANCE-PC-23",
            attacker_goal="Encrypt data and demand ransom",
        ),
        IncidentScenario(
            name="compromised_user_account",
            description=(
                "Unusual login activity detected: repeated failed attempts followed by "
                "a successful login from an unfamiliar location."
            ),
            critical_host="N/A",
            attacker_goal="Maintain access to user account and data",
        ),
        IncidentScenario(
            name="c2_beaconing",
            description=(
                "Network monitoring detected outbound traffic to a known command-and-control "
                "domain from a public-facing server."
            ),
            critical_host="WEB-SRV-10",
            attacker_goal="Maintain remote control over the host",
        ),
    ]
