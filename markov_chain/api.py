import random
import itertools

'''
class MarkovChain():
    def __init__(self, decay=1.0):
        self.decay = decay
        self.reset()
        self.last_state = 'RR'
        self.last_pred = ''

    def _create_matrix(self, order=1):
        def create_keys(order):            
            keys = ['R', 'P', 'S']
            for i in range((order * 2 - 1)):
                key_len = len(keys)
                for i in itertools.product(keys, ''.join(keys)):
                    keys.append(''.join(i))
                keys = keys[key_len:]
            return keys

        keys = create_keys(order)
        matrix = {}
        for key in keys:
            matrix[key] = {
                'R': {
                    'prob' : 1 / 3,
                    'n_obs' : 0
                },
                'P': {
                    'prob' : 1 / 3,
                    'n_obs' : 0
                },
                'S': {
                    'prob' : 1 / 3,
                    'n_obs' : 0
                }
            }
        return matrix

    def _update_matrix(self, pair, input):
        for i in self.matrix[pair]:
            self.matrix[pair][i]['n_obs'] = self.decay * self.matrix[pair][i]['n_obs']

        self.matrix[pair][input]['n_obs'] = self.matrix[pair][input]['n_obs'] + 1
        
        n_total = 0
        for i in self.matrix[pair]:
            n_total += self.matrix[pair][i]['n_obs']
            
        for i in self.matrix[pair]:
            self.matrix[pair][i]['prob'] = self.matrix[pair][i]['n_obs'] / n_total            

    def reset(self):
        self.matrix = self._create_matrix()

    def predict(self):
        pair = self.last_state
        probs = self.matrix[pair]
        

        if probs['R']['prob'] == probs['P']['prob'] == probs['S']['prob']:
            pred = random.choice(['R', 'P', 'S'])
        else:
            decision = 'R'
            prob = probs['R']['prob']
            for i in {'P', 'S'}:
                if probs[i]['prob'] > prob:
                    prob = probs[i]['prob']
                    decision = i
            beat = {'R':'P', 'P':'S', 'S':'R'}
            pred = beat[decision]
        self.last_pred = pred

        return {'R':'rock', 'P':'paper', 'S':'scissors'}[pred]
    
    def update(self, player_rps):
        player_rps = {'rock':'R', 'paper':'P', 'scissors':'S'}[player_rps]
        self.last_state = player_rps + self.last_pred
        self._update_matrix(self.last_state, player_rps)
'''

class MarkovChain():
    def __init__(self, decay, state):
        self.decay = decay
        self.state = state
        self.reset()
        self.last_state = ''
        self.last_pred = ''

    def _create_matrix(self, order=1):
        def rec(s, depth, max_depth):
            if depth > max_depth:
                matrix[s] = {
                    'R': {'prob': 1/3, 'n_obs': 0},
                    'P': {'prob': 1/3, 'n_obs': 0},
                    'S': {'prob': 1/3, 'n_obs': 0}
                }
                return
            rec(s+'R', depth+1, max_depth)
            rec(s+'P', depth+1, max_depth)
            rec(s+'S', depth+1, max_depth)
        matrix = {}
        rec('', 0, self.state*2-1)
        return matrix

    def _update_matrix(self, pair, user_input):
        for i in self.matrix[pair]:
            self.matrix[pair][i]['n_obs'] = self.decay * self.matrix[pair][i]['n_obs']

        self.matrix[pair][user_input]['n_obs'] += 1
        
        n_total = 0
        for i in self.matrix[pair]:
            n_total += self.matrix[pair][i]['n_obs']
            
        for i in self.matrix[pair]:
            self.matrix[pair][i]['prob'] = self.matrix[pair][i]['n_obs'] / n_total            

    def reset(self):
        self.matrix = self._create_matrix()

    def predict(self):
        if len(self.last_state) < self.state*2:
            pred = random.choice(['R', 'P', 'S'])
        else:
            probs = self.matrix[self.last_state]
            if probs['R']['prob'] == probs['P']['prob'] == probs['S']['prob']:
                pred = random.choice(['R', 'P', 'S'])
            else:
                probs = self.matrix[self.last_state]
                decision = ''
                prob = 0
                for i in {'R', 'P', 'S'}:
                    if probs[i]['prob'] > prob:
                        prob = probs[i]['prob']
                        decision = i
                beat = {'R':'P', 'P':'S', 'S':'R'}
                pred = beat[decision]

        self.last_pred = pred
        # return {'R':'rock', 'P':'paper', 'S':'scissors'}[pred]
        return pred
    
    def update(self, player_rps):
        # player_rps = {'rock':'R', 'paper':'P', 'scissors':'S'}[player_rps]
        if len(self.last_state) == self.state * 2:
            self._update_matrix(self.last_state, player_rps)

        self.last_state += (player_rps + self.last_pred)
        self.last_state = self.last_state[-self.state*2:]


agent = MarkovChain(0.9, 3)

def print_matrix(matrix):
    print('   |          R         |          P         |          S         |')
    print('--------------------------------------------------------------------')
    for i in matrix:
        print(i, '|', matrix[i]['R']['prob'], '|', matrix[i]['P']['prob'], '|', matrix[i]['S']['prob'], '|')
        print('--------------------------------------------------------------------')

def main():
    agentScore = 0
    playerScore = 0

    while(True):
        # player's decision
        pred = agent.predict()
        print("Computer play: ", pred)

        pd = input("Enter your play: ")
        pd = pd.upper()
        if pd not in {'R', 'S', 'P'}:
        # if pd not in {'rock', 'paper', 'scissors'}:
            print("invalid input")
            continue

        agent.update(pd)

        #player+agent
        playerwin = {'RS', 'SP', 'PR'}
        if pd == pred:
            print("Draw")
        elif pd+pred in playerwin:
            playerScore += 1
            print("You win")
        else:
            agentScore += 1
            print("You loss")

        print("Computer Score: ", agentScore, " Player Score: ", playerScore)
        # print_matrix(agent.matrix)
        
if __name__ == "__main__":
    main()