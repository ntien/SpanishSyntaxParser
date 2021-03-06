import nltk
from nltk.corpus import cess_esp as cess

sents = cess.parsed_sents()

test = False
some_sents = [sents[1]] + [sents[12]] + [sents[15]] + sents[19:26]
easy_sent = sents[20]
#sents = [easy_sent]
#sents = some_sents

def print_sent(sent):
    for word in sent.leaves():
        print word,

grammar = {}
probs = {}
terminals = {}

def addrule(tree, leaves):
  if tree[0] not in leaves:
    lhs = tree.label()
    rhs = tuple(t.label() for t in tree)
    if type(rhs) != type( (1,2) ):
      print "not tuple:", rhs
    rhs2 = [t.label() for t in tree]
    if lhs in grammar:
      grammar[lhs].append(rhs2)
      if rhs in probs[lhs]:
        probs[lhs][rhs] +=1
      else:
        probs[lhs][rhs] = 1

    else:
      if type(lhs) == type((1,2)):
        print lhs
      probs[lhs] = {}
      probs[lhs][rhs] = 1
      grammar[lhs] = [rhs2]
    for subtree in tree:
      addrule(subtree, leaves)
  else:
    terminal = (tree[0],) # syntax for 1-tuple is (object,) not (object)
    #terminal = (tree[0])
    terminal2 = [tree[0]]
    if type(terminal) != type( (1,2) ):
      print "not tuple:" + terminal
    pos = tree.label()
    pos1 = (pos)
    pos2 = [pos]
    if pos in grammar:
      if type(pos) == type((1,2)):
        print pos
      grammar[pos].append(terminal2)
      if terminal in probs[pos]:
        probs[pos][terminal] += 1
      else:
        probs[pos][terminal] = 1
    else:
      grammar[pos] = [terminal2]
      if type(pos) == type((1,2)):
        print pos
      probs[pos] = {}
      probs[pos][terminal] = 1

    if terminal in terminals:
      if pos1 in terminals[terminal]:
        terminals[terminal][pos1] += 1
      else:
        terminals[terminal][pos1] = 1
    else:
      terminals[terminal] = {}
      terminals[terminal][pos1] = 1


for t in sents:
  l = t.leaves()
  addrule(t, l)

fname1 = "grammar.txt"
fname2 = "probs.txt"
fname3 = "terminalprobs.txt"
if test:
    fname1 = "test" + fname1
    fname2 = "test" + fname2
    fname3 = "test" + fname3
with open(fname1, "w") as f:
  f.write(repr(grammar))

with open(fname2, "w") as f:
  f.write(repr(probs))

with open(fname3,"w") as f:
  f.write(repr(terminals))
