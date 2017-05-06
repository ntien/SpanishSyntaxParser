toy = {'S':[['NP','VP'],['Aux','NP','VP'],['VP']], 'NP':[['Pronoun'],['Proper-Noun'],['Det','Nominal']], 'Nominal':[['Noun'],['Nominal','Noun'],['Nominal','PP']], 'VP':[['Verb'],['Verb','NP'],['Verb','NP','PP'],['Verb','PP'],['VP','PP']], 'PP':[['Preposition','NP']], 'Det':[['that'], ['this'], ['the'], ['a']], 'Noun':[['book'], ['flight'], ['meal'], ['money']], 'Verb':[['book'], ['include'],['prefer']], 'Pronoun':[['I'], ['she'], ['me']], 'Proper-Noun':[['Houston'], ['TWA']], 'Aux':[['does']], 'Preposition':[['from'], ['to'], ['on'], ['near'], ['through']]} # my version - all rhs values are lists of lists (each list being a rule)

# type of toyProbs: dict [ tuple[string, tuple[string] ] => float ]
toyProbs = { ('S',  ('NP', 'VP') ): .31, \
             ('S',  ('Aux', 'NP', 'VP') ): .29, \
             ('S',  ('VP',) ): .4, \
             ('NP', ('Pronoun',) ) : .36, \
             ('NP', ('Proper-Noun',) ) : .34, \
             ('NP', ('Det', 'Nominal') ) : .3, \
             ('Nominal', ('Noun',) ) : .31, \
             ('Nominal', ('Nominal', 'Noun') ) : .34, \
             ('Nominal', ('Nominal', 'PP') ) : .35, \
             ('VP', ('Verb',) ) : .19, \
             ('VP', ('Verb', 'NP') ) : .21, \
             ('VP', ('Verb', 'NP', 'PP') ) : .18, \
             ('VP', ('Verb', 'PP') ) : .22, \
             ('VP', ('VP', 'PP') ) : .2, \
             ('PP', ('Preposition', 'NP') ) : 1.0, \
             ('Det', ('that',) ) : .26, \
             ('Det', ('this',) ) : .23, \
             ('Det', ('the',) ) : .27, \
             ('Det', ('a',) ) : .24, \
             ('Noun', ('book',) ) : .26, \
             ('Noun', ('flight',) ) : .23, \
             ('Noun', ('meal',) ) : .27, \
             ('Noun', ('money',) ) : .24, \
             ('Verb', ('book',) ) : .35, \
             ('Verb', ('include',) ) : .33, \
             ('Verb', ('prefer',) ) : .32, \
             ('Pronoun', ('I',) ) : .35, \
             ('Pronoun', ('she',) ) : .33, \
             ('Pronoun', ('me',) ) : .32, \
             ('Aux', ('does',) ) : 1.0, \
             ('Proper-Noun', ('Houston',) ) : .4, \
             ('Proper-Noun', ('TWA',) ) : .6, \
             ('Preposition', ('from',) ) : .19, \
             ('Preposition', ('to',) ) : .21, \
             ('Preposition', ('on',) ) : .18, \
             ('Preposition', ('near',) ) : .22, \
             ('Preposition', ('through',) ) : .2 \
           }

toy2 = {'S':[['NP','VP'],['Aux','NP','VP'],['VP']], 'NP':[['Pronoun'],['Proper-Noun'],['Det','Nominal']], 'Nominal':[['Noun', 'stealer'], ['Noun'],['Nominal','Noun'],['Nominal','PP']], 'VP':[['Verb'],['Verb','NP'],['Verb','NP','PP'],['Verb','PP'],['VP','PP']], 'PP':[['Preposition','NP']], 'Det':[['that'], ['this'], ['the'], ['a']], 'Noun':[['book'], ['flight'], ['meal'], ['money']], 'Verb':[['book'], ['include'],['prefer']], 'Pronoun':[['I'], ['she'], ['me']], 'Proper-Noun':[['Houston'], ['TWA']], 'Aux':[['does']], 'Preposition':[['from'], ['to'], ['on'], ['near'], ['through']]} # my version - all rhs values are lists of lists (each list being a rule)

# type of toyProbs: dict [ tuple[string, tuple[string] ] => float ]
toyProbs2 = { ('S',  ('NP', 'VP') ): .31, \
             ('S',  ('Aux', 'NP', 'VP') ): .29, \
             ('S',  ('VP',) ): .4, \
             ('NP', ('Pronoun',) ) : .36, \
             ('NP', ('Proper-Noun',) ) : .34, \
             ('NP', ('Det', 'Nominal') ) : .3, \
             ('Nominal', ('Noun', 'stealer') ) : .1, \
             ('Nominal', ('Noun',) ) : .29, \
             ('Nominal', ('Nominal', 'Noun') ) : .31, \
             ('Nominal', ('Nominal', 'PP') ) : .3, \
             ('VP', ('Verb',) ) : .19, \
             ('VP', ('Verb', 'NP') ) : .21, \
             ('VP', ('Verb', 'NP', 'PP') ) : .18, \
             ('VP', ('Verb', 'PP') ) : .22, \
             ('VP', ('VP', 'PP') ) : .2, \
             ('PP', ('Preposition', 'NP') ) : 1.0, \
             ('Det', ('that',) ) : .26, \
             ('Det', ('this',) ) : .23, \
             ('Det', ('the',) ) : .27, \
             ('Det', ('a',) ) : .24, \
             ('Noun', ('book',) ) : .26, \
             ('Noun', ('flight',) ) : .23, \
             ('Noun', ('meal',) ) : .27, \
             ('Noun', ('money',) ) : .24, \
             ('Verb', ('book',) ) : .35, \
             ('Verb', ('include',) ) : .33, \
             ('Verb', ('prefer',) ) : .32, \
             ('Pronoun', ('I',) ) : .35, \
             ('Pronoun', ('she',) ) : .33, \
             ('Pronoun', ('me',) ) : .32, \
             ('Aux', ('does',) ) : 1.0, \
             ('Proper-Noun', ('Houston',) ) : .4, \
             ('Proper-Noun', ('TWA',) ) : .6, \
             ('Preposition', ('from',) ) : .19, \
             ('Preposition', ('to',) ) : .21, \
             ('Preposition', ('on',) ) : .18, \
             ('Preposition', ('near',) ) : .22, \
             ('Preposition', ('through',) ) : .2 \
           }

### For testing to make sure I filled out the whole grammar/probs combo correctly
# for key in toy:
#   for rule in toy[key]:
#     theProb = toyProbs[ ( key, tuple(rule) ) ]
#     print "probability of " + str(key) + " => " + str(rule) + " : " + str(theProb)
# 
# sum1 = 0
# for key in toy:
#   for rule in toy[key]:
#     sum1 += 1
# 
# sum2 = 0
# for key in toyProbs:
#   sum2 += 1
# 
# print sum1 == sum2
