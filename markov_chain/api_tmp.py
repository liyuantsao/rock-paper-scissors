import random
import itertools
import json

class MarkovChain():
    def __init__(self, order=1, decay=1.0):
        pass

    def reset(self):
        pass
    
    def update(self, player_decision):
        pass

    def predict(self):
        return random.choice(['R','P','S'])

    
agent = MarkovChain(1, 0.9)

# reset when change player
agent.reset()
while (1):
    # pd is player's decision
    pd = input("Enter your play: ")
    pd = pd.upper()
    if pd not in {'R', 'S', 'P'}:
        print("invalid input")
        continue

    # get agent's play using predict()
    play = agent.predict()
    print(play)
    # update the agent with what player play
    agent.update(pd)