from csv_operations import load_csv_file

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
