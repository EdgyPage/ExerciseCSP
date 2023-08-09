
from constraints import *
from movements import *
from movements import movementsDict as m
from assignments import *

csp = Constraint()
csp.setAttributes(expandedList = [
                                  #(movement, num of times per cycle)
                                  (m['squat'], 1),
                                  (m['leg press'], 1),
                                  (m['stiff leg deadlift'], 1),
                                  (m['reverse hyper'], 1),
                                  (m['glute ham raise'], 1),
                                  
                                  (m['bench press'], 1), 
                                  (m['overhead press'], 1),
                                  (m['chest fly'], 1),
                                  (m['skullcrusher'], 1),

                                  (m['lat pulldown'], 1),
                                  (m['lat row'], 1),
                                  (m['bicep curl'], 1),
                                  #(m['lateral raise'], 1),
                                  (m['shrug'], 1),
                                  (m['reverse fly'], 2),
                                  (m['ab wheel'], 2)
                                  ],
                    cycleLength = 5, #how many days long is your cycle 
                    compoundLimit = 3, #max compound movements per day
                    isolationLimit = 3, #max isolation movements per day
                    totalLimit = 4, #max total movements per day
                    totalMin = 3, #min total movements per day
                    compoundGap = 1, #amount of days between overlapping compound movements
                    isolationGap = 1, #amount of days between overlapping isolation movements
                    compoundMin = 1, #min amount of compound movements per session
                    isolationMin = 1, #min amoun of isolation movements per session
                    #1 fatigue is roughly 1 minute in my current tuning
                    fatigueLimit = 75, #increase the fatigue maximum to make your programs potentially more exhausting 
                    fatigueMin = 45 #lower the fatigue minimum to see WAY more options
)

"""csp = Constraint()
csp.setAttributes(expandedList = [(m['bench press'], 3), 
                                  (m['ab wheel'], 3)
                                 
                                  ],
                    cycleLength = 5,
                    compoundLimit = 3,
                    isolationLimit = 3,
                    totalLimit = 4,
                    totalMin = 1,
                    compoundGap = 1,
                    isolationGap = 1,
                    compoundMin = 0,
                    isolationMin = 0,
                    fatigueLimit = 75,
                    fatigueMin = 10
)"""

answers = []
assign = Assignment(csp)
if assign.meetSpace():
    assign.findAssignment(assign.expandedList, answers)
    answers = list(set(answers))
    
    for answer in answers:
        print(answers.index(answer)+1)
        print(answer)
    
    filtered = [answer for answer in answers if m['bench press'] in answer.progressSchedule[1] and m['squat'] in answer.progressSchedule[5] and m['shrug'] in answer.progressSchedule[1]]
    print('______________________________')
    for filt in filtered:
        print(filtered.index(filt)+1)
        print(filt)
else:
    print('No available configurations!')
