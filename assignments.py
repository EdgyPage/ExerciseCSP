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

        self._progressList = [] #built up list of assigned movements, used for comparisons
        self._progressSchedule = {} #built up dictionary of assigned movements, used for tests of complete assignments
        for i in range(0, self._cycleLength):
            self._progressSchedule[i+1] = []

    @property
    def expandedList(self):
        return self._expandedList

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

    @property
    def cycleLength(self):
        return self._cycleLength

    @property
    def compoundLimit(self):
        return self._compoundLimit
    
    @property
    def isolationLimit(self):
        return self._isolationLimit
    
    @property
    def totalLimit(self):
        return self._totalLimit
    
    @property
    def compoundGap(self):
        return self._compoundGap
    
    def progressScheduleSplitter(self):
        compoundDict = {}
        isolationDict = {}
        for i in range(0, self._cycleLength):
            compoundDict[i+1] = []
            isolationDict[i+1] = []

        for day, movements in self.progressSchedule.items():
            for movement in movements:
                if movement.style == 'compound':
                    compoundDict[day] = compoundDict[day].append(movement)
                elif movement.style == 'isolation':
                    isolationDict[day] = isolationDict[day].append(movement)
        return compoundDict, isolationDict

    def meetSpace(self):
        max = self.cycleLength * self.totalLimit
        return max >= len(self.expandedList)
    
    def meetCompoundIsolationLimit(self):
        compoundDict, isolationDict = self.progressScheduleSplitter()
        flag = True
        for day, movements in compoundDict.items():
            if len(movements) > self.compoundLimit:
                flag = False
        for day, movements in isolationDict.items():
            if len(movements) > self.isolationLimit:
                flag = False
        return flag

    def meetTotalLimit(self):
        flag = True
        copyProgress = self.progressSchedule
        for day, movements in copyProgress.items():
            if len(movements) > self.totalLimit:
                flag = False
        return True
    
    def meetNoCompoundIsolationDailyOverlap(self):
        compoundDict, *_ = self.progressScheduleSplitter()
        tempDict = {}
        flag = True
        for i in range(0, self._cycleLength):
            tempDict[i+1] = []

        for day, movements in compoundDict.items():
            for movement in movements:
                tempDict[day] = tempDict[day].append(movement.part)
        
        for i in range(0, self.cycleLength):
            if len(tempDict[i]) != len(set(tempDict[i])):
                flag = False
        
        return flag
