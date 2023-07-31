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
        self._compoundGap = None #how many days of gap between similar compound movements

    @property
    def expandedList(self):
        return self._expandedList

    @expandedList.setter
    def expandedList(self, movementTupleList:tuple):
        l = []
        for tuple in movementTupleList:
            if len(tuple) != 2:
                raise ValueError(f'All tuples must be formatted (movement, int). Got {tuple}.')
            if not isinstance(tuple[0], Movement) or not isinstance(tuple[1], int):
                raise ValueError(f'All tuples must be formatted (movement, int). Got {type(tuple[0]), type(tuple[1])}.')
        for movement, frequency in movementTupleList:
            l.extend([movement] * frequency)
        self._expandedList = l
        
    @property
    def cycleLength(self):
        return self._cycleLength
    
    @cycleLength.setter
    def cycleLength(self, days: int):
        if not isinstance(days, int):
            raise ValueError(f'Expected integer for cycleLength, got {type(days)}')
        self._cycleLength = days

    @property
    def compoundLimit(self):
        return self._compoundLimit
    
    @compoundLimit.setter
    def compoundLimit(self, limit: int):
        if not isinstance(limit, int):
            raise ValueError(f'Expected integer for compoundLimit, got {type(limit)}')
        self._compoundLimit = limit

    @property
    def isolationLimit(self):
        return self._isolationLimit
    
    @isolationLimit.setter
    def isolationLimit(self, limit: int):
        if not isinstance(limit, int):
            raise ValueError(f'Expected integer for isolationLimit, got {type(limit)}')
        self._isolationLimit = limit

    @property
    def totalLimit(self):
        return self._totalLimit
    
    @totalLimit.setter
    def totalLimit(self, limit: int):
        if not isinstance(limit, int):
            raise ValueError(f'Expected integer for totalLimit, got {type(limit)}')
        self._totalLimit = limit
    
    @property
    def compoundGap(self):
        return self._compoundGap
    
    @compoundGap.setter
    def compoundGap(self, limit: int):
        if not isinstance(limit, int):
            raise ValueError(f'Expected integer for compoundGap, got {type(limit)}')
        self._compoundGap = limit

    #sets attributes on attribute ->  value pair where attribute is the respective setter function and value is the value
    def setAttributes(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def getAttributes(self):
        allAttributes = vars(self)
        #below line was part of previous implementation where class had no class attributes
        #attributesOfInterest = {attr: value for attr, value in allAttributes.items() if attr.startswith('_')}
        return allAttributes
    
from movements import Movement
from movements import movementsDict as m

csp = Constraint()
csp.setAttributes(expandedList = [(m['ab wheel'], 2), 
                                  (m['bench press'], 4), 
                                  (m['reverse fly'], 1)],
                    cycleLength = 5,
                    compoundLimit = 3,
                    isolationLimit = 4,
                    totalLimit = 4,
                    compoundGap = 1
)

print(csp.getAttributes())

#shift+alt+a to unblock code block
""" from movements import Movement
from movements import movementsDict as m

csp = Constraint()
print(m['bench press'].getAttributes())

csp.expandedList = [(m['ab wheel'], 2), (m['bench press'], 4), (m['reverse fly'], 1)]

print(csp.expandedList) """
