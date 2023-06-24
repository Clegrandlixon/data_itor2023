import random
import gc

MINIMUM_FREQUENCY = 0
MOST_FREQUENT_PATTERNS = 250
computeGap = lambda c1,c2: min(1, max(round(1 - (c2+0.1)/(c1+0.1), 3), -1))


class Pattern():
    """ Class representing patterns """

    def __init__(self, pattern: list, nbObjectives: int, iterationID) -> None:
        self.name = str(pattern)
        self.size = len(pattern)
        self.pattern = pattern
        self.frequency = 1
        self.isfrequent = self.frequency >= MINIMUM_FREQUENCY
        self.profile = [[[] for _ in range(nbObjectives)] for _ in range(nbObjectives)]
        self.nbObjectives = nbObjectives
        self.averageImprovement = [[0 for _ in range(nbObjectives)] for _ in range(nbObjectives)]
        self.lastUpdate = iterationID

    def get_name(self) -> str:
        return self.name

    def is_frequent(self):
        self.isfrequent = self.frequency >= MINIMUM_FREQUENCY
        return self.isfrequent

    def increment_frequency(self):
        self.frequency += 1

class StorePatterns():
    """ Class representing a data structure to store patterns """

    def __init__(self, maxPatternSize: int, nbObjectives: int, nbGroups):
        self.nbObjectives = nbObjectives
        self.groups = [[{} for _ in range(2, maxPatternSize+1)] for _ in range(nbGroups)]
        self.iterationID = 0 

    def store_pattern(self, pattern, sizePattern, groups):
        for index in groups:
            knowledgeGroup = self.groups[index][sizePattern-2]
            namePattern = str(pattern)
            if not (namePattern in knowledgeGroup.keys()):
                knowledgeGroup[namePattern] = (1, pattern)
            else:
                (v,p) = knowledgeGroup[namePattern] 
                knowledgeGroup[namePattern] = (v+1, p)

    def choosePatterns_setSize(self, groupID, sizePattern, nbChosen):
        # the size of pattern injected is set for the injection (it is not precised in the article detailing PILS), patterns are easier to track
        listOfPatterns = list(self.groups[groupID][sizePattern-2].values())
        listOfPatterns.sort()
        listOfPatterns.reverse()
        mostFrequentPatterns = listOfPatterns[:MOST_FREQUENT_PATTERNS]
        chosenPatterns = random.sample(mostFrequentPatterns, min(nbChosen, len(mostFrequentPatterns)))
        return [p for (_,p) in chosenPatterns]

    def choosePatterns_allSize(self, groupID, nbChosen):
        # possible redundancy between patterns
        chosenPatterns = []
        for i in range(nbChosen):
            size = random.randint(2, len(self.seenPatterns)+1)
            pattern = self.choosePatterns_setSize(groupID, size, 1)[0]
            chosenPatterns.append(pattern)
        return chosenPatterns
