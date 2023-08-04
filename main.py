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
from constraints import *
from movements import *
from movements import movementsDict as m
from assignments import *
import copy

csp = Constraint()
csp.setAttributes(expandedList = [(m['bench press'], 1), 
                                  (m['overhead press'], 1),
                                  (m['lat row'], 1),
                                  (m['lat pulldown'], 1),
                                  (m['squat'], 1),
                                  (m['stiff leg deadlift'], 1),
                                  (m['reverse fly'], 2),
                                  (m['chest fly'], 1),
                                  (m['skullcrusher'], 1),
                                  (m['bicep curl'], 1),
                                  (m['leg press'], 1),
                                  (m['lateral raise'], 1),
                                  (m['reverse hyper'], 1),
                                  (m['glute ham raise'], 1),
                                  (m['ab wheel'], 2),
                                  (m['shrug'], 1)
                                  ],
                    cycleLength = 5,
                    compoundLimit = 3,
                    isolationLimit = 3,
                    totalLimit = 4,
                    totalMin = 2,
                    compoundGap = 1,
                    isolationGap = 1,
                    compoundMin = 2,
                    isolationMin = 1,
                    fatigueLimit = 100,
                    fatigueMin = 70
)
count = 0
answers = []
assign = Assignment(csp)
if assign.meetSpace():
    assign.findAssignment(assign.expandedList, answers, count)
    for answer in answers:
        print(answer)
    print(count)
else:
    print('No available configurations!')
