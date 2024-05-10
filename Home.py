import pandas as pd
import streamlit as st

st.title("Calcolo seggi")

def dhont(nSeats, votes, verbose=False):
    """
    nSeats is the number of seats
    votes is a dictionary with the key:value {'party':votes}
    verbose is an option to print designation info
    """
    t_votes=votes.copy()
    seats={}
    for key in votes: seats[key]=0
    while sum(seats.values()) < nSeats:
        max_v= max(t_votes.values())
        next_seat=list(t_votes.keys())[list(t_votes.values()).index(max_v)]
        if next_seat in seats:
            seats[next_seat]+=1
        else:
            seats[next_seat]=1

        if verbose:
            print("{} Escaño: {}".format(sum(seats.values()),next_seat))
            for key in t_votes:
                print("\t{} [{}]: {:.1f}".format(key,seats[key],t_votes[key]))
            print("\b")
        t_votes[next_seat]=votes[next_seat]/(seats[next_seat]+1)
    return seats

votes_dict = {

    "FDI": 2500,
    "XBENE": 2900,
    "FORZAITALIA": 2600,
    "MASTRANGELO": 1545,

    "PD": 1400,
    "BOTTEGA": 1200,
    "PROCINO": 400,

    "PRODIGIO": 800,
    "M5S": 400,

}


votes_dict = pd.Series(votes_dict)

cols = st.columns((1, 1))
cols[0].subheader("Imposta numero voti")
cols[0].experimental_data_editor(votes_dict)

coalitions_dict = {
    "CENTRODESTRA": ["FDI", "XBENE", "FORZAITALIA", "MASTRANGELO"],
    "CENTROSINISTRA": ["PD", "BOTTEGA", "PROCINO"],
    "M5S": ["PRODIGIO", "M5S"],

}

coalitions_votes = {}
for c in coalitions_dict:
    coalitions_votes[c] = 0
    for l in coalitions_dict[c]:
        coalitions_votes[c] += votes_dict[l]

dhont_results = dhont(nSeats=16, votes=votes_dict.to_dict(), verbose=False)
cols[1].subheader("Seggi assegnati")
cols[1].write(dhont_results)

cols = st.columns((1, 1, 1))

cols[0].subheader("Percentuali liste")
cols[0].dataframe(
    ((pd.Series(votes_dict) / pd.Series(votes_dict).sum()) * 100).round(2).astype(str) + " %"
)

cols[1].subheader("Voti coalizione")
cols[1].dataframe(pd.Series(coalitions_votes))

cols[2].subheader("Percentuali")
cols[2].dataframe(
    ((pd.Series(coalitions_votes) / pd.Series(coalitions_votes).sum()) * 100).round(2).astype(str) + " %"
)
