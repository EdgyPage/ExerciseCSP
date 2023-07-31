from constraints import Constraint
from movements import Movement
class Assignment:

    def __init__(self, csp: Constraint):
        #test conditions copied from from Constraints
        self._expandedList = csp.expandedList #full list, including repeats, of all movements in cycle
        self._cycleLength = csp.cycleLength #how many sessions for each training cycle excluding rest days eg ppl is 6 days
        self._compoundLimit = csp.compoundLimit #how many compound movements per session
        self._isolationLimit = csp.isolationLimit #how many isolation movements per session
        self._totalLimit = csp.totalLimit #how many movements per day maximum
        self._compoundGap = csp.compoundGap #how many days of gap between similar compound movements

        self._progressList = []
        self._progressSchedule = {}
        for i in range(0, self._cycleLength):
            self._progressSchedule[i+1] = []

    @property
    def progressList(self):
        return self._progressList
    
    @progressList.setter
    def progressList(self, movement: Movement, condition = True):
        if condition:
            self._progressList = self.progressList.append(movement)
        else:
            self._progressList.pop()
    
    @property
    def progressSchedule(self):
        return self._progressSchedule
    
    @progressSchedule.setter
    def progressSchedule(self, day : int, movement: Movement, condition = True):
        if condition:
            self._progressSchedule[day] = self._progressSchedule[day].append(movement)
        else:
            self._progressSchedule[day].pop()

    @property
    def expandedList(self):
        return self._expandedList

    def sanityCheck(self):
        len()