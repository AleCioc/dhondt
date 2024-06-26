import pandas as pd
import streamlit as st

st.title("Calcolo seggi")


def dhondt(nSeats, votes, verbose=False):
    """
    nSeats is the number of seats
    votes is a dictionary with the key:value {'party':votes}
    verbose is an option to print designation info
    """

    t_votes = votes.copy()
    seats = {}

    for key in votes:
        seats[key] = 0

    # with st.expander("Dhondt procedimento completo"):

    while sum(seats.values()) < nSeats:
        max_v = max(t_votes.values())
        next_seat = list(t_votes.keys())[list(t_votes.values()).index(max_v)]
        if next_seat in seats:
            seats[next_seat] += 1
        else:
            seats[next_seat] = 1

        if verbose:
            print("Seggio {}: {}".format(sum(seats.values()), next_seat))
            for key in t_votes:
                print("\t{} [{}]: {:.1f}".format(key,seats[key], t_votes[key]))
            print("\b")

        t_votes[next_seat] = votes[next_seat]/(seats[next_seat]+1)

    return seats


votes_dict = {

    "FDI": 2600,
    "XBENE": 2900,
    "FORZAITALIA": 2600,
    "MASTRANGELO": 1500,

    "PD": 1300,
    "BOTTEGA": 1100,
    "PROCINO": 600,

    "PRODIGIO": 800,
    "M5S": 600,

}


votes_dict = pd.Series(votes_dict, name="n_voti")

st.header("Liste")

cols = st.columns((1, 1, 1))

cols[0].subheader("Imposta voti")
votes_dict = cols[0].data_editor(votes_dict)
cols[0].write(f"Tot voti: {votes_dict.sum()}")


coalitions_dict = {
    "CENTRODESTRA": ["FDI", "XBENE", "FORZAITALIA", "MASTRANGELO"],
    "CENTROSINISTRA": ["PD", "BOTTEGA", "PROCINO"],
    "CENTRO": ["PRODIGIO", "M5S"],
}

coalitions_votes = {}
for c in coalitions_dict:
    coalitions_votes[c] = 0
    for l in coalitions_dict[c]:
        coalitions_votes[c] += votes_dict[l]

dhont_results_coalizioni = dhondt(nSeats=16, votes=coalitions_votes, verbose=True)

dhont_results_by_list = dict()
for coalizione in coalitions_dict:
    votes_coalizione_by_list = {k: votes_dict[k] for k in votes_dict.index if k in coalitions_dict[coalizione]}
    _dhont_results_by_list = dhondt(
        nSeats=dhont_results_coalizioni[coalizione],
        votes=votes_coalizione_by_list,
        verbose=True
    )
    dhont_results_by_list = dhont_results_by_list | _dhont_results_by_list


cols[1].subheader("Percentuali")
cols[1].dataframe(
    (((pd.Series(votes_dict) / pd.Series(votes_dict).sum()) * 100).round(2).astype(str) + " %").rename(
        "%_voti"
    )
)

cols[2].subheader("Seggi")
cols[2].write(pd.Series(dhont_results_by_list, name="n_seggi"))
sum_seats = pd.Series(dhont_results_by_list).sum()
cols[2].write(f"Tot seggi: {sum_seats}")

st.header("Coalizioni")

cols = st.columns((1, 1, 1))

cols[0].subheader("Voti")
cols[0].dataframe(pd.Series(coalitions_votes, name="n_voti"))
tot_votes = pd.Series(coalitions_votes).sum()
cols[0].write(f"Tot seggi: {tot_votes}")


cols[1].subheader("Percentuali")
cols[1].dataframe(
    (((pd.Series(coalitions_votes) / pd.Series(coalitions_votes).sum()) * 100).round(2).astype(str) + " %").rename(
        "%_voti"
    )
)

cols[2].subheader("Seggi")
cols[2].dataframe(pd.Series(dhont_results_coalizioni, name="n_seggi"))
tot_seats = pd.Series(dhont_results_coalizioni).sum()
cols[2].write(f"Tot seggi: {tot_seats}")

