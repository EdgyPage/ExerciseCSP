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

csp = Constraint()
csp.setAttributes(expandedList = [(m['ab wheel'], 2), 
                                  (m['bench press'], 3), 
                                  (m['reverse fly'], 1)
                                  ],
                    cycleLength = 5,
                    compoundLimit = 3,
                    isolationLimit = 4,
                    totalLimit = 2,
                    totalMin = 2,
                    compoundGap = 1
)

answers = []

assign = Assignment(csp)

