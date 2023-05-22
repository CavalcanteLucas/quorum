import os
from pathlib import Path
import pandas as pd
from enum import Enum
import logging
import argparse


PROVIDED_DATA_PATH = Path("provided_data")
DELIVERABLE_DATA_PATH = Path("deliverable_data")

class VoteType(Enum):
    """
    Enum for vote types.
    Assuming 'vote_type' 1 is support and 'vote_type' 2 is oppose.
    """

    SUPPORT = 1
    OPPOSE = 2


def load_csv_file(
    filename: str,
    data_path: Path = PROVIDED_DATA_PATH,
) -> pd.DataFrame:
    """Load data from csv file."""
    csv_path = os.path.join(data_path, filename)
    return pd.read_csv(csv_path)


def save_csv_file(
    result_df: pd.DataFrame,
    filename: str,
    data_path: Path = DELIVERABLE_DATA_PATH,
) -> None:
    """Save data to csv file."""
    target_path = os.path.join(data_path, filename)
    result_df.to_csv(target_path, index=False)
    logging.info(f" [x] CSV saved in {target_path}")



def get_legislator_vote_count(
    legislators_df: pd.DataFrame,
    vote_results_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    This method returns the first deliverable, which asks for the following:
        - For every legislator, how many bills did they support?
        - For every legislator, how many bills did they oppose?

    The answer is a dataframe with the columns "num_supported_bills" and
    "num_opposed_bills" added to the legislators dataframe. These columns contain
    the number of bills supported and opposed, respectively, by each legislator.
    """

    """
    SELECT legislator.id,
           legislator.name
           COUNT(CASE WHEN vote_results.vote_type = 1 THEN TRUE ELSE NULL END) as num_supported_bills,
           COUNT(CASE WHEN vote_results.vote_type = 2 THEN TRUE ELSE NULL END) as num_opposed_bills
    FROM legislators
LEFT JOIN vote_results ON vote_results.legislator_id = legislators.id
    GROUP BY legislator.id, legislator.name
    """

    vote_counts = (
        vote_results_df.groupby(
            [
                "legislator_id",
                "vote_type",
            ]
        )
        .size()
        .unstack(fill_value=0)
        .reset_index()
    ).rename(
        columns={
            VoteType.SUPPORT.value: "num_supported_bills",
            VoteType.OPPOSE.value: "num_opposed_bills",
        }
    )

    legislator_vote_count = (
        legislators_df.merge(
            vote_counts,
            left_on="id",
            right_on="legislator_id",
            how="left",
        )
        .drop(columns=["legislator_id"])
        .fillna(0)
    )

    return legislator_vote_count[
        [
            "id",
            "name",
            "num_supported_bills",
            "num_opposed_bills",
        ]
    ]


def get_bill_vote_counts(
    bills_df: pd.DataFrame,
    vote_results_df: pd.DataFrame,
    votes_df: pd.DataFrame,
    legislators_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    This method returns the second deliverable, which asks for the following:
        - For every bill, how many legislators supported it?
        - For every bill, how many legislators opposed it?
        - Who was the sponsor of the bill?

    The answer is a dataframe with the columns "supporter_count",
    "opposer_count", and "legislator_name" added to the bills dataframe.
    These columns contain the number of legislators who supported and opposed each
    bill, respectively, and the name of the legislator who sponsored the bill.
    """

    vote_counts = (
        vote_results_df.groupby(
            [
                "vote_id",
                "vote_type",
            ]
        )
        .size()
        .unstack(fill_value=0)
        .reset_index()
    ).rename(
        columns={
            VoteType.SUPPORT.value: "supporter_count",
            VoteType.OPPOSE.value: "opposer_count",
        }
    )

    bill_vote_counts = (
        votes_df.merge(
            vote_counts,
            left_on="id",
            right_on="vote_id",
        )
        .merge(
            bills_df,
            left_on="bill_id",
            right_on="id",
            how="right",
        )
        .merge(
            legislators_df,
            left_on="sponsor_id",
            right_on="id",
            how="left",
        )
        .drop(columns=["vote_id", "id_x", "id_y", "id"])
        .fillna("Unavailable")
        .drop(columns=["sponsor_id"])
    ).rename(
        columns={
            "name": "primary_sponsor",
            "bill_id": "id",
        }
    )

    # return bill_vote_counts
    return bill_vote_counts[
        [
            "id",
            "title",
            "supporter_count",
            "opposer_count",
            "primary_sponsor",
        ]
    ]


def main() -> None:
    # Setup file names
    # Provided data
    BILLS_FILE = "bills.csv"
    LEGISLATORS_FILE = "legislators.csv"
    VOTE_RESULTS_FILE = "vote_results.csv"
    VOTES_FILE = "votes.csv"
    # Deliverable data
    LEGISLATOR_VOTE_COUNT_FILE = "legislator_vote_count.csv"
    BILLS_VOTE_COUNT_FILE = "bills.csv"

    # Load data
    bills_df = load_csv_file(BILLS_FILE)
    legislators_df = load_csv_file(LEGISLATORS_FILE)
    vote_results_df = load_csv_file(VOTE_RESULTS_FILE)
    votes_df = load_csv_file(VOTES_FILE)

    # First deliverable
    legislator_vote_count_df = get_legislator_vote_count(legislators_df, vote_results_df)
    save_csv_file(legislator_vote_count_df, LEGISLATOR_VOTE_COUNT_FILE)
    logging.debug(f"\n{legislator_vote_count_df.to_string()}\n")

    # Second deliverable
    bill_vote_counts_df = get_bill_vote_counts(bills_df, vote_results_df, votes_df, legislators_df)
    save_csv_file(bill_vote_counts_df, BILLS_VOTE_COUNT_FILE)
    logging.debug(f"\n{bill_vote_counts_df.to_string()}\n")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Quorum Application')
    parser.add_argument('--debug', action='store_true', help='Debug mode')
    args = parser.parse_args()

    debug_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=debug_level)

    main()
