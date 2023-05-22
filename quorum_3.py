from sqlalchemy import create_engine, select, func, case, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, relationship
from typing import List

from loaded_data import (
    bills_df,
    legislators_df,
    vote_results_df,
    votes_df,
)


engine = create_engine("sqlite:///:memory:", echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Legislator(Base):
    __tablename__ = "legislators"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

    vote_results: Mapped[List["VoteResult"]] = relationship(back_populates="legislator")  # 1 : M

    bills: Mapped[List["Bill"]] = relationship(back_populates="sponsor")  # 1 : M

    def __repr__(self):
        return f"<Legislator(id={self.id}, name={self.name})>"


class Vote(Base):
    __tablename__ = "votes"

    id: Mapped[int] = mapped_column(primary_key=True)
    bill_id: Mapped[int] = mapped_column(foreign_key=True)

    vote_results: Mapped["VoteResult"] = relationship(back_populates="vote")  # 1 : 1

    def __repr__(self):
        return f"<Vote(id={self.id}, bill_id={self.bill_id})>"


class VoteResult(Base):
    __tablename__ = "vote_results"

    id: Mapped[int] = mapped_column(primary_key=True)

    legislator_id: Mapped[int] = mapped_column(ForeignKey("legislators.id"))
    legislator: Mapped["Legislator"] = relationship(back_populates="vote_results")  # M : 1

    vote_id: Mapped[int] = mapped_column(ForeignKey("votes.id"))
    vote: Mapped["Vote"] = relationship(back_populates="vote_results")  # 1 : 1

    vote_type: Mapped[int] = mapped_column()

    def __repr__(self):
        return f"<VoteResult(id={self.id}, legislator_id={self.legislator_id}, vote_id={self.vote_id}, vote_type={self.vote_type})>"


class Bill(Base):
    __tablename__ = "bills"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()

    sponsor_id: Mapped[int] = mapped_column(ForeignKey("legislators.id"))
    sponsor: Mapped["Legislator"] = relationship(back_populates="bills")  # M : 1

    def __repr__(self):
        return f"<Bill(id={self.id}, title={self.title}, sponsor_id={self.sponsor_id})>"


Base.metadata.create_all(bind=engine)


def main():
    connection = engine.connect()

    # First question
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


    # Second question


if __name__ == "__main__":
    # Load data
    legislators = legislators_df.to_sql(con=engine, name="legislators", if_exists="replace", index=False)
    vote_results = vote_results_df.to_sql(con=engine, name="vote_results", if_exists="replace", index=False)
    votes = votes_df.to_sql(con=engine, name="votes", if_exists="replace", index=False)
    bills = bills_df.to_sql(con=engine, name="bills", if_exists="replace", index=False)

    # Alternatively:
    # session = Session()
    # session.add_all([Legislator(**row) for row in legislators_df.to_dict(orient="records")])
    # ...
    # session.commit()

    # Run main
    main()

    # session.close()
