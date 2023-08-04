from movements import Movement
class Constraint:
    def __init__(self):
        self._expandedList = None #full list, including repeats, of all movements in cycle
        self._cycleLength = None #how many sessions for each training cycle excluding rest days eg ppl is 6 days
        self._compoundLimit = None #how many compound movements per session
        self._isolationLimit = None #how many isolation movements per session
        self._totalLimit = None #how many movements per day maximum
        self._totalMin = None #how many movements per day minimum
        self._compoundGap = None #how many days of gap between similar compound movements   
        self._isolationGap = None
        self._compoundMin = None
        self._isolationMin = None
        self._fatigueMin = None
        self._fatigueLimit = None

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
                raise ValueError(f'All tuples must be formatted (movement, int). Got ({type(tuple[0]), type(tuple[1])}).')
        for movement, frequency in movementTupleList:
            l.extend([movement] * frequency)
        self._expandedList = l
        
    @property
    def cycleLength(self):
        return self._cycleLength
    
    @cycleLength.setter
    def cycleLength(self, days: int):
        if not isinstance(days, int) or days < 1:
            raise ValueError(f'Expected integer for cycleLength greater than 0, got {type(days)}: {days}')
        self._cycleLength = days

    @property
    def compoundLimit(self):
        return self._compoundLimit
    
    @compoundLimit.setter
    def compoundLimit(self, limit: int):
        if not isinstance(limit, int) or limit < 0:
            raise ValueError(f'Expected integer for compoundLimit greater than 0, got {type(limit)}: {limit}')
        self._compoundLimit = limit

    @property
    def isolationLimit(self):
        return self._isolationLimit
    
    @isolationLimit.setter
    def isolationLimit(self, limit: int):
        if not isinstance(limit, int) or limit < 0:
            raise ValueError(f'Expected integer for isolationLimit greater than 0, got {type(limit)}: {limit}')
        self._isolationLimit = limit

    @property
    def totalLimit(self):
        return self._totalLimit
    
    @totalLimit.setter
    def totalLimit(self, limit: int):
        if not isinstance(limit, int) or limit < 0:
            raise ValueError(f'Expected integer for totalLimit greater than 0, got {type(limit)}: {limit}')
        self._totalLimit = limit

    @property
    def totalMin(self):
        return self._totalMin
    
    @totalMin.setter
    def totalMin(self, limit: int):
        if not isinstance(limit, int) or limit > self.totalLimit or limit < 0:
            raise ValueError(f'Expected integer for totalMin less than totalLimit, got {type(limit)}: {limit}')
        self._totalMin = limit
    
    @property
    def compoundGap(self):
        return self._compoundGap
    
    @compoundGap.setter
    def compoundGap(self, limit: int):
        if not isinstance(limit, int) or limit < 0:
            raise ValueError(f'Expected integer for compoundGap greater than 0, got {type(limit)}: {limit}')
        self._compoundGap = limit

    @property
    def isolationGap(self):
        return self._isolationGap
    
    @isolationGap.setter
    def isolationGap(self, limit: int):
        if not isinstance(limit, int) or limit < 0:
            raise ValueError(f'Expected integer for isolationGap greater than 0, got {type(limit)}: {limit}')
        self._isolationGap = limit

    @property
    def compoundMin(self):
        return self._compoundMin
    
    @compoundMin.setter
    def compoundMin(self, limit: int):
        if not isinstance(limit, int) or limit > self.compoundLimit or limit < 0 :
            raise ValueError(f'Expected integer for compoundMin less than compoundLimit, got {type(limit)}: {limit}')
        self._compoundMin = limit

    @property
    def isolationMin(self):
        return self._isolationMin
    
    @isolationMin.setter
    def isolationMin(self, limit: int):
        if not isinstance(limit, int) or limit > self.isolationLimit or limit < 0 :
            raise ValueError(f'Expected integer for isolationMin less than isolationLimit, got {type(limit)}: {limit}')
        self._isolationMin = limit
    
    @property
    def fatigueLimit(self):
        return self._fatigueLimit
    
    @fatigueLimit.setter
    def fatigueLimit(self, limit: int):
        if not isinstance(limit, int) or limit < 0:
            raise ValueError(f'Expected int for fatigueLimit greater than 0, got {type(limit)}: {limit}')
        self._fatigueLimit = limit

    @property
    def fatigueMin(self):
        return self._fatigueMin
    
    @fatigueMin.setter
    def fatigueMin(self, limit: int):
        if not isinstance(limit, int) or limit > self.fatigueLimit or limit < 0 :
            raise ValueError(f'Expected int for fatigueMin less than fatigueLimit, got {type(limit)}: {limit}')
        self._fatigueMin = limit


    #sets attributes on attribute ->  value pair where attribute is the respective setter function and value is the value
    def setAttributes(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def getAttributes(self):
        allAttributes = vars(self)
        #below line was part of previous implementation where class had no class attributes
        #attributesOfInterest = {attr: value for attr, value in allAttributes.items() if attr.startswith('_')}
        return allAttributes


        





