import numpy as np
from Game import Game

game = Game(4, 4, wrong_action_p=0.1, alea=False, wind=True)

n_states = 16
n_actions = 4

Q = np.zeros((n_states, n_actions))

# plus alpha est grand plus on favorise l'exploration
alpha = 0.85
gamma = 0.99

nb_episods = 1000

list_actions = []
list_states = []
cumul_reward = []
game.print()
for step in range(nb_episods):
    s = game.reset()
    e = False
    mem_actions = []
    mem_states = []
    mem_rewards = []

    while not e:
        # Génération d'un tableau de variables aléatoires
        l = np.random.randn(1, n_actions)
        # On choisit une des actions au hasard
        a = np.argmax(Q[s, :] + l)

        s1, r, e, _ = game.move(a)
        mem_rewards.append(r)
        Q[s, a] = Q[s, a] + alpha * (r + gamma * np.max(Q[s1, :]) - Q[s, a])
        mem_actions.append(a)
        s = s1
        mem_states.append(s)
        #Q[(state, action)] = (1 - alpha) * Q + alpha * (reward + gamma * maxNext)

    list_actions.append(mem_actions)
    list_states.append(mem_states)
    cumul_reward.append(np.sum(mem_rewards))

print(f'Mean score over time: {np.mean(cumul_reward)}')
print(f'Sum score over time: {np.sum(cumul_reward)}')
for action in mem_actions:
    print(game.ACTIONS_NAMES[action])

game.print()
def get_legal_actions():
    line, col = game.position
    actions = []
    if line < 3:
        actions.append((line + 1, col))
    if line > 0:
        actions.append((line - 1, col))
    if col < 3:
        actions.append((line, col + 1))
    if col > 0:
        actions.append((line, col - 1))

    return actions