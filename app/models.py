from sqlalchemy import ForeignKey, String, Integer, DateTime, func, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Players(Base):
    __tablename__ = "players"
    name: Mapped[str] = mapped_column(String(30), primary_key=True)
    games_won: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    games_lost: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    def __repr__(self):
        return f"Player: {self.name!r}\nWon games: {self.games_won!r}\nLost games: {self.games_lost!r}"

class Games(Base):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(primary_key=True)
    winner: Mapped[str] = mapped_column(String(30), ForeignKey("players.name"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    def __repr__(self):
        self.created_at_str = self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else 'N/A'
        return f"Game id: {self.id!r}\nWinner: {self.winner!r}\nCreated at: {self.created_at_str!r}"

class Rounds(Base):
    __tablename__ = "rounds"
    round_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    round_number: Mapped[int] = mapped_column(Integer)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    player: Mapped[str] = mapped_column(String(30), ForeignKey("players.name"))
    points: Mapped[int] = mapped_column(Integer)
    __table_args__ = (UniqueConstraint('round_number', 'game_id', 'player', name='_unique_round'),)

    def return_dict(self):
        return {self.round_number:f"Player: {self.player!r} - Points: {self.points!r}"}