from datetime import datetime
import random
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, create_engine, delete, false, select, update
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship    


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
    data_points = relationship("DataPoint", back_populates="experiment")

class DataPoint(Base):
    __tablename__ = "data_points"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    real_value: Mapped[float] = mapped_column(Float)
    target_value: Mapped[float] = mapped_column(Float)
    experiment_id: Mapped[int] = mapped_column(Integer, ForeignKey("experiments.id"))
    experiment = relationship("Experiment", back_populates="data_points")

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

    '''
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
    '''
    for i in range(10):
        session.add(DataPoint(real_value=round(random.random() * 10, 2), target_value=round(random.random() * 10, 2), experiment=new_experiment_1))
        session.add(DataPoint(real_value=round(random.random() * 10, 2), target_value=round(random.random() * 10, 2), experiment=new_experiment_2))
    session.commit()

    print("Experiments:")
    for i, experiment in enumerate(session.scalars(select(Experiment)).all(), start=1):        
        print(f"{i}:", experiment.title, experiment.created_at, experiment.type, experiment.finished)

    print("Data Points:")
    for i, data_point in enumerate(session.scalars(select(DataPoint)).all(), start=1):
        print(f"{i}:", data_point.real_value, data_point.target_value)


    print("Data Points - Experiments for experiment_id == 1")
    stmt = select(DataPoint).where(DataPoint.experiment_id == 1)
    for i, data_point in enumerate(session.scalars(stmt).all(), start=1):
        print(f"{i}:", data_point.real_value, data_point.target_value, data_point.experiment.title, data_point.experiment.created_at, data_point.experiment.type, data_point.experiment.finished)
    
    #session.execute(update(Experiment).where(Experiment.finished == False).values(finished=True))
    #session.commit()

    # ORM approach - extremly inefficient - use only for small datasets if consistency of the model is priority:
    # session.delete_all(session.scalars(select(Experiment)).all())
    
    # SQL approach:
    #session.execute(delete(Experiment))
    #session.execute(delete(DataPoint))
    #session.commit()    