import nltk
from nltk.corpus import cess_esp as cess

sents = cess.parsed_sents()
grammar = {}
probs = {}

def addrule(tree, leaves):
  if tree[0] not in leaves:
    lhs = tree.label()
    rhs = tuple(t.label() for t in tree)
    rhs2 = [t.label() for t in tree]
    if lhs in grammar:
      grammar[lhs].append(rhs2)
      if rhs in probs[lhs]:
        probs[lhs][rhs] +=1
      else:
        probs[lhs][rhs] = 1

    else:
      probs[lhs] = {}
      probs[lhs][rhs] = 1
      grammar[lhs] = [rhs2]
    for subtree in tree:
      addrule(subtree, leaves)

for t in sents:
  l = t.leaves()
  addrule(t, l)


with open("grammar.txt", "w") as f:
  f.write(repr(grammar))

with open("probs.txt", "w") as f:
  f.write(repr(probs))


