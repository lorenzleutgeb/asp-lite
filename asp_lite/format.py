from functools import reduce
from sys       import stdin, stdout
from itertools import combinations

import networkx as nx
from networkx.algorithms.dag import lexicographical_topological_sort

from .constants import *
from .parse     import *

def uniq(xs):
    prio = {}
    res = []
    for x in xs:
        if x not in prio:
            res.append(x)
            prio[x] = len(res) + 1
    return (res, prio)

def flatten(xs):
    return reduce(lambda x, y: x + [y] if type(y) != list else x + y, xs, [])

def project(i, xs):
    return list(map(lambda x: x[i], xs))

def bare(xs):
    return list(map(lambda x: x.strip(), xs))

def plain(w, head, body):
    if head != []:
        w(tab + ' | '.join([('-' if cneg else '') + pred + ('' if terms == [] else ' ' + ' '.join(terms)) for (cneg, pred, terms) in head]) + lf)
    if body != []:
        w(lf.join([
                tab * indent +
                ('not ' if dneg else '') +
                ('-' if cneg else '') +
                predicate +
                ('' if terms == [] else ' ' + ' '.join(terms))
            for (indent, dneg, cneg, predicate, terms) in body
        ]))

def emit(w, skip, head, body):
    if not(not skip and len(body) > 1):
        plain(w, head, body)
        return

    mkDneg = ' ' * len('not ') if not skip and any(project(1, body)) else ''
    mkCneg = ' ' * len('-') if not skip and any(project(2, body)) else ''
    body = list(map(lambda x: (x[0], x[1], x[2], x[3].strip(), bare(x[4])), body))
    offset = max(map(len, project(3, body)))

    g = nx.DiGraph()

    prio = []
    head = list(head)
    if head != []:
        lastHead = head[-1]
        prio = [bare(lastHead[2])]
        offset = max(offset, len(lastHead[1]) - tablen)
        g.add_edges_from(zip(lastHead[2], lastHead[2][1:]))

    # Establish some order for incomparable sets.
    lex, prio = uniq(flatten(prio + list(sorted(map(bare, project(4, body)), key=len, reverse=True))))

    for _, _, _, _, terms in body:
        if len(terms) == 1:
            g.add_node(terms[0])
        else:
            g.add_edges_from(zip(terms, terms[1:]))

    def foo(x):
        if not x in prio:
            return None
        return prio[x]

    if len(lex) > 1:
        try:
            lex = list(lexicographical_topological_sort(g))#, key=prio.get))
        except nx.exception.NetworkXUnfeasible:
            # we're fine with that...
            print('DANGER')
            ''

    print(tab + tab + ' ' + ' ' * offset + ' '.join(lex))

    g = nx.DiGraph()

    # Generate nodes for all sets of variables.
    for atom in body:
        bareVars = map(lambda y: y.strip(), atom[4])
        ts = list(set(list(bareVars)[:]))
        # Attention, we destroy the order of the terms here!
        ts.sort()
        ts = tuple(ts)
        if ts in g:
            g.node[ts]['atoms'].append(atom)
        else:
            g.add_node(ts, atoms=[atom])

    for u, v in combinations(g, 2):
        # If u is a superset of v, then u should come earlier in the topo.
        if set(v).issubset(set(u)):
            g.add_edge(u, v)

    if head != []:
        w(tab + ' | '.join([('-' if cneg else '') + pred + ('' if terms == [] else ' ' + ' '.join(terms)) for (cneg, pred, terms) in head]) + lf)

    atoms = nx.get_node_attributes(g, 'atoms')
    for v in lexicographical_topological_sort(g, key=lambda x: lex.index(x[0]) if len(x) > 0 else 0):
        for (indent, dneg, cneg, predicate, terms) in atoms[v]:
            w(
                tab * indent +
                ('not ' if dneg else mkDneg) +
                ('-' if cneg else mkCneg) +
                predicate.ljust(offset,' ') +
                ('' if terms == [] else ' ' + ' '.join(terms)) +
                lf
            )

def ingest(atom, dneg=False):
    ln = keepSpaces(atom.strip())
    xdneg = ln[0] == 'not' and dneg
    ln = ln[xdneg:]
    cneg = ln[0][0] == '-'
    result = (cneg, ln[0][cneg:], ln[1:])
    return (xdneg, *result) if dneg else result

def format(src, dst):
    w = dst.write

    head = []
    body = []
    skip = False

    for ln in src:
        bk = ln
        if ignore(ln):
            emit(w, skip, head, body)
            if body != []:
                w(lf)

            head, body = [], []

            w(ln)
            continue

        # Strip first tab.
        ln = ln[1:]

        if isBody(ln):
            ln = ln[1:]

            indentation = 2
            while ln[0] == tab:
                indentation += 1
                ln = ln[1:]

            if indentation > 2:
                #print('Skipping for aggregate!')
                skip = True

            ln = ln.strip()

            # TODO: This breaks for quoted strings (there might be a space in a quoted string).
            #ln = list(filter(len, ln.split(' ')))
            body.append((indentation, *ingest(ln, True)))
        else:
            emit(w, skip, head, body)

            skip = False
            body = []

            ln = ln.strip()

            # TODO: This breaks for string literals g(there may be a pipe in  a string literal).
            ln = ln.split('|')

            if len(ln) > 1:
                skip = True

            head = map(ingest, ln)

if __name__ == '__main__':
    _format(stdin, stdout)
