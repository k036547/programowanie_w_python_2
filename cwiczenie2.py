from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, Integer, String, create_engine, false
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declarative_base


class Base(DeclarativeBase):
    pass

class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    type: Mapped[int] = mapped_column(Integer)
    finished: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=false()
    )


class DataPoint(Base):
    __tablename__ = "data_points"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    real_value: Mapped[float] = mapped_column(Float)
    target_value: Mapped[float] = mapped_column(Float)


engine = create_engine("sqlite:///test.db", echo=True)
Base.metadata.create_all(engine)
