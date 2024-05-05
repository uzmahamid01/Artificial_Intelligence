# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    start_node = problem.getStartState()
    explored_nodes = []
    OPEN = util.Stack()
    OPEN.push((start_node, []))

    while not OPEN.isEmpty():
        # tuple with current node and list of actions taken to get there
        curr_node, actions_taken = OPEN.pop() 

        if problem.isGoalState(curr_node):
            return actions_taken

        if curr_node not in explored_nodes:
            explored_nodes.append(curr_node)
            
            next_nodes = problem.getSuccessors(curr_node)

            for next_node, action, cost in next_nodes:
                new_actions = actions_taken + [action]
                OPEN.push((next_node, new_actions))

    return []




def breadthFirstSearch(problem: SearchProblem):

    """Search the shallowest nodes in the search tree first."""

    "*** YOUR CODE HERE ***"
    start_node = problem.getStartState()
    explored_nodes = []
    OPEN = util.Queue()
    OPEN.push( (start_node, []) )

    while not OPEN.isEmpty():
        # tuple with current node and list of actions taken to get there
        curr_node, actions_taken = OPEN.pop()   
        

        if problem.isGoalState(curr_node):
            return actions_taken                       
             
        if curr_node not in explored_nodes:         
            explored_nodes.append(curr_node)
            next_nodes = problem.getSuccessors(curr_node)
            for next_node, action, cost in next_nodes:
                new_actions = actions_taken + [action]
                OPEN.push((next_node, new_actions))

    return []                              
    #util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    start_node = problem.getStartState()
    explored_nodes = []
    OPEN = util.PriorityQueue()
    OPEN.push((start_node, [], 0), 0)  #cost of initial state
    
    while not OPEN.isEmpty():
        curr_node, actions_taken, cost = OPEN.pop()
    
        if problem.isGoalState(curr_node):
            return actions_taken
            
        if curr_node not in explored_nodes:     
            explored_nodes.append(curr_node)
            next_nodes = problem.getSuccessors(curr_node)
            if len(next_nodes) == 0:
                continue
            for next_node, action, step_cost in next_nodes:
                if next_node not in explored_nodes:
                    new_cost = cost + step_cost
                    OPEN.push((next_node, actions_taken + [action], new_cost), new_cost)

    return []
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start_node = problem.getStartState()
    OPEN = util.PriorityQueue()
    explored_nodes = []

    h = heuristic(start_node, problem)
    OPEN.push((start_node, []), h)

    while not OPEN.isEmpty():
        curr_node, actions_taken = OPEN.pop()

        if problem.isGoalState(curr_node):
            return actions_taken

        if curr_node not in explored_nodes:
            explored_nodes.append(curr_node)
            next_nodes = problem.getSuccessors(curr_node)
            for next_node, action, step_cost in next_nodes:
                h = heuristic(next_node, problem)
                new_cost = problem.getCostOfActions(actions_taken + [action]) + h
                OPEN.push((next_node, actions_taken + [action]), new_cost)

    return []
    #             d = util.manhattanDistance(next_node, problem.isGoalState(curr_node))
    #             new_cost = step_cost + heuristic(next_node, problem)
    #             OPEN.push((next_node, actions_taken + [action]), d + new_cost)

    # return []
    #util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
