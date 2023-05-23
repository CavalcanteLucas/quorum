import pandas as pd
from vote_type import VoteType
from loaded_data_frames import (
    bills_df,
    legislators_df,
    vote_results_df,
    votes_df,
)

if __name__ == "__main__":

    bills = [
        {
            "id": str(row["id"]),
            "title": str(row["title"]),
            "sponsor_id": str(row["sponsor_id"]),
        }
        for _, row in bills_df.iterrows()
    ]

    legislators = [
        {
            "id": str(row["id"]),
            "name": str(row["name"]),
        }
        for _, row in legislators_df.iterrows()
    ]

    vote_results = [
        {
            "id": str(row["id"]),
            "legislator_id": str(row["legislator_id"]),
            "vote_id": str(row["vote_id"]),
            "vote_type": str(row["vote_type"]),
        }
        for _, row in vote_results_df.iterrows()
    ]

    votes = [
        {
            "id": str(row["id"]),
            "bill_id": str(row["bill_id"]),
        }
        for _, row in votes_df.iterrows()
    ]

    # print(bills)
    # print(legislators)
    # print(vote_results)
    # print(votes)

    # First deliverable

    legislators_vote_count_list = []
    for legislator in legislators:
        legislators_vote_count_list.append(
            {
                "legislator_id": legislator["id"],
                "name": legislator["name"],
                "num_supported_bills": 0,
                "num_opposed_bills": 0,
            }
        )

    legislators_vote_count_df = pd.DataFrame(legislators_vote_count_list)

    for vote_result in vote_results:
        if vote_result["vote_type"] == VoteType.SUPPORT.value:
            legislators_vote_count_df.loc[
                legislators_vote_count_df["legislator_id"] == vote_result["legislator_id"],
                "num_supported_bills",
            ] += 1
        if vote_result["vote_type"] == VoteType.OPPOSE.value:
            legislators_vote_count_df.loc[
                legislators_vote_count_df["legislator_id"] == vote_result["legislator_id"],
                "num_opposed_bills",
            ] += 1

    # print(legislators_vote_count_df)
    # save_csv_file(legislators_vote_count_df, LEGISLATOR_VOTE_COUNT_FILE)

    # Second deliverable

    def get_bill_sponsor_name(bill_sponsor_id, legislators):
        for legislator in legislators:
            if legislator["id"] == bill_sponsor_id:
                return legislator["name"]

    bills_vote_count_list = []
    for bill in bills:
        bills_vote_count_list.append(
            {
                "bill_id": bill["id"],
                "title": bill["title"],
                "supporter_count": 0,
                "opposer_count": 0,
                "primary_sponsor": get_bill_sponsor_name(bill["sponsor_id"], legislators),
            }
        )

    bills_vote_count_df = pd.DataFrame(bills_vote_count_list)

    def get_bill_id(vote_id, votes):
        for vote in votes:
            if vote_id == vote["id"]:
                return vote["bill_id"]

    for vote_result in vote_results:
        if vote_result["vote_type"] == VoteType.SUPPORT.value:
            bills_vote_count_df.loc[
                bills_vote_count_df["bill_id"] == get_bill_id(vote_result["vote_id"], votes), "supporter_count"
            ] += 1
        if vote_result["vote_type"] == VoteType.OPPOSE.value:
            bills_vote_count_df.loc[
                bills_vote_count_df["bill_id"] == get_bill_id(vote_result["vote_id"], votes), "opposer_count"
            ] += 1

    # print(bills_vote_count_df)
    # save_csv_file(bills_vote_count_df, BILLS_VOTE_COUNT_FILE)
