# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        self.qValues = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        # em razão de usar Counter, vai retornar 0.0 se o valor ainda não existe e Q(s,a) caso contrário
        return self.qValues[(state, action)]


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """

        legalActions = self.getLegalActions(state)

        # se não há ações legais (estado terminal), retorna 0.0
        if not legalActions:
            return 0.0

        # inicializa max_action com o menor valor possível
        max_action = float('-inf')

        # itera sobre as ações possíveis no estado e seleciona a ação com maior valor
        for action in legalActions:
            currentQValue = self.getQValue(state, action)
            if currentQValue > max_action:
                max_action = currentQValue

        return max_action

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        legalActions = self.getLegalActions(state)

        # se não há ações legais (estado terminal), retorna None
        if not legalActions:
            return None

        # inicializa max_action com o menor valor possível
        max_action = float('-inf')

        # best_actions é uma lista porque pode haver empate
        best_actions = []

        for action in legalActions:
            currentQValue = self.getQValue(state, action)

            # se encontra um novo máximo, reseta a lista
            if currentQValue > max_action:
                max_action = currentQValue
                best_actions = [action]

            # se ocorre um empate, adiciona ação à lista
            elif max_action == currentQValue:
                best_actions.append(action)

        # retorna randomicamente em caso de empate
        return random.choice(best_actions)


    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action

        legalActions = self.getLegalActions(state)

        if not legalActions:
            return None

        return (
            random.choice(legalActions)
            if util.flipCoin(self.epsilon)
            else self.computeActionFromQValues(state)
        )


    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        future_optimal_value = self.computeValueFromQValues(nextState)
        learned_value = reward + self.discount * future_optimal_value

        old_value = self.qValues[(state, action)]
        self.qValues[(state, action)] = (1 - self.alpha) * old_value + self.alpha * learned_value

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
    ApproximateQLearningAgent

    Implementa Q-Learning com aproximação linear de funções.
    Sobrescreve os métodos getQValue e update.
    """

    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
        Retorna Q(state, action) = w * featureVector
        onde * é o operador de produto escalar (dot product).
        """
        features = self.featExtractor.getFeatures(state, action)
        return sum(self.weights[feature] * value for feature, value in features.items())

    def update(self, state, action, nextState, reward):
        """
        Atualiza os pesos com base na transição (state, action, nextState, reward).
        """
        correction = (reward + self.discount * self.computeValueFromQValues(nextState)) - self.getQValue(state, action)

        features = self.featExtractor.getFeatures(state, action)
        for feature, value in features.items():
            self.weights[feature] += self.alpha * correction * value

    def final(self, state):
        """
        Chamado ao final de cada jogo.
        """
        PacmanQAgent.final(self, state)

