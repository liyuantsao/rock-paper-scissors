import random
import itertools

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


def main(level):
    agent = MarkovChain(0.9, level)
    total_ratio = []
    for i in range(5):
        agent.reset()
        agentScore = 0
        playerScore = 0
        cnt = 0
        # pred = random.choice(['R', 'P', 'S'])
        while(cnt < 10000):
            # player's decision
            pred = agent.predict()
            # pd = input("Enter your play: ")
            
            # pd = pred
            # if cnt % 3 == 0:
            #     pd = 'R'
            # elif cnt % 3 == 1:
            #     pd = 'P'
            # else:
            #     pd = 'S'

            # if cnt % 4 == 0:
            #     pd = 'R'
            # elif cnt % 4 == 1:
            #     pd = 'R'
            # elif cnt % 4 == 2:
            #     pd = 'P'
            # else:
            #     pd = 'P'

            # if cnt % 6 == 0:
            #     pd = 'R'
            # elif cnt % 6 == 1:
            #     pd = 'R'
            # elif cnt % 6 == 2:
            #     pd = 'P'
            # elif cnt % 6 == 3:
            #     pd = 'P'
            # elif cnt % 6 == 4:
            #     pd = 'S'
            # else:
            #     pd = 'S'
            # pd = random.choice(['R', 'P', 'S'])

            if cnt % 10 < 5:
                pd = 'R'
            else:
                pd = 'P'

            pd = pd.upper()

            if pd not in {'R', 'S', 'P'}:
                print("invalid input")
                continue

            agent.update(pd)

            # state = pd + pred

            # if cnt > 9980:
            #     print('user_play: ', pd)
            # print("Computer play: ", pred)

            #player+agent
            playerwin = {'RS', 'SP', 'PR'}
            if pd == pred:
                # print("Draw")
                pass
            elif pd+pred in playerwin:
                playerScore += 1
                # print("You win")
            else:
                agentScore += 1
                # print("You loss")

            # print("Computer Score: ", agentScore, " Player Score: ", playerScore)
            cnt = cnt + 1

        ratio = agentScore / (agentScore + playerScore)
        total_ratio.append(ratio)

    print('Level: {}, Average win ratio: {}'.format(level, sum(total_ratio) / len(total_ratio)))
    # print(agent.state, agent.last_state, agent.last_pred)
    # print(agent.matrix)
   


if __name__ == "__main__":
    for i in range(1,7):
        main(i)