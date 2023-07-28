"""
function BACKTRACK-SEARCH(csp) returns solution or failure
    return BACKTRACK({}, csp)

function BACKTRACK(assignment, csp) returns a solution or failure
    if assignment is complete then return assignment
    var <- SELECT-UNASSIGNED-VARIABLE(csp)

    for each value in ORDER-DOMAIN-VALUES(var, assignment, csp) do
        if value is consistent with assignment then 
            add {var = value} to assignment
            inferences <- INFERENCE(csp, var, value)
            if inferences != failure then 
                add inferences to assignment
                result <- BACKTRACK(assignment, csp)
                if result != failure then
                    return result
        remove {var = value} and inferences from assignment
    return failure
"""

class Constraint:

    _expandedList: list




    def __init__(self):
        self._expandedList = None #full list, including repeats, of all movements in cycle
        self._cycleLength = None #how many sessions for each training cycle excluding rest days eg ppl is 6 days
        self._compoundLimit = None #how many compound movements per session
        self._isolationLimit = None #how many isolation movements per session
        self._totalLimit = None #how many movements per day maximum
        self._compoundDayOverDayOverlap = None #how many days between overlapping compound movements

    @property
    def expand(self):
        return self._expandedList

    @expand.setter
    def expand(self, movementTupleList):
        l = []
        for movement, frequency in movementTupleList:
            l.extend([movement] * frequency)
        self._expandedList = l
        
    


import movements as m

csp = Constraint()
csp.expand = [(m.abWheel, 2), (m.benchPress, 4), (m.chestFly, 1)]

print(csp.expand)