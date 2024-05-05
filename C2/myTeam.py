# myTeam.py
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

from captureAgents import CaptureAgent
import random, util
from game import Directions
from util import nearestPoint
import time

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first='OffensiveReflexAgent', second='DefensiveReflexAgent'):

  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class DummyAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).

    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """
    self.start = gameState.getAgentPosition(self.index)

    '''
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py.
    '''
    CaptureAgent.registerInitialState(self, gameState)

    '''
    Your initialization code goes here, if you need any.
    '''
    self.boundary_top = True
    if gameState.getAgentState(self.index).getPosition()[0] == 1:
        self.isRed = True
    else:
        self.isRed = False

    #calculating the boundary positions based on the team color and the dimensions of the game board.
    walls = gameState.getWalls()
    height = walls.height
    width = walls.width
    if self.isRed:
        self.boundaries = ((1, height), (width, height))
    else:
        self.boundaries = ((1, 1), (width, 1))

    self.treeDepth = 3

  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """
    actions = gameState.getLegalActions(self.index)

    '''
    You should change this in your own agent.
    '''
    start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    evaluation_time = time.time() - start
    
    #evaluation time for debugging
    if evaluation_time > 0.9:
        print('Evaluation time for agent %d: %.4f' % (self.index, evaluation_time))
    
    #maximum evaluated value
    max_value = max(values)
    
    #actions with the maximum evaluated value
    best_actions = [action for action, value in zip(actions, values) if value == max_value]
    
    return random.choice(best_actions)

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid placement (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
        return successor.generateSuccessor(self.index, action)    # Only half a grid placement was covered
    else:
        return successor

  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights

  # def getFeatures(self, gameState, action):
  #   """
  #   Returns a counter of features for the state
  #   """
  #   features = util.Counter()
  #   successor = self.getSuccessor(gameState, action)
  #   features['successorScore'] = self.getScore(successor)
  #   return features
  def getFeatures(self, gameState, action):
    """
    Returns a counter of features for the state
    """
    features = util.Counter()  #feature counter
    successor = self.getSuccessor(gameState, action)
    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    #calculating various features and update the features counter 
    self.ScoreFeatures(features, myState, successor)
    self.CapsuleFeatures(features, myPos, successor)
    self.FoodFeatures(features, myPos, successor)
    self.ActionFeatures(features, action, gameState)
    self.GhostAndInvaderFeatures(features, myPos, myState, successor)

    return features

  def ScoreFeatures(self, features, myState, successor):
      features['successorScore'] = myState.numCarrying + self.getScore(successor)

  def CapsuleFeatures(self, features, myPos, successor):
      #distance to nearest capsule and update features
      capsule_distances = [self.getMazeDistance(myPos, capsule) for capsule in self.getCapsules(successor)]
      if capsule_distances:
          features['distanceToCapsule'] = min(capsule_distances)
      elif myPos in self.getCapsules(self.getCurrentObservation()):
          features['distanceToCapsule'] = -100000   #if I am carrying a capsule, then you get penalty so move away

  def FoodFeatures(self, features, myPos, successor):
      #distance to nearest food
      foodList = self.getFood(successor).asList()
      if foodList:
          features['distanceToFood'] = min([self.getMazeDistance(myPos, food) for food in foodList])

  def ActionFeatures(self, features, action, gameState):
      if action == Directions.STOP:
          features['stop'] = 1   #don't stop

        #checking if the action is a reverse direction
      back = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
      if action == back:
          features['backDir'] = 1    # penalization for going back

  def GhostAndInvaderFeatures(self, features, myPos, myState, successor):
      for enemy in self.getOpponents(successor):
          enemy_state = successor.getAgentState(enemy)
          enemy_pos = enemy_state.getPosition()
          if enemy_pos is None:
              continue
          distance = self.getMazeDistance(myPos, enemy_pos)
          if enemy_state.isPacman:
              if myState.scaredTimer <= 0:
                  features['crossingOpponent'] = distance    #chase opponent
              elif distance < 3: 
                  features['crossingOpponent'] = -distance    # move away from opponents
                  features['avoidDeadEnds'] = int(len(successor.getLegalActions(self.index)) < 3)
          else:
              if not enemy_state.scaredTimer > 0:
                  ghostDist = self.getMazeDistance(myPos, enemy_pos)
                  if myState.isPacman and ghostDist < 5:
                      features['avoidDeadEnds'] = int(len(successor.getLegalActions(self.index)) < 3)
                  if ghostDist < 4:
                      features['getToYourSide'] = self.getMazeDistance(myPos, self.start)  #return to your side if opponents ghost are nearby
                  if ghostDist < 3:
                      features['enemyIsNear'] = ghostDist    #opponent are nearby


  def getWeights(self, gameState, action):
    """
    Normally, weights do not depend on the gamestate. They can be either
    a counter or a dictionary.
    """
    return {'successorScore': 1.0}

class OffensiveReflexAgent(DummyAgent):
  """
  A reflex agent that seeks food. This is an agent
  we give you to get an idea of what an offensive agent might look like,
  but it is by no means the best or only way to build an offensive agent.
  """

  def getFeatures(self, gameState, action):
    features = DummyAgent.getFeatures(self, gameState, action)
    previous_observation = self.getPreviousObservation()

    #current agent state and position
    myState = gameState.getAgentState(self.index)
    myPos = myState.getPosition()

    #checking the previous  observation for information about the opponent's last move 
    if myPos in previous_observation:
        features['prev'] = 1
    return features

  def getPreviousObservation(self):
      """
      Returns the previous observation in the observation history.
      """
      #extract the positions of the agent from the last two observations if any
      if len(self.observationHistory) > 1:
          return [lastState.getAgentState(self.index).getPosition() for lastState in self.observationHistory[-2:]]
      else:
          return []


  def getWeights(self, gameState, action):
      return {'numInvaders': -1000, 'successorScore': 200,'distanceToCapsule': -1,'distanceToFood': -1, 'avoidDeadEnds': -100, 'invaderDistance': -5, 'getToYourSide': -10, 'enemyIsNear': 100, 'crossingOpponent': -0.50, 'stop': -100, 'backDir': -2, 'prev': -50}


class DefensiveReflexAgent(DummyAgent):
  """
  A reflex agent that keeps its side Pacman-free. Again,
  this is to give you an idea of what a defensive agent
  could be like.  It is not the best or only way to make
  such an agent.
  """
#   def getFeatures(self, gameState, action):
#     """
#     Returns a counter of features for the state
#     """
#     features = util.Counter()  #feature counter
#     successor = self.getSuccessor(gameState, action)
#     myState = successor.getAgentState(self.index)
#     myPos = myState.getPosition()

#     #calculating various features and update the features counter 
#     self.ScoreFeatures(features, myState, successor)
#     self.CapsuleFeatures(features, myPos, successor)
#     self.FoodFeatures(features, myPos, successor)
#     self.ActionFeatures(features, action, gameState)
#     self.GhostAndInvaderFeatures(features, myPos, myState, successor)

#     return features

#   def ScoreFeatures(self, features, myState, successor):
#       features['successorScore'] = myState.numCarrying + self.getScore(successor)

#   def CapsuleFeatures(self, features, myPos, successor):
#       #distance to nearest capsule and update features
#       capsule_distances = [self.getMazeDistance(myPos, capsule) for capsule in self.getCapsules(successor)]
#       if capsule_distances:
#           features['distanceToCapsule'] = min(capsule_distances)
#       elif myPos in self.getCapsules(self.getCurrentObservation()):
#           features['distanceToCapsule'] = -100000   #if I am carrying a capsule, then you get penalty so move away

#   def FoodFeatures(self, features, myPos, successor):
#       #distance to nearest food
#       foodList = self.getFood(successor).asList()
#       if foodList:
#           features['distanceToFood'] = min([self.getMazeDistance(myPos, food) for food in foodList])

#   def ActionFeatures(self, features, action, gameState):
#       if action == Directions.STOP:
#           features['stop'] = 1   #don't stop

#         #checking if the action is a reverse direction
#       back = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
#       if action == back:
#           features['backDir'] = 1    # penalization for going back

#   def GhostAndInvaderFeatures(self, features, myPos, myState, successor):
#       for enemy in self.getOpponents(successor):
#           enemy_state = successor.getAgentState(enemy)
#           enemy_pos = enemy_state.getPosition()
#           if enemy_pos is None:
#               continue
#           distance = self.getMazeDistance(myPos, enemy_pos)
#           if enemy_state.isPacman:
#               if myState.scaredTimer <= 0:
#                   features['crossingOpponent'] = distance    #chase opponent
#               elif distance < 3: 
#                   features['crossingOpponent'] = -distance    # move away from opponents
#                   features['avoidDeadEnds'] = int(len(successor.getLegalActions(self.index)) < 3)
#           else:
#               if not enemy_state.scaredTimer > 0:
#                   ghostDist = self.getMazeDistance(myPos, enemy_pos)
#                   if myState.isPacman and ghostDist < 5:
#                       features['avoidDeadEnds'] = int(len(successor.getLegalActions(self.index)) < 3)
#                   if ghostDist < 4:
#                       features['getToYourSide'] = self.getMazeDistance(myPos, self.start)  #return to your side if opponents ghost are nearby
#                   if ghostDist < 3:
#                       features['enemyIsNear'] = ghostDist    #opponent are nearby


  def getWeights(self, gameState, action):
    # return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}
    return {'numInvaders': -1000, 'successorScore': 100,'distanceToCapsule': -1,'distanceToFood': -1, 'avoidDeadEnds': -100, 'invaderDistance': -5, 'getToYourSide': -10, 'enemyIsNear': 100, 'crossingOpponent': -100, 'stop': -100, 'backDir': -2}

