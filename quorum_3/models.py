from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import List

from quorum_3.db import engine, Base


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
