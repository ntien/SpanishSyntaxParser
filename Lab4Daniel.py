# Name: Daniel Washburn
import copy
from collections import deque


terminals = set(['that','this','a','book','flight','meal','money','include','prefer','I','she','me','Houston','TWA','does','from','to','on','near','through','test','the'])
terminals_CI = {x.lower() for x in terminals}

nonterminals = set(['S','NP','Nominal','VP','PP','Det','Noun','Verb','Pronoun','Proper-Noun','Aux','Preposition'])
nonterminals_CI = {x.lower() for x in nonterminals}

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

# grammar =  {'S':[['NP','VP'],['Aux','NP','VP'],['VP']],'NP':[['Pronoun'],['Proper-Noun'],['Det','Nominal']],'Nominal':[['Noun'],['Nominal','Noun'],['Nominal','PP']],'VP':[['Verb'],['Verb','NP'],['Verb','NP','PP'],['Verb','PP'],['VP','PP']],'PP':[['Preposition','NP']],'Det':['that','this','a'],'Noun':['book','flight','meal','money'],'Verb':['book','include','prefer'],'Pronoun':['I','she','me'],'Proper-Noun':['Houston','TWA'],'Aux':['does'],'Preposition':['from','to','on','near','through']} # original version
grammar = {'S':[['NP','VP'],['Aux','NP','VP'],['VP']], 'NP':[['Pronoun'],['Proper-Noun'],['Det','Nominal']], 'Nominal':[['Noun'],['Nominal','Noun'],['Nominal','PP']], 'VP':[['Verb'],['Verb','NP'],['Verb','NP','PP'],['Verb','PP'],['VP','PP']], 'PP':[['Preposition','NP']], 'Det':[['that'], ['this'], ['the'], ['a']], 'Noun':[['book'], ['flight'], ['meal'], ['money']], 'Verb':[['book'], ['include'],['prefer']], 'Pronoun':[['I'], ['she'], ['me']], 'Proper-Noun':[['Houston'], ['TWA']], 'Aux':[['does']], 'Preposition':[['from'], ['to'], ['on'], ['near'], ['through']]} # my version - all rhs values are lists of lists (each list being a rule)
# also added the word "the" to the determiners


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
                #if not bool:
                #    print "wrong: unit production"
                #    print "offending rule:   " + str(rule)
            if not bool:
                return bool 
    return True


# Takes in a grammar (in the given dictionary format), and modifies it to get 
#   rid of rules that mix terminals and nonterminals.
# Does not return anything - it modifies the given grammar.
def convertMixedRules(g):
    for left_side in g:
        rule_list = g[left_side]
        for rule in rule_list:
            if len(rule) > 1:
                for i in range(len(rule)):
                    if rule[i] in terminals:
                        dummy = rule[i] + "_dummy"
                        g[dummy] = rule[i]
                        rule[i] = dummy


# Takes a grammar in the dictionary format and returns a list of tuples, each representing the start and end of a chain of unit productions - so if we have A -> B and B -> C, it should return [('A', 'B'), ('B', 'C'), ('A', 'C')]
def findUnitProductionChains(g):
    unitChains = set([])
    for left_side in g:
        #print "loop1"
        rule_list = g[left_side]
        for rule in rule_list:
            if (len(rule) == 1) and (rule[0] in nonterminals): # string comparison
                unitChains.add( (left_side, rule[0]) )
    foundSome = True
    while foundSome:
        #print "loop2"
        foundSome = False
        newOnes = set([])
        for pair in unitChains:
            #print "loop3"
            #print pair
            A, B = pair
            for rule in g[B]:
                #print B + " -> " + str(rule)
                if (len(rule) == 1) and (rule[0] in nonterminals): # string comparison
                    #print "got here"
                    new = (A, rule[0])
                    #print new
                    #print (new not in unitChains)
                    if (new not in unitChains) and (new not in newOnes): # string comparison
                        #print "got here22222"
                        newOnes.add( new )
                        foundSome = True
        unitChains.update(newOnes) # same as `unitChains = unitChains.union(newOnes)` or `unitChains = (unitChains | newOnes)`, but faster
    return unitChains


# Takes in a grammar (in the given dictionary format), and modifies it to get 
#   rid of unit productions.
# Does not return anything - it modifies the given grammar.    
def removeUnitProductions(g):
    unitChains = findUnitProductionChains(g)
    for pair in unitChains:
        A, B = pair
        for rule in g[B]:
            g[A].append(rule)
        g[A].remove([B])


# Takes a single "long" rule: lhs is the nonterminal on the left-hand-side, rhs is the right-hand-side of the rule, and returns a suitable set of replacement rules in CNF, as tuples (i.e., expandRule("Z", ["A", "B", "C", "D"]) -> [("Z", ["A", "X1"]), ("X1", ["B", "X2"]), ("X2", ["C", "D"])]
def expandRule(lhs, rhs):
    newRules = []
    prev = lhs
    for i in range(0, len(rhs)-2): # we assume that rhs is at least length 3, or else this function shouldn't be called
        nextName = getNewName()
        newRules.append( (prev, [rhs[i], nextName]) )
        prev = nextName
        
    newRules.append( (prev, [rhs[len(rhs)-2], rhs[len(rhs)-1]]) )
    return newRules


# Remove and replace "long" rules (more than 3 nondeterminals on the right hand side) with equivalent sequences of shorter ones. Takes a grammar and modifies it - does not return anything.
def removeLongRules(g):
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
        replacement = expandRule(lhs, rhs)
        for newPair in replacement:
            newLHS, newRHS = newPair
            if newLHS in g:
                g[newLHS].append(newRHS)
            else:
                g[newLHS] = [newRHS]

                
# This function takes a grammar and returns an equivalent grammar in Chomsky Normal Form
def ConvertToCNF(g):
    g = copy.deepcopy(g)
    convertMixedRules(g)
    removeUnitProductions(g)
    removeLongRules(g)
    
    return g


# Just grabbed my tokenizer from lab 3 - takes a string and returns a list of strings, each a word (or punctuation)
punctuationEtc = ['.', "(", ")", "--", ",", ":", "n't"]
def containsPunct(string):
    for punc in punctuationEtc:
        if punc in string: # string comparison
            return True
    return False
def punctContained(string):
    for punc in punctuationEtc:
        if punc in string: # string comparison
            return punc
    return False
def tokenize(text):
    draft = deque(text.split()) # O(1) append/pop from both ends - efficient stack/queue
    ret = []
    while len(draft) > 0:
        word = draft.popleft()
        if containsPunct(word):
            #print("THE WORD: " + word)
            punc = punctContained(word)
            #print("THE PUNCTATION: " + punc)
            if word == punc: # string comparison
                ret.append(word)
            else:
                index = word.find(punc)
                lastPart = word.split(punc, 1)[1] # split once at the first period found, and return part after the period
                middle = punc
                firstPart = word[:index] # everything before the period
                if punc == '.': # string comparison
                    if lastPart == '': # final period (at the end of a word), i.e. to end a sentence # string comparison
                        draft.appendleft(punc)
                        draft.appendleft(firstPart)
                    else:
                        ret.append(word)
                else:
                    if lastPart != '':
                        draft.appendleft(lastPart) # push back onto the stack (there may be more punctuation in this token)
                    draft.appendleft(middle)
                    if firstPart != '':
                        draft.appendleft(firstPart)
        else: # plain word w/o punctuation in it
            ret.append(word)
    return ret

    
# This function takes a grammar and a string and returns True if that grammar generates that string, False otherwise. 
def CKYRecognizer(g,s):
    words = tokenize(s)
    cols_count = len(words) + 1
    rows_count = cols_count
    table = [[set([]) for x in range(cols_count)] for x in range(rows_count)]
    for j in range(1, len(words)+1):
        # fill in every POS that word j could be
        for left_side in g:
            rule_list = g[left_side]
            if ([words[j-1]] in rule_list) or ([words[j-1].lower()] in rule_list): # string comparison ???
                table[j-1][j].add(left_side)
        
        for i in range(j-2, -1, -1):         # j-2 (inclusive) down to -1 (exclusive), i.e., j-2 (inlusive) down to 0 (inclusive)
            for k in range(i+1, j):          # normal - i+1 (inclusive) to j (exclusive), which is i+1 (inclusive) to (j-1) inclusive)
                for B in table[i][k]:
                    for C in table[k][j]:
                        for A in g:
                            if [B, C] in g[A]: # string comparison ???
                                table[i][j].add(A)
    #print table

    return 'S' in table[0][len(words)] # string comparison
    #return table



# Extra Credit (optional): Modify your CKYRecognizer function to instead return a valid parse of the string, if one exists.
def CKYParser(g,s):

    # Fill in your algorithm here

    return []  # Placeholder

######
testg1 = {'S':[['NP','VP'], ['Aux','VP'], ['VP','NP']]} # should be true
testg2 = {'S':[['book'], ['flight'], ['that']]} # should be true
testg3 = {'S':[['book'], ['Aux','VP']]} # should be true

testg4 = {'S':[['NP','VP'], ['Aux'], ['VP','NP']]} # should be false (unit production)
testg5 = {'S':[['book'], ['Nominal']]} # should be false (unit production)
testg6 = {'S':[['NP','VP'],['Aux','NP','VP']]} # should be false (long rule)
testg7 = {'S':[['NP','VP'],['Aux','NP','VP'],['VP']]} # should be false (long rule, unit production)
testg8 = {'S':[['NP','VP'],['Aux','book']]} # should be false (mixed nonterminals and terminals)
###### Demonstrations

print InCNF(grammar) # Should return False!

newgrammar = ConvertToCNF(grammar)

print newgrammar

print InCNF(newgrammar) # Should return True!

print CKYRecognizer(newgrammar,'Book the flight through Houston') # Should return True!

# Add more tests of CKYRecognizer here.

print "more CKYRecognizer tests:"
print CKYRecognizer(newgrammar, 'Houston through the flight book') # should return False!
print CKYRecognizer(newgrammar, 'Book') # should return True!
print CKYRecognizer(newgrammar, 'Does the flight through Houston include the money') # should return True!
print CKYRecognizer(newgrammar, 'Does the flight through Houston include') # should return True!
print CKYRecognizer(newgrammar, 'the flight through Houston') # should return False!
print CKYRecognizer(newgrammar, 'include the flight through Houston') # should return True!
print CKYRecognizer(newgrammar, 'flight through Houston include the money') # should return False!
print CKYRecognizer(newgrammar, 'Does the flight') # should return False!
print CKYRecognizer(newgrammar, 'Book that money') # should return True!
print CKYRecognizer(newgrammar, 'Money that book') # should return False!



# Extra Credit: Add tests of CKYParse here.






