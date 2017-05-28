import random

def q_lookup(q_table, state, action):
    if (state,action) not in q_table:
        q_table[(state,action)] = float("-inf")
    return q_table[(state,action)]

def choose_e_greedy(state, actions, q_table, epsilon):
    if random.random() < epsilon:
        return random.choice(actions)
    else:
        q_scores = {(state,action):q_lookup(q_table,state,action) for action in actions}
        max_q = max(q_scores.values())
        max_actions = [k for k,v in q_scores.items() if v == max_q]
        return random.choice(max_actions)
 
def sarsa_trial(s, actions, perform, is_terminal, q_table = {}, alpha=0.5, gamma=0.9, epsilon = 0.2):
    # s = initial state
    # actions = list of actions valid from s
    # perform = function which takes an action as a parameter and returns:    reward, s_prime, valid actions from s_prime
    # is_terminal = function which takes a state and returns a boolean indicating whether the state is terminal
    # alpha = learning rate (0-1)   0: learn nothing, 1: recent only
    # gamma = discount factor (0-1) 0: current rewards only, 1: long-term reward
    # epsilon = action selection factor. If r~uniform[0,1) < epsilon, action is determined randomly
    
    a = choose_e_greedy(s, actions, q_table, epsilon)
    while not is_terminal(state):
        reward, s_prime, actions = perform(a)
        a_prime = choose_e_greedy(s_prime, actions, q_table, epsilon)
        q_table[(s,a)] = q_table[(s,a)] + alpha * (reward + (gamma * q_lookup(q_table, s_prime, a_prime)) - q_table[(s,a)])
        s = s_prime
        a = a_prime
    return q_table