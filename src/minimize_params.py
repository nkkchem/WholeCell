import gurobipy
def print_rxns( newRxns, oldRxns ):
    ratios = {}
    print "Rxn\tNewFlux\tOldFlux\tMultiplier"
    for rxn in sorted(newRxns):
        print "%s\t%f\t%f\t%f" % (rxn, newRxns[rxn], oldRxns[rxn], newRxns[rxn]/oldRxns[rxn])
        ratios[rxn] = newRxns[rxn]/oldRxns[rxn]
    return ratios

rxns = ['Tmk', 'Fba', 'MetK', 'Pgi', 'AceE', 'Pta', 'CmkA2', 'AckA', 'Eno', 'TpiA', 'Growth']
m = gurobipy.read('metabolism.full.mmol-gDCW-h.gurobi.lp')
m.optimize()
oldRxns = dict([(rxn, m.getVarByName(rxn).X) for rxn in rxns])

#print_rxns( oldRxns )

m.setObjective( gurobipy.quicksum([m.getVarByName(rxn) for rxn in rxns]), gurobipy.GRB.MINIMIZE )
growth = m.getVarByName('Growth')
growth.setAttr('lb', growth.X*0.75 )
m.update()
m.optimize()
newRxns = dict([(rxn, m.getVarByName(rxn).X) for rxn in rxns])
ratios = print_rxns( newRxns, oldRxns )
del m
m = gurobipy.read('metabolism.full.mmol-gDCW-h.gurobi.lp')
for rxn in rxns:
    m.getVarByName(rxn).ub = newRxns[rxn]
m.update()
m.optimize()

def print_rxns( newRxns, oldRxns, renewedFlux ):
    print "Rxn\tNewFlux\tOldFlux\tMultiplier"
    for rxn in sorted(newRxns):
        print "%s\t%f\t%f\t%f" % (rxn, newRxns[rxn], oldRxns[rxn], newRxns[rxn]/oldRxns[rxn])
