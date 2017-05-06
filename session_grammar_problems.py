import parse

# this is a part of speech - it maps to something that is techically a list of 
#   lists of strings, but it's not a proper rule, just a word spilt into a list of letters
parse.newgrammar[u'px2fs0s0']
# Let's grab some other parts of speech that are of the same type
px_poses = [x for x in parse.newgrammar.keys() if 'px' in x]
# here they are
px_poses
# ... and they all map to the same messed-up-word bullshit. Some of them have two messed-up-words
for pos in px_poses:
   print parse.newgrammar[pos]
# if we go find these rules in probs, at first they look fine (no fucked-up words), 
#   but you can see that what should be a tuple of strings on the right-hand-side 
#   of the rule (which is part of the tuple key for probs) is just a single string
[x for x in parse.probs.keys() if x[0] in px_poses]
# If we go looking for all rules in probs that have this format (right-hand-side of rule is not a tuple), there are fucktons of them, and they all seem to be of the form (part-of-speech, word)
[x for x in parse.probs.keys() if type(x[1]) != type( (1,2) )]
