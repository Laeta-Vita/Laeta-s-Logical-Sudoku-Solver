
#   Laeta's Logical Sudoku Solver!   -   laeta@cox.net

from time import time
from copy import deepcopy
from itertools import product
from winsound import Beep

count = 0

#   data structures
pos = {i: {1, 2, 3, 4, 5, 6, 7, 8, 9} for i in range(81)}   #   remaining possibilities

row = {i: {i//9*9+j for j in range(9)} for i in range(81)}

col = {i: {j*9+i%9 for j in range(9)} for i in range(81)}

box = {i: {(i//9//3*3+j)*9+i%9//3*3+k for j,k in \
           product(range(3), range(3))} for i in range(81)}

peers = {i: row[i].union(col[i]).union(box[i]) for i in range(81)}

band = dict()
for i in range(81):
    if i//9%3 == 0: a, b = 9, 18
    elif i//9%3 == 1: a, b = -9, 9
    elif i//9%3 == 2: a, b = -18, -9
    band[i] = row[i].union(row[i+a]).union(row[i+b])

stack = dict()
for i in range(81):
    if i%9%3 == 0: a, b = 1, 2
    elif i%9%3 == 1: a, b = -1, 1
    elif i%9%3 == 2: a, b = -2, -1
    stack[i] = col[i].union(col[i+a]).union(col[i+b])

#   test cases
ez1 = list((0,0,2,0,0,6,0,0,0,0,0,0,0,2,0,9,0,4,0,0,4,0,0,0,0,0,0,
            0,0,0,8,0,0,0,0,0,5,0,0,0,0,0,0,0,2,0,8,0,0,4,9,0,5,3,  #   easy
            3,0,0,0,5,0,6,0,0,0,5,0,0,0,0,0,0,8,7,0,0,0,6,0,0,3,0))
ez2 = list((1,0,0,0,0,5,0,0,0,0,3,0,4,0,0,9,0,0,0,7,0,0,0,0,0,0,4,
            0,0,1,0,0,0,0,0,0,0,0,0,5,0,9,7,0,3,6,0,0,0,0,0,0,0,0,
            0,0,0,0,0,4,0,7,9,0,0,8,0,1,0,4,0,0,0,0,0,0,8,0,0,0,5))
ez3 = list((0,0,0,0,9,2,0,0,0,5,0,0,0,8,0,6,0,0,0,0,6,3,0,0,1,0,0,
            0,0,1,2,0,7,0,0,0,0,2,0,0,4,0,0,0,0,9,0,0,5,3,8,0,0,0,
            0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,9,7,7,0,8,0,0,0,0,0,3))
ez4 = list((0,2,3,0,0,0,0,0,7,0,6,0,0,0,1,0,0,0,0,7,0,6,0,0,0,5,0,
            0,0,6,3,0,4,0,0,0,0,0,8,0,0,0,5,0,0,0,0,0,0,9,0,2,0,0,
            3,0,0,0,0,5,0,0,9,0,0,9,4,0,0,0,3,0,0,0,0,0,0,0,0,4,0))
ez5 = list((0,5,7,9,0,0,0,0,0,0,9,0,0,0,0,0,0,4,2,0,0,0,0,0,0,0,6,
            0,0,0,0,0,9,0,7,0,0,3,0,7,0,0,0,8,0,0,1,0,0,3,0,9,6,0,
            0,0,0,0,2,4,0,5,0,0,0,3,0,0,0,0,0,0,0,0,0,0,6,8,0,0,0))
me1 = list((0,5,0,1,0,8,0,7,0,4,0,0,3,0,0,0,0,0,2,0,0,0,0,0,0,0,0,
            0,1,0,7,0,0,0,8,0,9,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,  #   medium
            0,3,0,0,0,0,0,1,0,0,0,0,0,4,0,2,0,0,0,0,0,0,5,0,6,0,0))
me2 = list((0,0,0,0,2,0,0,0,0,9,0,6,0,7,0,0,0,8,8,0,0,0,0,0,0,4,0,
            0,0,0,0,6,0,4,0,0,6,0,0,0,0,0,0,0,9,0,1,2,4,0,0,0,3,0,
            0,0,0,3,0,0,0,8,0,0,0,8,0,0,0,0,7,1,0,0,0,0,5,8,9,0,0))
me3 = list((0,4,0,3,0,0,0,0,0,0,0,0,0,0,0,0,7,8,0,0,0,0,0,0,0,5,0,
            7,0,0,6,5,0,0,0,0,5,0,0,0,9,0,0,0,0,0,1,0,0,0,0,2,0,0,
            0,0,0,1,0,4,3,0,0,8,0,0,0,0,0,0,0,6,0,0,0,2,0,0,0,0,0))
me4 = list((4,0,0,0,0,0,0,6,0,0,0,0,9,4,0,0,5,0,1,0,9,0,6,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,6,0,0,2,0,0,5,0,5,2,3,1,0,0,0,8,
            0,7,0,0,0,8,0,0,1,0,0,0,0,0,0,7,0,0,0,0,8,0,5,0,3,0,6))
me5 = list((0,5,0,0,0,0,4,6,0,0,0,0,0,9,0,0,0,0,0,0,3,0,8,0,2,0,0,
            0,0,0,0,5,1,0,0,0,0,0,1,3,4,0,5,8,0,0,4,6,0,0,0,0,0,0,
            0,0,0,1,0,0,0,0,0,4,0,0,0,0,0,8,0,9,7,0,0,0,0,0,0,1,0))
hd1 = list((5,0,0,0,0,0,0,0,9,0,2,0,1,0,0,0,7,0,0,0,8,0,0,0,3,0,0,
            0,4,0,0,0,1,0,0,0,0,0,0,4,9,2,0,0,0,0,0,0,7,0,0,0,1,0,  #   hard
            0,0,3,0,0,0,8,0,0,0,6,0,0,0,4,0,2,0,9,0,0,0,0,0,0,0,5))
hd2 = list((0,0,0,0,0,0,1,0,0,6,0,0,0,0,0,8,7,4,0,0,0,0,0,7,0,2,6,
            0,3,0,4,0,0,0,0,0,0,0,5,0,9,0,0,0,0,1,0,0,0,0,8,0,0,2,
            0,0,9,0,5,0,0,0,0,2,0,0,0,0,1,0,0,8,0,4,0,3,0,0,0,0,0))
hd3 = list((1,0,0,0,0,0,0,0,2,0,3,0,4,0,0,0,5,0,0,0,6,0,0,0,7,0,0,
            0,8,0,3,0,0,0,0,0,0,0,0,0,6,5,0,0,0,0,0,0,8,0,9,0,4,0,
            7,0,0,0,0,0,1,0,0,0,5,0,0,0,8,0,9,0,0,0,2,0,0,0,0,0,6))
hd4 = list((1,0,0,0,0,0,0,0,2,0,3,0,4,0,0,0,5,0,0,0,6,0,0,0,7,0,0,
            0,8,0,3,0,0,0,0,0,0,0,0,0,1,9,0,0,0,0,0,0,8,0,5,0,4,0,
            7,0,0,0,0,0,6,0,0,0,5,0,0,0,8,0,9,0,0,0,2,0,0,0,0,0,1))
hd5 = list((1,0,0,0,0,0,0,0,2,0,3,0,4,0,0,0,5,0,0,0,6,0,0,0,7,0,0,
            0,8,0,3,0,0,0,0,0,0,0,0,0,6,9,0,0,0,0,0,0,8,0,5,0,4,0,
            7,0,0,0,0,0,1,0,0,0,5,0,0,0,8,0,9,0,0,0,2,0,0,0,0,0,6))
ex1 = list((6,0,0,0,0,8,9,4,0,9,0,0,0,0,6,1,0,0,0,7,0,0,4,0,0,0,0,
            2,0,0,6,1,0,0,0,0,0,0,0,0,0,0,2,0,0,0,8,9,0,0,2,0,0,0,  #   extreme
            0,0,0,0,6,0,0,0,5,0,0,0,0,0,0,0,3,0,8,0,0,0,0,1,6,0,0))
nos = list((0,0,0,0,0,5,0,8,0,0,0,0,6,0,1,0,4,3,0,0,0,0,0,0,0,0,0,
            0,1,0,5,0,0,0,0,0,0,0,0,1,0,6,0,0,0,3,0,0,0,0,0,0,0,5,  #   no solution!
            5,3,0,0,0,0,0,6,1,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0))

new = list((0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,  #   blank
            0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0))

ez, nez = [ez1, ez2, ez3, ez4, ez5], ['ez1', 'ez2', 'ez3', 'ez4', 'ez5']
me, nme = [me1, me2, me3, me4, me5], ['me1', 'me2', 'me3', 'me4', 'me5']
hd, nhd = [hd1, hd2, hd3, hd4, hd5], ['hd1', 'hd2', 'hd3', 'hd4', 'hd5']
each, nea = ez + me + hd, nez + nme + nhd

def printgrid(grid):                                    #   print grid
    i = 0
    print()
    for j in range(i, i+9):
        print(f"\t    {grid[i]} {grid[i+1]} {grid[i+2]}" \
              f" | {grid[i+3]} {grid[i+4]} {grid[i+5]}" \
              f" | {grid[i+6]} {grid[i+7]} {grid[i+8]}")
        if i == 18 or i == 45: print("\t    ---------------------")
        i += 9
    print()

def index():                                            #   print grid indices
    grid = list()
    for i in range(81):
        if i < 10: grid.append(('0' + str(i)))
        else: grid.append(i)
    printgrid(grid)

def ask():                                              #   ask for user board
    grid = list()
    print()
    for i in range(1,10):
        while True:
            try:
                a = input(f"Please enter line {i} (0 for empty): ")
                if len(a) != 9: raise ValueError
                int(a)
            except: print("Oops! Try again...")
            else: break
        for j in a: grid.append(int(j))
    return grid

def allsearch(ogrid, c = 0):                            #   use all searches on 1 grid
    global count, pos
    a, b = 0, time()
    for i in range(1, 4):
        count, grid = 0, ogrid.copy()
        pos = {i: {1, 2, 3, 4, 5, 6, 7, 8, 9} for i in range(81)}
        prop(grid)
        start = time()
        if not solve(grid, i): print("\t\tNo solution!")
        a += count
        if c != 0: print(f" {c}) ", end = '')
        print(f"\t{i})\tcount = {count:,}\ttime = {time() - start:.3f}")
    print(f"\t   grid count = {a:,} \tgrid time = {time() - b:.3f}\n")
    return a

def searchall(search = 3):                              #   use 1 search on all grids
    global count, pos
    print()
    a, b = 0, time()
    for i in range(len(each)):
        count, grid = 0, each[i]
        pos = {i: {1, 2, 3, 4, 5, 6, 7, 8, 9} for i in range(81)}
        prop(grid)
        start = time()
        if not solve(grid, search): print("\t\tNo solution!")
        a += count
        print(f"\t{nea[i]})\tcount = {count:,}\ttime = {time() - start:.3f}")
    print(f"\n\t   grid count = {a:,} \tgrid time = {time() - b:.3f}\n")

def allsearchall():                                     #   use all searches on all grids
    print()
    a, start = 0, time()
    for i in range(len(each)):
        grid = each[i]
        print(f" {nea[i]}) ", end = '')
        a += allsearch(grid)
    print(f"\t  total count = {a:,}\ttotal time = {time() - start:.3f}\n")

def sortgrid(grid):                                     #   sort grid
    a = {i: [grid[j] for j in peers[i]].count(0) for i in range(81)}
    return [j[0] for j in sorted(a.items(), key=lambda x:x[1]) if j[1] > 1]

def sortpos():                                          #   sort possibilities
    a = {i: sum(len(pos[j]) for j in peers[i]) for i in range(81)}
    return [j[0] for j in sorted(a.items(), key=lambda x:x[1]) if j[1] > 9]

def dup(grid):                                          #   check for duplicate test case
    for i in range(len(each)):
        if grid == each[i]:
            print(f"\n\t{nea[i]} match!\n")
            return
    print("\n\tno match.\n")

def dupfile(grid):                                      #   check for duplicate in file
    a, b = 0, str()
    for i in grid: b += str(i)
    f = open("Laeta's Test Cases.txt")
    for i in f:
        a += 1
        if b == i.replace('.', '0').strip():
            print(f"\nDuplicate found on line {a}!\n")
            return
    print(f"\nNo duplicate found.\n")
    f.close()

def lenfile():
    f = open("Laeta's Test Cases.txt")
    a = 0
    for i in f: a += 1
    print(a)
    f.close

def write(e = 0):                                       #   write file
    global count, pos
    a, b, c, d, h, k = 0, time(), 0, [], 0, list()
    f = open("Laeta's Test Cases.txt")
    g = open("New Test Cases.txt", "a")
    if e == 1: d = range(1, 57)
    print()
    for i in f:
        c += 1
        if e == 0: d.append(c)
        if c in d:
            m, n = i.replace('.', '0').strip(), list()
            pos = {i: {1, 2, 3, 4, 5, 6, 7, 8, 9} for i in range(81)}
            for j in m: n.append(int(j))
            count = allsearch(n, c)
            a += count
            if count == 0: h += 1
            else: k.append((count, n))
    m = sorted(k)
    for i in m:
        n = str()
        for j in i[1]:
            n += str(j).replace('0', '.')
        n += "\n"
        g.write(n)
    print(f"\n\t  total count = {a:,} \ttotal time = {time() - b:.3f}\n")
    print(f"\t   ave. count = {a/(len(d)-h):.0f} \tave. time = {(time() - b)/(len(d)-h):.3f}\n")
    if h != 0: print(f"\t\t        solved: {h}\n")
    f.close()
    g.close()

def read(search = 3, e = 0):                            #   read file
    global count, pos
    a, b, c, d, h, fail = 0, time(), 0, [], 0, 0
    f = open("Laeta's Test Cases.txt")
    if e == 1: d = range(1, 46)
    elif e == 2: d = range(676,721)
    elif e == 3: d = range(1351, 1396)
    print()
    for i in f:
        c += 1
        if e == 0: d.append(c)
        if c in d:
            count, m, n = 0, i.replace('.', '0').strip(), list()
            pos = {i: {1, 2, 3, 4, 5, 6, 7, 8, 9} for i in range(81)}
            for j in m: n.append(int(j))
##            print()
##            for j in n: print(j, end=",")
##            print()
            prop(n)
            start = time()
            if not solve(n, search):
                print("\t\tNo solution!")
                fail += 1
            print(f"\t{c})\tcount = {count:,}\ttime = {time() - start:.3f}")
            a += count
            if count == 0: h += 1
    print(f"\n\t  total count = {a:,} \ttotal time = {time() - b:.3f}\n")
    print(f"\t   ave. count = {a/(len(d)-h):.0f} \tave. time = {(time() - b)/(len(d)-h):.3f}\n")
    if h != 0: print(f"\t\t        solved: {h}\n")
    if fail != 0: print(f"\t\t        failed: {fail}\n")
    f.close()

def prop(grid):                                         #   propagate information
    global pos
    change = False

    for i in range(81):                             #   read from grid to pos
        if grid[i] != 0 and len(pos[i]) != 1:
            for j in peers[i]: pos[j].discard(grid[i])
            pos[i], change = {grid[i]}, True

    while change:                                   #   propagate along pos
        change, start = False, deepcopy(pos)

        for i in range(81):                     #   singleton
            for j in peers[i]:
                if i != j and len(pos[i]) == 1: pos[j].difference_update(pos[i])

        for i in col[0]: rules(sorted(row[i]), i)
        for i in row[0]: rules(sorted(col[i]), i)
        for i in (0,3,6,27,30,33,54,57,60): rules(sorted(box[i]))

        for i in range(81):                     #   forward check
            if len(pos[i]) == 0: return False

        if pos != start: change = True

    for i in range(81):                             #   read from pos to grid
        if len(pos[i]) == 1 and grid[i] == 0:
            if list(pos[i])[0] not in [grid[j] for j in peers[i]]: grid[i] = list(pos[i])[0]
            else: return False
    return True

def rules(group, ii = -1):                              #   logic rules

    a = {i: {j for j in range(9) if i not in pos[group[j]]} for i in range(1,10)}
    for i in range(1, 10):                          #   void permutation
        b = {i}
        for j in range(i+1, 10):
            if a[i].issubset(a[j]): b.add(j)
        if len(b) == 9 - len(a[i]):
            for k in range(9):
                if k not in a[i]: pos[group[k]].intersection_update(b)

    if ii != -1:                                    #   void 2 of 3
        if group == sorted(row[ii]):
            if ii in (0,27,54): group2, group3 = sorted(row[ii+9]), sorted(row[ii+18])
            elif ii in (9, 36, 63): group2, group3 = sorted(row[ii-9]), sorted(row[ii+9])
            elif ii in (18, 45, 72): group2, group3 = sorted(row[ii-18]), sorted(row[ii-9])
        elif group == sorted(col[ii]):
            if ii in (0, 3, 6): group2, group3 = sorted(col[ii+1]), sorted(col[ii+2])
            elif ii in (1, 4, 7): group2, group3 = sorted(col[ii-1]), sorted(col[ii+1])
            elif ii in (2, 5, 8): group2, group3 = sorted(col[ii-2]), sorted(col[ii-1])

        a1, a2, a3 = set(), set(), set()
        for i in group[:3]: a1.update(pos[i])
        for i in group[3:6]: a2.update(pos[i])
        for i in group[6:]: a3.update(pos[i])

        b1, b2, b3 = set(), set(), set()
        for i in group2[:3]: b1.update(pos[i])
        for i in group2[3:6]: b2.update(pos[i])
        for i in group2[6:]: b3.update(pos[i])

        c1, c2, c3 = set(), set(), set()
        for i in group3[:3]: c1.update(pos[i])
        for i in group3[3:6]: c2.update(pos[i])
        for i in group3[6:]: c3.update(pos[i])

        for i in range(1, 10):
            if i not in b1 and i not in c1:
                for j in group[3:]: pos[j].discard(i)
            elif i not in b2 and i not in c2:
                for j in (0,1,2,6,7,8): pos[group[j]].discard(i)
            elif i not in b3 and i not in c3:
                for j in group[:6]: pos[j].discard(i)

            if i not in a2 and i not in a3:
                for j in group2[:3]: pos[j].discard(i)
                for j in group3[:3]: pos[j].discard(i)
            elif i not in a1 and i not in a3:
                for j in group2[3:6]: pos[j].discard(i)
                for j in group3[3:6]: pos[j].discard(i)
            elif i not in a1 and i not in a2:
                for j in group2[6:]: pos[j].discard(i)
                for j in group3[6:]: pos[j].discard(i)

    a = {i: [p for p in group if i in pos[p]] for i in range(1,10)}
    for i in a:                                     #   pair exclusion
        if len(a[i]) != 2: continue             #   1 pair - done by void 2 of 3

        p0 = {p for p in peers[a[i][0]] if i in pos[p] and p not in (a[i][0], a[i][1])}
        p1 = {p for p in peers[a[i][1]] if i in pos[p] and p not in (a[i][0], a[i][1])}
        for j, k in product(p0, p1):            #   2 pairs - x-wing
            if j in peers[k] and a[i][0] not in band[k] and a[i][0] not in stack[k]:
                b = {p for p in row[k] if i in pos[p]}
                if len(b) == 2 and j in b:  #   row
                    for p in col[a[i][0]].union(col[k]):
                            if p not in (a[i][0], a[i][1], j, k): pos[p].discard(i)
                b = {p for p in col[k] if i in pos[p]}
                if len(b) == 2 and j in b:  #   col
                        for p in row[a[i][0]].union(row[k]):
                            if p not in (a[i][0], a[i][1], j, k): pos[p].discard(i)
                                            #   box - done by void 2 of 3

            p2 = {p for p in peers[j] if i in pos[p] and p not in (a[i][0], a[i][1], j, k)}
            p3 = {p for p in peers[k] if i in pos[p] and p not in (a[i][0], a[i][1], j, k)}
            for l, m in product(p2, p3):        #   3 pairs - swordfish
                if l in peers[m] and j not in band[m] and j not in stack[m] and \
                   k not in band[l] and k not in stack[l]:
                    b, c, d, e, f = {a[i][0], a[i][1], j, k, l, m}, 0, 0, 0, 0
                    for g in b:
                        h = {p for p in row[g] if i in pos[p]}
                        if len(h) == 2 and len(b.intersection(h)) == 2: c += 1
                        if len(h) >= 2 and len(b.intersection(h)) == 2: d += 1
                        h = {p for p in col[g] if i in pos[p]}
                        if len(h) == 2 and len(b.intersection(h)) == 2: e += 1
                        if len(h) >= 2 and len(b.intersection(h)) == 2: f += 1
                    if c == 6 and f == 6:   #   row
                        for p in col[a[i][0]].union(col[a[i][1]]).union(col[j]) \
                            .union(col[k]).union(col[l]).union(col[m]):
                            if p not in b: pos[p].discard(i)
                    if e == 6 and d == 6:   #   col
                        for p in row[a[i][0]].union(row[a[i][1]]).union(row[j]) \
                            .union(row[k]).union(row[l]).union(row[m]):
                            if p not in b: pos[p].discard(i)

##                p4 = {p for p in peers[l] if i in pos[p] and p not in (a[i][0], a[i][1], j, k, l, m)}
##                p5 = {p for p in peers[m] if i in pos[p] and p not in (a[i][0], a[i][1], j, k, l, m)}
##                for n, o in product(p4, p5):    #   4 pairs - jellyfish
##                    if n in peers[o] and \
##                       a[i][0] not in peers[k] and a[i][0] not in peers[l] and \
##                       a[i][0] not in peers[m] and a[i][0] not in peers[n] and \
##                       a[i][0] not in peers[o] and a[i][1] not in peers[j] and \
##                       a[i][1] not in peers[l] and a[i][1] not in peers[m] and \
##                       a[i][1] not in peers[n] and a[i][1] not in peers[o] and \
##                       j not in peers[k] and j not in peers[m] and \
##                       j not in peers[n] and j not in peers[o] and \
##                       k not in peers[l] and k not in peers[n] and \
##                       k not in peers[o] and l not in peers[m] and \
##                       l not in peers[o] and m not in peers[n]:
##                        b, c, d, e, f = {a[i][0], a[i][1], j, k, l, m, n, o}, 0, 0, 0, 0
##                        for g in b:
##                            h = {p for p in row[g] if i in pos[p]}
##                            if len(h) == 2 and len(b.intersection(h)) == 2: c += 1
##                            if len(h) >= 2 and len(b.intersection(h)) == 2: d += 1
##                            h = {p for p in col[g] if i in pos[p]}
##                            if len(h) == 2 and len(b.intersection(h)) == 2: e += 1
##                            if len(h) >= 2 and len(b.intersection(h)) == 2: f += 1
##                        if c == 8 and f == 8:   #   row
##                            for p in col[a[i][0]].union(col[a[i][1]]).union(col[j]) \
##                                .union(col[k]).union(col[l]).union(col[m]).union(col[n]).union(col[o]):
##                                if p not in b: pos[p].discard(i)
##                        if e == 8 and d == 8:   #   col
##                            for p in row[a[i][0]].union(row[a[i][1]]).union(row[j]) \
##                                .union(row[k]).union(row[l]).union(row[m]).union(row[n]).union(row[o]):
##                                if p not in b: pos[p].discard(i)

    a, b = set(), set()                             #   chaining
    for i in (2, 3, 4):
        for j in group:
            if len(pos[j]) == i:
                a.update(pos[j])
                b.add(j)
        if len(a) == i + 1 and len(b) == i + 1:
            for j in group:
                if j not in b: pos[j].difference_update(a)

    a = {i: [j for j in group if i in pos[j]] for i in range(1,10)}
    for i in range(1,10):                           #   pair deduction
        if len(a[i]) != 2: continue
        b, c, q = [a[i][0]], list(), [a[i][0]]
        while len(q) != 0:
            d = q.pop(0)
            e = [j for j in row[d] if i in pos[j] and j != d]
            f = [j for j in col[d] if i in pos[j] and j != d]
            g = [j for j in box[d] if i in pos[j] and j != d]
            for j in (e, f, g):
                if len(j) == 1 and j[0] not in b and j[0] not in c:
                    if d in b: c.append(j[0])
                    else: b.append(j[0])
                    q.append(j[0])
        for j in (b, c):
            for k, l in product(j, j):
                if k != l and k in peers[l]:
                    for m in j: pos[m].discard(i)
                    if j == b:
                        for m in c: pos[m] = {i}
                    else:
                        for m in b: pos[m] = {i}

    for i, j in product(group, group):              #   hook
        if i not in box[j] and len(pos[i]) == 2 and len(pos[j]) == 2:
            a = pos[i].union(pos[j])
            if len(a) == 3:
                for k in a:
                    if k in pos[i] and k in pos[j]:
                        b, c = a.copy(), pos[j].copy()
                        b.discard(k)
                        c.discard(k)
                        c = c.pop()
                        for l in peers[i]:
                            if pos[l] == b and l not in group:
                                d, e = set(), set()
                                for m in peers[l]:
                                    if c in pos[m]: d.add(m)
                                for m in peers[j]:
                                    if c in pos[m]: e.add(m)
                                f = d.intersection(e)
                                for m in f: pos[m].discard(c)

def solve(grid, search = 3):                            #   recursive brute force
    global count, pos

    if 0 not in grid: return True                   #   base case

    if search == 1: search = range(81)              #   unsorted control
    elif search == 2: search = sortgrid(grid)       #   sorted grid
    elif search == 3: search = sortpos()            #   sorted possibilities
    for i in search:
        if grid[i] == 0:
            for j in sorted(pos[i]):
                if j not in {grid[k] for k in peers[i]}:
                    g, p, grid[i] = deepcopy(grid), deepcopy(pos), j
                    if not prop(grid):
                        grid, pos, grid[i] = g, p, 0
                        continue
                    count += 1
                    if solve(grid, search): return True
                    grid, pos, grid[i] = g, p, 0
            return False

#grid = ask()    #   ask user for grid
#grid = ez1      #   use test cases from the top

##prop(grid)
##start = time()
##if not solve(grid, 3): print("\n\t\tNo solution!")
##print(f"\n\tcount = {count:,}\ttime  = {time() - start:.3f}\n")

read(3, 0)      #   read file - 0 can be changed to 1-3 for just one page
#allsearch(grid) #   use all searches on 1 grid
#searchall(3)    #   use 1 search on all grids
#allsearchall()  #   use all searches on all grids

Beep(500, 500)


















