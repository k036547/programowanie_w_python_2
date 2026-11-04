from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, Integer, String, create_engine, delete, false, select, update
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session    


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


engine = create_engine("sqlite:///test.db", echo=False)
Base.metadata.create_all(engine)

with Session(engine) as session:
    new_experiment_1 = Experiment(
        title="Test Experiment 1",
        created_at=datetime.now(),
        type=1,
        finished=False
    )
    new_experiment_2 = Experiment(
        title="Test Experiment 2",
        created_at=datetime.now(),
        type=2,
        finished=True
    )
    session.add(new_experiment_1)
    session.add(new_experiment_2)

    session.add_all([
        DataPoint(real_value=3.14, target_value=3.0),
        DataPoint(real_value=3.15, target_value=3.0),
        DataPoint(real_value=3.16, target_value=3.0),
        DataPoint(real_value=3.17, target_value=3.0),
        DataPoint(real_value=3.18, target_value=3.0),
        DataPoint(real_value=6.89, target_value=6.0),
        DataPoint(real_value=7.01, target_value=7.0),
        DataPoint(real_value=9.05, target_value=9.0),
        DataPoint(real_value=2.79, target_value=2.0),
        DataPoint(real_value=1.99, target_value=1.0)
       ])
    session.commit()

    print("Experiments:")
    for i, experiment in enumerate(session.scalars(select(Experiment)).all(), start=1):        
        print(f"{i}:", experiment.title, experiment.created_at, experiment.type, experiment.finished)

    print("Data Points:")
    for i, data_point in enumerate(session.scalars(select(DataPoint)).all(), start=1):
        print(f"{i}:", data_point.real_value, data_point.target_value)

    session.execute(update(Experiment).where(Experiment.finished == False).values(finished=True))
    session.commit()

    # ORM approach - extremly inefficient - use only for small datasets if consistency of the model is priority:
    # session.delete_all(session.scalars(select(Experiment)).all())
    
    # SQL approach:
    session.execute(delete(Experiment))
    session.execute(delete(DataPoint))
    session.commit()    