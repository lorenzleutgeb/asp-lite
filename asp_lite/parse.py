from .constants import *

def keepSpaces(s):
    def f(acc, x):
        if x == '' and acc != []:
            acc[-1] += ' '
        else:
            acc.append(x)
        return acc

    return reduce(f, s.split(' '), [])

def atomize(s):
    s = keepSpaces(s)
    dneg = s[0] == 'not'
    if len(s) - dneg == 1:
        return ('not ' if dneg else '') + s[dneg]
    return ('not ' if dneg else '') + s[dneg] + '(' + ','.join(s[dneg + 1:]) + ')'

def ignore(ln):
    return len(ln) < 2 or ln[0] != tab

def isBody(ln):
    return len(ln) > 0 and ln[0] == tab
