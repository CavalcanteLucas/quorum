# Quorum

This application is a simple script to query legislative data.

## Running the application

### Locally

1. Clone the repository
2. Create a virtualenv with
```
virtualenv -p python3 venv
```
3. Activate the virtualenv with
```
source venv/bin/activate
```
4. Install the dependencies with
```
pip install -r requirements.txt
```
5. Run the application with
```
python quorum.py
```
or
```
python quorum.py --debug
```

For more information run 
```
python quorum.py --help
```

The results will be generated at the folder `deliverable_data`.

### With Docker

Clone the repository, and run:
```
docker-compose up --build
```


## Discussion points

### 1. On the solution’s time complexity and the tradeoffs.

#### a. On the time complexity

The complete solution has two main parts, one for each deliverable. The complexity of the first part depends on the method `get_legislator_vote_count`. The complexity of the second part depends on the method `get_bill_vote_counts`.

The method `get_legislator_vote_count` is composed of two main parts:

i. Grouping and aggregating data, which requires sorting the data, thus taking **O(N log N)** time, where **N** is the number of rows in `vote_results_df`.

ii. Merging dataframes, which also requires sorting the data, thus taking **O(M log M)** time, where **M** is the number of rows in `legislators_df`.

All other operations require linear time, thus having a complexity **O(1)**.

Therefore, the overall time complexity of `get_legislator_vote_count` is **O(N log N + M log M)**.

The method `get_bill_vote_counts` is also composed of two main parts:

i. Grouping and aggregating data, which requires sorting the data, thus taking **O(N log N)** time, where **N** is the number of rows in `vote_results_df`.

ii. Joining tables, which can vary depending on the type of the join, the size of the tables, and the number of common columns. Assuming standard inner-joins, the time complexity of each join operation is **O(M log M)**, where **M** is the number of rows in the largest table.

All other operations require linear time, thus having a complexity **O(1)**.

Therefore, the overall time complexity of `get_bill_vote_counts` is **O(N log N + 3M log M)**.


#### b. On the tradeoff's:

Some tradeoffs of the given solution include:
- **Efficiency vs. readability**: the solution is concise and easy to read. However, in can be memory-intensive and slow for large datasets.
- **Accuracy vs speed**: the solution performs several left-join operations. This can be faster than other types of joins, but it can also lead to inaccurate results if the data is not properly cleaned beforehand.
- **Flexibility vs. complexity**: the solution is specialized for the specific data format and task at hand. If the data format changes or the requirements change, the solution will need to be updated.


### 2. On changing the to account for future columns that might be requested, such as “Bill Voted On Date” or “Co-Sponsors”

Now that we have a new column in `provided_data/bills.csv`, if such a new information is not required in the output, no changes would be required in the main program. Otherwise, the method `get_bill_vote_counts` would need to be updated to include the new column in the returned dataframe:

```
return bill_vote_counts[
    [
        "id",
        "title",
        "supporter_count",
        "opposer_count",
        "primary_sponsor",
        "bill_voted_on_date",  # Add the new column
    ]
]
```

### 3. On chaning the solution solution in case of a list of legislators or bills instead of a CSV:

The solution I would choose is to create a function for converting the list of legislators or bills into a pandas DataFrame. This function could accept a list of dictionaries, where each dictionary represents a legislator or bill with its respective properties, and return a DataFrame with the same structure as the one currently loaded from the CSV files. That way the rest of the program would not need to be changed.


### 4. Time spent:

This assignment took me between 3 to 5 hours to complete, plus 1 hour to answer the questions above.


## Author

**Quorum** is developed by **Lucas C Cavalcante**. If you have any questions or feedback about the app, please feel free to contact me at lucascpcavalcante@gmail.com.
