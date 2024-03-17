from Player import Player
from Game import Action
import numpy as np

class MyPlayer(Player):
    # 1. Add your UINs seperated by a ':'
    #    DO NOT USE A COMMA ','
    #    We use CSV files and commas will cause trouble
    # 2. Write your strategy under the play function
    # 3. Add your team's name (this will be visible to your classmates on the leader board)
    

    UIN = "332009674"
    def play(self, opponent_prev_action):
        # Strategy based on opponent's previous action and error rate for previous action report
        """If opponent confessed in the previous round, continue to confess to avoid exploitation
        If opponent remained silent in the previous round, consider whether to exploit or cooperate considering error rate
        Calculate the likelihood of opponent's silent action being reported with error
        Adjust decision based on error rate for previous action report
        If error rate is lower, confess
        If error rate is higher, remain silent
        If opponent's previous action is unknown, default to remaining silent.
        """
        if opponent_prev_action == Action.Confess:
            return Action.Confess
        elif opponent_prev_action == Action.Silent:        
            if self.error_rate < 0.2:
                return Action.Confess   
            else:
                return Action.Silent   
        else:
            return Action.Silent
  

    def __str__(self):
        return "Yeti"
