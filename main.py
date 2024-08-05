
from constraints import *
from movements import *
from movements import movementsDict as m
from assignments import *

#create Constraint 
csp = Constraint()
csp.setAttributes(expandedList = [
                                  #(movement, num of times per cycle)
                                  (m['squat'], 1),
                                  #(m['leg press'], 1),
                                  (m['stiff leg deadlift'], 1),
                                  (m['reverse hyper'], 1),
                                  #(m['glute ham raise'], 1),
                                  
                                  (m['bench press'], 1), 
                                  (m['overhead press'], 1),
                                  #(m['chest fly'], 1),
                                  (m['skullcrusher'], 1),

                                  (m['lat pulldown'], 1),
                                  (m['lat row'], 1),
                                  (m['bicep curl'], 1),
                                  #(m['lateral raise'], 1),
                                  (m['shrug'], 1),
                                  (m['reverse fly'], 1),
                                  #(m['ab wheel'], 2)
                                  ],
                    cycleLength = 4, #how many days long is your cycle 
                    compoundLimit = 2, #max compound movements per day
                    isolationLimit = 3, #max isolation movements per day
                    totalLimit = 6, #max total movements per day
                    totalMin = 1, #min total movements per day
                    compoundGap = 0, #amount of days between overlapping compound movements
                    isolationGap = 0, #amount of days between overlapping isolation movements
                    compoundMin = 0, #min amount of compound movements per session
                    isolationMin = 0, #min amoun of isolation movements per session
                    #1 fatigue is roughly 1 minute in my current tuning
                    fatigueLimit = 75, #increase the fatigue maximum to make your programs potentially more exhausting 
                    fatigueMin = 25 #lower the fatigue minimum to see WAY more options
)

answers = []
assign = Assignment(csp)
if assign.meetSpace():
    assign.findAssignment(assign.expandedList, answers)
    answers = list(set(answers))
    
    #for answer in answers:
    #    print(answers.index(answer)+1)
    #    print(answer)
    
    #little code snippet below can be commented out
    #it's meant to create a sublist of all answers where a Movement is assigned to a particular day
    #complete implementation for this idea would require a slight edit to Assignments to take in partial Assignments but whatever
    filtered = [answer for answer in answers 
                if m['squat'] in answer.progressSchedule[4] 
                and m['bench press'] in answer.progressSchedule[1] 
                and m['stiff leg deadlift'] in answer.progressSchedule[1]
                and m['shrug'] in answer.progressSchedule[1]
                and len(answer.progressSchedule[1]) == 3
                and (len(answer.progressSchedule[4]) == 1 or (len(answer.progressSchedule[4]) == 2))
                ]
    print('______________________________')
    for filt in filtered:
        print(filtered.index(filt)+1)
        print(filt)
else:
    print('No available configurations!')
