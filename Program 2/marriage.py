"""
Demo of Gale-Shapley stable marriage algorithm.
Written by Michael Goldwasser
Modifed by Vicki Allan

Usage is:
   python marriage.py  [menfile]  [womenfile]

or   

   python marriage.py  [menfile]  [womenfile]  V

for verbose mode.

If you want the women to propose, simply run:
   python marriage.py  [womenfile]  [menfile]

For simplicity, the file format is assumed (without checking) to match
the following format:

  bob:     alice,carol
  david:   carol,alice

and likewise for the womenfile,  and the identifiers should be
self-consistent between the two files.
If a partner is unacceptable, it is not listed in the preferences.

"""
import sys


class Person:
    """
    Represent a generic person
    """

    def __init__(self, name, priorities):
        """
        name is a string which uniquely identifies this person

        priorities is a list of strings which specifies a ranking of all
          potential partners, from best to worst
        """
        self.name = name
        self.priorities = priorities
        self.partner = None
        self.rank = None

    def __repr__(self):
        return 'Name is ' + self.name + '\n' + \
               'Partner is currently ' + str(self.partner) + str(self.rank) + '\n' + \
               'priority list is ' + str(self.priorities)


class Man(Person):
    """
    Represents a man
    """

    def __init__(self, name, priorities):
        """
        name is a string which uniquely identifies this person

        priorities is a list of strings which specifies a ranking of all
          potential partners, from best to worst
        """
        Person.__init__(self, name, priorities)
        self.proposalIndex = 0  # next person in our list to whom we might propose

    def nextProposal(self):
        if self.proposalIndex >= len(self.priorities):
            print('returned None')
            return None
        goal = self.priorities[self.proposalIndex]
        self.proposalIndex += 1
        return goal

    def __repr__(self):
        return Person.__repr__(self) + '\n' + \
               'next proposal would be to person a position ' + str(self.proposalIndex)


class Woman(Person):
    """
    Represents a woman
    """

    def __init__(self, name, priorities):
        """
        name is a string which uniquely identifies this person

        priorities is a list of strings which specifies a ranking of all
          potential partners, from best to worst
        """
        Person.__init__(self, name, priorities)

        # now compute a reverse lookup for efficient candidate rating
        self.ranking = {}
        for rank in range(len(priorities)):
            self.ranking[priorities[rank]] = rank

    def evaluateProposal(self, suitor):
        """
        Evaluates a proposal, though does not enact it.

        suitor is the string identifier for the man who is proposing

        returns True if proposal should be accepted, False otherwise
        """
        if suitor in self.ranking:
            if self.partner == None or self.ranking[suitor] < self.ranking[self.partner]:
                self.rank = self.ranking[suitor] + 1
                return True
            else:
                return False
        else:
            return False


def parseFile(filename):
    """
    Returns a list of (name,priority) pairs.
    """
    people = []
    # f = file(filename)
    with open(filename) as f:
        for line in f:
            pieces = line.split(':')
            name = pieces[0].strip()
            if name:
                priorities = pieces[1].strip().split(',')
                for i in range(len(priorities)):
                    priorities[i] = priorities[i].strip()
                people.append((name, priorities))
        f.close()
    return people


def calcHappiness(men, totalHappines=0):
    for man in men.values():
        if man.partner:
            totalHappines += man.rank
    return totalHappines


def printPairings(men, women):
    # print(women)
    for man in men.values():
        # print(man)
        print(man.name, 'is paired with', str(man.partner), end='')
        if man.partner:
            print(' rank ', man.rank, ' rank :', women[str(man.partner)].rank)
        else:
            print()


if __name__ == "__main__":
    verbose = len(sys.argv) > 3

    # initialize dictionary of men
    menlist = parseFile(sys.argv[1])
    men = dict()
    for person in menlist:
        men[person[0]] = Man(person[0], person[1])
    unwedMen = list(men.keys())

    # initialize dictionary of women
    womenlist = parseFile(sys.argv[2])
    women = dict()
    for person in womenlist:
        women[person[0]] = Woman(person[0], person[1])

    ############################### the real algorithm ##################################
    while len(unwedMen) > 0:
        print(unwedMen)
        m = men[unwedMen[0]]  # pick arbitrary unwed man
        n = m.nextProposal()
        if n is None:
            print('No more options ' + str(m))
            unwedMen.pop(0)
            continue
        w = women[n]  # identify highest-rank woman to which
        #    m has not yet proposed
        if verbose:  print(m.name, 'proposes to', w.name)

        if w.evaluateProposal(m.name):
            if verbose: print('  ', w.name, 'accepts the proposal')

            if w.partner:
                # previous partner is getting dumped
                mOld = men[w.partner]
                mOld.partner = None
                unwedMen.append(mOld.name)

            unwedMen.pop(0)
            w.partner = m.name
            m.partner = w.name
            m.rank = m.proposalIndex
        else:
            if verbose: print('  ', w.name, 'rejects the proposal')

        if verbose:
            print("Tentative Pairings are as follows:")
            printPairings(men, women)

    # we should be done
    print("Final Pairings are as follows:")
    printPairings(men, women)
    print("Total Male Happiness: ", calcHappiness(men))
    print("Total Female Happiness: ", calcHappiness(women))
