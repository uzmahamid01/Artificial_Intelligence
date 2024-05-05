# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        
        for _ in range(self.iterations):
            updated_values = util.Counter()
            for state in self.mdp.getStates():
                if not self.mdp.isTerminal(state):
                    qValues = []
                    for action in self.mdp.getPossibleActions(state):
                        qValue = self.computeQValueFromValues(state, action)
                        qValues.append(qValue)
                    maxQvalue = max(qValues)
                    updated_values[state] = maxQvalue
            self.values = updated_values.copy()


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        qValue = 0.0
        transition_probs =   self.mdp.getTransitionStatesAndProbs(state, action)
        for nextState, p in transition_probs:
            #using the Q(s,a)=∑s′T(s,a,s′)[R(s,a,s′)+γmaxa′Q(s′,a′)]
            qValue += p * (self.mdp.getReward(state, action, nextState)+self.discount* self.getValue(nextState))
        return qValue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        allActions=self.mdp.getPossibleActions(state)
        optimal_action = None      
        max_reward = float("-inf")
        for act in allActions:
            reward = self.computeQValueFromValues(state,act)
            if reward > max_reward:
                max_reward = reward
                optimal_action = act
        return optimal_action

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class PrioritizedSweepingValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        """YOUR  CODE HERE"""
        states = self.mdp.getStates()
        #actions = self.mdp.getActions()
        fringe  = util.PriorityQueue()
        predecessors = {}

        def maxQval(state):
            return  max([self.getQValue(state, act) for act in self.mdp.getPossibleActions(state)])
        # Add all states to the fringe with high priority
        for s in states:
            self.values[s] = 0
            predecessors[s] = set()
            moves = ['north', 'south', 'east', 'west']
            if not self.mdp.isTerminal(s):
                for p in states:
                    terminal = self.mdp.isTerminal(p)    
                    legal_act = self.mdp.getPossibleActions(p)

                    if not terminal:
                        for move in moves:
                            if move in legal_act:
                                transition_state = self.mdp.getTransitionStatesAndProbs(p, move)
                                for x, t in transition_state:
                                    if (x == s) and (t > 0):
                                        predecessors[s].add(p)
                                        #break
            terminal = self.mdp.isTerminal(s)
            if not terminal:
                currState = self.values[s]
                diff = abs(currState - maxQval(s))
                fringe.push(s, -diff)

        for _ in range(self.iterations):
            if fringe.isEmpty():
                return
            s = fringe.pop()
            self.values[s] = maxQval(s)

            for p in predecessors[s]:
                diff = abs(self.values[p] - maxQval(p))
                if diff > self.theta:
                    fringe.update(p, -diff)

        