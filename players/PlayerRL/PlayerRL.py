from interfaces import IPlayer
from enum import Enum
import belot

class CardState(Enum):
    UNKNOWN = 0
    AVAILABLE = 1
    TABLE = 2
    UNAVAILABLE = 3

class PlayerRL(IPlayer):

    def __init__(self, name):
        IPlayer.__init__(name, human=False)

        self.knowledge = dict()

        # inicijalno sve karte stavi u stanje UNKNOWN
        self.knowledge[CardState.UNKNOWN]=set(belot.cards)

        for player in [belot.PlayerRole.LEFT_OPPONENT, belot.PlayerRole.TEAMMATE, belot.PlayerRole.RIGHT_OPPONENT]:
            self.knowledge[player] = dict()
            for cardStatus in [CardState.AVAILABLE, CardState.UNAVAILABLE, CardState.TABLE]:
                self.knowledge[player][cardStatus]=set()

    def notifyDeclarations(self, declarations):
        knowledge = self.knowledge

        # sve karte poznate iz zvanja prebaci u stanje AVAILABLE
        for player in declarations:
            if player!=belot.PlayerRole.ME:
                for declaredSet in declarations[player]:
                    for card in declaredSet:
                        knowledge[CardState.UNKNOWN].remove(card)
                        knowledge[player][CardState.AVAILABLE].add(card)

    def playCard(self, table, legalCards):
        knowledge = self.knowledge

        # karte na stolu prebaci u stanje TABLE
        for player in table:
            card = player[table]

            if card in knowledge[player][CardState.AVAILABLE]:
                knowledge[player][CardState.AVAILABLE].remove(card)
            elif card in knowledge[CardState.UNKNOWN]:
                knowledge[CardState.UNKNOWN].remove(card)

            knowledge[player][CardState.TABLE].clear()
            knowledge[player][CardState.TABLE].add(card)

        # odredi potez na temelju cijelog stanja igre
        # TODO playing policy network
        cardToPlay = None

        # sve karte iz stanja TABLE prebaci u UNAVAILABLE
        for player in table:
            knowledgeTableCopy = set(knowledge[player][CardState.TABLE])
            for card in knowledgeTableCopy:
                knowledge[player][CardState.TABLE].remove(card)
                knowledge[player][CardState.UNAVAILABLE].add(card)

        return cardToPlay

    def bid(self, must):
        # TODO bidding policy network
        choice = None

        return choice

    def notifyHand(self, pointsUs, pointsThem):
        self.knowledge.clear()

    def notifyTrick(self, cards, value):
        pass

    def notifyBela(self, player, card):
        pass

    def declareBela(self, table):
        # TODO bela declaring policy network
        choice = None

        return choice