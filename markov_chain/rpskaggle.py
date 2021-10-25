import random

class MarkovChain():
    def __init__(self, order, decay=1.0):
        self.decay = decay
        self.matrix = self.create_matrix(order)
        self.state = 'RR'

    @staticmethod
    def create_matrix(order):
        matrix = {'RR': {'R': {'prob': 1/3, 'n_obs': 0}, 'P': {'prob': 1/3, 'n_obs': 0}, 'S': {'prob': 1/3, 'n_obs': 0}}, 'RP': {'R': {'prob': 1/3, 'n_obs': 0}, 'P': {'prob': 1/3, 'n_obs': 0}, 'S': {'prob': 1/3, 'n_obs': 0}}, 'RS': {'R': {'prob': 1/3, 'n_obs': 0}, 'P': {'prob': 1/3, 'n_obs': 0}, 'S': {'prob': 1/3, 'n_obs': 0}}, 'PR': {'R': {'prob': 1/3, 'n_obs': 0}, 'P': {'prob': 1/3, 'n_obs': 0}, 'S': {'prob': 1/3, 'n_obs': 0}}, 'PP': {'R': {'prob': 1/3, 'n_obs': 0}, 'P': {'prob': 1/3, 'n_obs': 0}, 'S': {'prob': 1/3, 'n_obs': 0}}, 'PS': {'R': {'prob': 1/3, 'n_obs': 0}, 'P': {'prob': 1/3, 'n_obs': 0}, 'S': {'prob': 1/3, 'n_obs': 0}}, 'SR': {'R': {'prob': 1/3, 'n_obs': 0}, 'P': {'prob': 1/3, 'n_obs': 0}, 'S': {'prob': 1/3, 'n_obs': 0}}, 'SP': {'R': {'prob': 1/3, 'n_obs': 0}, 'P': {'prob': 1/3, 'n_obs': 0}, 'S': {'prob': 1/3, 'n_obs': 0}}, 'SS': {'R': {'prob': 1/3, 'n_obs': 0}, 'P': {'prob': 1/3, 'n_obs': 0}, 'S': {'prob': 1/3, 'n_obs': 0}}}
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

NumbertoWord = {0:'R', 1:'P', 2:'S'}
WordtoNumber = {'R':0, 'P':1, 'S':2}

def copy_opponent(observation, configuration):
    if observation.step > 0:
        pd = NumbertoWord[observation.lastOpponentAction]
        markov_model.update_matrix(markov_model.state, pd)
        pred = markov_model.predict(markov_model.state)
        markov_model.state = pd+pred
        return WordtoNumber[pred]
    else:
        pred = random.randrange(0, configuration.signs)
        return pred