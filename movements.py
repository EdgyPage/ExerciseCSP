class Movement:
    #valid names creates list of valid values for all Movements
    """validNames = list(map(str.lower, 
                            ['Bench Press', 'Shrug', 'Reverse Fly', 'Ab Wheel',
                            'Stiff Leg Deadlift', 'Skullcrusher', 'Overhead Press',
                            'Leg Press', 'Lat Row', 'Reverse Hyper', 'Bicep Curl', 
                            'Squat', 'Lat Pulldown', 'Lat Raise', 'Glute Ham Raise']))"""
    validParts = list(map(str.lower, 
                          ['traps', 'front delts', 'side delts', 'rear delts', 
                           'biceps', 'triceps', 'pecs', 'abs', 'lats', 'quads',
                           'hamstrings', 'glutes', 'lower back']))
    validStyles = list(map(str.lower, ['compound', 'isolation']))

    def __init__(self):
        
        #all attributes are none until they go through the @property decorator setters else
        self._name = None
        self._style = None
        self._parts = None
        self._fatigue = None
    
    def __repr__(self):
        return f'{self.name}'
    
    def __eq__(self, other):
        flag = True
        if not isinstance(other, Movement):
            flag = False
            return flag
        selfAttributes = self.getAttributes()
        otherAttributes = other.getAttributes()
        flag = selfAttributes == otherAttributes
        return flag
    
    def __hash__(self):
        hashable = tuple()
        hashable = hashable + (self.name, self.style, self.fatigue)
        for part in self.part:
            hashable = hashable + (part,)
        return hash(hashable)
    
    @property
    def fatigue(self):
        return self._fatigue
    
    @fatigue.setter
    def fatigue(self, exhaust: int):
        if exhaust < 0:
            raise ValueError(f'Invalid fatigue. Valid values are > 0, got {exhaust}')
        self._fatigue = exhaust

    @property
    #returns name of Movement
    def name(self):
        return self._name

    @name.setter
    #validates name and enforces lowercase convention for attributes
    def name(self, value):
        value = value.lower()
        """if value not in self.validNames:
            raise ValueError(f"Invalid value. Valid values are: {', '.join(self.validNames)}")"""
        self._name = value

    @property
    def part(self):
        return self._parts

    @part.setter
    #creates list from unique set of parts
    #sorted list is used as attribute
    def part(self, value):
        value = list(map(str.lower, list(set(value))))
        if not set(value).issubset(set(self.validParts)):
            raise ValueError(f"Invalid value. Valid values are: {', '.join(self.validParts)}")
        self._parts = sorted(value)

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, value):
        value = value.lower()
        if value not in self.validStyles:
            raise ValueError(f"Invalid value. Valid values are: {', '.join(self.validStyles)}")
        self._style = value

    #sets attributes on attribute ->  value pair where attribute is the respective setter function and value is the value
    def setAttributes(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
    
    #gets all attributes
    def getAttributes(self):
        allAttributes = vars(self)
        #below line was part of previous implementation where class had no class attributes
        #attributesOfInterest = {attr: value for attr, value in allAttributes.items() if attr.startswith('_')}
        return allAttributes

#can use this later to maybe create list of 
def createMovementFromDict(movementDict : dict):
    movement = Movement()
    movement.setAttributes(name = movementDict["name"], part = movementDict["part"], style = movementDict["style"], fatigue = movementDict['fatigue'])
    return movement

def createTempMovementDict(name: str, part: list, style: str, exhaust: int):
    return {'name': name, 'part': part, 'style': style, 'fatigue': exhaust}

movements = [
    createTempMovementDict('bench press', ['Front Delts', 'Pecs', 'Triceps'], 'compound', 25),
    createTempMovementDict('shrug', ['traps'], 'isolation', 10),
    createTempMovementDict('reverse fly', ['rear delts'], 'isolation', 10),
    createTempMovementDict('ab wheel', ['abs'], 'isolation', 10),
    createTempMovementDict('stiff leg deadlift', ['hamstrings', 'lower back', 'glutes'], 'compound', 30),
    createTempMovementDict('skullcrusher', ['triceps'], 'isolation', 15),
    createTempMovementDict('overhead press', ['triceps', 'front delts', 'side delts'], 'compound', 25),
    createTempMovementDict('leg press', ['quads'], 'compound', 20),
    createTempMovementDict('lat row', ['lats'], 'compound', 20),
    createTempMovementDict('reverse hyper', ['hamstrings'], 'isolation', 10),
    createTempMovementDict('bicep curl', ['biceps'], 'isolation', 15),
    createTempMovementDict('squat', ['quads', 'lower back'], 'compound', 30),
    createTempMovementDict('glute ham raise', ['glutes', 'hamstrings'], 'isolation', 10),
    createTempMovementDict('chest fly', ['pecs', 'front delts'], 'isolation', 20),
    createTempMovementDict('lateral raise', ['side delts'], 'isolation', 10),
    createTempMovementDict('lat pulldown', ['lats', 'biceps'], 'compound', 20)
            ]

movementsDict = {createMovementFromDict(tempMovementDict).name : createMovementFromDict(tempMovementDict) for tempMovementDict in movements}

