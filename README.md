<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=rect&color=0:0f2027,100:203a43&height=160&section=header&text=SOC%20Incident%20Response%20Trainer&fontSize=40&fontColor=00f2ff&animation=fadeIn" />
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/vasanth-boyez/soc-incident-trainer?color=00f2ff&style=for-the-badge">
  <img src="https://img.shields.io/github/forks/vasanth-boyez/soc-incident-trainer?color=00f2ff&style=for-the-badge">
  <img src="https://img.shields.io/badge/AI-CyberSecurity-00f2ff?style=for-the-badge">
  <img src="https://img.shields.io/badge/Streamlit-App-ff4b4b?style=for-the-badge">
</p>

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,github" height="45">
</p>

---

## 🧠 What is this?

A cyber incident response training simulator that blends **Reinforcement Learning (Q-learning)** with **LLM-based SOC narration**.  
It helps students and junior analysts practise incident response decisions in a realistic, safe, and interactive way.

---

## ⚡ Core Capabilities

| Feature | Description |
|--------|------------|
🧠 RL Agent | Tabular Q-learning agent that learns response strategies |
🗣 LLM Narration | SOC-style alert narration using OpenRouter |
📊 Readiness Scoring | Converts performance into skill levels |
📄 Auto PDF Reports | Generates downloadable training reports |
🎮 Streamlit UI | Human-in-the-loop simulator interface |

---

## 🏗 Architecture (High Level)

```

LLM (Narrator)
│
▼
Streamlit UI
│
▼
Incident Simulation Engine (Ground Truth)
│
├── Reward + Termination Logic
▼
RL Agent (Q-learning) ──▶ Scoring ──▶ PDF Reports

```

---

## 📁 Folder Structure

```

soc_incident_trainer/
│
├── .env                 # API keys & environment variables (NOT committed)
├── requirements.txt     # Dependencies for reproducible setup
├── llm_client.py        # OpenRouter LLM client (narration only)
├── incidents.py         # Incident templates/scenario library
├── env_incident.py      # Deterministic incident environment + rewards
├── agent.py             # Q-learning agent implementation
├── train.py             # Automated RL training loop
├── app.py               # Streamlit UI (human training mode)
├── report.py            # PDF report generation
├── scoring.py           # Human-friendly scoring & readiness levels
└── assets/              # (Optional) screenshots for README preview

````

---

## 🖼 Live Simulator Preview

> Add 2–3 screenshots inside `/assets/` and they will render here.

<p align="center">
  <img src="assets/ui1.png" width="32%">
  <img src="assets/ui2.png" width="32%">
  <img src="assets/ui3.png" width="32%">
</p>

---

## 🚀 Quick Start

### 1) Clone and install

```bash
git clone https://github.com/vasanth-boyez/soc-incident-trainer.git
cd soc-incident-trainer
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
````

### 2) Add `.env`

Create a file called `.env` in the project root:

```
OPENROUTER_API_KEY=your_key_here
```

### 3) Run the simulator

```bash
streamlit run app.py
```

Open:

```
http://localhost:8501
```

---

## 🤖 Train the RL Agent (Optional)

```bash
python train.py
```

---

## 🎓 Who is this for?

* Students learning SOC incident response workflows
* Cybersecurity training labs and university coursework
* Blue-team practise for structured response sequencing
* AI research experiments on decision-making under uncertainty

---

## 👨‍🚀 Author

**Vasanth Boyez**


---

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=rect&color=0:203a43,100:0f2027&height=120&section=footer&text=STAR%20THE%20REPO&fontColor=00f2ff&fontSize=28&animation=fadeIn" />
</p>

