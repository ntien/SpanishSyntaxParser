# Name: Nora Tien
from __future__ import division
grammar = {'S':[['NP','VP'],['Aux','NP','VP'],['VP']],'NP':[['Pronoun'],['Proper-Noun'],['Det','Nominal']],'Nominal':[['Noun'],['Nominal','Noun'],['Nominal','PP']],'VP':[['Verb'],['Verb','NP'],['Verb','NP','PP'],['Verb','PP'],['VP','PP']],'PP':[['Preposition','NP']],'Det':['that','this','a', 'the'],'Noun':['book','flight','meal','money'],'Verb':['book','include','prefer'],'Pronoun':['I','she','me'],'Proper-Noun':['Houston','TWA'],'Aux':['does'],'Preposition':['from','to','on','near','through']}

# This function determines whether a grammar is in Chomsky Normal Form
def InCNF(g):
    # Fill in your algorithm here
    nonterminals = g.keys()
    for key in g:
      RHS = g[key]
      if any(isinstance(i, list) for i in RHS):
        #nested lists, more than one RHS rule
        for rule in RHS:
          if not checkRule(rule, nonterminals):
            return False
      else:
        if not checkRule(RHS, nonterminals):
          return False

    return True # Placeholder

#this function takes a particular RHS of a rule and checks if it is in CNF, and takes the list of nonterminals in the grammar
#returns True if grammar is in CNF, false otherwise
def checkRule(rule, nonterminals):
  nonterminals = set(nonterminals)
  l = len(rule)
  nont = [token for token in rule if token in nonterminals]
  ll = len(nont)
  if (l != ll and ll != 0) or (l == ll and l > 2) or (l == ll and l < 2):
    return False
  return True

# This function takes a grammar and returns an equivalent grammar in Chomsky Normal Form

def ConvertToCNF(g, old):
    new = {}
    if InCNF(g):
      return g
    else:
      for key in g:
        nonterminals = old.keys() + g.keys() + new.keys()
        RHS = g[key]
        #if there is more than one RHS rule
        if any(isinstance(i, list) for i in RHS):
          for i,rule in enumerate(RHS):
            if not checkRule(rule, nonterminals):
              new = update(key, rule, new, old, nonterminals)
            else:
              if key in new:
                if rule not in new[key]:
                  new[key].append(rule)
              else:
                new[key] = [rule]
        else:
          if not checkRule(RHS, nonterminals):
            new = update(key, RHS, new, old, nonterminals)
          else:
            if key in new:
              new[key].append(RHS)
            else:
              new[key] = RHS
      return new

#after identifying a rule not in CNF, this function updates the grammar to include a CNF version of that rule and returns the updated grammar
#it takes as input the left hand side of the rule, the right hand side of the rule, the new grammar (the one being updated to be in CNF), the old grammar (possibly not in CNF, and a list of terminals
def update(LHS, RHS, new, old, nonterminals):
 #more than two nonterminals or more than two nonterminals and terminals
  if len(RHS) > 2:
    first, second = RHS[0], RHS[1]
    newrule = first + "_" + second
    new[newrule] = [[first, second]]
    newRHS = [newrule] + RHS[2:]
    if len(newRHS) > 2:
      update(LHS, newRHS, new, old, nonterminals)
    else:
      if LHS in new:
        new[LHS].append(newRHS)
      else:
        new[LHS] = newRHS
      return new
  else:
    if len(RHS) == 2:
      first, second = RHS[0], RHS[1]
      if LHS in new:
        new[LHS].append([first, second])
      else:
        new[LHS] = [[first, second]]
      return new
    else:
    #only one thing (must be nonterminal)
      newRHS = old[RHS[0]]
      if LHS in new:
       new[LHS] = new[LHS] + newRHS
      else:
        new[LHS] = newRHS
      second2 = True
      return ConvertToCNF(new, old)

def CKYRecognizer(g,s):
  s = s.split()
  rev = [(value, tup[0]) for tup in g.items() for value in tup[1]]
  table = [[[] for j in range(len(s)+1)] for i in range(len(s))]
  #add the LHS of all the rules that go to word[j] in the grammar
  for j in range(1,len(s)+1):
    lhs = [tup[1] for tup in rev if tup[0] == s[j-1]]
    table[j-1][j] = lhs
    for i in range(j-2, -1, -1):
      for k in range(i+1, j):
        cc = table[k][j]
        bb = table[i][k]
        for b in bb:
          for c in cc:
            lhs = list(set([tup[1] for tup in rev if tup[0] == ([b, c])]))
            for l in lhs:
              if l:
                table[i][j] = list(set(table[i][j] + [l]))
  if "S" in set(table[0][-1]):
    return True
  else:
    return False


# Extra Credit (optional): Modify your CKYRecognizer function to instead return a valid parse of the string, if one exists.


#grammar is of form
#probability is product of probs * probability of rule
def CKYParser(g,probs, s):
  ss = s
  s = s.split()
  rev = [(value, tup[0]) for tup in g.items() for value in tup[1]]
  table = [[[] for j in range(len(s)+1)] for i in range(len(s))]
  parseTable = [[[] for j in range(len(s)+1)] for i in range(len(s))]
  probTable = [[[] for j in range(len(s)+1)] for i in range(len(s))]
  #add the LHS of all the rules that go to word[j] in the grammar
  for j in range(1,len(s)+1):
    lhs = [tup[1] for tup in rev if tup[0] == s[j-1]]
    word = s[j-1]
    p = [(rule, probs[(rule, word)]) for rule in lhs]
    table[j-1][j] = lhs
    parseTable[j-1][j] = (lhs, word)
    probTable[j-1][j] = (p, word)
    for i in range(j-2, -1, -1):
      for k in range(i+1, j):
        bb = table[i][k]
        cc = table[k][j]
        bbp = probTable[i][k]
        ccp = probTable[k][j]
        if bbp:
          if len(bbp) > 1:
            if type(bbp[1]) == type("string"):
              bbp = bbp[0]
        if ccp:
          if len(ccp) > 1:
            if type(ccp[1]) == type("string"):
              ccp = ccp[0]
        for bp in bbp:
          for cp in ccp:
            plhs = []
            for tup in rev:
              if len(bp) > 0 and len(cp) > 0:
                if tup[0] == [bp[0], cp[0]]:
                  product = bp[1] * cp[1] * probs[(tup[1], (bp[0], cp[0]))]
                  plhs.append((tup[1], product))
            if len(plhs) > 0:
              for pl in plhs:
                if len(pl) > 0:
                  probTable[i][j] = list(set(probTable[i][j] + [(pl[0], pl[1], (k, j), (i, k))]))
        for b in bb:
          for c in cc:
            #want to include k,j and i,k as pointers
            lhs = [tup[1] for tup in rev if tup[0] == ([b, c])]
            for l in lhs:
              if l:
                table[i][j] = list(set(table[i][j] + [l]))
                parseTable[i][j] = list(set(parseTable[i][j] + [(l, (k, j),(i,k))]))

  if "S" in table[0][-1]:
    parses = [rule for rule in parseTable[0][-1] if rule[0] == "S"]
    trees = [getParse(parseTable, s,g, True, "") for s in parses]
    parse = sorted([rule for rule in probTable[0][-1] if rule[0] == "S"], key=lambda x: x[1])[-1]
    trees2 = getMostProbableParse(probTable, parse, g, True, "", probs)
    print trees2
    return True
  else:
    return False

def getMostProbableParse(table, start, grammar, startsymbol, terminal, probs):
    #base case: we reached a POS with no indices
    if type(start) == type("string"):
      return [terminal]
    if len(start) < 3:
      return [terminal]
    i = start[3][0]
    j = start[2][1]
    k = start[2][0]
    ruledown = table[k][j]
    ruleleft = table[i][k]
    product = start[1] #from this, and probs dict, should be able to find rule

    if not ruleleft or not ruledown:
      return [start[0]]
    else:
      parses = []
      terminaldown = False
      terminalleft = False
      worddown = ""
      wordleft = ""
      if type(ruledown[-1]) == type("string"):
        terminaldown = True
        worddown = ruledown[-1]
        ruledown = ruledown[:-1][0]
      if type(ruleleft[-1]) == type("string"):
        terminalleft = True
        wordleft = ruleleft[-1]
        ruleleft = ruleleft[:-1][0]

      for rd in ruledown:
        for rl in ruleleft:
          rule1 = rl
          rule2 = rd
          if type(rule1) != type("str"):
            rule1 = rl[0]
          if type(rule2) != type("str"):
            rule2 = rd[0]
          p1 = rd[1]
          p2 = rl[1]
          lhs = start[0]
          #check to see if this rule should be expanded (did it actually come from start?
          RHS = grammar[start[0]]
          thisRHS = [rule1, rule2]
          if thisRHS in RHS:
            p = p1 * p2 * probs[(lhs, (rule1, rule2))]
            if p == product:
              if startsymbol:
                parses.append([[product] + [start[0]] + [[rule1] + [rule2] + [getMostProbableParse(table, rl, grammar, False, wordleft, probs) + getMostProbableParse(table, rd, grammar, False, worddown, probs)]]])
              else:
                parses.append([[rule1] + [rule2] + [getMostProbableParse(table, rl, grammar, False, wordleft, probs) + getMostProbableParse(table, rd, grammar, False, worddown, probs)]])
      return parses


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


# Demonstrations
#print InCNF(grammar) # Should return False!
import random
newgrammar = ConvertToCNF(grammar, grammar)
probs = {}
for key in newgrammar:
  RHS = newgrammar[key]
  if any(isinstance(i, list) for i in RHS) or len(RHS) > 1:
    for rule in newgrammar[key]:
      if type(rule) == type('string'):
        rule = (rule)
      else:
        rule = tuple(rule)
      probs[(key, rule)] = random.randint(1,10)/10
  else:
    probs[(key, tuple(RHS))] = random.randint(1,10)/10

#print InCNF(newgrammar) # Should return True!
#print CKYRecognizer(newgrammar,'book the flight through Houston') # Should return True!

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
'''
CKYParser(newgrammar, probs, 'book the flight through Houston') # Should return True!
'''
f1 = CKYParser(newgrammar, 'book the') #should return False
f2 = CKYParser(newgrammar, 'flight through') #False
f3 = CKYParser(newgrammar, 'flight through Houston') #False

t1 = CKYParser(newgrammar, 'include this meal from Houston') #True
t2 = CKYParser(newgrammar, 'I prefer the money') #True
t3 = CKYParser(newgrammar, 'she prefer that book') #True
if not f1 and not f2 and not f3 and t1 and t2 and t3:
  print "All tests passed for CKY Parser \n"

'''



