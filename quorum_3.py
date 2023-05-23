from sqlalchemy import select, func, case, text

from loaded_data_frames import (
    bills_df,
    legislators_df,
    vote_results_df,
    votes_df,
)

from quorum_3.models import (
    Legislator,
    VoteResult,
    Vote,
    Bill,
)
from quorum_3.db import engine

connection = engine.connect()


def first_question():
    sql_query = """
    SELECT legislators.id,
           legislators.name,
           COUNT(CASE WHEN vote_results.vote_type = 1 THEN TRUE ELSE NULL END) as num_supported_bills,
           COUNT(CASE WHEN vote_results.vote_type = 2 THEN TRUE ELSE NULL END) as num_opposed_bills
    FROM legislators
    LEFT JOIN vote_results ON vote_results.legislator_id = legislators.id
    GROUP BY legislators.id, legislators.name
    """
    results__1_1 = connection.execute(text(sql_query)).fetchall()

    sqlalchemy_query = (
        select(
            Legislator.id,
            Legislator.name,
            func.count(case((VoteResult.vote_type == 1, True), else_=None)).label("num_supported_bills"),
            func.count(case((VoteResult.vote_type == 2, True), else_=None)).label("num_opposed_bills"),
        )
        .join(VoteResult, Legislator.id == VoteResult.legislator_id, isouter=True)
        .group_by(Legislator.id, Legislator.name)
    )
    results__1_2 = connection.execute(sqlalchemy_query).fetchall()

    assert results__1_1 == results__1_2
    for row in results__1_2:
        print(row)


def second_question():
    # # Second question
    # sql_query = """
    # """
    # results__2_1 = connection.execute(text(sql_query)).fetchall()

    # sqlalchemy_query = ()
    # results__2_2 = connection.execute(sqlalchemy_query).fetchall()

    # assert results__2_1 == results__2_2
    # for row in results__2_1:
    #     print(row)
    pass


def main():
    first_question()
    second_question()


if __name__ == "__main__":
    # Load data
    legislators = legislators_df.to_sql(con=engine, name="legislators", if_exists="replace", index=False)
    vote_results = vote_results_df.to_sql(con=engine, name="vote_results", if_exists="replace", index=False)
    votes = votes_df.to_sql(con=engine, name="votes", if_exists="replace", index=False)
    bills = bills_df.to_sql(con=engine, name="bills", if_exists="replace", index=False)

    # Run main
    main()

    # Alternatively:
    # from sqlalchemy.orm import sessionmaker
    # Session = sessionmaker(bind=engine)
    # session = Session()
    # session.add_all([Legislator(**row) for row in legislators_df.to_dict(orient="records")])
    # ...
    # session.commit()
    # main()
    # session.close()
