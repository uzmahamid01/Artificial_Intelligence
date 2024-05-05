# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


        #consider both food locations and ghost locations
        #How does your agent fare? It will likely often die with 2 ghosts on the default board, unless your evaluation function is quite good.
        #Remember that newFood has the function asList()
        foods = newFood.asList()
        #If then statement - for if you see the  item at location x it is in newFood.aslist()[x]
        #print(newGhostStates)

        dist_to_ghost, dist_to_food  = float("inf"), float("inf")

        ghost_positions = [(int(ghost_state.getPosition()[0]), int(ghost_state.getPosition()[1])) for ghost_state in newGhostStates if ghost_state.scaredTimer == 0]

        for ghost_pos in ghost_positions:
            dist_to_ghost = min(dist_to_food, manhattanDistance(ghost_pos, newPos))

        if not foods:
            dist_to_food = 0
        else:
            food_positions = [(int(food[0]), int(food[1])) for food in foods]
            for food in foods:
                dist_to_food = min(dist_to_food, manhattanDistance(food, newPos))
        
        score = successorGameState.getScore() - 7 / (dist_to_ghost + 1) - dist_to_food / 3
        return score

        "*** YOUR CODE HERE ***"
        #return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    # if currentGameState.isWin() or currentGameState.isLose():
    #     return currentGameState.getScore()
    # else:
    #     return 0
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    def getAction(self, gameState: GameState):   
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(index):
        Returns a list of legal actions for an agent
        index=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(index, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
#         "*** YOUR CODE HERE ***"
#         #for any number of ghosts
#         #your minimax tree will have multiple min layers (one for each ghost) for every max layer
#         #Your code should also expand the game tree to an arbitrary depth
#         #core the leaves of your minimax tree with the supplied self.evaluationFunction, which defaults to scoreEvaluationFunction 
#         #MinimaxAgent extends MultiAgentSearchAgent, which gives access to self.depth and self.evaluationFunction
#         #Make sure your minimax code makes reference to these two variables where appropriate as these variables are populated in response to command line options.
#         #if current state is terminal state that is win or lose return score of the state
    
        def minimax(state, depth, index):
            if depth == 0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state), Directions.STOP

            legalActions = state.getLegalActions(index)
            if not legalActions:  
                return self.evaluationFunction(state), Directions.STOP

            # Pacman (maximizing player)
            if index == 0:  
                maxScore = float('-inf')
                bestAction = Directions.STOP
                for action in legalActions:
                    successorState = state.generateSuccessor(index, action)
                    score, _ = minimax(successorState, depth, (index + 1) % state.getNumAgents())
                    if score > maxScore:
                        maxScore = score
                        bestAction = action
                return maxScore, bestAction
            # Ghosts (minimizing player)
            else:  
                minScore = float('inf')
                bestAction = Directions.STOP
                for action in legalActions:
                    successorState = state.generateSuccessor(index, action)
                    if index == state.getNumAgents() - 1:
                        score, _ = minimax(successorState, depth - 1, 0)
                    else:
                        score, _ = minimax(successorState, depth, index + 1)
                    if score < minScore:
                        minScore = score
                        bestAction = action
                return minScore, bestAction

        
        _, bestAction = minimax(gameState, self.depth, 0)
        return bestAction

    
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def alpha_beta_search(state, depth, index, alpha, beta):
            if depth == 0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state), Directions.STOP

            legalActions = state.getLegalActions(index)
            if not legalActions: 
                return self.evaluationFunction(state), Directions.STOP
            

            # Pacman (maximizing player)
            if index == 0:  
                maxScore = float('-inf')
                bestAction = Directions.STOP
                for action in legalActions:
                    successorState = state.generateSuccessor(index, action)
                    score, _ = alpha_beta_search(successorState, depth, (index + 1) % state.getNumAgents(), alpha, beta)
                    if score > maxScore:
                        maxScore = score
                        bestAction = action
                    alpha = max(alpha, maxScore)
                    if maxScore > beta:
                        break  
                return maxScore, bestAction
            # Ghosts (minimizing player)
            else: 
                minScore = float('inf')
                bestAction = Directions.STOP
                for action in legalActions:
                    successorState = state.generateSuccessor(index, action)
                    if index == state.getNumAgents() - 1:
                        score, _ = alpha_beta_search(successorState, depth - 1, 0, alpha, beta)
                    else:
                        score, _ = alpha_beta_search(successorState, depth, index + 1, alpha, beta)
                    if score < minScore:
                        minScore = score
                        bestAction = action
                    beta = min(beta, minScore)
                    if minScore < alpha:
                        break  
                return minScore, bestAction


        _, bestAction = alpha_beta_search(gameState, self.depth, 0, float('-inf'), float('inf'))
        return bestAction
    
        #util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectimax(state, depth, index):
            if depth == 0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state), Directions.STOP

            legalActions = state.getLegalActions(index)
            if not legalActions: 
                return self.evaluationFunction(state), Directions.STOP

            # Pacman
            if index == 0:  
                maxScore = float('-inf')
                bestAction = Directions.STOP
                for action in legalActions:
                    successorState = state.generateSuccessor(index, action)
                    score, _ = expectimax(successorState, depth, (index + 1) % state.getNumAgents())
                    if score > maxScore:
                        maxScore = score
                        bestAction = action
                return maxScore, bestAction
            #Ghost
            else:  
                totalScore = 0
                for action in legalActions:
                    successorState = state.generateSuccessor(index, action)
                    if index == state.getNumAgents() - 1:
                        score, _ = expectimax(successorState, depth - 1, 0)
                    else:
                        score, _ = expectimax(successorState, depth, index + 1)
                    totalScore += score
                avgScore = totalScore / len(legalActions)
                return avgScore, Directions.STOP

        
        _, bestAction = expectimax(gameState, self.depth, 0)
        return bestAction
    
        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    foods = newFood.asList()

    dist_to_ghost, dist_to_food  = float("inf"), float("inf")

    ghost_positions = [(int(ghost_state.getPosition()[0]), int(ghost_state.getPosition()[1])) for ghost_state in newGhostStates if ghost_state.scaredTimer == 0]
    
    for ghost_pos in ghost_positions:
        dist_to_ghost = min(dist_to_ghost, manhattanDistance(ghost_pos, newPos))
    else:
        
        dist_to_ghost = -10

    if not foods:
        dist_to_food = 0
    else:
        food_positions = [(int(food[0]), int(food[1])) for food in foods]
        for food in foods:
            dist_to_food = min(dist_to_food, manhattanDistance(food, newPos))

    score = currentGameState.getScore() - 7 / (dist_to_ghost + 1) - dist_to_food / 3
    return score
    

# Abbreviation
better = betterEvaluationFunction
