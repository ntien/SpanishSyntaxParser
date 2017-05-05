from __future__ import division

grammar = {}
with open("probs.txt","r") as f:
  x = f.read()
  grammar = eval(x)

probs = {}
newgrammar = {}

for key in grammar:
  RHS = grammar[key]
  total = sum(RHS.values())
  for rule in RHS:
    probs[key, rule] = RHS[rule]/total
  newgrammar[key] = RHS.keys()
  break

print newgrammar
print probs

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




