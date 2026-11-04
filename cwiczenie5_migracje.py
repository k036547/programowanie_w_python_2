from datetime import datetime
from itertools import count
import random
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, create_engine, delete, false, func, select, update
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship    

class Base(DeclarativeBase):
    pass

class SubjectExperimentLink(Base):
    __tablename__ = "subject_experiment_link"

    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), primary_key=True)
    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiments.id"), primary_key=True)

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
    subjects = relationship("Subject", secondary="subject_experiment_link", back_populates="experiments")

class DataPoint(Base):
    __tablename__ = "data_points"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    real_value: Mapped[float] = mapped_column(Float)
    target_value: Mapped[float] = mapped_column(Float)
    experiment_id: Mapped[int] = mapped_column(Integer, ForeignKey("experiments.id"))
    experiment = relationship("Experiment", back_populates="data_points")

class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gdpr_accepted: Mapped[bool] = mapped_column(Boolean, default=False)
    experiments = relationship("Experiment", secondary="subject_experiment_link", back_populates="subjects")

#engine = create_engine("sqlite:///test.db", echo=False)
#Base.metadata.create_all(engine)                           # Must not be called if migrations are used!
'''
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

    for i in range(10):
        session.add(DataPoint(real_value=round(random.random() * 10, 2), target_value=round(random.random() * 10, 2), experiment=new_experiment_1))
        session.add(DataPoint(real_value=round(random.random() * 10, 2), target_value=round(random.random() * 10, 2), experiment=new_experiment_2))
    session.commit()
'''

'''
    print("Experiments:")
    for i, experiment in enumerate(session.scalars(select(Experiment)).all(), start=1):        
        print(f"{i}:", experiment.title, experiment.created_at, experiment.type, experiment.finished)

    print("Data Points:")
    for i, data_point in enumerate(session.scalars(select(DataPoint)).all(), start=1):
        print(f"{i}:", data_point.real_value, data_point.target_value)
'''

"""
    print("Aggregated Data Points for each Experiment:")
    stmt = select(Experiment.id, func.sum(DataPoint.real_value), func.avg(DataPoint.real_value)).join(DataPoint).group_by(Experiment.id)
    for experiment_id, sum_values, avg_values in session.execute(stmt).all():
        print(f"{experiment_id:d} {sum_values:0.2f} {avg_values:0.2f}")
"""

    #session.execute(update(Experiment).where(Experiment.finished == False).values(finished=True))
    #session.commit()

    # ORM approach - extremly inefficient - use only for small datasets if consistency of the model is priority:
    # session.delete_all(session.scalars(select(Experiment)).all())
    
    # SQL approach:
    #session.execute(delete(Experiment))
    #session.execute(delete(DataPoint))
    #session.commit()