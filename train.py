from llm_client import OpenRouterLLMClient
from env_incident import IncidentEnv, available_actions
from agent import QLearningAgent, encode_state


def run_episode(env: IncidentEnv, agent: QLearningAgent, max_steps: int = 12, verbose: bool = False):
    state_text = env.reset()
    state_id = encode_state(state_text)
    total_reward = 0.0
    done = False

    if verbose:
        print("Initial analyst view:")
        print(state_text)
        print("=" * 80)

    for step in range(max_steps):
        action = agent.choose_action(state_id)
        next_state_text, reward, done = env.step(action)
        next_state_id = encode_state(next_state_text)

        agent.update(state_id, action, reward, next_state_id)
        state_id = next_state_id
        total_reward += reward

        if verbose:
            print(f"Step {step + 1} | action: {action}")
            print(next_state_text)
            print(f"Reward: {reward:.2f}, Done: {done}")
            print("-" * 80)

        if done:
            break

    return total_reward, done


def main():
    llm_client = OpenRouterLLMClient()
    env = IncidentEnv(llm_client)
    actions = available_actions()
    agent = QLearningAgent(actions, alpha=0.15, gamma=0.95, epsilon=0.3)

    episodes = 30
    for ep in range(1, episodes + 1):
        total_reward, done = run_episode(env, agent, verbose=False)
        if ep % 5 == 0:
            status = "success" if done and total_reward > 0 else "fail"
            print(f"Episode {ep}: total_reward={total_reward:.2f}, status={status}")

    agent.epsilon = 0.0
    print("\nGreedy policy evaluation:\n")
    total_reward, done = run_episode(env, agent, verbose=True)
    print(f"Eval total reward: {total_reward:.2f}, success={done and total_reward > 0}")


if __name__ == "__main__":
    main()
