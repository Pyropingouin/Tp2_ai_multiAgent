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
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

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
        capsulePositions = successorGameState.getCapsules()



        tempoScore = successorGameState.getScore()

     
        if capsulePositions:  
            capsuleDistances = [manhattanDistance(newPos, capsule) for capsule in capsulePositions]
            closestCapsuleDistance = min(capsuleDistances)  

            tempoScore += 90 / (1 + closestCapsuleDistance)
       

        ghostDistances = [manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates]
        if ghostDistances: 
            closestGhostDistance = min(ghostDistances)
            if any(time > 0 for time in newScaredTimes):
                 tempoScore += 100000

            else:     
                tempoScore -= 100 / (1 + closestGhostDistance)


        
        foodPositions = newFood.asList()

    
        if foodPositions:
            closestFoodDistance = min([manhattanDistance(newPos, foodPos) for foodPos in foodPositions])
            tempoScore += 10 / (1 + closestFoodDistance)
            
            
        
        

        return tempoScore

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
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
       
        _, action = self.maxValue(gameState, depth=0)
    
        return action


    def maxValue(self, gameState, depth):

        if gameState.isWin():
            return self.evaluationFunction(gameState), None       
        if gameState.isLose():
            return self.evaluationFunction(gameState), None       
        if depth == self.depth:
            return self.evaluationFunction(gameState), None       
        

        bestScore = -1000000
        bestAction = None

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0,action)
            score, _ = self.minValue(successor, depth, 1)

            if score > bestScore:
                bestScore = score
                bestAction = action    

        return bestScore, bestAction    

    

    def minValue(self, gameState, depth, ghostIndex):
        

        if gameState.isWin():
            return self.evaluationFunction(gameState), None       
        if gameState.isLose():
            return self.evaluationFunction(gameState), None       
        if depth == self.depth:
            return self.evaluationFunction(gameState), None          
        
        

        bestScore = 1000000
        bestAction = None

        for action in gameState.getLegalActions(ghostIndex):
            successor = gameState.generateSuccessor(ghostIndex,action)
           
            if ghostIndex == gameState.getNumAgents() - 1:
                score, _ = self.maxValue(successor, depth + 1)

            else:
                score, _ = self.minValue(successor, depth, ghostIndex + 1)

            if score < bestScore:
                bestScore = score
                bestAction = action    

        return bestScore, bestAction    
        




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        _, action = self.maxValue(gameState, depth=0, alpha=float("-inf"), beta=float("inf") )
    
        return action
    

    def maxValue(self, gameState, depth, alpha, beta):
        if gameState.isWin():
            return self.evaluationFunction(gameState), None       
        if gameState.isLose():
            return self.evaluationFunction(gameState), None       
        if depth == self.depth:
            return self.evaluationFunction(gameState), None    



        bestScore = float("-inf")
        bestAction = None

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0,action)
            score, _ = self.minValue(successor, depth, 1, alpha, beta)

            if score > bestScore:
                bestScore = score
                bestAction = action    

            alpha = max(alpha, bestScore)

            if bestScore > beta:
                break

        return bestScore, bestAction


    def minValue(self, gameState, depth, ghostIndex, alpha, beta):
        if gameState.isWin():
            return self.evaluationFunction(gameState), None       
        if gameState.isLose():
            return self.evaluationFunction(gameState), None       
        if depth == self.depth:
            return self.evaluationFunction(gameState), None    
        


        bestScore = float("inf")
        bestAction = None

        for action in gameState.getLegalActions(ghostIndex):
            successor = gameState.generateSuccessor(ghostIndex, action)

            if ghostIndex == gameState.getNumAgents() - 1:
                score, _ = self.maxValue(successor, depth + 1, alpha, beta)
            else:
                score, _ = self.minValue(successor, depth, ghostIndex + 1, alpha, beta)

            if score < bestScore:
                bestScore = score
                bestAction = action  

            beta = min(beta, bestScore)  

            if bestScore < alpha:  
                break  


        return bestScore, bestAction
        


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
        _, action = self.maxValue(gameState, depth=0)
    
        return action


    def maxValue(self, gameState, depth):

        if gameState.isWin():
            return self.evaluationFunction(gameState), None       
        if gameState.isLose():
            return self.evaluationFunction(gameState), None       
        if depth == self.depth:
            return self.evaluationFunction(gameState), None       
        

        bestScore = float("-inf")
        bestAction = None

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0,action)
            score, _ = self.expectValue(successor, depth, 1)

            if score > bestScore:
                bestScore = score
                bestAction = action    

        return bestScore, bestAction if bestAction is not None else None 

    
    def expectValue(self, gameState, depth, ghostIndex):
        

        if gameState.isWin():
            return self.evaluationFunction(gameState), None       
        if gameState.isLose():
            return self.evaluationFunction(gameState), None       
        if depth == self.depth:
            return self.evaluationFunction(gameState), None          
        

        legalActions = gameState.getLegalActions(ghostIndex)
        if not legalActions:
            return self.evaluationFunction(gameState), None
        

        totalScore = 0
        probability = 1.0 / len(legalActions)
       

        for action in gameState.getLegalActions(ghostIndex):
            successor = gameState.generateSuccessor(ghostIndex,action)
           
            if ghostIndex == gameState.getNumAgents() - 1:
                score, _ = self.maxValue(successor, depth + 1)

            else:
                score, _ = self.expectValue(successor, depth, ghostIndex + 1)

            totalScore += score



        expectedScore = totalScore * probability  

        return expectedScore, None 
        




def betterEvaluationFunction(currentGameState):



    
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <Je n'ai pas réussi à rendre mon PacMan assez rapide. Par contre, il est presque toujours (9/10) victorieux. 
    Je me suis basé sur la fonction d'évaluation écrit au début et j'ai ajouter des condtions pour la distance du fantôme.>
    """
    "*** YOUR CODE HERE ***"
 

  
    pacmanPos = currentGameState.getPacmanPosition()
    foodGrid = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    capsulePositions = currentGameState.getCapsules()

  
    score = currentGameState.getScore()

   
    for ghost in ghostStates:
        ghostPos = ghost.getPosition()
        distance = manhattanDistance(pacmanPos, ghostPos)

        if ghost.scaredTimer > 0:  
            score += 500 / (1 + distance)  
        else:  
            if distance < 3:  
                score -= 1500 / (1 + distance) 
            else:
                score -= 300 / (1 + distance)  

   
    foodList = foodGrid.asList()
    if foodList:
        closestFoodDistance = min(manhattanDistance(pacmanPos, food) for food in foodList)
        score += 300 / (1 + closestFoodDistance)  

 
    if capsulePositions:
        closestCapsuleDistance = min(manhattanDistance(pacmanPos, capsule) for capsule in capsulePositions)
        score += 500 / (1 + closestCapsuleDistance) 


    score -= 15 * len(foodList) 
    score -= 50 * len(capsulePositions)  

    return score

# Abbreviation
better = betterEvaluationFunction
