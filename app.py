# app.py

import streamlit as st

st.set_page_config(page_title="LLM-Guided RL Simulator for Cyber Incident Response Training", layout="wide")

from llm_client import OpenRouterLLMClient
from env_incident import IncidentEnv, available_actions
from scoring import compute_human_score
from report import build_pdf_bytes


@st.cache_resource
def get_env() -> IncidentEnv:
    client = OpenRouterLLMClient()
    env = IncidentEnv(client)
    return env


def init_state():
    st.session_state.setdefault("state_text", None)
    st.session_state.setdefault("done", False)
    st.session_state.setdefault("log", [])
    st.session_state.setdefault("step", 0)
    st.session_state.setdefault("reward_log", [])


def start_new(env: IncidentEnv):
    text = env.reset()
    st.session_state["state_text"] = text
    st.session_state["done"] = False
    st.session_state["log"] = [("SCENARIO", text)]
    st.session_state["step"] = 0
    st.session_state["reward_log"] = []


def do_action(env: IncidentEnv, action: str):
    text, reward, done = env.step(action)
    st.session_state["state_text"] = text
    st.session_state["done"] = done
    st.session_state["step"] += 1
    st.session_state["log"].append(("ACTION", action))
    st.session_state["log"].append(("ENV", text))
    st.session_state["reward_log"].append(reward)


def build_timeline_for_report(log_items):
    """
    Turns session log into readable timeline lines for PDF.
    Keeps ENV text trimmed to avoid massive PDFs.
    """
    timeline = []
    step_num = 0
    for role, msg in log_items:
        if role == "SCENARIO":
            timeline.append("Scenario start:")
            timeline.append(msg.strip())
            timeline.append("")
        elif role == "ACTION":
            step_num += 1
            timeline.append(f"{step_num}. Action: {msg}")
        elif role == "ENV":
            snippet = msg.strip().replace("\n", " ")
            if len(snippet) > 350:
                snippet = snippet[:350] + "..."
            timeline.append(f"   Outcome: {snippet}")
    return timeline


def main():
    st.title("LLM-Guided RL Simulator for Cyber Incident Response Training")

    init_state()

    try:
        env = get_env()
    except Exception as e:
        st.error("Failed to initialize environment. Fix this first:")
        st.exception(e)
        st.stop()

    actions = available_actions()
    left, right = st.columns([2.2, 1])

    with left:
        if st.button("Start / Reset Incident"):
            start_new(env)

        st.markdown(f"**Step:** {st.session_state['step']}")

        st.subheader("Analyst View")
        if st.session_state["state_text"] is None:
            st.info("Click Start / Reset Incident to begin.")
        else:
            st.write(st.session_state["state_text"])

        st.subheader("Timeline")
        if not st.session_state["log"]:
            st.write("No events yet.")
        else:
            for role, msg in st.session_state["log"]:
                if role == "ACTION":
                    st.markdown(f"**Action:** `{msg}`")
                elif role == "SCENARIO":
                    st.markdown("**Scenario start:**")
                    st.write(msg)
                else:
                    st.markdown("**Environment:**")
                    st.write(msg)

    with right:
        st.subheader("Actions")

        if st.session_state["state_text"] is None:
            st.write("Start an incident first.")
        elif st.session_state["done"]:
            st.success("Incident ended.")
            if st.button("Start New Incident"):
                start_new(env)
        else:
            for act in actions:
                if st.button(act):
                    do_action(env, act)
                    st.rerun()

        # Scoring + PDF export (shows when incident ends)
        if st.session_state.get("done"):
            actions_taken = [x[1] for x in st.session_state["log"] if x[0] == "ACTION"]
            reward_log = st.session_state.get("reward_log", [])
            total_steps = st.session_state.get("step", 0)

            score, level, feedback = compute_human_score(
              actions_taken,
              reward_log,
              total_steps,
              True
            )


            st.markdown("---")
            st.subheader("Session Result")
            st.success(f"Final Score: {score}/100 — {level}")

            scenario_text = st.session_state["log"][0][1] if st.session_state["log"] else "N/A"
            timeline = build_timeline_for_report(st.session_state["log"])

            pdf_bytes = build_pdf_bytes(
                scenario_text=scenario_text,
                timeline=timeline,
                score=score,
                level=level,
                feedback=feedback,
            )

            st.download_button(
                label="Download Training Report (PDF)",
                data=pdf_bytes,
                file_name="incident_report.pdf",
                mime="application/pdf",
            )


if __name__ == "__main__":
    main()
