# myAgents.py
# ---------------
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

from game import Agent
from searchProblems import PositionSearchProblem

import util
import time
import search

"""
IMPORTANT
`agent` defines which agent you will use. By default, it is set to ClosestDotAgent,
but when you're ready to test your own agent, replace it with MyAgent
"""
def createAgents(num_pacmen, agent='MyAgent'):
    return [eval(agent)(index=i) for i in range(num_pacmen)]

class MyAgent(Agent):
    """
    Implementation of your agent.
    """

    def __init__(self, index):
        super().__init__(index)
        self.optimal_path = [None] * 10
        self.target_pos = [(-1, -1)] * 10

    def getAction(self, state):
        """
        Returns the next action the agent will take
        """

        "*** YOUR CODE HERE ***"
        startPosition = state.getPacmanPosition(self.index)
        food = state.getFood()
        problem = AnyFoodSearchProblem(state, self.index)

        pos_x, pos_y = self.target_pos[self.index]
        if not food[pos_x][pos_y] or (pos_x, pos_y) == (-1, -1) or len(self.optimal_path[self.index]) <= 1:
            target_pos_found = False
            for i in range(food.width):
                for j in range(food.height):
                    if food[i][j]:
                        path = search.aStarSearch(problem)
                        self.optimal_path[self.index] = path
                        self.target_pos[self.index] = (i, j)
                        if len(self.optimal_path[self.index]) > 1:
                            target_pos_found = True
                            break
                if target_pos_found:
                    break
        else:
            del self.optimal_path[self.index][0]

        # print("Pacman Position:", startPosition)
        # print("Target Position:", self.target_pos[self.index])
        # print("optimal_pathimal_pathimal Path:", self.optimal_path[self.index])

        return self.optimal_path[self.index][0]

    def initialize(self):
        """
        Intialize anything you want to here. This function is called
        when the agent is first created. If you don't need to use it, then
        leave it blank
        """
        pass

    
class ClosestDotAgent(Agent):

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition(self.index)
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState, self.index)


        "*** YOUR CODE HERE ***"
        if len(self.optimal_path[self.index]) <= 1:
            cost = float('inf')
            for i in range(food.width):
                for j in range(food.height):
                    if food[i][j]:
                        path = search.aStarSearch(problem)
                        if len(path) < cost:
                            self.optimal_path[self.index] = path
                            cost = len(path)
            return self.optimal_path[self.index]
        else:
            return self.optimal_path[self.index]

    def getAction(self, state):
        return self.findPathToClosestDot(state)[0]
    

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState, agentIndex):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state
        return self.food[x][y]

