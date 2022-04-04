import numpy
import statistics

CAND = 0  # subscript of list which represents the candidate
SCORE = 1  # subscript of list which represents the score of the candidate
PLACE = 2  # subscript of list which represents the ranking, lowest is best


def print_connections(names, c, voters, candidates):
    print("CONNECTIONS")
    for i in range(voters):
        print("%10s" % (names[i]), end=" ")
        for j in range(voters):
            print(c[i][j], end=' ')
        print()


def print_rankings(names, r, voters, candidates, ordered):
    print("CANDIDATE Rankings")
    for i in range(voters):
        # print("First choice for {} is {}".format(names[i], ordered[i][CAND]), end=" ")
        print(names[i], end=" ")
        for j in range(candidates):
            print(r[i][j], end='')
        print(" ORDER ", ordered[i])


def socwel(ordered, candidateRanking, winner):
    card_util = 0
    ord_util = 0
    for i in range(len(candidateRanking)):
        if winner == ordered[i][0]:
            card_util += 0
            ord_util += 0
        else:
            card_pref_first = candidateRanking[i][ordered[0][0] - 1][1]
            card_pref_winner = candidateRanking[i][winner - 1][1]
            card_util += abs(card_pref_first - card_pref_winner)
            ord_util_first = candidateRanking[i][ordered[0][0] - 1][2]
            loc_of_winner = candidateRanking[i][winner - 1][2]
            ord_util += abs(ord_util_first - loc_of_winner)
    card_util_round = round(card_util, 2)
    print("The Cardinal Utility of this Winner is: " + str(card_util_round))
    print("The Ordinal Utility of this Winner is: " + str(ord_util))
    return card_util_round


def rcv(ordered):
    ranks = numpy.array(ordered)
    loserlist = numpy.zeros(1)
    majority = 0
    for i in range(len(ordered[0])):
        currank = ranks[:, i]
        for l in loserlist:
            currank = currank[currank != l]
        cnt = numpy.bincount(currank)
        minimum = numpy.nonzero(cnt == cnt[numpy.nonzero(cnt)].min())[0][0]
        maxs = statistics.multimode(currank)
        if len(maxs) == 1:
            majority = (ranks[:, i] == maxs).sum()
        if len(maxs) == 1 and maxs not in loserlist and majority >= len(currank) / 2:
            winner = str(maxs[0])
            print("The Winner is Candidate: " + winner)
            return int(maxs[0])
        else:
            if i + 1 == len(ordered[0]):
                winner = str(maxs[0])
                print("The Winner is Candidate: " + winner)
                return int(maxs[0])
            loserlist = numpy.append(loserlist, minimum)
            loser = str(minimum)
            print("Candidate " + loser + " was eliminated.")


def create_voting(voters, candidates):
    names = ["Alice ", "Bart  ", "Cindy ", "Darin ", "Elmer ", "Finn  ", "Greg  ", "Hank  ", "Ian   ", "Jim   ",
             "Kate  ", "Linc  ", "Mary  ", "Nancy ", "Owen  ", "Peter ", "Quinn ", "Ross  ", "Sandy ", "Tom   ",
             "Ursula", "Van   ", "Wendy ", "Xavier", "Yan   ", "Zach  "]

    connections = [[0 for i in range(voters)] for j in range(voters)]
    ordered = [[] for i in range(voters)]
    numpy.random.seed(1052)
    for i in range(voters):
        conn = round(numpy.random.uniform(0, voters / 2))
        for j in range(conn):
            connectTo = numpy.random.randint(0, voters)
            if (connectTo != i):
                connections[i][connectTo] = 1
    print_connections(names, connections, voters, candidates)
    candidateRanking = [[list() for i in range(candidates)] for j in range(voters)]
    for i in range(voters):
        for j in range(candidates):
            candidateRanking[i][j] = [j + 1, round(numpy.random.uniform(0, 100)) / 10, 0]
        print(candidateRanking[i])
        s = sorted(candidateRanking[i], reverse=True, key=lambda v: v[SCORE])
        ordered[i] = [s[i][CAND] for i in range(candidates)]
        for v in range(candidates):
            candidate = s[v][CAND] - 1  # which candidate has rank v+1
            candidateRanking[i][candidate][PLACE] = v + 1
    print_rankings(names, candidateRanking, voters, candidates, ordered)
    winner = rcv(ordered)
    socwel(ordered, candidateRanking, winner)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_voting(10, 10)
