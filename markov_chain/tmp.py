import random
import itertools

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

def main():
    total_ratio = []
    for i in range(5):
        agentScore = 0
        playerScore = 0
        state = 'RR'
        cnt = 0

        while(cnt < 10000):
            # player's decision
            pred = markov_model.predict(state)
            # pd = input("Enter your play: ")
            if cnt % 4 < 2:
                pd = 'R'
            else:
                pd = 'P'

            pd = pd.upper()
            # if pd == 'L':
            #     print(markov_model.matrix)
            if pd not in {'R', 'S', 'P'}:
                print("invalid input")
                continue

            if agentScore != 0 or playerScore != 0:
                markov_model.update_matrix(state, pd)

            state = pd + pred

            if cnt > 9980:
                print('user_play: ', pd)
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
            # print(markov_model.matrix)
            cnt = cnt + 1

        ratio = agentScore / (agentScore + playerScore)
        total_ratio.append(ratio)

    print(total_ratio)
    print('Average win ratio: {}'.format(sum(total_ratio) / len(total_ratio)))

if __name__ == "__main__":
    main()


# class RLModel:
#     def predict():
#         # return one of {'R', 'P', 'S'}
#         return pred

#     def update(player_decision): # enter what player play
#         pass

#     def reset(): # change player
#         pass