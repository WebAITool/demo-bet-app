from typing import Optional
import datetime
import decimal

from sqlalchemy import BigInteger, Boolean, ForeignKeyConstraint, Identity, Integer, Numeric, PrimaryKeyConstraint, String, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class EmailCode(Base):
    __tablename__ = 'email_codes'
    __table_args__ = (
        PrimaryKeyConstraint('email', name='email_codes_pkey'),
        UniqueConstraint('email', name='email_codes_email_unique')
    )

    email: Mapped[str] = mapped_column(String(255), primary_key=True)
    code: Mapped[int] = mapped_column(Integer, nullable=False)
    expires_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=0), nullable=False)


class Event(Base):
    __tablename__ = 'events'
    __table_args__ = (
        ForeignKeyConstraint(['final_outcome_id'], ['outcomes.id'], name='events_final_outcome_id_foreign'),
        PrimaryKeyConstraint('id', name='events_pkey')
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    ended_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=0), nullable=False)
    final_outcome_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    final_outcome: Mapped[Optional['Outcome']] = relationship('Outcome', foreign_keys=[final_outcome_id], back_populates='events')
    outcomes: Mapped[list['Outcome']] = relationship('Outcome', foreign_keys='[Outcome.event_id]', back_populates='event')
    bets: Mapped[list['Bet']] = relationship('Bet', back_populates='event')


class Outcome(Base):
    __tablename__ = 'outcomes'
    __table_args__ = (
        ForeignKeyConstraint(['event_id'], ['events.id'], name='outcomes_event_id_foreign'),
        PrimaryKeyConstraint('id', name='outcomes_pkey')
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    event_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    coefficient: Mapped[decimal.Decimal] = mapped_column(Numeric(8, 2), nullable=False)

    events: Mapped[list['Event']] = relationship('Event', foreign_keys='[Event.final_outcome_id]', back_populates='final_outcome')
    event: Mapped['Event'] = relationship('Event', foreign_keys=[event_id], back_populates='outcomes')
    bets: Mapped[list['Bet']] = relationship('Bet', back_populates='outcome')


class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('email', name='users_email_unique')
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    login: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    balance: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text('0'))
    can_create_events: Mapped[bool] = mapped_column(Boolean, nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    is_confirmed: Mapped[bool] = mapped_column(Boolean, nullable=False)

    bets: Mapped[list['Bet']] = relationship('Bet', back_populates='user')
    sessions: Mapped[list['Session']] = relationship('Session', back_populates='user')


class Bet(Base):
    __tablename__ = 'bets'
    __table_args__ = (
        ForeignKeyConstraint(['event_id'], ['events.id'], name='bets_event_id_foreign'),
        ForeignKeyConstraint(['outcome_id'], ['outcomes.id'], name='bets_outcome_id_foreign'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='bets_user_id_foreign'),
        PrimaryKeyConstraint('id', name='bets_pkey')
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    event_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    outcome_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    coefficient: Mapped[decimal.Decimal] = mapped_column(Numeric(8, 2), nullable=False)

    event: Mapped['Event'] = relationship('Event', back_populates='bets')
    outcome: Mapped['Outcome'] = relationship('Outcome', back_populates='bets')
    user: Mapped['User'] = relationship('User', back_populates='bets')


class Session(Base):
    __tablename__ = 'sessions'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], name='sessions_user_id_foreign'),
        PrimaryKeyConstraint('id', name='sessions_pkey')
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    expires_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=0), nullable=False)

    user: Mapped['User'] = relationship('User', back_populates='sessions')
