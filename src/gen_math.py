#!/usr/bin/env python
import sys
from random import randint, choice

def rand_op():
    ops = ['+','-']
    return choice(ops)

def gen_math_prob():
    min = 1
    max = 20
    terms = 5
    if terms == 0:
        return ""
    prob = str(randint(min, max))
    for i in range(terms-1):
        prob+=' '+rand_op()+' '+str(randint(min,max))
    return prob

if __name__ == '__main__':
    filename = 'questions.txt'
    if len(sys.argv)>2:
        filename = sys.argv[2]
    outfile = open(filename, 'w')
    n = int(sys.argv[1])
    lines = []
    for i in range(n):
        new_prob = gen_math_prob()
        lines.append(new_prob+'\n\n')
        lines.append(str(eval(new_prob))+'\n\n')
    outfile.writelines(lines)
    outfile.close()
        
