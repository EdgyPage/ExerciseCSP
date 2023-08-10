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
        self._isolationGap = csp.isolationGap #how many days of gap between any isolated part being used again
        self._compoundMin = csp.compoundMin #how many compound movements per day minimum
        self._isolationMin = csp.isolationMin #how many isolation movmeents per day minimum
        self._fatigueMin = csp.fatigueMin #how much fatigue per day minimum
        self._fatigueLimit = csp.fatigueLimit #how much fatigue per day maximum

        self._progressList = [] #built up list of assigned movements, used for comparisons
        self._progressSchedule = {} #built up dictionary of assigned movements, used for tests of complete assignments; formated {day (as int): [Movements]}
        self._maxPossibleDays = self.maxPossibleTotalDaysCalc() #calculates maximum amount of days needed to accomodate all Movements to be assigned
        self._maxPossibleCompoundDays = self.maxPossibleCompoundDaysCalc() #calculates maximum amount of days needed to accomodate all compound Movements to be assigned
        self._maxPossibleIsolationDays = self.maxPossibleIsolationDaysCalc() #calculates maximum amount of days needed to accomodate all isolation Movements to be assigned
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
    
    #equality defined as dict of variables equalling other dict with matching object classes
    def __eq__(self, other):
        flag = True
        if not isinstance(other, Assignment):
            flag = False
            return flag
        selfAttributes = self.getAttributes()
        otherAttributes = other.getAttributes()
        flag = selfAttributes == otherAttributes
        return flag
    
    #hashable object is tuple of (day1, m1, m2, m3, day2, etc.)
    def __hash__(self):
        hashable = tuple()
        for key, movements in self.progressSchedule.items():
            hashable = hashable + (key,)
            for movement in movements:
                hashable = hashable + (movement,)
        return hash(hashable)
        
    def getAttributes(self):
        allAttributes = vars(self)
        return allAttributes 

    @property
    def expandedList(self):
        return self._expandedList

    @property
    def progressList(self):
        return self._progressList
    
    #helper method used to assign list of Movements that is built up as Movements are assigned, bool parameter is important
    #tuple is unpacked 
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
    
    #helper method used to assign Movements to certain days
    #tuple is unpacked
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
    def isolationGap(self):
        return self._isolationGap
    
    @property
    def compoundMin(self):
        return self._compoundMin
    
    @property
    def isolationMin(self):
        return self._isolationMin
    
    @property
    def fatigueLimit(self):
        return self._fatigueLimit

    @property
    def fatigueMin(self):
        return self._fatigueMin
    
    @property
    def maxPossibleDays(self):
        return self._maxPossibleDays
    
    def maxPossibleTotalDaysCalc(self):
        if self.totalMin == 0:
            days = 0
        else:
            #if there are 12 movements to be assigned but there is a per session minimum of 5, then max number of days is 2
            days = len(self.expandedList) // self.totalMin #highest amount of days a program can have
        return days
    
    @property
    def maxPossibleCompoundDays(self):
        return self._maxPossibleCompoundDays
    
    def maxPossibleCompoundDaysCalc(self):
        if self.compoundMin == 0:
            days = 0
        else:
            days = len([movement for movement in self.expandedList if movement.style == 'compound']) // self.compoundMin
        return days
    
    @property
    def maxPossibleIsolationDays(self):
        return self._maxPossibleIsolationDays
    
    def maxPossibleIsolationDaysCalc(self):
        if self.isolationMin == 0:
            days = 0
        else:
            days = len([movement for movement in self.expandedList if movement.style == 'isolation']) // self.isolationMin
        return days

    #helper function that splits self.progressSchedule in to two similar dicts where keys are the same but Movement assignment is based on style
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
    
    #tests if current assignment of Movements matches complete assignment of Movements
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

    #sanity check to see all Movements can fit in to alotted amount of days
    def meetSpace(self):
        max = self.cycleLength * self.totalLimit
        return max >= len(self.expandedList)
    
    #tests if Assignment meets compound and isolation limits
    def meetCompoundIsolationLimit(self):
        compoundDict, isolationDict = self.progressScheduleSplitter()
        flag = True
        for day, movements in compoundDict.items():
            if len(movements) > self.compoundLimit:
                flag = False
                return flag
        for day, movements in isolationDict.items():
            if len(movements) > self.isolationLimit:
                flag = False
                break
        return flag

    #tests if Assignment meets total limit
    def meetTotalLimit(self):
        flag = True
        for key in self.progressSchedule:
            if len(self.progressSchedule[key]) > self.totalLimit:
                flag = False
                break
        return flag
    
    #helper function that returns amount of assigned and unassigned days in self.progressSchedule
    def assignedDays(self):
        assignedDays = 0
        unassignedDays = 0
        for key, value in self.progressSchedule.items():
            if value:
                assignedDays += 1
            else:
                unassignedDays += 1
        return assignedDays, unassignedDays
    
    #helper function that returns dicts where {day : number of compound/isolation movmements on that day}
    def assignedCompoundIsolationDays(self):
        compoundDict, isolationDict = self.progressScheduleSplitter()
        compoundMovementPerDayDict = {}
        isolationMovementPerDayDict = {}
        for key, movements in compoundDict.items():
            compoundMovementPerDayDict[key] = 0
            if movements:
                compoundMovementPerDayDict[key] = compoundMovementPerDayDict[key] + len(movements)
        for key, movements in isolationDict.items():
            isolationMovementPerDayDict[key] = 0
            if movements:
                isolationMovementPerDayDict[key] = isolationMovementPerDayDict[key] + len(movements)
        return compoundMovementPerDayDict, isolationMovementPerDayDict
    
    #tests if PARTIAL Assignment CAN meet total, isolation, and compound mins by clever comparison with floored ints
    def meetTotalCompoundIsolationMinPartial(self):
        flag = True
        assignedDays, unassignedDays = self.assignedDays()
        maxPossibleDays = self.maxPossibleDays
        if assignedDays > maxPossibleDays:
            flag = False
            return flag
        
        compoundMovementPerDayDict, isolationMovementPerDayDict = self.assignedCompoundIsolationDays()
        for key, count in compoundMovementPerDayDict.items():
            if self.maxPossibleCompoundDays == 0:
                pass
            else:
                if count > self.maxPossibleCompoundDays:
                    flag = False
                    return flag
        
        for key, count in isolationMovementPerDayDict.items():
            if self.maxPossibleIsolationDays == 0:
                pass
            else:
                if count > self.maxPossibleIsolationDays:
                    flag = False
                    return flag

        return flag

    #tests if COMPLETE Assignment meets all minimums
    def meetTotalCompoundIsolationMinComplete(self):
        flag = True
        compoundDict, isolationDict = self.progressScheduleSplitter()
        for day, movements in compoundDict.items():
                if len(movements) < self.compoundMin:
                    flag = False
                    return flag
        
        for day, movements in isolationDict.items():
                if len(movements) < self.isolationMin:
                    flag = False
                    return flag
                
        for key in self.progressSchedule:
            if self.progressSchedule[key]:
                if len(self.progressSchedule[key]) < self.totalMin:
                    flag = False
                    return flag
        return flag

    #tests if partial Assignment exceeds fatigue limit    
    def meetFatigueLimitPartial(self):
        flag = True
        for key, movements in self.progressSchedule.items():
            if movements:
                exhaust = 0
                for movement in movements:
                    exhaust += movement.fatigue
                if exhaust > self.fatigueLimit:
                    flag = False
                    return flag
        return flag
    
    #thanks, chatGPT-chan
    #function that mostly works
    #helper function that checks to see if list of numbers can meet or exceed a threshold amount
    def is_combination_above_threshold(self, numbers, threshold):
        def check_combination(index, current_sum):
            if current_sum >= threshold:
                return True
            if index >= len(numbers):
                return False

            # Include the current number in the sum
            if check_combination(index + 1, current_sum + numbers[index]):
                return True

            # Exclude the current number from the sum
            if check_combination(index + 1, current_sum):
                return True

            return False

        return check_combination(0, 0)    
    
    #test that checks if partial Assignment has enough Movements left to meet fatigue minimum for each assigned day
    def meetFatigueMinPartial(self, unassignedMovements):
        fatigueList = [movement.fatigue for movement in unassignedMovements]
        flag = True
        for key, movements in self.progressSchedule.items():
            if movements:
                threshold = self.fatigueMin - sum([movement.fatigue for movement in movements]) 
                flag = self.is_combination_above_threshold(fatigueList, threshold)
                if not flag:
                    return flag
        return flag

    #tests complete assignments to see if all days fit within fatigue min and max
    def meetFatigueLimitMinComplete(self):
        flag = True
        for key, movements in self.progressSchedule.items():
            if movements:
                exhaust = 0
                for movement in movements:
                    exhaust += movement.fatigue
                if exhaust > self.fatigueLimit or exhaust < self.fatigueMin:
                    flag = False
                    return flag
        return flag

    #tests Assignment to see if there is no overlap between any Movement parts eg bench press on same day as tricep pushdowns
    #this function is assumed to be what the user wants so it is hard coded to work, can easily make a case to take in a bool upon Constraint instatiation
    #to allow overlaps between compound and isolation movements
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

    #tests to see if parts of all assigned movements meet respective gaps
    def meetCompoundIsolationGap(self):
        compoundDict, isolationDict = self.progressScheduleSplitter()
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
                        return flag
                prevDay = currentDay

        tempDict = {}
        for day, movements in isolationDict.items():
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
                    if currentDay - prevDay <= self.isolationGap:
                        flag = False
                        return flag
                prevDay = currentDay
        
        return flag
    
    #tests to see if parts of all assigned movements meet respective gaps when accounting for overlap between compound and isolation parts
    def meetCompoundIsolationGapOverlap(self):
        compoundDict, isolationDict = self.progressScheduleSplitter()
        tempDict = {}
        flag = True

        for day, movements in compoundDict.items():
            if movements:
                for movement in movements:
                    for part in movement.part:  
                        if part in tempDict:
                            tempDict[part].append(day)
                        else:
                            tempDict[part] = [day]

        for day, movements in isolationDict.items():
            if movements:
                for movement in movements:
                    for part in movement.part:  
                        if part in tempDict:
                            tempDict[part].append(day)
                        else:
                            tempDict[part] = [day]

        for part, days in tempDict.items():
            prevDay = None
            for currentDay in days:
                if prevDay is not None:
                    if currentDay - prevDay <= self.isolationGap:
                        flag = False
                        return flag
                prevDay = currentDay
        
        return flag
    
    #All partial tests in one helper function
    def partialTestSuite(self, unassignedMovements):
        flag = self.meetCompoundIsolationGap() and \
            self.meetCompoundIsolationLimit() \
                and self.meetNoCompoundIsolationDailyOverlap() and \
                    self.meetTotalLimit() \
                and self.meetTotalCompoundIsolationMinPartial() and \
                    self.meetFatigueLimitPartial() \
                and self.meetFatigueMinPartial(unassignedMovements) and \
                    self.meetCompoundIsolationGap() \
                and self.meetCompoundIsolationGapOverlap()
        return flag

    #all complete tests and partial tests in one helper function
    def completeTestSuite(self, unassignedMovements):
        flag = self.partialTestSuite(unassignedMovements) \
            and self.meetMovements() \
                    and self.meetFatigueLimitMinComplete() \
                    and self.meetTotalCompoundIsolationMinComplete()
        return flag

    #main function
    def findAssignment(self, movements : list, answers :list):
        flag = True
        if movements: #if list has Movements
            for movement in movements: #for each Movement
                updateMovements = movements[1:] #new list is input list's tail
                for key in self.progressSchedule: #for each possible day
                    self.progressSchedule = (key, movement, True) #assign Movement to day
                    self.progressList = (movement, True) #assign Movement to list of assigned movements
                    passConditions = self.partialTestSuite(updateMovements) #check partial assignment
                    if passConditions: 
                        self.findAssignment(updateMovements, answers) #recurse if Assignment is 'good enough' with tail of Movements left to be assigned
                    self.progressSchedule = (key, movement, False) #removes Movement assignment after recursion fails or if conditions don't pass
                    self.progressList = (movement, False) 
                    if key == list(self.progressSchedule.keys())[-1]: #if key is last in list of all possible keys, then Movement has no where else to go ie failure
                        flag = False
                if not flag: #breaks out of loop so that next Movement is not assigned if previous Movement has not been assigned 
                    break
        else:
            if self.completeTestSuite([]): #if Assignment has no more Movements left to assign AND meets complete constraints
                answers.append(copy.deepcopy(self)) #make a copy of Assignment and append to list of valid answers







        




