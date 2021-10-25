import random
import itertools
import json

class MarkovChain():
    def __init__(self, order, decay=1.0):
        self.decay = decay
        self.matrix = self.create_matrix(order)

    @staticmethod
    def create_matrix(order):
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
        # matrix = {'RR': {'R': {'prob': 1/3, 'n_obs': 0}, 'P': {'prob': 1/3, 'n_obs': 0}, 'S': {'prob': 1/3, 'n_obs': 0}}, 'RP': {'R': {'prob': 1/3, 'n_obs': 0}, 'P': {'prob': 1/3, 'n_obs': 0}, 'S': {'prob': 1/3, 'n_obs': 0}}, 'RS': {'R': {'prob': 1/3, 'n_obs': 0}, 'P': {'prob': 1/3, 'n_obs': 0}, 'S': {'prob': 1/3, 'n_obs': 0}}, 'PR': {'R': {'prob': 1/3, 'n_obs': 0}, 'P': {'prob': 1/3, 'n_obs': 0}, 'S': {'prob': 1/3, 'n_obs': 0}}, 'PP': {'R': {'prob': 1/3, 'n_obs': 0}, 'P': {'prob': 1/3, 'n_obs': 0}, 'S': {'prob': 1/3, 'n_obs': 0}}, 'PS': {'R': {'prob': 1/3, 'n_obs': 0}, 'P': {'prob': 1/3, 'n_obs': 0}, 'S': {'prob': 1/3, 'n_obs': 0}}, 'SR': {'R': {'prob': 1/3, 'n_obs': 0}, 'P': {'prob': 1/3, 'n_obs': 0}, 'S': {'prob': 1/3, 'n_obs': 0}}, 'SP': {'R': {'prob': 1/3, 'n_obs': 0}, 'P': {'prob': 1/3, 'n_obs': 0}, 'S': {'prob': 1/3, 'n_obs': 0}}, 'SS': {'R': {'prob': 1/3, 'n_obs': 0}, 'P': {'prob': 1/3, 'n_obs': 0}, 'S': {'prob': 1/3, 'n_obs': 0}}}
        return matrix

    def update_matrix(self, pair, input):
        
        for i in self.matrix[pair]:
            self.matrix[pair][i]['n_obs'] = self.decay * self.matrix[pair][i]['n_obs']

        self.matrix[pair][input]['n_obs'] = self.matrix[pair][input]['n_obs'] + 1
        
        n_total = 0
        for i in self.matrix[pair]:
            n_total += self.matrix[pair][i]['n_obs']
            
        for i in self.matrix[pair]:
            self.matrix[pair][i]['prob'] = self.matrix[pair][i]['n_obs'] / n_total            

    def predict(self, pair):

        probs = self.matrix[pair]
        # if max(probs.values()) == min(probs.values()):
        if probs['R']['prob'] == probs['P']['prob'] == probs['S']['prob']:
            return random.choice(['R', 'P', 'S'])
        else:
            # print(probs['R']['prob'])
            decision = 'R'
            prob = probs['R']['prob']
            for i in {'P', 'S'}:
                if probs[i]['prob'] > prob:
                    prob = probs[i]['prob']
                    decision = i
            beat = {'R':'P', 'P':'S', 'S':'R'}
            return beat[decision]
    
markov_model = MarkovChain(1, 0.9)

def print_matrix(matrix):
    print('   |          R         |          P         |          S         |')
    print('--------------------------------------------------------------------')
    for i in matrix:
        print(i, '|', matrix[i]['R']['prob'], '|', matrix[i]['P']['prob'], '|', matrix[i]['S']['prob'], '|')
        print('--------------------------------------------------------------------')

def main():
    agentScore = 0
    playerScore = 0

    state = 'RR'

    while(True):
        # player's decision
        pred = markov_model.predict(state)

        pd = input("Enter your play: ")
        pd = pd.upper()
        if pd not in {'R', 'S', 'P'}:
            print("invalid input")
            continue

        markov_model.update_matrix(state, pd)

        print("Computer play: ", pred)
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
        state = pd+pred
        print_matrix(markov_model.matrix)
        # for i in {'RR','RS','RP','PR','PS','PP','SS','SR','SP'}:
        #     print(i, markov_model.matrix[i])
        # print(json.dumps(markov_model.matrix, sort_keys=True, indent=4))
        
if __name__ == "__main__":
    main()