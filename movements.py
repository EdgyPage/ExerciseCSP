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

    _name : str
    _style : str
    _parts : list

    def __init__(self):
        
        #all attributes are none until they go through the @property decorator setters else
        self._name = None
        self._style = None
        self._parts = None

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
    movement.setAttributes(name = movementDict["name"], part = movementDict["part"], style = movementDict["style"])
    return movement

def createTempMovementDict(name: str, part: list, style: str):
    return {'name': name, 'part': part, 'style': style}

movements = [
    createTempMovementDict('bench press', ['Front Delts', 'Pecs', 'Triceps'], 'compound'),
    createTempMovementDict('shrug', ['traps'], 'isolation'),
    createTempMovementDict('reverse fly', ['rear delts'], 'isolation'),
    createTempMovementDict('ab wheel', ['abs'], 'isolation'),
    createTempMovementDict('stiff leg dealift', ['hamstrings', 'lower back', 'glutes'], 'compound'),
    createTempMovementDict('skullcrusher', ['triceps'], 'isolation'),
    createTempMovementDict('overhead press', ['triceps', 'front delts', 'side delts'], 'compound'),
    createTempMovementDict('leg press', ['quads'], 'isolation'),
    createTempMovementDict('lat row', ['lats', 'biceps', 'rear delts'], 'compound'),
    createTempMovementDict('reverse hyper', ['lower back', 'hamstrings'], 'isolation'),
    createTempMovementDict('bicep curl', ['biceps'], 'isolation'),
    createTempMovementDict('squat', ['quads', 'lower back'], 'compound'),
    createTempMovementDict('glute ham raise', ['glutes', 'hamstrings'], 'isolation'),
    createTempMovementDict('chest fly', ['pecs', 'front delts'], 'isolation'),
    createTempMovementDict('lateral raise', ['side delts'], 'isolation')
            ]

movementsDict = {createMovementFromDict(tempMovementDict).name : createMovementFromDict(tempMovementDict) for tempMovementDict in movements}

