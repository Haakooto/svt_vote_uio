import sys
import pyrankvote as prv


path = sys.argv[1]

try:
    spots = int(sys.argv[2])
except:
    spots = 1
candidates = {}
ballots = []


def get_votes(file):
    with open(path, "r") as file:
        lines = file.readlines()[1:]
    return lines


def get_names(line):
    names = []
    for word in line.strip().split():
        word = word.strip().replace(".", "")
        try:
            int(word)
        except:

            word = word.lower()
            if word not in ["sekunder", "minutter", "sekund", "minutt"]:
                if word not in names:  # stop double voting
                    names.append(word)
        else:
            continue
    return names


votes = get_votes(path)
for vote in votes:
    names = get_names(vote)
    ballot = []
    for name in names:
        name = name[0].upper() + name[1:]
        if name not in candidates:
            candidates[name] = prv.Candidate(name)
        ballot.append(candidates[name])
    ballots.append(prv.Ballot(ranked_candidates=ballot))

Candidates = [candidates[i] for i in candidates]
election = prv.single_transferable_vote(Candidates, ballots, spots)

if "show_all" in sys.argv:
    print(election)

elif "show_last" in sys.argv:
    print(f"Final result, last of {len(election.rounds) + 1} rounds")
    print(election.rounds[-1])

else:
    winners = election.get_winners()
    for winner in winners:
        print(winner)
