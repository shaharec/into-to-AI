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


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
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
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
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
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        numCapsules = len(successorGameState.getCapsules())  # contain the number of capsules.
        # Find the closest distance to the food available in the game.
        closestFoodDist = float('inf')
        for food in newFood.asList():
            dist = manhattanDistance(newPos, food)  # Get distance from food.
            if closestFoodDist > dist:
                closestFoodDist = dist

        # Find closest ghost
        closestGhost = float('inf')
        for ghost in newGhostStates:
            dist = manhattanDistance(newPos, ghost.getPosition())  # Get distance from ghost.
            if ghost.getPosition() == newPos:  # If there is a ghost in the new position
                if (ghost.scaredTimer != 0):  # If the ghost is scared eat it. else run away.
                    return float('inf')
                else:
                    return float('-inf')
            # else:  # If the new position is not a ghost position, save the closest distance.
            #     if closestGhost > dist:
            #         closestGhost = dist
        # If the new position is not where a ghost is and there is no food left choos this action.
        if not newFood.asList(): return float('inf')

        return successorGameState.getScore() - closestFoodDist - successorGameState.getNumFood()*100 - \
               numCapsules



def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.max_value(gameState, 0, 0)[0]  # Return max value action.

    def min_max_decision(self, gameState, agentIndex, depth):
        """
        Helper recursive function,
        returns the best score of action for the agent index.
        """
        if depth >= self.depth * gameState.getNumAgents() or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        if agentIndex is 0:  # If its pacman return max value of tree.
            return self.max_value(gameState, agentIndex, depth)[1]  # Return node score.
        else:  # If its ghost return min value of tree.
            return self.min_value(gameState, agentIndex, depth)[1]  # Return node score.

    def max_value(self, gameState, agentIndex, depth):
        """
        Choose the max brench value - represent pacman choice.
        Returns a tuple of 2 elements (action,score of action)
        Gets the max score of action.
        """
        maxAction = ("none", float("-inf"))
        newDepth = depth + 1
        nextAgent = newDepth % gameState.getNumAgents()
        for action in gameState.getLegalActions(agentIndex):
            newGameStat = gameState.generateSuccessor(agentIndex, action)
            succAction = (action, self.min_max_decision(newGameStat, nextAgent, newDepth))
            maxAction = max(maxAction, succAction, key=lambda x: x[1])
        return maxAction

    def min_value(self, gameState, agentIndex, depth):
        """
        Choose the min brench value - represent ghost choice.
        Returns a tuple of 2 elements (action,score of action)
        Gets the min score of action.
        """
        minAction = ("none", float("inf"))
        newDepth = depth + 1
        nextAgent = newDepth % gameState.getNumAgents()
        for action in gameState.getLegalActions(agentIndex):
            newGameStat = gameState.generateSuccessor(agentIndex, action)
            succAction = (action, self.min_max_decision(newGameStat, nextAgent, newDepth))
            minAction = min(minAction, succAction, key=lambda x: x[1])
        return minAction



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.max_value(gameState,0,0,float('-inf'),float('inf'))[0]

    def min_max_decision(self, gameState, agentIndex, depth,alpha, beta):
        """
        Helper recursive function,
        returns the best score of action for the agent index.
        """
        if depth >= self.depth * gameState.getNumAgents() or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        if agentIndex is 0:  # If its pacman return max value of tree.
            return self.max_value(gameState, agentIndex, depth,alpha, beta)[1]  # Return node score.
        else:  # If its ghost return min value of tree.
            return self.min_value(gameState, agentIndex, depth,alpha,beta)[1]  # Return node score.

    def max_value(self, gameState, agentIndex, depth,alpha, beta):
        """
        Choose the max brench value - represent pacman choice.
        Returns a tuple of 2 elements (action,score of action)
        Gets the max score of action.
        By using alpha beta algorithm reduces the nodes expended.
        """
        maxAction = ("none", float('-inf'))
        newDepth = depth + 1
        nextAgent = newDepth % gameState.getNumAgents()
        for action in gameState.getLegalActions(agentIndex):
            newGameStat = gameState.generateSuccessor(agentIndex, action)
            succAction = (action, self.min_max_decision(newGameStat, nextAgent,
                                                        newDepth,alpha, beta))
            maxAction = max(maxAction, succAction, key=lambda x: x[1])
            if maxAction[1] > beta :
                return maxAction
            alpha = max(alpha,maxAction[1])
        return maxAction

    def min_value(self, gameState, agentIndex, depth ,alpha, beta):
        """
        Choose the min brench value - represent ghost choice.
        Returns a tuple of 2 elements (action,score of action)
        Gets the min score of action.
        By using alpha beta algorithm reduces the nodes expended.
        """
        minAction = ("none", float("inf"))
        newDepth = depth + 1
        nextAgent = newDepth % gameState.getNumAgents()
        for action in gameState.getLegalActions(agentIndex):
            newGameStat = gameState.generateSuccessor(agentIndex, action)
            succAction = (action, self.min_max_decision(newGameStat, nextAgent,
                                                        newDepth,alpha, beta))
            minAction = min(minAction, succAction, key=lambda x: x[1])
            if minAction[1] < alpha :
                return minAction
            beta = min(beta,minAction[1])
        return minAction


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        pacmanIndex = 0
        nextAgent =  1
        nextDepth = 1
        bestScore = float('-inf')
        bestAction = None
        for action in gameState.getLegalActions(0):
            newGameStat = gameState.generateSuccessor(pacmanIndex, action)
            score = self.min_max_decision(newGameStat,nextAgent,nextDepth)
            if score >= bestScore :
                bestAction = action
                bestScore = score
        return bestAction

    def min_max_decision(self, gameState, agentIndex, depth):
        """
        Helper recursive function,
        returns the best score of action for the agent index.
        """
        if depth >= self.depth * gameState.getNumAgents() or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        if agentIndex is 0:  # If its pacman return max value of tree.
            return self.max_value(gameState, agentIndex, depth)  # Return node score.
        else:  # If its ghost return min value of tree.
            return self.min_value(gameState, agentIndex, depth)  # Return node score.

    def max_value(self, gameState, agentIndex, depth):
        """
        Choose the max brench value - represent pacman choice.
        Returns the score of action.
        Gets the max score of action.
        """
        maxScore = float('-inf')
        newDepth = depth + 1
        nextAgent = newDepth % gameState.getNumAgents()
        for action in gameState.getLegalActions(agentIndex):
            newGameStat = gameState.generateSuccessor(agentIndex, action)
            score = self.min_max_decision(newGameStat, nextAgent,newDepth)
            maxScore = max(maxScore, score)
        return maxScore

    def min_value(self, gameState, agentIndex, depth):
        """
        Choose the min brench value - represent ghost choice.
        Returns the score of action
        Gets the avg score of action.
        """
        newDepth = depth + 1
        nextAgent = newDepth % gameState.getNumAgents()
        scores = []
        for action in gameState.getLegalActions(agentIndex):
            newGameStat = gameState.generateSuccessor(agentIndex, action)
            scores.append(self.min_max_decision(newGameStat, nextAgent,newDepth))
        scoresAvg = sum(scores)/float(len(scores))
        return scoresAvg

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    gamestatFood = currentGameState.getFood()

    pos = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    numCapsules = len(currentGameState.getCapsules())

    closestGhost = float('inf')
    for state in ghostStates:
        dist = manhattanDistance(state.getPosition(), pos)
        if dist < closestGhost: closestGhost = dist

    if closestGhost <= 1:
        if scaredTimes == 0: # If the ghost is near and not scared run away.
             return float('-inf')


    closestFoodDist =0
    foodDists = []
    for food in gamestatFood.asList():
        foodDists.append(manhattanDistance(pos, food))
    if len(foodDists) > 0: # There is still food in the game.
        closestFoodDist = min(foodDists)
    # If closestGhost <= 1 is true then the ghost is scared and we need to eat it, else in line 364 we would return.
    return currentGameState.getScore() - closestFoodDist + 100*(closestGhost <= 1)-numCapsules


# Abbreviation
better = betterEvaluationFunction
