import random

def q_lookup(q_table, state, action):
    if (state,action) not in q_table:
        q_table[(state,action)] = 0
    return q_table[(state,action)]

def choose_e_greedy(state, actions, q_table, epsilon):
    if random.random() < epsilon:
        a = random.choice(actions)
    else:
        q_scores = {(state,action):q_lookup(q_table,state,action) for action in actions}
        max_q = max(q_scores.values())
        max_actions = [k for k,v in q_scores.items() if v == max_q]
        a = random.choice(max_actions)[1]
    return a

def iteration_continue(iterations, max_iterations):
    return True if max_iterations == 0 else (iterations < max_iterations)

# def sarsa_trial(s, actions, perform, is_terminal, iteration, q_table = {}, alpha=0.5, gamma=0.9, epsilon = 0.2):
def perform_trial(s, actions, perform, is_terminal, q_table = {}, alpha=0.1, gamma=1, epsilon = 0.2, max_iterations=0):
    # s = initial state
    # actions = list of actions valid from s
    # perform = function which takes an action as a parameter and returns:    reward, s_prime, valid actions from s_prime
    # is_terminal = function which takes a state and returns a boolean indicating whether the state is terminal
    # alpha = learning rate (0-1)   0: learn nothing, 1: recent only
    # gamma = discount factor (0-1) 0: current rewards only, 1: long-term reward
    # epsilon = action selection factor. If r~uniform[0,1) < epsilon, action is determined randomly

    a = choose_e_greedy(s, actions, q_table, epsilon)
    itt = 0
    while not is_terminal(s) and iteration_continue(itt,max_iterations):
        reward, s_prime, actions = perform(s, a)
        a_prime = choose_e_greedy(s_prime, actions, q_table, epsilon)
        q_table[(s,a)] = q_lookup(q_table, s, a) + alpha * (reward + (gamma * q_lookup(q_table, s_prime, a_prime)) - q_lookup(q_table, s,a))
#        print "{:24} {:15} {}".format(s,a,q_table[(s,a)])
        s = s_prime
        a = a_prime
        itt = itt + 1
    return q_table
