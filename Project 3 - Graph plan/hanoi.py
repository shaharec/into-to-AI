"""
Maman 15
Student: Shahar Cohen.
ID: 313566077
"""

def createDomainFile(domainFileName, n):
  numbers = list(range(n)) # [0,...,n-1]
  pegs = ['a','b', 'c']
  domainFile = open(domainFileName, 'w') #use domainFile.write(str) to write to domainFile
  "*** YOUR CODE HERE ***"
  writeProp(domainFile, numbers, pegs,n)
  writeActions(domainFile, numbers, pegs,n)
  domainFile.close()  
        
  
def createProblemFile(problemFileName, n):
  numbers = list(range(n)) # [0,...,n-1]
  pegs = ['a','b', 'c']
  problemFile = open(problemFileName, 'w') #use problemFile.write(str) to write to problemFile
  "*** YOUR CODE HERE ***"
  problemFile.write("Initial state: ")
  # Put all disc in the same peg
  for disc in range(n-1):
    # Add disc on disc attribute
    problemFile.write(discOnDisc(disc, disc + 1))

  # First disc and bottom disc
  problemFile.write(discTopPre(0,pegs[0])+discbottomPeg(n-1,pegs[0]))

  # Two pegs are empty
  problemFile.write(emptyPeg(pegs[1])+emptyPeg(pegs[2])+'\n')

  # Write goal state
  problemFile.write("Goal state: ")
  for disc in range(n-1):
    # Add disc on disc attribute
    problemFile.write(discOnDisc(disc, disc + 1))

  # First disc and bottom disc
  problemFile.write(discTopPre(0, pegs[1]) + discbottomPeg(n - 1, pegs[1]))

  # Other pegs are empty
  problemFile.write(emptyPeg(pegs[0]) + emptyPeg(pegs[2]))

  problemFile.close()

def writeProp(domainFile, nRange, pegs,n):
  """
  Write Propositions with range of n discs
   and pegs to domainFile
  """
  domainFile.write("Propositions:\n")
  for peg in pegs:
    for disc in nRange:
      domainFile.write(discTopPre(disc,peg)) # disc on top of peg
      domainFile.write(discbottomPeg(disc,peg))  # disc on bottom of peg
    domainFile.write(emptyPeg(peg)) # add empty pegs
  # Add disc on disc
  for disc1 in nRange:
    for disc2 in range(disc1+1,n):
      domainFile.write(discOnDisc(disc1,disc2)) # Disc on disc.
  domainFile.write("\n")

def discTopPre(disc,peg):
  """
  Return precondition disc on top of peg
  """
  return 'D'+str(disc)+'TP'+peg + ' '


def discbottomPeg(disc,peg):
  """
  Return precondition disc on bottom peg
  """
  return 'D' + str(disc) + 'BP' + peg + ' '

def emptyPeg(peg):
  """
  Return precondition of peg empty.
  """
  return "EP" + peg + ' '

def discOnDisc(disc1,disc2):
  """
  Return precondition of disc1 on disc2
  """
  return 'D' + str(disc1) + 'OND' + str(disc2) +' '



def writeActions(domainFile, nRange, pegs, n):
  """
  Write Actions to domainfile
  """
  domainFile.write("Actions:\n")
  for currPeg in pegs:
    for nextPeg in pegs:
      if currPeg != nextPeg:
        for disc1 in nRange:
          # Move bottom disc to empy peg
          name = getActionName(4, disc1, None, currPeg, nextPeg)
          pre = discTopPre(disc1, currPeg) + \
                discbottomPeg(disc1,currPeg)+ \
                emptyPeg(nextPeg)
          _del = discTopPre(disc1, currPeg) + \
                 discbottomPeg(disc1, currPeg) + \
                 emptyPeg(nextPeg)
          add = emptyPeg(currPeg) + \
                discTopPre(disc1, nextPeg) + \
                discbottomPeg(disc1, nextPeg)
          writeAction(name, pre, _del, add, domainFile)
          for disc2 in range(disc1+1,n):
            # Move disc1 on disc2  to empty peg
            name = getActionName(1, disc1, disc2, currPeg, nextPeg)
            pre  = discTopPre(disc1,currPeg)  +\
                   discOnDisc(disc1, disc2) +\
                   emptyPeg(nextPeg)
            _del = discTopPre(disc1,currPeg)  +\
                   discOnDisc(disc1, disc2) + \
                   emptyPeg(nextPeg)
            add =  discTopPre(disc1,nextPeg) +\
                   discTopPre(disc2,currPeg) + \
                   discbottomPeg(disc1,nextPeg)
            writeAction(name, pre, _del, add, domainFile)

            # Move disc1 from bottom to top of next peg that is not empty
            name = getActionName(2, disc1, disc2, currPeg, nextPeg)
            pre =  discTopPre(disc1, currPeg) +  \
                   discTopPre(disc2, nextPeg) + \
                   discbottomPeg(disc1, currPeg)
            _del = discTopPre(disc1, currPeg) + \
                   discTopPre(disc2, nextPeg)+\
                   discbottomPeg(disc1,currPeg)
            add =  discTopPre(disc1,nextPeg) + \
                   discOnDisc(disc1,disc2) + \
                   emptyPeg(currPeg)
            writeAction(name, pre, _del, add, domainFile)

            for disc3 in range(disc1+1,n):
              # Move disc1 on disc2 to top of next peg with top of disc3
              name = getActionName(3, disc1, disc2, currPeg, nextPeg, disc3)
              pre =  discTopPre(disc1, currPeg) +\
                     discOnDisc(disc1,disc2)+\
                     discTopPre(disc3,nextPeg)
              _del = discTopPre(disc1, currPeg) + \
                     discOnDisc(disc1,disc2) + \
                     discTopPre(disc3,nextPeg)
              add =  discTopPre(disc1, nextPeg) + \
                     discOnDisc(disc1, disc3) + \
                     discTopPre(disc2, currPeg)
              writeAction(name, pre, _del, add, domainFile)

def getActionName(type, disc1, disc2, peg1, peg2,disc3=None):
  """
  Return name of action by type:
  1. Move disc from non empty peg to empty peg
  2. Move disc1 from bottom to top of next peg that is not empty
  3. Move disc1 on disc2 to top of next peg with top of disc3
  """
  if type == 1:
    return 'M'+str(disc1)+'ON'+str(disc2)+'F'+peg1+'TO'+peg2
  if type == 2:
    return 'M'+str(disc1)+'FE'+peg1+'TO'+peg2+'OND'+str(disc2)
  if type == 3:
    return 'M'+str(disc1)+'ON'+str(disc2)+'FROM'+peg1+'TO'+peg2+'ON'+str(disc3)
  if type == 4:
    return 'M'+str(disc1)+'P'+peg1+'TE'+peg2

def writeAction(name, preProps, delProps, addProps, file):
  """
  Write single action to file
  """
  file.write("Name: " + name + "\n")
  file.write("pre: " + preProps + "\n")
  file.write("add: " + addProps + "\n")
  file.write("delete: " + delProps + "\n")

import sys
if __name__ == '__main__':
  if len(sys.argv) != 2:
    print('Usage: hanoi.py n')
    sys.exit(2)
  
  n = int(float(sys.argv[1])) #number of disks
  domainFileName = 'hanoi' + str(n) + 'Domain.txt'
  problemFileName = 'hanoi' + str(n) + 'Problem.txt'
  
  createDomainFile(domainFileName, n)
  createProblemFile(problemFileName, n)