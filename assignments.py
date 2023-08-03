from constraints import Constraint
from movements import Movement
import copy
class Assignment:
    def __init__(self, csp: Constraint):
        #test conditions copied from from Constraints
        self._expandedList = csp.expandedList #full list, including repeats, of all movements in cycle
        self._cycleLength = csp.cycleLength #how many sessions for each training cycle excluding rest days eg ppl is 6 days
        self._compoundLimit = csp.compoundLimit #how many compound movements per session
        self._isolationLimit = csp.isolationLimit #how many isolation movements per session
        self._totalLimit = csp.totalLimit #how many movements per day maximum
        self._totalMin = csp.totalMin #how many movements per day minimum
        self._compoundGap = csp.compoundGap #how many days of gap between similar compound movements

        self._progressList = [] #built up list of assigned movements, used for comparisons
        self._progressSchedule = {} #built up dictionary of assigned movements, used for tests of complete assignments
        self._maxPossibleDays = len(self.expandedList) // self.totalMin #highest amount of days a program can have
        for i in range(0, self._cycleLength):
            self._progressSchedule[i+1] = []
    
    def __repr__(self):
        output = ''
        for key, movements in self.progressSchedule.items():
            output += f'{key}: '
            if movements:
                for movement in movements:
                    if movements.index(movement) == 0:
                        output += f' {movement}'
                    else:
                        output += f', {movement}'
            output += '\n'
        return output
    
    def __eq__(self, other):
        flag = True
        if not isinstance(other, Assignment):
            flag = False
            return flag
        selfAttributes = self.getAttributes()
        otherAttributes = other.getAttributes()
        flag = selfAttributes == otherAttributes
        return flag
    
    def __hash__(self):
        hashable = tuple()
        for key, movements in self.progressSchedule.items():
            hashable = hashable + (key,)
            for movement in movements:
                hashable = hashable + (movement,)
        return hash(hashable)
        
    def getAttributes(self):
        allAttributes = vars(self)
        #below line was part of previous implementation where class had no class attributes
        #attributesOfInterest = {attr: value for attr, value in allAttributes.items() if attr.startswith('_')}
        return allAttributes    

    @property
    def expandedList(self):
        return self._expandedList

    @property
    def progressList(self):
        return self._progressList
    
    @progressList.setter
    def progressList(self, value : (Movement, bool)):
        movement, condition = value
        if condition:
            self.progressList.append(movement)
        else:
            self._progressList.pop()
    
    @property
    def progressSchedule(self):
        return self._progressSchedule
    
    @progressSchedule.setter
    def progressSchedule(self, value: (int, Movement, bool)):
        day, movement, condition = value
        if condition:
            self._progressSchedule[day].append(movement)
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
    
    @property
    def totalMin(self):
        return self._totalMin
    
    @property
    def maxPossibleDays(self):
        return self._maxPossibleDays
    
    def progressScheduleSplitter(self):
        compoundDict = {}
        isolationDict = {}
        for i in range(0, self._cycleLength):
            compoundDict[i+1] = []
            isolationDict[i+1] = []

        for day, movements in self.progressSchedule.items():
            for movement in movements:
                if movement.style == 'compound':
                    compoundDict[day].append(movement)
                elif movement.style == 'isolation':
                    isolationDict[day].append(movement)
        return compoundDict, isolationDict

    def meetMovements(self):
        flag = True
        if len(self.progressList) != len(self.expandedList):
            flag = False
            return flag
        for m1, m2 in list(zip(self.progressList, self.expandedList)):
            flag = m1.getAttributes() == m2.getAttributes()
            if flag == False:
                break
        return flag

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
                break
        return flag

    def meetTotalLimit(self):
        flag = True
        for key in self.progressSchedule:
            if len(self.progressSchedule[key]) > self.totalLimit:
                flag = False
                break
        return flag
    
    def assignedDays(self):
        assignedDays = 0
        unassignedDays = 0
        for key, value in self.progressSchedule.items():
            if value:
                assignedDays += 1
            else:
                unassignedDays += 1
        return assignedDays, unassignedDays

    def meetMinLimitPartial(self):
        flag = True
        assignedDays, unassignedDays = self.assignedDays()
        maxPossibleDays = self.maxPossibleDays
        if assignedDays > maxPossibleDays:
            flag = False
        return flag

    def meetMinLimitComplete(self):
        flag = True
        for key in self.progressSchedule:
            if len(self.progressSchedule[key]) < self.totalMin:
                flag = False
                break
        return flag
    
    def meetNoCompoundIsolationDailyOverlap(self):
        compoundDict, isolationDict = self.progressScheduleSplitter()
        tempDict = {}
        flag = True
        for i in range(0, self.cycleLength):
            tempDict[i+1] = []

        for day, movements in compoundDict.items():
            for movement in movements:
                tempDict[day].extend(movement.part)
        
        for day, movements in isolationDict.items():
            for movement in movements:
                tempDict[day].extend(movement.part)
        
        for key in tempDict:
            if len(tempDict[key]) != len(list(set(tempDict[key]))):
                flag = False
                break
        return flag
    
    def meetCompoundGap(self):
        compoundDict, *_ = self.progressScheduleSplitter()
        tempDict = {}
        flag = True

        for day, movements in compoundDict.items():
            if movements:
                for movement in movements:  
                    if movement.name in tempDict:
                        tempDict[movement.name].append(day)
                    else:
                        tempDict[movement.name] = [day]
        
        for name, days in tempDict.items():
            prevDay = None
            for currentDay in days:
                if prevDay is not None:
                    if currentDay - prevDay <= self.compoundGap:
                        flag = False
                        break
                prevDay = currentDay
        return flag
    
    def partialTestSuite(self):
        flag = self.meetCompoundGap() and self.meetCompoundIsolationLimit() \
                and self.meetNoCompoundIsolationDailyOverlap() and self.meetTotalLimit() \
                and self.meetMinLimitPartial()
        return flag

    def completeTestSuite(self):
        flag = self.meetCompoundGap() and self.meetCompoundIsolationLimit() \
                and self.meetNoCompoundIsolationDailyOverlap() and self.meetTotalLimit() \
                and self.meetMinLimitComplete() and self.meetMovements() \
                and self.meetMinLimitPartial()
        return flag

    def findAssignment(self, movements : list, answers :list):
        if movements:
            for movement in movements:
                for key in self.progressSchedule:
                    updateAssignment = copy.deepcopy(self)
                    updateMovements = movements[1:]
                    updateAssignment.progressSchedule = (key, movement, True)
                    updateAssignment.progressList = (movement, True)
                    if updateAssignment.partialTestSuite():
                        updateAssignment.findAssignment(updateMovements, answers)
        else:
            if self.completeTestSuite():
                answers.append(self)
                removeDuplicates(answers)

    
def removeDuplicates(answers: list):
    unique = set(answers)
    answers.clear()
    answers.extend(unique)





        




