from __future__ import division
import copy
from collections import deque

english = False # set this when testing on an english grammar, such as toygrammar.toy and toygrammar.probs. Otherwise, set false
test = True

grammar = {}
fname1 = "probs.txt"
fname2 = "terminalprobs.txt"
if test:
    fname1 = "test" + fname1
    fname2 = "test" + fname2
with open(fname1,"r") as f:
  x = f.read()
  grammar = eval(x)

with open(fname2,"r") as f:
  x = f.read()
  terms = eval(x)

def getprobs(grammar):
  newgrammar = {}
  probs = {}
  for key in grammar:
    RHS = grammar[key]
    total = sum(RHS.values())
    for rule in RHS:
      probs[key, rule] = RHS[rule]/total
    ## Below commented out code is for figuring out what's up with the grammar
    ## i = 0
    ## for x in RHS.keys():
    ##     if type(x) == type("what"):
    ##         print "in getprobs: found a string: " + x
    ##         #print key, RHS
    ##         print "key: " + str(key) + "; RHS: " + str(RHS)
    ##     if i == 5:
    ##         print "regular one:"
    ##         print "key: " + str(key) + "; RHS: " + str(RHS)
    ##     i = i+1
    newgrammar[key] = [list(x) for x in RHS.keys()] #RHS.keys()
  return newgrammar, probs

newgrammar, probs = getprobs(grammar)
terminals, terminalprobs = getprobs(terms)

#print newgrammar['sps00']
############### Convert to CNF stuff ##################
# TODO: to identify terminals and nonterminals, just look at the keys of the grammar dictionary - they are non-terminals, others are terminals
# TODO: fix bug w/ removing unit productions - maybe switch to testing on smaller, baby grammar w/ probabilities
# TODO: figure out what's going on with things being in grammar that shouldn't - some code investigating this is commented out in extract.py


# Terminals for english
if english:
    terminals = set(['that','this','a','book','flight','meal','money','include','prefer','I','she','me','Houston','TWA','does','from','to','on','near','through','test','the', 'stealer']) # TODO: terminals defined twice - remove this one
    terminals_CI = {x.lower() for x in terminals}

# Nonterminals for english
if english:
    # Nonterminals for english
    nonterminals = set(['S','NP','Nominal','VP','PP','Det','Noun','Verb','Pronoun','Proper-Noun','Aux','Preposition'])
    nonterminals_CI = {x.lower() for x in nonterminals}
else:
    nonterminals = set(newgrammar.keys()) # nonterminals for scraped spanish grammar

def nameMaker():
    class context:
        y = 0
    def inner():
        context.y += 1
        ret = "_X" + str(context.y) + "_"
        nonterminals.add(ret)
        return ret
    return inner
getNewName = nameMaker() # using the above closure, when we say `getNewName` we will always get a new string each time

# This function determines whether a grammar is in Chomsky Normal Form
def InCNF(g):
    for left_side in g:
        rule_list = g[left_side]
        for rule in rule_list:
            if len(rule) > 2 or len(rule) < 1:
                bool = False
                #print "wrong: long or empty rule"
                #print "offending rule:   " + str(rule)
            elif len(rule) == 2:
                bool =  (rule[0] in nonterminals) and (rule[1] in nonterminals) # string comparison
                #if not bool:
                #    print "wrong: mixed rule"
                #    print "offending rule:   " + str(rule)
            else:     # i.e, len(rule) == 1
                #bool =  (rule[0] in terminals) # original
                bool =  (rule[0].lower() in terminals_CI) # string comparison
# TODO: adapt CNF converter to take a grammar and a probability dict, and return a modified version of each.
# TODO: adapt CNF converter to take a grammar and a probability dict, and return a modified version of each.
                #if not bool:
                #    print "wrong: unit production"
                #    print "offending rule:   " + str(rule)
            if not bool:
                return bool 
    return True


# Takes in a grammar (in the given dictionary format), and modifies it to get 
#   rid of rules that mix terminals and nonterminals.
# Does not return anything - it modifies the given grammar.
def convertMixedRules(g, p):
    for left_side in g.keys():
        rule_list = g[left_side]
        for rule in rule_list:
            if len(rule) > 1:
                for i in range(len(rule)):
                    if rule[i] in terminals:
                        dummy = rule[i] + "_dummy"
                        nonterminals.add(dummy)
                        g[dummy] = [[rule[i]]]
                        p[(dummy, tuple([rule[i]]))] = 1
                        #print left_side, rule, rule[i], dummy
                        prev_prob = p[ (left_side, tuple(rule) ) ]
                        del p[ (left_side, tuple(rule) ) ]
                        rule[i] = dummy
                        p[ (left_side, tuple(rule) ) ] = prev_prob


## # Takes a grammar in the dictionary format and returns a list of tuples, each representing the start and end of a chain of unit productions - so if we have A -> B and B -> C, it should return [('A', 'B'), ('B', 'C'), ('A', 'C')]
## def findUnitProductionChains(g, theProbs):
##     #print "~~~~begin~~~~~!!!!!" + str( type(theProbs))
##     unitChains = set([])
##     for left_side in g:
##         #print "loop1"
##         rule_list = g[left_side]
##         for rule in rule_list:
##             if (len(rule) == 1) and (rule[0] in nonterminals): # string comparison
##                 thisProb = theProbs[(left_side, tuple(rule))] # probability of this rule
##                 unitChains.add( (left_side, rule[0], thisProb) )
##     foundSome = True
##     while foundSome:
##         #print "loop2"
##         foundSome = False
##         newOnes = set([])
##         for triple in unitChains:
##             #print "loop3"
##             #print pair
##             A, B, p = triple
##             for rule in g[B]:
##                 #print B + " -> " + str(rule)
##                 if (len(rule) == 1) and (rule[0] in nonterminals): # string comparison
##                     #print "got here"
##                     #print "~~~~~~~~~!!!!!" + str( type(theProbs))
##                     #probAtoB = theProbs[ ( A, tuple([B]) ) ] # commented out because this should be p, and may not be in theProbs yet?
##                     probBtoNext = theProbs[ ( B, tuple(rule) ) ]
##                     #newProb = probAtoB * probBtoNext
##                     newProb = p * probBtoNext
##                     new = (A, rule[0], newProb)
##                     #print new
##                     #print (new not in unitChains)
##                     if (new not in unitChains) and (new not in newOnes): # string comparison
##                         #print "got here22222"
##                         newOnes.add( new )
##                         foundSome = True
##         unitChains.update(newOnes) # same as `unitChains = unitChains.union(newOnes)` or `unitChains = (unitChains | newOnes)`, but faster
##     return unitChains


## # Takes in a grammar (in the given dictionary format), and modifies it to get 
## #   rid of unit productions.
## # Does not return anything - it modifies the given grammar.    
## def removeUnitProductions(g, theProbs):
##     #print "'Verb' in g? : " + str('Verb' in g)
##     unitChains = findUnitProductionChains(g, theProbs)
##     print "found all unit production chains!"
##     print "len(unitChains):", len(unitChains)
##     for triple in unitChains:
##         print "loop forever?"
##         A, B, p = triple
##         print "len(g[B]):", len(g[B])
##         print "A, B:", A, B
##         for rule in g[B]:
##             #print "loop forever 2?"
##             #print "inside: len(g[B]):", len(g[B])
##             g[A].append(rule)
##             #theProbs[(dummy, tuple([rule[i]]))] = 1 # example probs usage
##             probBtoRule = theProbs[ ( B, tuple(rule) ) ]
##             theProbs[(A, tuple(rule))] = p * probBtoRule
##         #print "A: " + str(A) + "; B: " + str(B) + "; g[A]: " + str(g[A])
##         #g[A].remove([B])
##         if [B] in g[A]:
##             g[A].remove([B])
##         #del g[B] # no longer need rule B at all

def hasUnitProduction(g):
    for lhs in g:
        for indexOfRule in range(len(g[lhs])):
            rule = g[lhs][indexOfRule]
            if (len(rule) == 1) and rule[0] in nonterminals:
                return (True, (lhs, indexOfRule))
    return False

def removeUnitProductions(g, theProbs):
    while True: # because of next 3 lines, effectively `while there is a unit production`
        boolean, tup = hasUnitProduction(g)
        if not boolean:
            break

        lhs, indexOfRule = tup
        A = lhs
        rule = g[lhs]indexOfRule
        B = rule[0]
        len1BRules = [x[0] for x in g[B] if len(x) == 1]
        terminalBRules = [x in terminals for x in len1BRules]
        if any(terminalBRules): # if B goes to any terminal
            probAtoB = theProbs[ ( A, tuple([B]) ) ]
            for bRule in terminalBRules:
                probBtoBRule = theProbs[ ( B, tuple([bRule]) ) ]
                g[A] = bRule
                theProbs[ ( A, tuple([bRule]) ) ] = probAtoB * probBtoBRule
            g[A].remove([B])
            del theProbs[ (A, tuple([B]) ) ]

# Takes a single "long" rule: lhs is the nonterminal on the left-hand-side, rhs is the right-hand-side of the rule, and returns a suitable set of replacement rules in CNF, as tuples (i.e., expandRule("Z", ["A", "B", "C", "D"]) -> [("Z", ["A", "X1"]), ("X1", ["B", "X2"]), ("X2", ["C", "D"])]
def expandRule(lhs, rhs, theProbs):
    origProb = theProbs[ (lhs, tuple(rhs) ) ]
    newRules = []
    prev = lhs
    for i in range(0, len(rhs)-2): # we assume that rhs is at least length 3, or else this function shouldn't be called
        nextName = getNewName()
        #newRules.append( (prev, [rhs[i], nextName]) )
        if prev == lhs: # the rule w/ the original lhs
            newRules.append( (prev, [rhs[i], nextName], origProb) )
        else:
            newRules.append( (prev, [rhs[i], nextName], 1) )
        prev = nextName

    newRules.append( (prev, [rhs[len(rhs)-2], rhs[len(rhs)-1]], 1) )
    return newRules


# Remove and replace "long" rules (more than 3 nondeterminals on the right hand side) with equivalent sequences of shorter ones. Takes a grammar and modifies it - does not return anything.
def removeLongRules(g, theProbs):  # make change probabilites in p appropriately
    longRules = []

    # Find all rules of length 3 or more, "write them down"
    for left_side in g:
        rule_list = g[left_side]
        for rule in rule_list:
            if len(rule) > 2:
                longRules.append( (left_side, rule) )

    # remove them from the grammar
    for pair in longRules:
        lhs, rhs = pair
        g[lhs].remove(rhs)

    # expand each removed long rule into a sequence of rules w/ dummy nonterminals (X1, X2, etc.) and add them to the grammar
    for pair in longRules:
        lhs, rhs = pair
        replacement = expandRule(lhs, rhs, theProbs)
        for triple in replacement:
            newLHS, newRHS, p = triple
            theProbs[ (newLHS, tuple(newRHS)) ] = p
            if newLHS in g:
                g[newLHS].append(newRHS)
            else:
                g[newLHS] = [newRHS]
        del theProbs[ (lhs, tuple(rhs) ) ] # the original rule


# This function takes a grammar and returns an equivalent grammar in Chomsky Normal Form
def ConvertToCNF(g, p):
    g = copy.deepcopy(g)
    p = copy.deepcopy(p)
    convertMixedRules(g, p)
    removeUnitProductions(g, p)
    removeLongRules(g, p)

    return (g, p)

######################################################

# Extra Credit (optional): Modify your CKYRecognizer function to instead return a valid parse of the string, if one exists.
def CKYParser(g,s):
  ss = s
  s = s.split()
  rev = [(value, tup[0]) for tup in g.items() for value in tup[1]]
  table = [[[] for j in range(len(s)+1)] for i in range(len(s))]
  parseTable = [[[] for j in range(len(s)+1)] for i in range(len(s))]
  #add the LHS of all the rules that go to word[j] in the grammar
  for j in range(1,len(s)+1):
    lhs = [tup[1] for tup in rev if tup[0] == s[j-1]]
    table[j-1][j] = lhs
    parseTable[j-1][j] = (lhs, s[j-1])
    for i in range(j-2, -1, -1):
      for k in range(i+1, j):
        cc = table[k][j]
        bb = table[i][k]
        for b in bb:
          for c in cc:
            #want to include k,j and i,k as pointers
            lhs = [tup[1] for tup in rev if tup[0] == ([b, c])]
            for l in lhs:
              if l:
                table[i][j] = list(set(table[i][j] + [l]))
                parseTable[i][j] = list(set(parseTable[i][j] + [(l, (k, j),(i,k))]))

  if "S" in table[0][-1]:
    '''
    i = 0
    for row in parseTable:
      i += 1
      print row[i:]
    '''
    print "\n"
    parses = [rule for rule in parseTable[0][-1] if rule[0] == "S"]
    trees = [getParse(parseTable, s,g, True, "") for s in parses]

    print ss
    print "\n"
    for tree in trees:
      for tt in tree:
        for t in tt:
          print t
          print "\n"
    return True
  else:
    return False

#this function takes a table (with pointers), a start symbol and the pointers to which entries in the table it was derived from, a grammar, and a terminal (that is an empty string unless the start is POS tag in which case it deserives a terminal
#returns all parses
def getParse(table, start, grammar, startsymbol, terminal):
    #base case: we reached a POS with no indices
    if type(start) == type("string"):
      return [terminal]
    i = start[2][0]
    j = start[1][1]
    k = start[1][0]
    ruledown = table[k][j]
    ruleleft = table[i][k]
    if not ruleleft or not ruledown:
      return [start[0]]
    else:
      parses = []
      terminaldown = False
      terminalleft = False
      worddown = ""
      wordleft = ""
      if type(ruledown) == type(()):
        terminaldown = True
        worddown = ruledown[1]
        ruledown = ruledown[0]
      if type(ruleleft) == type(()):
        terminalleft = True
        wordleft = ruleleft[1]
        ruleleft = ruleleft[0]

      for rd in ruledown:
        for rl in ruleleft:
          rule1 = rl
          rule2 = rd
          if type(rule1) != type("str"):
            rule1 = rl[0]
          if type(rule2) != type("str"):
            rule2 = rd[0]

          #check to see if this rule should be expanded (did it actually come from start?
          RHS = grammar[start[0]]
          thisRHS = [rule1, rule2]
          if thisRHS in RHS:
            if startsymbol:
              parses.append([[start[0]] + [[rule1] + [rule2] + [getParse(table, rl, grammar, False, wordleft) + getParse(table, rd, grammar, False, worddown)]]])
            else:
              parses.append([[rule1] + [rule2] + [getParse(table, rl, grammar, False, wordleft) + getParse(table, rd, grammar, False, worddown)]])
      return parses

'''
# Add more tests of CKYRecognizer here.
f1 = CKYRecognizer(newgrammar, 'book the') #should return False
f2 = CKYRecognizer(newgrammar, 'flight through') #False
f3 = CKYRecognizer(newgrammar, 'flight through Houston') #False

t1 = CKYRecognizer(newgrammar, 'include this meal from Houston') #True
t2 =  CKYRecognizer(newgrammar, 'I prefer the money') #True
t3 =  CKYRecognizer(newgrammar, 'she prefer that book') #True
if not f1 and not f2 and not f3 and t1 and t2 and t3:
  print "All tests passed for CKY Recognizer \n"
else:
  print "what"

# Extra Credit: Add tests of CKYParse here.

print newgrammar
CKYParser(newgrammar,'book the flight through Houston') # Should return True!
f1 = CKYParser(newgrammar, 'book the') #should return False
f2 = CKYParser(newgrammar, 'flight through') #False
f3 = CKYParser(newgrammar, 'flight through Houston') #False

t1 = CKYParser(newgrammar, 'include this meal from Houston') #True
t2 = CKYParser(newgrammar, 'I prefer the money') #True
t3 = CKYParser(newgrammar, 'she prefer that book') #True
if not f1 and not f2 and not f3 and t1 and t2 and t3:
  print "All tests passed for CKY Parser \n"
'''




