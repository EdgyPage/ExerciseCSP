class Movement:
    name : str
    style: str
    parts: list

    def __init__(self, declaredName, declaredStyle, parts):
        self.validNames = ['Bench Press', 'Shrug', 'Reverse Fly', 'Ab Wheel',
                            'Stiff Leg Deadlift', 'Skullcrusher', 'Overhead Press',
                            'Leg Press', 'Lat Row', 'Reverse Hyper', 'Bicep Curl', 
                            'Squat', 'Lat Pulldown', 'Lat Raise', 'Glute Ham Raise']
        self.validParts = ['traps', 'front delts', 'side delts', 'rear delts', 
                           'biceps', 'triceps', 'pecs', 'abs', 'lats', 'quads',
                           'hamstring', 'glutes']
        self.validStyles = ['compound', 'isolation']
        self.name = declaredName
        self.style = declaredStyle
        self.parts = sorted(set(parts))

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, value):
        if value not in self.validNames:
            raise ValueError(f"Invalid value. Valid values are: {', '.join(self.validNames)}")
        self.name = value

    @property
    def part(self):
        return self.parts

    @part.setter
    def part(self, value):
        if not set(value).issubset(set(self.validParts)):
            raise ValueError(f"Invalid value. Valid values are: {', '.join(self.validParts)}")
        self.parts = value

    @property
    def style(self):
        return self.style

    @style.setter
    def style(self, value):
        if value not in self.validStyles:
            raise ValueError(f"Invalid value. Valid values are: {', '.join(self.validStyles)}")
        self.style = value

benchPress = Movement('Bench Press', 'compound', ['triceps', 'pecs', 'front delt'])
